import os

import requests
from dotenv import load_dotenv

load_dotenv()

mytoken = os.getenv("mytoken")
base_url = os.getenv("base_url")
"""
response1 = requests.get(
    f"{base_url}/api/v1/me/natural-person",
    headers={
      "Authorization": f"Bearer {mytoken}"
    }
)

response2 = requests.get(
    f"{base_url}/api/v1/me/natural-person/residency",
    headers={
      "Authorization": f"Bearer {mytoken}"
    }
)

print(response1.status_code)
print(response2.status_code)

response1 = response1.json()
response2 = response2.json()
"""

response1 = {
    "givenName": "Nicolas",
    "surname": "Liway",
    "name": "Nicolas Liway",
    "residentPermitNumber": "90000000000123",
    "countryOfBirth": "Honduras",
    "citizenships": ["Honduras", "United States"],
    "dateOfBirth": "1990-05-15",
    "sex": "Male",
    "address": {
        "country": "Honduras",
        "line1": "Calle Principal 123",
        "line2": "Apt 4B",
        "city": "Roatan",
        "state": "Islas de la Bahía",
        "postalCode": "34101"
    },
    "phoneNumber": "+50498765432"
}


response2 = {
    "wasEverResident": True,
    "activeResidency": {
        "effectiveDate": "2024-03-15T00:00:00.000Z",
        "terminationDate": None,
        "residencyType": "Resident",
        "version": "v08.29.2024"
    }
}
"""
response2 = {
    "wasEverResident": True,
    "activeResidency": None
}

response2 = {
    "wasEverResident": False,
    "activeResidency": None
}
"""



print(f"Name: {response1['givenName']} {response1['surname']}")
print(f"RPN: {response1['residentPermitNumber']}")

wasResident = response2["wasEverResident"]
activeResidency = response2["activeResidency"]

if wasResident and activeResidency:
    print(f"Residency Status: {activeResidency['residencyType']}")
elif wasResident and not activeResidency:
    print("Residency Status: Not active")
elif not wasResident:
    print("Never a resident")
    
