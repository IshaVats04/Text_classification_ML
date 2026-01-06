import requests

# Test batch analysis endpoint
with open('sample_batch.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/batch-analyze', files=files)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
