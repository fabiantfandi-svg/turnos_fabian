import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Tu Web API Key se encuentra en la configuración del proyecto en Firebase Console
API_KEY = "AIzaSyAUHPZrCAN0ww8nsekJmOCKbderQccHL0k"
EMAIL = "fabiant@gmail.com"
PASSWORD = "password1234"

def get_id_token():
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    data = response.json()
    
    if "idToken" in data:
        print("\n✅ TU TOKEN ES:\n")
        print(data["idToken"])
    else:
        print("❌ Error:", data.get("error", {}).get("message"))

if __name__ == "__main__":
    get_id_token()