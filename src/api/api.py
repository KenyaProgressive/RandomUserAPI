import requests
from src.const import REQUEST_URL, START_SERVER_DATA_GENERATE_LIMIT, INCLUDED_FIELDS_START_SERVER


def get_users_info() -> requests.Response:
    users_info_params = {
        "results": START_SERVER_DATA_GENERATE_LIMIT,
        "inc": INCLUDED_FIELDS_START_SERVER,
    }
    try:
        response = requests.get(REQUEST_URL, params=users_info_params)
        return response
    except Exception as e:
        print(e)

def parse_result(response) -> list:
    result = response["results"]
    temp_data_dict = dict()
    parsed_info = []
    for user_data in result:
        temp_data_dict = {
            'gender': user_data["gender"],
            'name': user_data["name"]["first"],
            'surname': user_data["name"]["last"],
            'phone_number': user_data["phone"],
            'email': user_data['email'],
            'residental_address': user_data
        }

    return parsed_info

def making_address_str(*args):
    ...