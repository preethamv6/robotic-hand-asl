from pyfirmata2 import Arduino
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

import speech_recognition as sr 

# Initialize the recognizer 
r = sr.Recognizer()

# Set up the Arduino board
board = Arduino('COM9 ')   # Change 'COM3' to your Arduino port
# Define servo pins
index_servo = board.get_pin('d:10:s')  
middle_servo = board.get_pin('d:6:s') 
ring_servo = board.get_pin('d:9:s')  
little_servo = board.get_pin('d:5:s') 
thumb_servo = board.get_pin('d:11:s') 

def record_text():
    # Loop in case of errors
    while True:
        try:
            # Use the microphone as source for input
            with sr.Microphone() as source2:
                # Prepare recognizer to receive input
                r.adjust_for_ambient_noise(source2, duration=0.2)
                # Listens for the user's input
                audio2 = r.listen(source2)
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")
        return

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text)
        f.write("\n")

def process_text():
    text = record_text()

    if not isinstance(text, str) or not text.strip():
        print("Invalid or empty text. Skipping...")
        return []

    # Save the raw text
    output_text(text)
    print("Wrote text:", text)

    # Tokenize the text into words
    try:
        word_tokens = word_tokenize(text)
    except Exception as e:
        print(f"Error during tokenization: {e}")
        return []

    # Remove stopwords
    filtered_words = [word for word in word_tokens if word.lower() not in stop_words]

    # Lemmatize
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # Process into ASL format (optional rearranging)
    processed_sentence = " ".join(lemmatized_words)

    # Extract individual letters and numbers
    letters_numbers = [char for char in processed_sentence if char.isalnum()]

    print("Original Text:", text)
    print("Filtered Words:", filtered_words)
    print("Lemmatized Words:", lemmatized_words)
    print("Processed Sentence:", processed_sentence)
    print("Letters and Numbers:", letters_numbers)

    return letters_numbers

def set_fingers(index=0, middle=0, ring=0, little=0, thumb=0):
    index_servo.write(index)
    middle_servo.write(middle)
    ring_servo.write(ring)
    little_servo.write(little)
    thumb_servo.write(thumb)
    time.sleep(1)

# MAIN LOOP
try:
    set_fingers()  # Initialize the servos with default positions
    print("Begin voice input")
    while True:
        letters_numbers = process_text()  # Get the processed letters and numbers from speech

        # Check if letters_numbers is empty, if so, skip the iteration
        if not letters_numbers:
            continue

        for i in letters_numbers:
            if i.isalpha():
                if i == 'a':
                   set_fingers(180, 180, 180, 180, 0)
                elif i == 'b':
                     set_fingers(0, 0, 0, 0, 180)
                elif i == 'c':
                     set_fingers(45, 45, 45, 45, 45)
                elif i == 'd':
                     set_fingers(180,135,135,135,180)
                elif i == 'e':
                     set_fingers(180, 180, 180, 180, 180)
                elif i == 'f':
                     set_fingers(180, 0, 0, 0, 180)
                elif i == 'g':
                     set_fingers(0, 90, 0, 90, 0)
                elif i == 'h':
                     set_fingers(90, 0, 90, 0, 0)
                elif i == 'i':
                     set_fingers(180,180,180,0,180)
                elif i == 'j':
                     set_fingers(180,180,180,0,180)
                elif i == 'k':
                     set_fingers(0, 0, 180, 180, 90)
                elif i == 'l':
                     set_fingers(0, 180, 180, 180, 0)
                elif i == 'm':
                     set_fingers(180, 150, 150, 180, 180)
                elif i == 'n':
                     set_fingers(180, 150, 180, 180, 180)
                elif i == 'o':
                     set_fingers(100,100,100,100,100)
                elif i == 'p':
                     set_fingers(0, 155, 155, 155, 20) #not done
                elif i == 'q':
                     set_fingers(45, 155, 155, 155, 20) #not done
                elif i == 'r':
                     set_fingers(25,0,180,180,180) 
                elif i == 's':
                     set_fingers(180,180,180,180,180)
                elif i == 't':
                     set_fingers(160, 180, 180, 180, 180)
                elif i == 'u':
                     set_fingers(0, 0, 180, 180, 180)
                elif i == 'v':
                     set_fingers(0, 0, 180, 180, 180)
                elif i == 'w':
                     set_fingers(0, 0, 0, 180, 180)
                elif i == 'x':
                     set_fingers(90, 180, 180, 180, 180)
                elif i == 'y':
                     set_fingers(180, 180, 180, 0, 0)
                elif i == 'z':
                     set_fingers(0, 180, 180, 180, 180)

            elif i.isdigit():
                if i == '1':
                     set_fingers(0,180,180,180,180)
                elif i == '2':
                     set_fingers(0,0,180,180,180)
                elif i == '3':
                     set_fingers(0,0,180,180,0)
                elif i == '4':
                     set_fingers(0,0,0,0,180)
                elif i == '5':
                     set_fingers(0,0,0,0,0)
                elif i == '6':
                     set_fingers(0,0,0,180,180)
                elif i == '7':
                     set_fingers(0,0,180,0,180)
                elif i == '8':
                     set_fingers(0,180,0,0,180)
                elif i == '9':
                     set_fingers(180,0,0,0,180)
                elif i == '0':
                     set_fingers(90,90,90,90,90)
            elif i == ' ':
                set_fingers()  # Reset all fingers

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    board.exit()  # Clean up and close the connection