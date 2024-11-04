# Text Translator

A simple Python package for detecting languages and translating text using the Google Translate API.

## Features

- Translate text from one language to another.
- Automatically detect the source language or specify it.


## Translating Text
To translate text, use the translate_text function:
```bash
from UGTranslate import translate_text

text_to_translate = "Hello world"
translated = translate_text(text_to_translate, input_lang='en', output_lang='fr')
print(translated)
```

## Parameters

- text (str): The text to be translated.
- input_lang (str, optional): The language code of the input text (e.g., 'en' for English). Defaults to 'auto'.
- output_lang (str, optional): The language code of the output text (e.g., 'fr' for French). Defaults to 'en'.

## Response Format
The translate_text function returns a JSON string containing:

- RESPONSE_STATUS: HTTP status code of the request.
- TranslatedText: The translated text.


## Example: 1
Here’s a complete example of how to use both functions:
```bash
text = "Hola, ¿cómo estás?"
translated = translate_text(text, input_lang='fr', output_lang='en')
print(translated)
```

## Example: 2
Here’s a complete example of how to use both functions:
```bash
from main import get_lan_code, translate_text

text = "Hola, ¿cómo estás?"
translated = translate_text(text)
print(translated)
```

## Contributing
If you'd like to contribute to this project, feel free to open an issue or submit a pull request.