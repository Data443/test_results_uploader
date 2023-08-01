import os
import sys
import requests
import xml.etree.ElementTree as ET
import logging
import re
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_test_run(qase_token, repository_code, test_plan_id):
    url = f"https://api.qase.io/v1/run/{repository_code}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Token": qase_token
    }

    # Generate the test run title with the current date and time
    test_run_title = f"Automated Test Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    payload = {
        "title": test_run_title,
        "plan_id": test_plan_id
    }

    response = requests.post(url, json=payload, headers=headers)
    logger.debug(f"Test Run Creation URL: {url}")
    logger.debug(f"Test Run Creation Payload: {payload}")
    logger.debug(f"Test Run Creation Response: {response.text}")

    if response.status_code == 200:
        return response.json()["result"]["id"]
    else:
        logger.error(f"Failed to create test run. Status code: {response.status_code}")
        logger.error(response.json())
        return None

def update_test_case(test_case_data, qase_token):
    url = f"https://api.qase.io/v1/result/{test_case_data['RepositoryCode']}/{test_case_data['TestRunId']}"

    # Extract CDATA content and split lines by newline character
    output_text = test_case_data['Output'].strip()
    lines = output_text.split('\n')

    # Process each line to extract key-value pairs
    additional_info = {}
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if '=' in line:
            key, value = line.split('=')
            additional_info[key.strip()] = value.strip()

    # Add additional_info to the payload
    payload = {
        "status": test_case_data["Status"],
        "case_id": test_case_data["TestCaseId"],
        "additional_info": additional_info
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Token": qase_token
    }

    response = requests.put(url, json=payload, headers=headers)
    logger.debug(response.text)

def main(xml_file_path, qase_token):
    # Load and parse the XML file here
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Debug: Print the content of the root element
    logger.debug("XML Root Element:")
    logger.debug(ET.tostring(root, encoding='utf-8').decode())

    # Log all elements present in the XML
    logger.debug("All Elements in the XML:")
    for elem in tree.iter():
        logger.debug(elem.tag)

    # Check if there are any 'test-case' elements in the XML
    test_case_elems = root.findall('.//test-case')
    num_test_cases = len(test_case_elems)
    logger.debug(f"Number of 'test-case' elements found in the XML: {num_test_cases}")

    if not test_case_elems:
        logger.error("No 'test-case' elements found in the XML.")
        logger.error("Raw XML Content:")
        logger.error(ET.tostring(root, encoding='utf-8').decode())  # Print the raw XML content for further inspection
        sys.exit(1)

    for test_case_elem in test_case_elems:
        # Extract 'RepositoryCode' and 'TestCaseId' from 'output' element using regular expressions
        output_elem = test_case_elem.find('.//output')  # <-- Updated XPath query here
        if output_elem is not None and output_elem.text:
            output_text = output_elem.text.strip()

            # Use regular expression to extract the content within CDATA tags
            cdata_pattern = r'<!\[CDATA\[(.*?)]]>'
            cdata_match = re.search(cdata_pattern, output_text, re.DOTALL)

            if cdata_match:
                output_text = cdata_match.group(1).strip()

                logger.debug(f"Extracted Output Text: {output_text}")

                # Call the functions with the extracted values
                repository_code, test_case_id_value = None, None
                for line in output_text.strip().split('\n'):
                    line = line.strip()  # Remove leading/trailing whitespace
                    key, value = line.split('=')
                    if key.strip() == 'RepositoryCode':
                        repository_code = value.strip()
                    elif key.strip() == 'TestCaseId':
                        test_case_id_value = value.strip()

                logger.debug(f"RepositoryCode: {repository_code}, TestCaseId: {test_case_id_value}")

                # Call the functions with the extracted values
                if repository_code and test_case_id_value:
                    test_run_id = create_test_run(qase_token, repository_code, 4)  # Replace '4' with the actual test plan ID
                    if test_run_id:
                        test_case_data = {
                            "RepositoryCode": repository_code,
                            "TestRunId": test_run_id,
                            "TestCaseId": int(test_case_id_value),
                            "Status": test_case_elem.get("result"),
                            "Output": output_text  # Store the original CDATA content in the dictionary
                        }
                        logger.debug(f"Updating test case: {test_case_data}")
                        update_test_case(test_case_data, qase_token)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logger.error("Usage: python main.py <path_to_xml_file> <qase_token>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    qase_token = sys.argv[2]

    logger.debug(f"XML File Path: {xml_file_path}")
    logger.debug(f"QASE Token: {qase_token}")

    main(xml_file_path, qase_token)