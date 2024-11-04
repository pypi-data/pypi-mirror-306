import requests
import json


def translate_text(text, input_lang=None, output_lang=None):
    if not input_lang:
        input_lang = 'auto'
    if not output_lang:
        output_lang = 'en'

    # Request URL...
    GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

    """Translates given text using the Google Translate API."""
    params = {
        'client': 'gtx',
        'sl': input_lang,
        'tl': output_lang,
        'dt': 't',
        'q': text,
    }
    response = requests.get(GOOGLE_TRANSLATE_URL, params=params)
    result = response.json()
    translated_text = ''.join([item[0] for item in result[0]])
    return json.dumps({'RESPONSE_STATUS': response.status_code,'TranslatedText': translated_text})