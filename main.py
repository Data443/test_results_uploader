import os
import requests
import xml.etree.ElementTree as ET

def update_test_case(test_case_data):
    url = f"https://api.qase.io/v1/result/{test_case_data['RepositoryCode']}/{test_case_data['TestRunId']}"

    payload = {
        "status": test_case_data["Status"],
        "case_id": test_case_data["TestCaseId"]
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Token": os.environ["QASE_TOKEN"]  # Access the environment variable here
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

def main(xml_file_path):
    # Load and parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    for test_case_elem in root.findall('TestCase'):
        test_case_data = {
            "RepositoryCode": test_case_elem.find('RepositoryCode').text,
            "TestRunId": int(test_case_elem.find('TestRunId').text),
            "TestCaseId": int(test_case_elem.find('TestCaseId').text),
            "Status": test_case_elem.find('Status').text
        }
        update_test_case(test_case_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_xml_file>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    main(xml_file_path)
