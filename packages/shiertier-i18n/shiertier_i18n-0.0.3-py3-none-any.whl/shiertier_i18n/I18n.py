import gettext
import os.path
from os import environ

__all__ = ['I18n', 'easy_i18n']

class I18n:
    def __init__(self, 
                 language_str: str = None, 
                 locales_dir: str = None):

        if not language_str:
            self.language_str = environ.get('LANGUAGE', 'en_US')
        else:
            self.language_str = language_str

        if not locales_dir:
            self.locales_dir = environ.get('SHIERTIER_LOCALES_DIR')
            if not self.locales_dir:
                self.locales_dir = os.path.join(os.path.expanduser("~"), ".shiertier", "locales")
                os.makedirs(self.locales_dir, exist_ok=True)
        else:
            self.locales_dir = locales_dir

        self.translation = gettext.translation('messages', locales_dir, languages=[language_str], fallback=True)
        self.translation.install()

    def translate(self, 
                  input: str,
                  replace_dict: dict = None):
        if replace_dict is None:
            return self.translation.gettext(input)
        else:
            result = self.translation.gettext(input)
            for key, value in replace_dict.items():
                result = result.replace(key, str(value))
            return result

easy_i18n = I18n().translate