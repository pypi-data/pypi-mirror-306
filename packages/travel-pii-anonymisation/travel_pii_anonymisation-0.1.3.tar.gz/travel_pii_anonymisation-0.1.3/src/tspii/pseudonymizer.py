# anonymizer.py
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from recognizers import create_recognizers
from generators import create_fake_data_generators

class CustomAnonymizer:
    def __init__(self, add_default_faker_operators=True, faker_seed=None):
        # Initialize the anonymizer with or without faker operators
        self.anonymizer = PresidioReversibleAnonymizer(
            add_default_faker_operators=add_default_faker_operators,
            faker_seed=faker_seed
        )

    def add_custom_recognizers(self):
        recognizers = create_recognizers()
        for recognizer in recognizers:
            self.anonymizer.add_recognizer(recognizer)

    def add_custom_fake_data_generators(self):
        operators = create_fake_data_generators()
        self.anonymizer.add_operators(operators)

    def reset_mapping(self):
        self.anonymizer.reset_deanonymizer_mapping()

    def anonymize_document(self, document_content):
        return self.anonymizer.anonymize(document_content)

    def deanonymize_mapping(self):
        return self.anonymizer.deanonymizer_mapping

# ----------
# Purpose: This file contains the main class responsible for anonymization processes, including setting up custom recognizers and adding fake data generators.
