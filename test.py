#Isso daqui é basicamente um postman/insomnia
import requests

BASE = "http://127.0.0.1:5000/"


response = requests.patch(BASE + "video/1", {"views": 300, "likes": 20})
print(response.json())
