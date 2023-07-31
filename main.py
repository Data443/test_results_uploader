import os
import sys
import requests
import xml.etree.ElementTree as ET
import logging
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
    if response.status_code == 200:
        return response.json()["result"]["id"]
    else:
        logger.error(f"Failed to create test run. Status code: {response.status_code}")
        logger.error(response.json())
        return None

def update_test_case(test_case_data, qase_token):
    url = f"https://api.qase.io/v1/result/{test_case_data['RepositoryCode']}/{test_case_data['TestRunId']}"

    payload = {
        "status": test_case_data["Status"],
        "case_id": test_case_data["TestCaseId"],
        "additional_info": f"RepositoryCode={test_case_data['RepositoryCode']}\nTestCaseId={test_case_data['TestCaseId']}"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Token": qase_token
    }

    response = requests.post(url, json=payload, headers=headers)
    logger.debug(response.text)

def main(xml_file_path, qase_token):
    # Load and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Debug: Print XML tree
    logger.debug("XML Tree:")
    logger.debug(ET.tostring(root, encoding='utf-8').decode())

    # Check if there are any 'test-case' elements in the XML using a different XPath expression
    test_case_elems = root.findall(".//test-case")
    num_test_cases = len(test_case_elems)
    logger.debug(f"Number of 'test-case' elements found in the XML: {num_test_cases}")

    if not test_case_elems:
        logger.error("No 'test-case' elements found in the XML.")
        sys.exit(1)

    for test_case_elem in test_case_elems:
        # Debug: Print XML of each 'test-case' element
        logger.debug("Test-case XML:")
        logger.debug(ET.tostring(test_case_elem, encoding='utf-8').decode())

        # Find the 'output' element within 'test-case'
        output_elem = test_case_elem.find('output')
        if output_elem is not None and output_elem.text:
            # Extract 'RepositoryCode' and 'TestCaseId' from the 'output' element text
            output_lines = output_elem.text.strip().split('\n')
            repository_code = None
            test_case_id_value = None
            for line in output_lines:
                key, value = line.strip().split('=')
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
                        "Status": test_case_elem.get("result")
                    }
                    logger.debug(f"Updating test case: {test_case_data}")
                    update_test_case(test_case_data, qase_token)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logger.error("Usage: python main.py <path_to_xml_file> <qase_token>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    qase_token = sys.argv[2]
    main(xml_file_path, qase_token)
