# to check if file alrady exits
import os

# to exit program with a message to the user
import sys

# to write result to a csv file
import csv

# to check if the user specified filename contains only valid characters
import re

# fetch data from API
import requests

# all the above modules were already installed on my computer, so I am unsure if the installation
# of any of them will be required. But I believe only requests might be the only one that will
# need to be installed

# to print coloured text in the terminal
# colour codes from https://www.geeksforgeeks.org/print-colors-python-terminal/
red = "\033[91m"
green = "\033[92m"
yellow = "\033[93m"
blue = "\033[94m"
purple = "\033[95m"
light_blue = "\033[96m"
# reset colour to the normal one after using any of the above
normal = "\033[00m"


def main():
    # welcome the user and print instructions
    print("------------------------------------")
    print(f"{blue}Welcome to the dictionary{normal}")
    print()
    print("Search for the required word.")
    print("Your will be provided with:")
    print(f"  {green}pronunciation,{normal}")
    print(f"  {purple}part of speech,{normal}")
    print(f"  {red}word definition,{normal}")
    print(f"  {yellow}synonyms,{normal}")
    print(f"  {blue}antonyms{normal}")
    print()
    print("You will also have the option to save your search in a CSV file.")
    print("------------------------------------")
    print()

    # keep running the program until the user chooses to quit
    while True:
        # ask for word they wish to search for
        word_to_search = get_word()
        try:
            found_word = get_word_from_API(word_to_search)
            print()
            print(f"Searched word: {light_blue}{word_to_search}{normal}")
            # display: part of speech, pronunciation, word definition, synonyms and antonyms
            print_data(found_word)
            # ask user if they want to save the word
            save = (
                input("Would you like to save this word in a CSV file (y/n)? ")
                .strip()
                .lower()
            )
            # run a function to verify if they want to save the word in a file based on the answer
            # and ask the user what do they want to name it
            file_name = save_to_file(save)
            # save the word in a file (this step is automatically skipped if they said NO)
            write_file(found_word, file_name)
        except Exception as e:
            print(str(e))

        # ask user if they'd like to look up anything else (accept both y/n and yes/no, case insensitive)
        more = (
            input("Would you like to look up more words (y/yes or n/no)? ")
            .strip()
            .lower()
        )
        # based on their choice, either continue or exit the program
        look_up_more_words(more)


def get_word():
    # ask user for word they wish to look up in the dictionary and remove any trailing spaces
    word = ""
    # keep asking if only enter is pressed/white spaces are entered
    while not word:
        word = input("Please enter the word you wish to search for: ").strip()
    return word


def get_word_from_API(word):
    # get the API data and store it in a variable

    # the used API does not require authorisation and no API key is necessary
    # as per their documentation, it is sufficient to make a call to:
    # https://api.dictionaryapi.dev/api/v2/entries/en/<word>

    endpoint = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    response = requests.get(endpoint + word)
    # if the word was not found, let the user know
    if response.status_code == 404:
        raise Exception("Word not found")
    # if the word is found, return the data
    elif response.status_code == 200:
        """
        the structure of the returned JSON is as follows:
        among various other keys, 'meanings' and 'phonetics' are lists of dictionaries
        the pronunciation is stored inside the 'phonetics' list under the key 'text'
        each dictionary of the 'meanings' list has among others the following keys: 'partOfSpeech',
        'definitions', 'synonyms' and 'antonyms'
        the value for the key 'synonyms' is a list of all synonyms (can often be empty)
        the value for the key 'antonyms' is a list of all antonyms (can often be empty)
        the value for the key 'definitions' is a list of dictionaries
        the actual meaning can be found nested inside each of those dictionaries under the key 'definition'
        additionally, some of the lists/dictionaries may not contain all of these details (e.g.
        'example' might be missing etc.)
        I will be using the following data from the response to display for user to read:
        data = [
            {   'word': 'word as it appears in the dictionary',
                'phonetics': [
                    {
                        'text': 'pronunciation',
                    }
                ],
                'meanings': [
                    {
                        'partOfSpeech': 'noun/verb/adj etc',
                        'definitions': [
                            {
                                'definition': 'here is the definition of the word',
                                'example': 'example sentence',
                            }
                        ],
                        'synonyms': ['list', 'of', 'synonyms', 'which', 'can', 'be', 'empty'],
                        'antonyms': ['list', 'of', 'antonyms', 'which', 'can', 'be', 'empty']
                    }
                ]
            }
        ]
        """
        # parse data into json object
        data = response.json()
        # if data comes back empty, raise an exception
        if len(data) == 0:
            raise Exception("An error occured, please try again.")
        return data
    # if an error occured, let the user know
    else:
        raise Exception("An error occured, please try again.")


def get_phonetics(data, index):
    # list of all the possible pronunciations
    phonetics = data[index]["phonetics"]
    if len(phonetics) > 0:
        # check if "text" exists (not every list item in pronunciation contains the key "text")
        # save & return all the pronunciation
        pronunciation = [each["text"] for each in phonetics if "text" in each]
        return pronunciation
    # if no pronunciation available, let user know
    else:
        return ["pronunciation unavailable"]


def print_data(data):
    # print data into terminal in user friendly format, using colours for better readability
    # iterate over each item in data list
    for index in range(len(data)):
        print()
        # display the word as it appears in data JSON
        print(f'{index+1}: {data[index]["word"]}')
        pronunciation = get_phonetics(data, index)
        # all available pronunciations
        print(f'{green}Pronunciation: {normal}{", ".join(pronunciation)}')
        print()

        # print all the available meanings, examples, synonyms and antonyms of the word
        for meaning in data[index]["meanings"]:
            print(f'Part of speech: {purple}{meaning["partOfSpeech"]}{normal}')
            # Print definitions
            for definition in meaning["definitions"]:
                print(f'{red}Definition: {normal}{definition["definition"]}')
                # print example, if available
                if "example" in definition:
                    print(f'Example: {definition["example"]}')
                else:
                    print("No Example available for this meaning.")
            # Print synonyms/let the user know they are unavailable
            if meaning["synonyms"]:
                print(f'{yellow}Synonyms: {normal}{", ".join(meaning["synonyms"])}')
            else:
                print(f"{yellow}No synonyms available for this meaning.{normal}")
            # Print antonyms/let the user know they are unavailable
            if meaning["antonyms"]:
                print(f'{blue}Antonyms: {normal}{", ".join(meaning["antonyms"])}')
            else:
                print(f"{blue}No antonyms available for this meaning.{normal}")
            print()


def save_to_file(save):
    # check if user wants to save the word to file
    if save in ["y", "yes"]:
        # ask for desired file name
        output_file_name = input("What do you want to name your file? ").strip()
        # check that the file name doesn't contain non letter characters/isn't entered with an extension
        # allowed characters are letters, numbers and underscore
        while not re.search(r"^\w+$", output_file_name):
            output_file_name = input(
                "Please enter a valid file name (alphanumeric characters & underscore only, no extensions): "
            ).strip()
        return output_file_name + ".csv"

    # if user doesn't want to save word, return None
    elif save in ["n", "no"]:
        return None

    # if invalid answer (not y/n or yes/no), keep asking again
    else:
        return save_to_file(
            input("Invalid input, please only enter (y/n): ").strip().lower()
        )


def write_file(data, file_name):
    # try to open file for reading to check if file with such name already exists
    try:
        if os.path.isfile(file_name):
            # display file name
            print(file_name)
            print()
            # if the file name already exists, ask if user wants to keep an existing file and append the
            # new word or if they want to overwrite the existing file
            mode = (
                input(
                    "This file name already exists, would you like to append to it (a) or overwrite it (o)? "
                )
                .strip()
                .lower()
            )
            # if incorrect option selected, inform the user only a/append or o/overwrite is accepted
            while mode not in ["a", "o"]:
                mode = (
                    input("Please only select append (a) or overwrite (o)? ")
                    .strip()
                    .lower()
                )
            if mode in ["o", "overwrite"]:
                # set mode to w+
                mode = "w+"
            elif mode in ["a", "append"]:
                # set mode to a+
                mode = "a+"
        else:
            # display file name
            print(file_name)
            # set mode to w+
            mode = "w+"

        write_word(file_name, data, mode)
        print()

    except TypeError:
        print("Your word will not be saved")
        print()
        pass


def write_word(file_name, data, mode):
    # function for writing text into a file in selected mode
    # this function assumes data does exist with length > 0
    # error handling was done before it could proceed to writing the file

    # fieldnames
    header = [
        "Word",
        "Pronunciation",
        "Part of Speech",
        "Word Definition",
        "Synonym",
        "Antonym",
    ]

    # open file in the required mode and write
    try:
        with open(file_name, mode) as write_file:
            writer = csv.DictWriter(write_file, fieldnames=header)
            # if writing new file/ overwriting an existing one, create a header
            if mode == "w+":
                writer.writeheader()
            # loop over the data list
            for index in range(len(data)):
                # get phonetics
                phonetics = get_phonetics(data, index)
                # loop over each of the meanings from data
                for meaning in data[index]["meanings"]:
                    row = {
                        "Word": data[index]["word"],
                        "Pronunciation": ", ".join(phonetics),
                        "Part of Speech": meaning["partOfSpeech"],
                        "Word Definition": ", ".join(
                            [
                                definition["definition"]
                                for definition in meaning["definitions"]
                            ]
                        ),
                        "Synonym": ", ".join(meaning["synonyms"]),
                        "Antonym": ", ".join(meaning["antonyms"]),
                    }
                    # write them as separate rows
                    writer.writerow(row)
            print("Your word was successfully created.")
            # the below line is to demonstrate the string slicing
            print(f"Your file '{file_name[0:-4]}' was saved as '{file_name}'")
    # if error occurs during writing the file, let the user know
    except IOError as e:
        print(f"Error occured when trying to write the word to file: {e}")


def look_up_more_words(more):
    # if yes, return true (to continue)
    if more in ["y", "yes"]:
        return True
    # if no, exit the program
    elif more in ["n", "no"]:
        print()
        sys.exit("Thank you for using the dictionary.")
    # if invalid input (anything else other than y/yes, n/no), re-prompt the user
    else:
        return look_up_more_words(
            input(
                "Invalid entry. Please only enter y/yes to look up more words or n/no to exit the program. "
            )
            .strip()
            .lower()
        )


if __name__ == "__main__":
    main()
