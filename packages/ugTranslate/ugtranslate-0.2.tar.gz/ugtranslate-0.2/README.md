# ugTranslate

`ugTranslate` is a simple Python wrapper for translating text using the Google Translate API.
Translate without getting blocked!

# Installation

``
pip install ugTranslate
``

# Usage
``````
python

from ugTranslate import translate_text

# Translate text from English to Spanish

response = translate_text("Hello, world!", input_lang='en', output_lang='es')
print(response)
