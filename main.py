import requests
from bs4 import BeautifulSoup
import json


def gather_morse_data():
    dictionary = {}

    response = requests.get("http://beta.wildwalks.com/bushcraft/technical-stuff/morse-code-and-phonetic-alphabet.html")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('tbody').find_all("tr")
    for row in table[1:]:
        boxes = row.find_all("td")
        try:
            this_letter = boxes[0].text.lower()
        except ValueError:
            this_letter = boxes[0].text
        if this_letter == "period":
            this_letter = '.'
        elif this_letter == "comma":
            this_letter = ','
        morse = boxes[1].text
        morse = morse.replace("\xa0", "")
        morse = morse.replace("·", ".")
        morse = morse.replace("–", "_")
        dictionary[this_letter] = morse

        with open("morse.json", "w") as file:
            json.dump(dictionary, file)


def get_morse_from_json():
    with open("morse.json") as file:
        return json.load(file)


try:
    morse_dictionary = get_morse_from_json()
except FileNotFoundError:
    gather_morse_data()
    morse_dictionary = get_morse_from_json()


while True:
    string_to_translate = input("Please type the phrase you wish to translate: ")

    if string_to_translate == "END":
        break

    translated_string = ""

    separated = string_to_translate.split(" ")

    morse_to_english = False

    for word in separated:
        alphanumeric = False
        for char in word:
            if char.isalnum():
                alphanumeric = True
        if not alphanumeric:
            morse_to_english = True
            break

    if morse_to_english:
        new_dict = {v: k for (k, v) in morse_dictionary.items()}

        string_to_translate = string_to_translate.replace(".", ".")
        string_to_translate = string_to_translate.replace("-", "_")

        for letter in string_to_translate.split(" "):
            if letter == '/':
                translated_string += " "
            else:
                translated_string += new_dict[letter]

        translated_string = translated_string.upper()
    else:
        for char in string_to_translate.lower():
            try:
                if char != " ":
                    translated_string += morse_dictionary[char] + " "
                else:
                    translated_string += "/"
            except KeyError:
                translated_string += "*****"

    print(translated_string)
    print("-----------------------------------------------------")
