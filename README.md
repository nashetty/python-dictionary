# Terminal Dictionary App

Welcome to the Terminal Dictionary App! This is a simple yet powerful console-based dictionary application built with Python. It allows users to search for words, fetch detailed information from an external API, and even save the results to a file for future reference.

## Features

- **Word Lookup**: Enter any word to retrieve its pronunciation, synonyms, antonyms, definition, example usage, and part of speech.
- **Error Handling**: The app gracefully handles situations where a word is not found or when there is a server error.
- **Multiple Results**: If a word has multiple definitions or related data, the app will display all relevant information.
- **File Storage**: Save your search results to a file with options to overwrite or append if the file already exists.
- **User-Friendly**: The app guides users through each step, ensuring an intuitive and seamless experience.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/nashetty/python-dictionary.git
    cd python-dictionary
    ```
2. **Install Dependencies**  
   Ensure you have Python installed, then install any necessary dependencies.
   ```bash
   pip install requests
   ```

4. **Run the App**  
   Start the dictionary app by running the main Python script.
   ```bash
   python dictionary.py
   ```
## Example Screenshot
<img width="1141" alt="Python_dictionary" src="https://github.com/user-attachments/assets/d0247147-28ae-485a-828e-f5fa31db0ae9">  

## How to Use

1. **Launch the App**  
   Run the app using the command above. You’ll be welcomed and given a brief explanation of what the app does.

2. **Search for a Word**  
   When prompted, enter the word you wish to search for. The app will fetch data from the API and display detailed information about the word.

3. **Save Results**  
   After displaying the word’s details, the app will ask if you want to save the result to a file. You can name the file, choose to overwrite or append, and the data will be saved accordingly.

4. **Continue Searching**  
   The app will ask if you want to search for another word. You can continue searching or exit the app at this time.

## API Reference

This app uses the [Dictionary API](https://dictionaryapi.dev/) to fetch word data. The API is free and does not require an API key.

## Future Enhancements

- Implement a feature to store and retrieve past searches.
- Expand the app with a GUI interface for easier use.

## Acknowledgements

- [Dictionary API](https://dictionaryapi.dev/) for providing the word data.
- [Python](https://www.python.org/) for being an awesome programming language.
