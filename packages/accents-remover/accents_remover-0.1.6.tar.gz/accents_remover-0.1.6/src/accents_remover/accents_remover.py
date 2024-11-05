__version__ = '0.1.6'

# %%
import re
from unicodedata import normalize

# %%

convert_list = {
    'a': ['àáâãäåąăāǎȧ'],
    'e': ['èéêëęěėēê̄ếê̌ề'],
    'i': ['ìíîïīǐ'],
    'o': ['òóôõöőŏōȫǒȯ'],
    'u': ['ùúûüůǔűūǖǘǚǜŭ'],
    'c': ['çčćĉċ'],
    'n': ['ñňńǹņṅ'],
    's': ['šśşŝṣs̱ṣ̄ṡ'],
    'z': ['žżz̄ẓz̤ẕẑź']
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
