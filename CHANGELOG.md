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