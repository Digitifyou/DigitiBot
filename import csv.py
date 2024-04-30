import csv

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
    exit_phrases = ["bye", "exit", "thanks", "thank you", "bye bye"]
    question_lower = question.lower()
    if any(phrase in question_lower for phrase in exit_phrases):
        return "Returning to main menu...", True
    data = read_csv(file_path)
    for keyword in data.keys():
        if keyword in question_lower:  # Check if keyword is a substring of the question
            return data[keyword], False
    return "Sorry, I don't understand that question.", False

def main_interface():
    """Main interface for the chatbot."""
    file_path = r"C:\Users\HP\Desktop\qus.csv"
    while True:
        mode = input("Enter mode (1 for Admin, 2 for Student, 'exit' to quit): ")
        if mode == 'exit':
            break
        elif mode == '1':
            update_keywords(file_path)
        elif mode == '2':
            while True:
                question = input("student: ")
                answer, should_return = find_answer(file_path, question)
                print("bot: " + answer)
                if should_return:
                    break
        else:
            print("Invalid mode selected. Please enter 1 or 2.")

if __name__ == "__main__":
    main_interface()
