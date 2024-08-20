import json
import os
import logging
from typing import Any, Dict, List
from openai import OpenAI
import tiktoken

class SchemaOrganizer:
    def __init__(self, api_key: str, config_file: str = 'config.json'):
        self.client = OpenAI(api_key=api_key)
        self.logger = self.setup_logger()
        self.config = self.load_config(config_file)
        self.schema = self.load_schema()
        self.encoder = tiktoken.encoding_for_model(self.config['model'])

    @staticmethod
    def setup_logger():
        logger = logging.getLogger('SchemaOrganizer')
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def load_config(self, config_file: str) -> Dict[str, Any]:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            self.logger.error(f"Config file not found: {config_file}")
            raise FileNotFoundError(f"Config file not found: {config_file}")

    def load_schema(self) -> Dict[str, Any]:
        if self.config['use_predefined_schema']:
            return {
                "title": "Product details",
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "price": {"type": "string"},
                    "link": {"type": "string"}
                }
            }
        else:
            try:
                with open(self.config['custom_schema_file'], 'r') as f:
                    custom_schema = json.load(f)
                self.logger.info(f"Loaded custom schema from {self.config['custom_schema_file']}")
                return custom_schema
            except FileNotFoundError:
                self.logger.error(f"Custom schema file not found: {self.config['custom_schema_file']}")
                raise
            except json.JSONDecodeError:
                self.logger.error(f"Invalid JSON in custom schema file: {self.config['custom_schema_file']}")
                raise

    @staticmethod
    def load_text(text_file: str) -> str:
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {text_file}")

    def count_tokens(self, text: str) -> int:
        return len(self.encoder.encode(text))

    def split_text(self, text: str, max_tokens: int = 4000) -> List[str]:
        chunks = []
        current_chunk = []
        current_length = 0

        for line in text.split('\n'):
            line_length = self.count_tokens(line)
            if current_length + line_length > max_tokens:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_length = line_length
            else:
                current_chunk.append(line)
                current_length += line_length

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks

    def organize_text(self, text: str) -> Dict[str, Any]:
        try:
            self.logger.debug("Splitting text into chunks")
            chunks = self.split_text(text)
            organized_data = {}

            for i, chunk in enumerate(chunks):
                self.logger.debug(f"Processing chunk {i+1}/{len(chunks)}")
                response = self.client.chat.completions.create(
                    model=self.config['model'],
                    messages=[
                        {"role": "system", "content": "You are an assistant that organizes content into a provided structure. Analyze the given text and structure it according to the provided schema. Your response should be in JSON format."},
                        {"role": "user", "content": f"Organize the following content according to this structure and respond with a JSON object. If the content is incomplete, fill in as much as possible:\n\n{json.dumps(self.schema, indent=2)}\n\nContent to organize:\n\n{chunk}"}
                    ],
                    response_format={"type": "json_object"}
                )
                
                chunk_data = json.loads(response.choices[0].message.content)
                self.logger.debug(f"Received response from GPT for chunk {i+1}")

                # Merge chunk_data into organized_data
                for key, value in chunk_data.items():
                    if key not in organized_data:
                        organized_data[key] = value
                    elif isinstance(value, str):
                        organized_data[key] = organized_data[key] + " " + value
                    elif isinstance(value, list):
                        organized_data[key].extend(value)
                    elif isinstance(value, dict):
                        organized_data[key].update(value)

            return organized_data
        except Exception as e:
            self.logger.error(f"Error in organizing text: {str(e)}")
            return {}

    @staticmethod
    def save_json(data: Dict[str, Any], output_file: str):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Organized data saved to {output_file}")
        except Exception as e:
            print(f"Error saving JSON file: {str(e)}")

    def process_file(self, input_file: str, output_file: str):
        try:
            input_text = self.load_text(input_file)
            self.logger.debug(f"Input text loaded from {input_file}")
            organized_data = self.organize_text(input_text)
            
            if not organized_data:
                self.logger.error("Failed to organize the text. Please check the model output and your input files.")
                return

            self.logger.info("Organized data:")
            print(json.dumps(organized_data, indent=2, ensure_ascii=False))
            self.save_json(organized_data, output_file)
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return

    input_text_file = 'input_text.txt'
    output_json_file = 'output.json'

    try:
        organizer = SchemaOrganizer(api_key)
        organizer.process_file(input_text_file, output_json_file)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
