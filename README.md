# Conwords App
A customizable dictionary with an integrated word generator that supports different styles, including custom.

The app has a Register/Login mechanism which allows the user to create one dictionary on an account.

# Settings
Here users can set the following options:

- Custom Parts of Speech and their Abbreviations
- Custom Grammatical Genders and their Abbreviations
- Custom words parts for the Word Generator (see: Generator)

# Add Word
Users can use this page to add a new word to their dictionary. 
The form will automatically display any new Parts of Speech or Grammatial Genders that have been added in the Settings.
This page will be blocked (and a corresponding information will be displayed) if the user has not added any Parts of Speech yet.

Users can add the following details:

- Word - The actual word in their constructed language. This field is required
- Meaning - The meaning of the word in any language. This field is required
- Part of Speech - Drop down list displaying all the Parts of Speech defined in the Settings by the user. This field is required
- Grammatical Gender - Drop down list displaying all the Grammatical Genders defined in the Settings by the user
- Phonetic form
- Morphology
- Etymology
- Literal meaning
- Example

# Dictionary
Here users can browse the added records that display as a list of added words allong with their parts of speech abbreviations. Users can also use this page to search words or to display the list of the meanings of the words and access words from there.

Upon cliking a word, the user can see all the details (as they were added in Add Word). 
Double-click a value will enter the edit mode where the user can enter new values and save the changes.
Clicking 'Delete' button removes the selected record and display a corresponding message about which record has just been deleted.

# Generator
The Generator generates words using different styles. 
Currently available styles are:

- Dalish (the language spoken by Dalish elves in Dragon Age game series)
- Dwemeris (the language spoken by ancient Dwarves in The Elder Scrolls game series)
- Huttese (the language spoken by Hutts in Star Wars)
- Custom (the user can define their own custom style in Settings (see: Settings))