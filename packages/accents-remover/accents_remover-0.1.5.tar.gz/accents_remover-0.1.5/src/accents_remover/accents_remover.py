__version__ = '0.1.5'

# %%
import re
from unicodedata import normalize

# %%

convert_list = {
    'a': ['àáâãäå'],
    'e': ['èéêë'],
    'i': ['ìíîï'],
    'o': ['òóôõö'],
    'u': ['ùúûü'],
    'c': ['ç'],
    'n': ['ñ']
}

# %%
def letter_replacer(letter: str) -> str:
    for item in convert_list:
        letter = re.sub(f'{convert_list[item]}', item, letter)
    return letter

def remove_accents(word: str) -> str:
    for letter in word:
        lower_letter = letter.lower()
        new_letter = letter_replacer(lower_letter)

        if letter.isupper():
            new_letter = new_letter.upper()
            
        word = word.replace(letter, new_letter)
    return word

def remove_diacritics(text: str) -> str:
    """
    This will remove diacritics such as umlauts and accents from a string. This is
    useful when we need to prepare data for systems such as LDAP.

    Example input: "Carina Müller"
    Example output: "Carina Muller"
    """
    return normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")

# %%
