import csv
import mysql.connector
import re
import random

# Database connection details
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '0000',
    'database': '1school'
}

# Connect to the MySQL database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

def read_csv(file_path):
    """Reads keywords and answers from a CSV file."""
    data = {}
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                keyword, answer = row
                data[keyword.lower()] = answer  # Store keywords in lowercase
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet.
    return data

def write_csv(file_path, data):
    """Writes keywords and answers to a CSV file."""
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for keyword, answer in data.items():
            writer.writerow([keyword, answer])

def update_keywords(file_path):
    """Allows admin to update keywords and answers."""
    data = read_csv(file_path)
    while True:
        keyword = input("Enter keyword (or type 'exit' to finish): ")
        if keyword.lower() == 'exit':
            break
        answer = input("Enter answer for keyword: ")
        data[keyword.lower()] = answer  # Store keywords in lowercase
    write_csv(file_path, data)

def find_answer(file_path, question):
    """Finds and returns the answer to a given question by searching for keywords within the sentence."""
    data = read_csv(file_path)
    for keyword in data.keys():
        if keyword in question.lower():  # Check if keyword is a substring of the question
            return data[keyword], False
    return "Sorry, I don't understand that question.", False

def main_interface():
    """Main interface for the chatbot."""
    file_path = "path/to/your/csv.csv"  # Update this path to your CSV file location
    while True:
        mode = input("Enter mode (1 for Admin, 2 for Student, 'exit' to quit): ")
        if mode == 'exit':
            break
        elif mode == '1':
            update_keywords(file_path)
        elif mode == '2':
            user_input = input("student: ")
            if user_input.lower() in ['bye', 'exit', 'thanks', 'thank you', 'bye bye']:
                print("Bot: Returning to main menu...")
                continue
            answer, _ = find_answer(file_path, user_input)
            if answer == "Sorry, I don't understand that question.":
                response = chatbot_response(user_input)
                print("Bot:", response)
            else:
                print("Bot:", answer)
        else:
            print("Invalid mode selected. Please enter 1 or 2.")

def chatbot_response(user_input):
    # Implementation of chatbot_response function as before
    # This includes all the database interaction and keyword-based response logic
    # Make sure to include global variables and functions used within chatbot_response
    pass  # Replace pass with the actual implementation

if __name__ == "__main__":
    main_interface()
