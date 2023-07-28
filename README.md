# test_results_uploader

## Description

This Docker container is designed to create a test run based on a specified test plan in QASE and update test case statuses in the created run using XML input. 

### Dependencies

* QASE API access (credentials required)
* Docker environment for container execution

### Executing program

Below is an example of how you could call the action in another repository's workflow.

```
name: EXAMPLE
on: [pull_request]

jobs:
  unit-test:
    runs-on: ubuntu-latest
    env:
      QASE_TOKEN: ${{ secrets.FNU_QASE_TOKEN }}
    steps:
      - uses: actions/checkout@v3
      
      - name: Set file permissions
        run: chmod +r ${{ github.workspace }}/TestResults.xml

      - name: login
        run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

      - name: Run QASE Test Results Upload
        run: |
          docker run --name test_results_uploader \
          -v ${{ github.workspace }}/TestResults.xml:/app/TestResults.xml \
          -e QASE_TOKEN=${{ secrets.FNU_QASE_TOKEN }} \
          ghcr.io/data443/test_results_uploader:latest /app/TestResults.xml ${{ secrets.FNU_QASE_TOKEN }}


```
## Authors

Contributors names and contact info

* Andrew Lazare
* andrew.lazare@data443.com

## Version History

* 1.0.28
    * Initial Release