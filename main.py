import os
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

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
        print(f"Failed to create test run. Status code: {response.status_code}")
        print(response.json())
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
    print(response.text)

def main(xml_file_path, qase_token):
    # Load and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract repository code and test plan ID from the XML
    repository_code = root.find("TestCase/RepositoryCode").text
    test_plan_id = 4  # Replace this with the actual test plan ID from your XML or pass it as a command-line argument
    
    # Create a new test run and get the test run ID
    test_run_id = create_test_run(qase_token, repository_code, test_plan_id)
    
    if not test_run_id:
        sys.exit(1)

    for test_case_elem in root.findall('TestCase'):
        test_case_data = {
            "RepositoryCode": repository_code,
            "TestRunId": test_run_id,
            "TestCaseId": int(test_case_elem.find('TestCaseId').text),
            "Status": test_case_elem.find('Status').text
        }
        update_test_case(test_case_data, qase_token)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <path_to_xml_file> <qase_token>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    qase_token = sys.argv[2]
    main(xml_file_path, qase_token)
