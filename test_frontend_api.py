import requests

# Test with the exact file format frontend would use
with open('test_frontend_batch.csv', 'rb') as f:
    files = {'file': ('test_frontend_batch.csv', f, 'text/csv')}
    response = requests.post('http://localhost:5000/batch-analyze', files=files)
    print("Status Code:", response.status_code)
    print("Response:", response.text[:200] + "..." if len(response.text) > 200 else response.text)
