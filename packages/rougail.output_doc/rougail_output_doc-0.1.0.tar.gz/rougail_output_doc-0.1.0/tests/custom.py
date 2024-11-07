from os import environ
environ['TIRAMISU_LOCALE'] = 'en'
from tiramisu import StrOption


class CustomOption(StrOption):
    pass
