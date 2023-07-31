import os
import sys
import requests
import xml.etree.ElementTree as ET
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
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
        "case_id": test_case_data["TestCaseId"]
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Token": qase_token
    }

    response = requests.post(url, json=payload, headers=headers)
    logger.info(response.text)

def main(xml_file_path, qase_token):
    # Load and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract repository code and test plan ID from the XML
    test_case_elem = root.find("./test-case")
    if test_case_elem is None:
        logger.error("No 'test-case' elements found in the XML.")
        print("Error: No 'test-case' elements found in the XML.", file=sys.stderr)
        sys.exit(1)

    repository_code = test_case_elem.get("name").split(".")[0]
    test_plan_id = 4  # Replace this with the actual test plan ID from your XML or pass it as a command-line argument

    # Create a new test run and get the test run ID
    test_run_id = create_test_run(qase_token, repository_code, test_plan_id)

    if not test_run_id:
        logger.error("Failed to create test run.")
        print("Failed to create test run.", file=sys.stderr)
        sys.exit(1)

    for test_case_elem in root.findall('test-case'):
        # Extract data from the <output> tag's CDATA section
        output_elem = test_case_elem.find('output')
        if output_elem is None:
            logger.error("'output' element not found in the XML.")
            sys.exit(1)

        output_data = output_elem.text.strip()
        test_case_data = {}
        for line in output_data.split("\n"):
            key, value = line.strip().split("=")
            test_case_data[key] = value

        test_case_data["RepositoryCode"] = repository_code
        test_case_data["TestRunId"] = test_run_id
        test_case_data["TestCaseId"] = int(test_case_data["TestCaseId"])
        test_case_data["Status"] = test_case_elem.get("result")

        update_test_case(test_case_data, qase_token)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        logger.error("Usage: python main.py <path_to_xml_file> <qase_token>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    qase_token = sys.argv[2]
    main(xml_file_path, qase_token)
