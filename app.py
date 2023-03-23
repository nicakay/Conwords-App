from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import random
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_db, login_required, validate_password
import itertools

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    # The cash of the currently logged user
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Define 'error' - variable for displaying errors
        notification_error = ""
        
        # Open DB connection
        db = get_db()

        # Query database for username
        results = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"), )).fetchall()

        # Ensire the user exists
        if len(results) == 0:
            notification_error = "The user does not exist"
            # Close DB connection
            db.close()
            return render_template("login.html", notification_error = notification_error)
       
        elif not check_password_hash(results[0][2], request.form.get("password")):
            notification_error = "The password is incorrect"
            # Close DB connection
            db.close()
            return render_template("login.html", notification_error = notification_error)

        else:
            # Remember which user has logged in
            session["user_id"] = results[0][0]
        
            # Redirect user to home page
            return redirect("/")   

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Define 'error' - variable for displaying errors
        notification_error = ""

        # Save the password in a variable
        password = request.form.get("password")

        # if validate_password(password) == True:
        # Open DB connection
        db = get_db()

        # Check if that username already exists
        username = request.form.get("username")
        results = db.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchall()

        # If the user already exists
        if len(results) == 1:
            notification_error = "The user already exists"
            db.close()
            return render_template("register.html", notification_error = notification_error)

        else:
            # Hash the password and the user into the database
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            print(password_hash)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", (username, password_hash))
            db.commit()
            # Close DB connection
            db.close()

            return render_template("login.html", show_modal=True, account=username)
        

    return render_template("register.html")


@app.route("/")
@login_required
def home():

    # Connect to the database
    db = get_db()

    # Get the username
    username = db.execute("SELECT username FROM users WHERE id = ?;", (session["user_id"],)).fetchone()

    # Get the number of all the entries
    num_of_entries = db.execute("SELECT COUNT(*) FROM entries WHERE user_id = ?;", (session["user_id"],)).fetchone()

    # Get the number of all the words
    num_of_words = db.execute("SELECT COUNT(*) FROM words WHERE user_id = ?;", (session["user_id"],)).fetchone()

    db.close()
    return render_template("index.html", num_of_words=num_of_words, num_of_entries=num_of_entries, username=username)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    # Connect to the database
    db = get_db()

    pos_list_empty = 0
    gram_list_empty = 0
    pos_list = db.execute("SELECT part_of_speech, abbreviation FROM parts_of_speech WHERE user_id = ?;", (session["user_id"],)).fetchall()
    gram_gender_list = db.execute("SELECT grammatical_gender, abbreviation FROM grammatical_genders WHERE user_id = ?;", (session["user_id"], )).fetchall()

    # If the Parts of Speech list is empty
    if len(pos_list) == 0:
        pos_list_empty = 1
        pos_placeholder = "Parts of Speech have not been defined yet"
    else:
        pos_list_empty = 0
        pos_placeholder = ""

    if len(gram_gender_list) == 0:
        gram_list_empty = 1
        gram_placeholder = "Grammatical Genders have not been defined yet"
    else:
        gram_list_empty = 0
        gram_placeholder = "ddd"

    if request.method == "POST":
        if "partOfSpeech" in request.form:
            part_of_speech = request.form.get("partOfSpeech")
            pos_abbreviation = request.form.get("partOfSpeechAbbreviation")
            db.execute("INSERT INTO parts_of_speech (part_of_speech, abbreviation, user_id) VALUES (?, ?, ?)", (part_of_speech, pos_abbreviation, session["user_id"]))
            db.commit()
        
        elif "gramGender" in request.form:
            gram_gender = request.form.get("gramGender")
            gram_abbreviation = request.form.get("gramGenderAbbreviation")
            db.execute("INSERT INTO grammatical_genders (grammatical_gender, abbreviation, user_id) VALUES (?, ?, ?)", (gram_gender, gram_abbreviation, session["user_id"]))
            db.commit()

        elif "pos_item" in request.form:
            item_to_remove = request.form.get("pos_item")
            db.execute("DELETE FROM parts_of_speech WHERE part_of_speech = ? AND user_id = ?", (item_to_remove, session["user_id"]))
            db.commit()

        elif "gram_gender_item" in request.form:
            item_to_remove = request.form.get("gram_gender_item")
            db.execute("DELETE FROM grammatical_genders WHERE grammatical_gender = ? AND user_id = ?", (item_to_remove, session["user_id"]))
            db.commit()

    db.close()
    return render_template("settings.html", pos_list=pos_list, gram_gender_list=gram_gender_list, pos_placeholder=pos_placeholder, gram_placeholder=gram_placeholder, pos_list_empty=pos_list_empty, gram_list_empty=gram_list_empty)


@app.route("/addword", methods=["GET", "POST"])
@login_required
def add_word():
    db = get_db()

    # Display links for each entry on the left
    words = db.execute("SELECT entries.id, word, abbreviation FROM entries, words, parts_of_speech WHERE entries.word_id = words.id AND entries.part_of_speech_id = parts_of_speech.id AND entries.user_id = ? ORDER BY word;", (session["user_id"],)).fetchall()

    pos_list = db.execute("SELECT part_of_speech FROM parts_of_speech WHERE user_id = ?;", (session["user_id"],)).fetchall()
    gram_gender_list = db.execute("SELECT grammatical_gender FROM grammatical_genders WHERE user_id = ?;", (session["user_id"], )).fetchall()

    if len(pos_list) == 0:
        return render_template("addword.html", pos_list=pos_list, gram_gender_list=gram_gender_list, words=words, pos_list_empty=True)

    if request.method == "POST":
        # Get the user inputs from all the fields
        word = request.form.get("inputWord")
        meaning = request.form.get("inputMeaning")
        part_of_speech = request.form.get("inputPOS")
        gram_gender = request.form.get("inputGender")
        phonetic_form = request.form.get("inputPhonetic")
        morphology = request.form.get("inputMorphology")
        etymology = request.form.get("inputEtymology")
        literal_meaning = request.form.get("inputLiteralMeaning")
        example = request.form.get("inputExample")

        # ======== Insert the values into the database ========
    
        # Insert the word
        db.execute("INSERT INTO words (word, user_id) VALUES (?, ?)", (word, session["user_id"]))
        db.commit()
        # Get the id of the word
        word_id = db.execute("SELECT id FROM words WHERE word = ? AND user_id = ?;", (word, session["user_id"],)).fetchone()[0]
        # Instert the meaning
        db.execute("INSERT INTO meanings (meaning, user_id) VALUES (?, ?)", (meaning, session["user_id"]))
        db.commit()
        # Get the id of the meaning
        meaning_id = db.execute("SELECT id FROM meanings WHERE meaning = ? AND user_id = ?;", (meaning, session["user_id"],)).fetchone()[0]
        # Get the id of the part of speech
        pos_id = db.execute("SELECT id FROM parts_of_speech WHERE part_of_speech = ? AND user_id = ?;", (part_of_speech, session["user_id"],)).fetchone()[0]
        # Get the id of the grammatical gender IF there is any selected
        if not gram_gender == "none":
            gram_id = db.execute("SELECT id FROM grammatical_genders WHERE grammatical_gender = ? AND user_id = ?;", (gram_gender, session["user_id"],)).fetchone()[0]
 
        # ======== Insert this record (except the gender id) to the ENTRIES table ========
        db.execute("INSERT INTO entries (word_id, meaning_id, part_of_speech_id, phonetic_form, morphology, etymology, literal_meaning, example, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (word_id, meaning_id, pos_id, phonetic_form, morphology, etymology, literal_meaning, example, session["user_id"]))
        db.commit()
        
        # Insert grammatical gender ID there's any
        if not gram_gender == "none":
            last_entry_of_this_user = db.execute("SELECT id FROM entries WHERE user_id = ? ORDER BY id DESC LIMIT 1;", (session["user_id"],)).fetchone()[0]
            db.execute("UPDATE entries SET grammatical_gender_id = ? WHERE id = ?;", (gram_id, last_entry_of_this_user,))
            db.commit()
    
    db.close()
    return render_template("addword.html", pos_list=pos_list, gram_gender_list=gram_gender_list, words=words)


@app.route("/dictionary", methods=["GET", "POST"])
@login_required
def dictionary():

    # Connect to the database
    db = get_db()

    # Display links for each entry on the left
    words = db.execute("SELECT entries.id, word, abbreviation FROM entries, words, parts_of_speech WHERE entries.word_id = words.id AND entries.part_of_speech_id = parts_of_speech.id AND entries.user_id = ? ORDER BY word;", (session["user_id"],)).fetchall()

    # Details of each entry after clicking a link
    if request.method == "GET":
        entry_id = str(request.args.get('value'))
        session["entry_id"] = entry_id
        record = db.execute("SELECT * FROM entries WHERE id = ? AND user_id = ?;", (entry_id, session["user_id"],)).fetchone()
        if not record == None:
            session["record"] = record

            word = db.execute("SELECT word FROM words WHERE id = ? AND user_id = ?;", (record[1], session["user_id"],)).fetchone()[0]
            session["word"] = word
            session["word_id"] = str(record[1])

            meaning = db.execute("SELECT meaning FROM meanings WHERE id = ? AND user_id = ?;", (record[2], session["user_id"],)).fetchone()[0]
            session["meaning"] = meaning
            session["meaning_id"] = str(record[2])

            part_of_speech = db.execute("SELECT part_of_speech FROM parts_of_speech WHERE id = ? AND user_id = ?;", (record[3], session["user_id"],)).fetchone()[0]
            session["pos"] = part_of_speech
            part_of_speech_abbr = db.execute("SELECT abbreviation FROM parts_of_speech WHERE id = ? AND user_id = ?;", (record[3], session["user_id"],)).fetchone()[0]
            session["pos_abbr"] = part_of_speech_abbr

            if not record[4] == None:
                gender = db.execute("SELECT grammatical_gender FROM grammatical_genders WHERE id = ? AND user_id = ?;", (record[4], session["user_id"],)).fetchone()[0]
                gender_abbr = db.execute("SELECT abbreviation FROM grammatical_genders WHERE id = ? AND user_id = ?;", (record[4], session["user_id"],)).fetchone()         
            else:             
                gender = ""
                gender_abbr = ""
            session["gender"] = gender
            session["gender_abbr"] = gender_abbr

            session["phonetic"] = record[5]
            session["morphology"] = record[6]
            session["etymology"] = record[7]
            session["literal"] = record[8]
            session["example"] = record[9]

        else:
            word = ["empty"]
            meaning = ["empty"]
            part_of_speech = ["empty"]
            part_of_speech_abbr = ["empty"]
            gender = ["empty"]
            gender_abbr = ["empty"]


    # On POS
    else:

        # If the user presses 'Save'
        if request.form["formsubmit"] == "Save":
            # Connect to the database
            db = get_db()

            # Get data from all the editable fields
            edited_pos = request.form.get("pos")
            edited_gender = request.form.get("gender")
            edited_meaning = request.form.get("meaning")
            edited_phonetic = request.form.get("phonetic")
            edited_morphology = request.form.get("morphology")
            edited_etymology = request.form.get("etymology")
            edited_literal = request.form.get("literal")
            edited_example = request.form.get("example")

            # If the user changed 'part of speech'
            if edited_pos != session["pos"]:

                # Verify if the entered 'part_of_speech' exists
                # Fetch all the 'parts of speech' stored in the databse
                pos_tuples = db.execute("SELECT part_of_speech FROM parts_of_speech WHERE user_id = ?;", (session["user_id"],)).fetchall()
                # Convert the list of tuples into a list using itertools convertion
                pos_list = list(itertools.chain(*pos_tuples))

                # If the value gave by the user is in that list
                if edited_pos in pos_list:

                    # Commit the change in the database
                    db.execute("UPDATE entries SET part_of_speech_id = (SELECT id FROM parts_of_speech WHERE part_of_speech = ?) WHERE id = ?;", (edited_pos, session["entry_id"]))
                    db.commit()

                    # And save the 'part of speech' info to display it on the page once the record is updated 
                    part_of_speech = edited_pos
                    part_of_speech_abbr = db.execute("SELECT abbreviation FROM parts_of_speech WHERE part_of_speech = ?;", (part_of_speech,)).fetchone()[0]

                # If the user value is not in the database
                else:
                    # Create an error message
                    error = f"The entered part of speech: '{edited_pos}' does not exist. Please check your settings"
                    # Send that error to the error template
                    return render_template("dict_error.html", words=words, error=error)
            
            else:
                part_of_speech = session["pos"]
                part_of_speech_abbr = session["pos_abbr"]

            # If the user changed 'grammatical gender'
            if not session["gender"] == None and edited_gender != session["gender"]:

                # Verify if the entered 'grammatical_gender' exists
                # Fetch all the 'grammatical genders' stored in the databse
                genders_tuples = db.execute("SELECT grammatical_gender FROM grammatical_genders WHERE user_id = ?;", (session["user_id"],)).fetchall()
                # Convert the list of tuples into a list using itertools convertion
                genders_list = list(itertools.chain(*genders_tuples))

                # If the value gave by the user is in that list
                if edited_gender in genders_list:

                    # Commit the change in the database
                    db.execute("UPDATE entries SET grammatical_gender_id = (SELECT id FROM grammatical_genders WHERE grammatical_gender = ?) WHERE id = ?;", (edited_gender, session["entry_id"]))
                    db.commit()

                    # And save the 'gender' info to display it on the page once the record is updated 
                    gender = edited_gender
                    gender_abbr = db.execute("SELECT abbreviation FROM grammatical_genders WHERE grammatical_gender = ?;", (gender,)).fetchone()[0]

                # If the user value is not in the database
                else:
                    # Create an error message
                    error = f"The entered grammatical gender: '{edited_gender}' does not exist. Please check your settings"
                    # Send that error to the error template
                    return render_template("dict_error.html", words=words, error=error)
            else:
                gender = session["gender"]
                gender_abbr = session["gender_abbr"]

            # If the user changed 'meaning'
            if edited_meaning != session["meaning"]:
                db.execute("UPDATE meanings SET meaning = ? WHERE id IN (SELECT meaning_id FROM entries WHERE id = ?);", (edited_meaning, session["entry_id"]))
                db.commit()
                meaning = edited_meaning
            else:
                meaning = session["meaning"]

            # If the user changed 'phonetic form'
            if edited_phonetic != session["phonetic"]:
                db.execute("UPDATE entries SET phonetic_form = ? WHERE id = ?;", (edited_phonetic, session["entry_id"]))
                db.commit()
                phonetic = edited_phonetic
            else:
                phonetic = session["phonetic"]

            # If the user changed 'morphology'
            if edited_morphology != session["morphology"]:
                db.execute("UPDATE entries SET morphology = ? WHERE id = ?;", (edited_morphology, session["entry_id"]))
                db.commit()
                morphology = edited_morphology
            else:
                morphology = session["morphology"]

            # If the user changed 'etymology'
            if edited_etymology != session["etymology"]:
                db.execute("UPDATE entries SET etymology = ? WHERE id = ?;", (edited_etymology, session["entry_id"]))
                db.commit()
                etymology = edited_etymology
            else:
                etymology = session["etymology"]

            # If the user changed 'literal meaning'
            if edited_literal != session["literal"]:
                db.execute("UPDATE entries SET literal_meaning = ? WHERE id = ?;", (edited_literal, session["entry_id"]))
                db.commit()
                literal = edited_literal
            else:
                literal = session["literal"]

            # If the user changed 'example'
            if edited_example != session["example"]:
                db.execute("UPDATE entries SET example = ? WHERE id = ?;", (edited_example, session["entry_id"]))
                db.commit()
                example = edited_example
            else:
                example = session["example"]

            record = (None, None, None, None, None, phonetic, morphology, etymology, literal, example)
            word = session["word"]
            info = "The record has been updated"
        
            db.close()

            return render_template("dictionary.html", record=record, word=word, meaning=meaning, part_of_speech=part_of_speech, words=words, gender=gender, part_of_speech_abbr=part_of_speech_abbr, gender_abbr=gender_abbr, info=info)
        
        # If the user click the 'Delete' button
        elif request.form["formsubmit"] == "Delete":
            # Save the word to pass it to the info modal
            word_to_delete = session["word"]

            # Delete the entry from the 'entries' table
            db.execute("DELETE FROM entries WHERE word_id = ? AND meaning_id = ?;", (session["word_id"], session["meaning_id"]))
            db.commit()

            # Delete the word from the 'words' table
            db.execute("DELETE FROM words WHERE id = ?;", (session["word_id"],))
            db.commit()

            # Delete the meaning from the 'meanings' table
            db.execute("DELETE FROM meanings WHERE id = ?;", (session["meaning_id"],))
            db.commit()

            return render_template("dictionary.html", words=words, word_to_delete=word_to_delete, show_modal=True, record=None)
        
    db.close()

    return render_template("dictionary.html", record=record, word=word, meaning=meaning, part_of_speech=part_of_speech, part_of_speech_abbr=part_of_speech_abbr, gender_abbr=gender_abbr, words=words, gender=gender)


@app.route("/word-generator", methods=["GET", "POST"])
@login_required
def word_generator():
    
    # Connect to the database
    db = get_db()

    generated_words = []

    # Get all the beginnings
    def getBeginnings(style):
        b_list = db.execute("SELECT word_part FROM word_parts WHERE style_id = ? AND position_id = ?;", (style, 1,)).fetchall()
        return b_list

    # Get all the middles
    def getMLiddles(style):
        m_list = db.execute("SELECT word_part FROM word_parts WHERE style_id = ? AND position_id = ?;", (style, 2,)).fetchall()
        return m_list

    # Get all the endings
    def getEndings(style):
        e_list = db.execute("SELECT word_part FROM word_parts WHERE style_id = ? AND position_id = ?;", (style, 3,)).fetchall()
        return e_list

    # If the user clicks 'Generate'
    if request.method == "POST":
        try:
            if request.form["style"] == "dalishStyle2":
                for _ in range(10):
                    b_list = getBeginnings(1)
                    m_list = getMLiddles(1)
                    e_list = getEndings(1)
                    beginnnig = random.choice(b_list)[0]
                    end = random.choice(e_list)[0]
                    word = beginnnig + end

                    generated_words.append(word)

                    session["style"] = request.form["style"]

            elif request.form["style"] == "dalishStyle3":
                for _ in range(10):
                    b_list = getBeginnings(1)
                    m_list = getMLiddles(1)
                    e_list = getEndings(1)
                    beginnnig = random.choice(b_list)[0]
                    middle = random.choice(m_list)[0]
                    end = random.choice(e_list)[0]
                    word = beginnnig + middle + end

                    generated_words.append(word)

                    session["style"] = request.form["style"]
                    
            elif request.form["style"] == "dalishStyle4":
                for _ in range(10):
                    b_list = getBeginnings(1)
                    m_list = getMLiddles(1)
                    e_list = getEndings(1)
                    beginnnig = random.choice(b_list)[0]
                    middle1 = random.choice(m_list)[0]
                    middle2 = random.choice(m_list)[0]
                    end = random.choice(e_list)[0]
                    word = beginnnig + middle1 + middle2 + end

                    generated_words.append(word)

                    session["style"] = request.form["style"]

            session["generated_words"] = generated_words

        except KeyError:
            print("There was a key error in the generator template")
            return render_template("word-generator.html")
        
    db.close()

    # Saves the chosen_style in order to pass it to the JS script
    try:
        if not session["style"] == None:
            chosen_style = session["style"]
        else:
            chosen_style = "Undefined"
    except KeyError:
        return render_template("word-generator.html")

    return render_template("word-generator.html", generated_words=generated_words, chosen_style=chosen_style)
