import requests

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"


def translate_text(text, input_lang='auto', output_lang='en'):
    """
    Translates given text using the Google Translate API.

    Args:
        text (str): Text to be translated.
        input_lang (str): Source language code (default 'auto' for auto-detect).
        output_lang (str): Target language code (default 'en' for English).

    Returns:
        dict: Contains response status and translated text.
    """
    params = {
        'client': 'gtx',
        'sl': input_lang,
        'tl': output_lang,
        'dt': 't',
        'q': text,
    }
    try:
        response = requests.get(GOOGLE_TRANSLATE_URL, params=params)
        response.raise_for_status()
        result = response.json()
        translated_text = ''.join([item[0] for item in result[0]])
        return {'RESPONSE_STATUS': response.status_code, 'TranslatedText': translated_text}
    except requests.exceptions.RequestException as e:
        return {'RESPONSE_STATUS': 'Error', 'error_message': str(e)}
