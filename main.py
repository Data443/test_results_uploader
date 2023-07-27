import os
import requests
import xml.etree.ElementTree as ET

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

def main(xml_file_path, qase_token):  # Add xml_file_path as an argument
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
        update_test_case(test_case_data, qase_token)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py <path_to_xml_file> <qase_token>")
        sys.exit(1)
    xml_file_path = sys.argv[1]
    qase_token = sys.argv[2]
    main(xml_file_path, qase_token)  # Pass xml_file_path and qase_token to main function



# import os
# import requests
# import xml.etree.ElementTree as ET

# def update_test_case(test_case_data, qase_token):
#     url = f"https://api.qase.io/v1/result/{test_case_data['RepositoryCode']}/{test_case_data['TestRunId']}"

#     payload = {
#         "status": test_case_data["Status"],
#         "case_id": test_case_data["TestCaseId"]
#     }
    
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/json",
#         "Token": qase_token
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     print(response.text)

# def main():
#     # Get xml_file_path and qase_token from environment variables
#     xml_file_path = os.environ.get('XML_FILE_PATH')
#     qase_token = os.environ.get('QASE_TOKEN')

#     # Load and parse the XML file
#     tree = ET.parse(xml_file_path)
#     root = tree.getroot()

#     for test_case_elem in root.findall('TestCase'):
#         test_case_data = {
#             "RepositoryCode": test_case_elem.find('RepositoryCode').text,
#             "TestRunId": int(test_case_elem.find('TestRunId').text),
#             "TestCaseId": int(test_case_elem.find('TestCaseId').text),
#             "Status": test_case_elem.find('Status').text
#         }
#         update_test_case(test_case_data, qase_token)

# if __name__ == "__main__":
#     main()



