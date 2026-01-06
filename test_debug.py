import requests

# Test the debug upload endpoint
with open('test_frontend_batch.csv', 'rb') as f:
    files = {'file': ('test_frontend_batch.csv', f, 'text/csv')}
    response = requests.post('http://localhost:5000/debug-upload', files=files)
    print("Status Code:", response.status_code)
    print("Response:", response.json())
