pip install Flask

pip install requests

pip install Flask-RESTful

pip install Flask-Cors

BASE_URL = 'http://127.0.0.1:5000/api/users'

response = requests.get(f"{BASE_URL}/1")

print(response.json())