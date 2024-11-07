from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from generators import create_fake_data_generators
from presidio_analyzer import Pattern, PatternRecognizer

def create_recognizers():
    recognizers = []

    # PNR Recognizer
    pnr_pattern = Pattern(name="pnr_pattern", regex="[A-Z0-9]{5}\d{1}", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="PNR", patterns=[pnr_pattern], context=["PNR", "PNRs", "PNR codes"]))

    # E-TICKET Recognizer
    ticket_pattern = Pattern(name="e-ticket_pattern", regex="[0-9]{3}(-)?[0-9]{10}", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="E-TICKET", patterns=[ticket_pattern], context=["e-ticket", "ticket number"]))

    # Aircraft Registrations
    registration_pattern = Pattern(name="registration_pattern", regex="^[A-Z]-[A-Z]{4}|[A-Z]{2}-[A-Z]{3}|N[0-9]{1,5}[A-Z]{0,2}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="REGISTRATION", patterns=[registration_pattern], context=["registration", "registration number"]))

    # IATA Aircraft Type
    iata_aircraft_pattern = Pattern(name="iata_aircraft_pattern", regex="^[A-Z0-9]{3}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="IATA_AIRCRAFT", patterns=[iata_aircraft_pattern], context=["IATA aircraft type", "aircraft type"]))

    # ICAO Aircraft Type
    icao_aircraft_pattern = Pattern(name="icao_aircraft_pattern", regex="^[A-Z]{1}[A-Z0-9]{1,3}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="ICAO_AIRCRAFT", patterns=[icao_aircraft_pattern], context=["ICAO aircraft type"]))


    icao_airline_pattern = Pattern(name="icao_airline_pattern", regex="^[A-Z]{3}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="ICAO_AIRLINE", patterns=[icao_airline_pattern], context=["ICAO airline code", "operational code"]))

    # Ticketing Prefix
    ticketing_prefix_pattern = Pattern(name="ticketing_prefix_pattern", regex="^[0-9]{3}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="TICKETING_PREFIX", patterns=[ticketing_prefix_pattern], context=["ticketing prefix", "eTicket operator code"]))

    # Airport Codes
    iata_airport_pattern = Pattern(name="iata_airport_pattern", regex="^[A-Z]{3}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="IATA_AIRPORT", patterns=[iata_airport_pattern], context=["IATA airport code", "airport code"]))

    icao_airport_pattern = Pattern(name="icao_airport_pattern", regex="^[A-Z]{4}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="ICAO_AIRPORT", patterns=[icao_airport_pattern], context=["ICAO airport code"]))

    faa_airport_pattern = Pattern(name="faa_airport_pattern", regex="^[A-Z0-9]{3,4}$", score=1)  # Adjusted score
    recognizers.append(PatternRecognizer(supported_entity="FAA_AIRPORT", patterns=[faa_airport_pattern], context=["FAA airport code", "US FAA-specific locator"]))

    return recognizers

# ----------
# Purpose: This file contains all the regular expressions and recognizers required for detecting different aviation-related entities like PNR, aircraft types, and airport codes.


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
