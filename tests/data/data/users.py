from datetime import datetime
from extensions import bcrypt


def get_test_user_credentials():
    return {
        'username': 'test',
        'password': '1',
        'email': 'test@gmail.com',
    }


def get_test_user():

    credentials = get_test_user_credentials()

    return {
        "username": credentials.get('username'),
        "first_name": "test",
        "last_name": "test",
        "birth_date": datetime.strptime('24-03-1997', "%d-%m-%Y"),
        "email": credentials.get('email'),
        "password": bcrypt.generate_password_hash(
            credentials.get('password')
        ),
        "phone": "0456734567",
        "role": "admin",
        "location": {
            "country": "UK",
            "region": "Scotland",
            "city": "Glasgo",
            "street": "Menhi street 2"
        }
    }


def get_pseudo_real_users():
    return [
        {
            "username": "sam_smith",
            "first_name": "Sam",
            "last_name": "Smith",
            "birth_date": datetime.strptime('24-03-1999', "%d-%m-%Y"),
            "email": "sam_smith@gmail.com",
            "password": bcrypt.generate_password_hash('12345678'),
            "phone": "034333343451",
            "location": {
                "country": "UK",
                "region": "Scotland",
                "city": "Glasgo",
                "street": "Mengo street 2"
            }
        },
        {
            "username": "bill_golgo",
            "first_name": "Bill",
            "last_name": "Golgo",
            "birth_date": datetime.strptime('14-06-1987', "%d-%m-%Y"),
            "email": "bill_golgo@gmail.com",
            "password": bcrypt.generate_password_hash('87654321'),
            "phone": "03341111331",
            "location": {
                "country": "USA",
                "region": "California",
                "city": "Cupertino",
                "street": "Algerd street 34"
            }
        }
    ]








