from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from presidio_analyzer import Pattern, PatternRecognizer
from faker import Faker
from presidio_anonymizer.entities import OperatorConfig

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


fake = Faker()

def fake_pnr(_=None):
    return fake.bothify(text="?#?###").upper()

def fake_e_ticket(_=None):
    return fake.bothify(text="###-#########").upper()

def fake_registration(_=None):
    return fake.bothify(text="######").upper()

def fake_iata_aircraft(_=None):
    return fake.bothify(text="###").upper()

def fake_icao_aircraft(_=None):
    return fake.bothify(text="####").upper()

def fake_iata_airline(_=None):
    return fake.bothify(text="##").upper()

def fake_icao_airline(_=None):
    return fake.bothify(text="###").upper()

def fake_ticketing_prefix(_=None):
    return fake.bothify(text="#####").upper()

def fake_iata_airport(_=None):
    return fake.bothify(text="#####").upper()

def fake_icao_airport(_=None):
    return fake.bothify(text="#####").upper()

def fake_faa_airport(_=None):
    return fake.bothify(text="#####").upper()

def fake_us_driver_license(_=None):
    return fake.bothify(text="D#?###-###").upper()  # Example format for US driver's license

def fake_date_time(_=None):
    return fake.date_time_this_decade().strftime("%Y-%m-%d %H:%M:%S")

def fake_person(_=None):
    return fake.name()

def fake_email(_=None):
    return fake.email()

def fake_phone_number(_=None):
    return fake.phone_number()


def create_fake_data_generators():
    return {
        "PNR": OperatorConfig("custom", {"lambda": fake_pnr}),
        "E-TICKET": OperatorConfig("custom", {"lambda": fake_e_ticket}),
        "REGISTRATION": OperatorConfig("custom", {"lambda": fake_registration}),
        "IATA_AIRCRAFT": OperatorConfig("custom", {"lambda": fake_iata_aircraft}),
        "ICAO_AIRCRAFT": OperatorConfig("custom", {"lambda": fake_icao_aircraft}),
        "IATA_AIRLINE": OperatorConfig("custom", {"lambda": fake_iata_airline}),
        "ICAO_AIRLINE": OperatorConfig("custom", {"lambda": fake_icao_airline}),
        "TICKETING_PREFIX": OperatorConfig("custom", {"lambda": fake_ticketing_prefix}),
        "IATA_AIRPORT": OperatorConfig("custom", {"lambda": fake_iata_airport}),
        "ICAO_AIRPORT": OperatorConfig("custom", {"lambda": fake_icao_airport}),
        "FAA_AIRPORT": OperatorConfig("custom", {"lambda": fake_faa_airport}),
        "US_DRIVER_LICENSE": OperatorConfig("custom", {"lambda": fake_us_driver_license}),
        "DATE_TIME": OperatorConfig("custom", {"lambda": fake_date_time}),
        "PERSON": OperatorConfig("custom", {"lambda": fake_person}),
        "EMAIL_ADDRESS": OperatorConfig("custom", {"lambda": fake_email}),
        "PHONE_NUMBER": OperatorConfig("custom", {"lambda": fake_phone_number})

    }


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


