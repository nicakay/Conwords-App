(v1.06) 27/03/2023

Dictionary:
- Added: Search module
- Added: The word list view can be now switched between the default view (dictionary words) and the meaning view (user's translation, eg. English)

Settings:
- Added: Option to add cutsom word parts. They can be added in 'Settings' and used in 'Generator'. The user can now create 3 lists of word parts: Beginnings, Middles and Endings, and add as many word parts to each list as they want. Generator will user the word parts from the user's lists to generate new words according to the following rules:
    - For 2-word-parts words it will use 1 random Beginning and 1 random Ending
    - For 3-word-parts words it will use 1 random Beginning, 1 random Middle and 1 random Ending
    - For 4-word-parts words it will use 1 random Beginning, 2 random Middles and 1 random Ending
- Added: Added an option to delete custom word parts

Generator:
- Added: Custom style implementet in 'Settings' is now available to use in Generator


(v1.05) 25/03/2023

Register:
- Added: Password validation (it compares both fields: 'password' and 'confirmation', checks if the password length is minimum 6 characters and if it contains at least one number)

Dictionary:
- Changed: The 'Save' button is now disabled by default and gets enabled as soon as a user enters the edit more by double-clicking any editable field. It then gets disabled again after saving the record
- Added: Started implementing a search module

Generator:
- Added: Huttese language style

(v1.04) 24/03/2023

Generator:
- Changed: Separated names of styles and numbers of syllables into two separate sections of radio buttons.
- Added: Dwemeris language style


(v1.03) 23/03/2023

Register, Login:
- Added: Modal confirming a creation of an account

Add Word:
- Added: If a new user opens this page without having any parts of speech added yet, the form will be blocked by a pop up - 'The Part of speech cannot be empty. Please check your Settings' - which links to settings.html


(v1.02) 22/03/2023

Dictionary:
- Fixed: Some words had 'part of speech' equal to NULL, which generate errors as this is a none-null field.
- Fixed: Grammatical gender displaying as None if the value was empty
- Added: Separate functionality for the 'Save' and 'Delete' buttons.
- Added: Option to delete a record by pressing 'Delete' and the confirmation modal that pops up after the deletion is completed.
Upon this change the database became now fully functional to a user, who can now create, modify and delete their entries.


(v1.01) 21/03/2023

Dictionary:
- Changed: Moved the 'part of speech' and 'grammatical gender' abbreviations so they now addtionaly display on the right side of the dictionary word
- Changed: 'part of speech' and 'grammatical gender' are now fully displayed on a record
- Fixed: Disappearing cell formatting after editing the cell
- Added: ALT text (title attribute) to all the editable cells
- Added: Verification for two fields: 'part of speech' and 'grammatical gender'. Inputting an value that doesn't exist in the databse will now result with an error message and will terminate all the changes in any cells that follow that cell