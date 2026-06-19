import os

import requests
from dotenv import load_dotenv

load_dotenv()

mytoken = os.getenv("mytoken")

response = requests.post(
    "https://staging-portal.eprospera.com/api/v1/verify_rpn",
    headers={
      "Authorization": f"Bearer {mytoken}",
      "Content-Type": "application/json"
    },
    json={
      "rpn": "80000000000012"
    }
)

print(response.status_code)
print(response.json())
