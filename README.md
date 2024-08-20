# 🧠 Organize My Data

Organize My Data is a Python package that helps you structure text data according to a specified schema using OpenAI's GPT models.

## Project Structure

```
organize-my-data/
├── organize_my_data/
│   ├── __init__.py
│   └── schema_organizer.py
├── setup.py
├── config.json
├── my_schema.json
├── input_text.txt
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/organize-my-data.git
cd organize-my-data
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Install the package in editable mode:

```bash
pip install -e .
```

## Usage

1. Set up your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

2. Prepare your input:
   - Edit the `input_text.txt` file in the project directory with the text you want to organize.

3. Customize the schema (optional):
   - Edit the `my_schema.json` file in the project directory with your custom schema.

4. Run the organizer:

```bash
organize-my-data
```

The program will use `input_text.txt` as input and save the results to `output.json`.

## ⚙️ Configuration

The configuration is stored in `config.json`:

```json
{
  "use_predefined_schema": false,
  "custom_schema_file": "my_schema.json",
  "model": "gpt-4-0125-preview"
}
```

- `use_predefined_schema`: Set to `false` to use a custom schema, `true` to use the predefined schema.
- `custom_schema_file`: Specifies the filename of your custom schema (default is "my_schema.json").
- `model`: Specifies the OpenAI model to use for text organization.

## Custom Schema

When `use_predefined_schema` is set to `false`, the program will use the custom schema specified in `my_schema.json`. Here's an example of a custom schema:

```json
{
  "type": "object",
  "properties": {
    "product_name": {"type": "string"},
    "product_description": {"type": "string"},
    "product_price": {"type": "string"},
    "product_url": {"type": "string"}
  }
}
```

## Example Input

Here's an example of what your `input_text.txt` might look like:

```
Smart Home Security Camera

Enhance your home security with our cutting-edge wireless camera system. This high-definition camera offers crystal-clear 1080p video quality, allowing you to monitor your property day and night. With its advanced motion detection technology, you'll receive instant alerts on your smartphone whenever any unusual activity is detected.

Key features:
- 1080p HD video quality
- Night vision up to 30 feet
- Two-way audio communication
- Weather-resistant design for indoor and outdoor use
- Easy DIY installation
- Compatible with Alexa and Google Home

Keep an eye on what matters most, whether you're at work or on vacation. Our user-friendly app lets you view live footage and recorded videos anytime, anywhere.

Price: $129.99

For more information and to purchase, visit: https://example.com/smart-home-camera
```

## Troubleshooting

If you encounter any issues:

1. Ensure all required files are present in the correct locations as shown in the project structure.
2. Verify that the OpenAI API key is correctly set as an environment variable.
3. Check that all dependencies are installed by running `pip list`.
4. If you get a "module not found" error, try reinstalling the package:
   ```
   pip uninstall organize-my-data
   pip install -e .
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
