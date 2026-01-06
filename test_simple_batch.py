import requests

# Test simple batch endpoint
with open('small_test.csv', 'rb') as f:
    files = {'file': ('small_test.csv', f, 'text/csv')}
    response = requests.post('http://localhost:5000/simple-batch', files=files)
    print("Status Code:", response.status_code)
    print("Response:", response.text[:200] + "..." if len(response.text) > 200 else response.text)
