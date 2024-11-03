import random
import string

import requests
from bs4 import BeautifulSoup

_letter_cumulative_probabilities = [
    0.059927035685846036,
    0.06883460804829719,
    0.13853960258523307,
    0.07685327506064928,
    0.023037463656734383,
    0.0773718031815404,
    0.06574195818441082,
    0.008148299042574863,
    0.035778440341487805,
    0.0002777829219059612,
    0.0,
    0.053315802144484156,
    0.06357525139354432,
    0.022741161873368027,
    0.0150373155058427,
    0.040797051797255506,
    5.555658438119224e-05,
    0.03274134706198263,
    0.13333580251486138,
    0.06720494823978222,
    0.013833589510916868,
    0.0021111502064853054,
    0.0,
    0.000537046982351525,
    5.555658438119224e-05,
    0.00014815089168317933,
]


def get_random_definition() -> str:
    """Get a random irish word and its definition"""
    word = get_random_word()
    return get_translation(word)


def get_random_word() -> str:
    """
    Get a random word from http://www.teanglann.ie
    in Irish. Uses a cumulative probability distribution
    based on the number of entries for each letter.

    Returns:
        A random Irish word without translation
    """
    # get the resulting page of words for a given random letter
    letter, *_ = random.choices(
        string.ascii_lowercase, _letter_cumulative_probabilities
    )
    result = requests.get(f"https://www.teanglann.ie/en/fgb/_{letter}")
    result.raise_for_status()

    # pick a word randomly for the given letter
    soup = BeautifulSoup(result.content, "html.parser")
    samples = soup.find_all("span", class_="abcItem")
    word = random.choice(samples)
    return word.a.text


def get_translation(word: str) -> str:
    """
    Get the translation of a given `word` from http://www.teanglann.ie

    Args:
        word: Irish language word

    Returns:
        dictionary definiton in English
    """
    word_result = requests.get(f"https://www.teanglann.ie/en/fgb/{word}")
    word_result.raise_for_status()

    word_page = BeautifulSoup(word_result.content, "html.parser")
    trans = word_page.find_all("div", class_="entry")
    all_trans = []
    for tran in trans:
        if "=" in tran.text:
            word = tran.text.split("=")[-1]
            word = "".join(filter(str.isalpha, word))
        all_trans.append(tran.text)

    trans = " ".join(all_trans)
    if "=" in trans:
        trans += "(AUTOSEARCH) " + get_translation(word)

    return trans
