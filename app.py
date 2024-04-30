from flask import Flask, render_template, request, jsonify


import mysql.connector
import re
import random
import csv

# Database connection details
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '0000',
    'database': '1school',
    'raise_on_warnings': True,
}

# Connect to the MySQL database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()




def get_details(register_number, detail_type):
    """Fetches details for a given register number from the specified type (fees or result)."""
    try:
        register_number_int = int(register_number)
    except ValueError:
        return "Register number must be a number."
    
    # Adjusted to the correct table name based on detail_type
    table = "fees" if detail_type == "fees" else "result"
    query = f'SELECT * FROM {table} WHERE Register_Number = %s'
    
    cursor.execute(query, (register_number_int,))
    result = cursor.fetchone()
    
    if result:
        columns = [desc[0] for desc in cursor.description]
        details = "\n".join([f"{col}: {val}" for col, val in zip(columns, result)])
        return f"{detail_type.capitalize()} details for register number {register_number}:\n\n{details}"
    else:
        return f" {register_number}  this register number is wrong, enter the correct register number for {detail_type} details."

def extract_register_number(user_input):
    """Extracts register number from user input using regex."""
    match = re.search(r'\b\d+\b', user_input)
    return match.group(0) if match else None

last_requested_type = None

def chatbot_response(user_input):
    global last_requested_type
    greetings = ['hi', 'hello', 'hey', 'hai']
    result_keywords = ['result details', 'results', 'exam report', 'mark', 'mark details','result', 'report']
    fee_keywords = ['fees', 'fee details', 'fee', 'fees detail']
    admission_keywords = ['admission details', 'admission', 'join', 'vacancy', 'admissions']
    
    user_input_lower = user_input.lower()

    if any(greeting in user_input_lower for greeting in greetings):
        return random.choice(['Hello! How can I assist you?', 'Hi there! How can I help you today?', 'Hi, how can I assist you?'])
    if last_requested_type:
        register_number = extract_register_number(user_input)
        
        if register_number:
            response = get_details(register_number, last_requested_type)
            last_requested_type = None  # Reset after use
            return response
        else:
            return "That doesn't look like a valid register number. Please try again."
    
    if any(keyword in user_input_lower for keyword in fee_keywords):
        last_requested_type = "fees"
        register_number = extract_register_number(user_input)
        if register_number:
            return get_details(register_number, "fees")
        return "Please provide a student Register Number."
    
    elif any(keyword in user_input_lower for keyword in result_keywords):
        last_requested_type = "result"
        register_number = extract_register_number(user_input)
        if register_number:
            return get_details(register_number, "result")
        return "Please provide a student Register Number."
    
    elif any(keyword in user_input_lower for keyword in admission_keywords):
        return "Which standard admission do you need for your son/daughter? (Enter a number between 1 and 10)"

    # Handling admission standard selection
    elif user_input_lower.isdigit():
        standard = int(user_input_lower)
        if 1 <= standard <= 10:
            # Assuming 'Admission' is the correct table name
            cursor.execute("SELECT * FROM Admission WHERE Standard = %s", (standard,))
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                details = "\n".join([f"<table><tr><td>{col}</td><td>{val}</td></tr></table>" for col, val in zip(columns, result)])
                return f"Admission details for standard {standard}:\n\n{details}"
            else:
                return f"No admission information found for standard {standard}."
        else:
            return "Please enter a number between 1 and 10 for the standard."

    return "I'm not sure how to respond to that. Can you specify what you need?"


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Extract the user input from the form data
    user_input = request.form['message']
    
    # Process the input here (example: echo the input)
    response_text = f"You said: {user_input}"
    # Return the processed input as JSON
    return jsonify({'response': user_input,'replay':chatbot_response(user_input)})

if __name__ == "__main__":
    app.run(debug=True)

    




