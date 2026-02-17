import requests

url = 'http://127.0.0.1:8000/generate_summary/'
resp = requests.post(url, json={"content": "AI models are changing the world."})
print(resp.status_code, resp.text)

url2 = 'http://127.0.0.1:8000/generate_mcqs/'
resp2 = requests.post(url2, json={"content": "AI and machine learning are evolving fields."})
print(resp2.status_code, resp2.text)

url3 = 'http://127.0.0.1:8000/generate_exam_questions/'
resp3 = requests.post(url3, json={"content": "Deep learning is a subset of machine learning."})
print(resp3.status_code, resp3.text)
