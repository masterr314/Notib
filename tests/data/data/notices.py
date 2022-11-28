from datetime import datetime


def get_pseudo_real_notices():
    return [
        {
            'title': 'Sell car',
            'text': 'Sell good car so cheap',
            'endAt': datetime.strptime('12-12-2023', "%d-%m-%Y"),
            "location": {
                "country": "USA",
                "region": "California",
                "city": "Cupertino",
                "street": "Algerd street 45"
            },
            'username': 'sam_smith'
        },
        {
            'title': 'Rent apartment',
            'text': 'Rent good apartment so cheap',
            'endAt': datetime.strptime('12-12-2023', "%d-%m-%Y"),
            "location": {
                "country": "UK",
                "region": "England",
                "city": "Birmingem",
                "street": "Algerdist street 56"
            },
            "username": "bill_golgo"
        }
    ]


