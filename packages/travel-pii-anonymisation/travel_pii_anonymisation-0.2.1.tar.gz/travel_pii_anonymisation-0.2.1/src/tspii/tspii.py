from .tools.pseudonymizer import CustomAnonymizer

def load_document_from_file(file_path):
    """Function to load document content from a text file"""
    try:
        with open(file_path, "r") as file:
            document_content = file.read()
        return document_content
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

def save_pseudonymized_content_to_file(file_path, content):
    """Function to save pseudonymized content to a text file"""
    with open(file_path, "w") as file:
        file.write(content)
    print(f"pseudonymized content saved to {file_path}")
    
def run_pseudonymization_process(document_content):
    """Function to handle the pseudonymization process"""
    # Initialize custom pseudonymizer
    pseudonymizer = CustomAnonymizer(add_default_faker_operators=False)
    
    # Add custom recognizers and fake data generators
    pseudonymizer.add_custom_recognizers()
    pseudonymizer.add_custom_fake_data_generators()

    # pseudonymize the document
    print("\nOriginal Document:")
    print(document_content)

    pseudonymized_content = pseudonymizer.anonymize_document(document_content)
    print("\npseudonymized Document:")
    print(pseudonymized_content)

    print("\nDepseudonymization Mapping:")
    print(pseudonymizer.deanonymize_mapping())

    return pseudonymized_content

def main():
    # Sample document for testing
    sample_document = """Date: August 12, 2023
    To: Delta Airlines Customer Service

    Subject: Complaint Regarding Flight disruption and request to compensate 

    Dear Delta Airlines,

    I am writing to express my dissatisfaction with the disruption of flight DL1234 on August 10, 2023,. The disruption was announced just two hours before the scheduled departure time, leaving many passengers stranded.

    Below are the relevant details for my booking:
    - PNR: RFAKP8 - E-ticket: 006-9876543210
    - Passenger Name: John Doe
    - Flight Number: DL1234
    - Aircraft Registration: N835DN (Boeing 737-900ER)
    - ICAO Aircraft Type: B739
    - Departure Airport: JFK (John F. Kennedy International Airport)


    I had important business meetings scheduled upon my arrival, and this disruption caused significant inconvenience. I would like to request compensation as per EU Regulation 261/2004 since I was rebooked on flight DL5678 the next day, arriving over 24 hours later than originally planned.

    Please treat this complaint with urgency and respect for my privacy. You may reach me at my contact details below for any updates:
    - Phone: +1 555-123-4567
    - Email: johndoe@businessmail.com

    Thank you for your prompt attention to this matter.

    Sincerely,
    John Doe
    Frequent Flyer Number: 123456789

    """


    # Option for user to either load document from file or use sample
    print("Welcome to the Document pseudonymizer.")
    choice = input("Would you like to (1) Load a document from a file or (2) Use the sample document? Enter 1 or 2: ")

    if choice == "1":
        file_path = input("Enter the path to the text file: ")
        document_content = load_document_from_file(file_path)
        if document_content:
            pseudonymized_content = run_pseudonymization_process(document_content)
            save_path = input("Enter the path to save the pseudonymized content (e.g., pseudonymized_document.txt): ")
            save_pseudonymized_content_to_file(save_path, pseudonymized_content)
    elif choice == "2":
        # Run the process on the sample document
        pseudonymized_content = run_pseudonymization_process(sample_document)
        save_option = input("Would you like to save the pseudonymized document? (y/n): ")
        if save_option.lower() == "y":
            save_path = input("Enter the path to save the pseudonymized content (e.g., pseudonymized_document.txt): ")
            save_pseudonymized_content_to_file(save_path, pseudonymized_content)
    else:
        print("Invalid choice. Please run the program again and select a valid option.")
        
if __name__ == "__main__":
  main()
