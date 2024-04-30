from flask import Flask, request, render_template_string, session
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'JooQzyTgv4YjT1VdodK96A'  # Needed to secure sessions

# Database connection details
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '0000',
    'database': '1school'
}

# Initialize database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

def get_details(register_number, detail_type):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    table = "fees" if detail_type == "fees" else "result"
    query = f"SELECT * FROM {table} WHERE Register_Number = %s"
    
    cursor.execute(query, (register_number,))
    result = cursor.fetchone()
    
    connection.close()
    
    if result:
        columns = [desc[0] for desc in cursor.description]
        details = "<br>".join([f"{col}: {val}" for col, val in zip(columns, result)])
        return f"{detail_type.capitalize()} details for register number {register_number}:<br>{details}"
    else:
        return f"No {detail_type} information found for register number {register_number}."

def chatbot_response(user_input):
    register_number = re.search(r'\b\d+\b', user_input)
    detail_type = "fees" if "fees" in user_input.lower() else "result" if "result" in user_input.lower() else None
    
    if register_number and detail_type:
        return get_details(register_number.group(), detail_type)
    
    return "Please specify if you are asking for 'fees' or 'result' and provide a valid register number."

@app.route("/", methods=["GET", "POST"])
def chat():
    if 'history' not in session:
        session['history'] = []  # Initialize history in session

    if request.method == "POST":
        user_input = request.form.get("user_input")
        response = chatbot_response(user_input)
        session['history'].append(('You', user_input))  # Store user input
        session['history'].append(('Bot', response))  # Store bot response
    
    return render_template_string(HTML_TEMPLATE, history=session.get('history'))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot Interface</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f5f5f5; }
        .chat-container { width: 90%; max-width: 600px; background-color: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); border-radius: 8px; }
        .bot-response { background-color: #e1f5fe; padding: 10px; margin: 10px 0; border-radius: 8px; }
        input[type="text"], button { padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
        input[type="text"] { width: calc(100% - 122px); }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .chat-history { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>Chat with our Bot</h2>
        <form method="post">
            <input type="text" name="user_input" autofocus placeholder="Ask me something...">
            <button type="submit">Send</button>
        </form>
        <div class="chat-history">
            {% for speaker, message in history %}
                <div><strong>{{ speaker }}:</strong> {{ message }}</div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
