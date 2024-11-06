# TravelSpecificPIIPseudonymization

**TravelSpecificPIIPseudonymization** is a Python-based tool designed to detect and pseudonymize personally identifiable information (PII) in travel-related documents. It leverages custom recognizers and fake data generators for specific aviation industry entities such as Passenger Name Records (PNRs), e-tickets, flight numbers, airline and aircraft codes, and airport codes. The pseudonymization tool ensures the privacy and confidentiality of sensitive data commonly found in aviation documents, making it suitable for airline companies, travel agencies, and other organizations dealing with flight information.

## Features

- **Pseudonymization of Travel-Related PII**: Detects and pseudonymizes common entities in airline and aviation-related documents such as:
  - Passenger Name Records (PNRs)
  - E-tickets
  - Aircraft registration numbers
  - IATA/ICAO aircraft and airline codes
  - IATA/ICAO/FAA airport codes
  - Contact information (phone numbers, email addresses)
  
- **Custom Recognizers**: Includes custom patterns to detect industry-specific codes such as flight numbers, e-ticket prefixes, and more.

- **Faker Integration**: Replaces sensitive data with synthetic data using the Faker library, while also providing flexibility for adding custom fake data generators (e.g., generating fake PNRs, e-tickets).

- **Reversible Pseudonymization**: The tool provides mapping between the original and pseudonymized data, allowing for reversible pseudonymization when required (useful for testing or regulatory purposes).

## Project Structure

The project is organized into several Python modules for better scalability and maintenance:


### Files Overview:

1. **`main.py`**: This is the main entry point for the project. It handles document input, pseudonymization execution, and saving the pseudonymized document to a file.
   
2. **`pseudonymizer.py`**: Contains the core class `CustomPseudonymizer`, which performs the pseudonymization process and stores the depseudonymization mappings. It integrates with custom recognizers and synthetic data generators.

3. **`recognizers.py`**: Defines custom recognizers to detect specific PII entities in travel-related documents (e.g., PNR, e-tickets, IATA/ICAO codes).

4. **`generators.py`**: Implements custom fake data generators that create realistic synthetic data for aviation-related entities (e.g., generating fake PNRs or e-tickets).

5. **`test_pseudonymizer.py`**: Contains unit tests for the CustomPseudonymizer class, validating the accuracy of the pseudonymization process and ensuring that sensitive information is properly anonymized while maintaining a correct mapping for potential deanonymization.

## Usage

To use the tool, follow these steps:

1. **Install Dependencies**: Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install langchain==0.2.11 presidio-analyzer==2.2.351 presidio-anonymizer==2.2.351 faker==20.1.0
   
   
   
   
## Contributing

Contributions to improve the tool are welcome! Feel free to open issues for bugs or feature requests, or submit pull requests for enhancements.



## Acknowledgements

This project utilizes various libraries, including LangChain for document processing and Presidio for PII detection and anonymization.
