import os

import requests

from src.const import REQUEST_URL, START_SERVER_DATA_GENERATE_LIMIT, INCLUDED_FIELDS_START_SERVER


def get_users_info() -> requests.Response:
    """Получение данных с API"""
    users_info_params = {
        "results": START_SERVER_DATA_GENERATE_LIMIT,
        "inc": INCLUDED_FIELDS_START_SERVER,
    }
    try:
        response = requests.get(REQUEST_URL, params=users_info_params)
        return response.json()['results']
    except requests.exceptions.RequestException as e:
        print(e)


def parse_result(response) -> list:
    """Выборка и преобразование нужных данных для удобного пуша в БД"""
    if not os.path.exists("photos"):
        os.mkdir("photos")
    users_data = response
    parsed_info = []
    for i in range(len(users_data)):
        get_photo_from_url(users_data[i]["picture"]["thumbnail"], i)
        temp_data_dict = {
            'gender': users_data[i]["gender"],
            'name': users_data[i]["name"]["first"],
            'surname': users_data[i]["name"]["last"],
            'phone_number': users_data[i]["phone"],
            'email': users_data[i]['email'],
            'residental_address': making_residental_address_str(users_data[i]["location"]),
            'photo': f"user-photo-{i}.jpg"
        }
        parsed_info.append(temp_data_dict)

    return parsed_info


def making_residental_address_str(location_dict) -> str:
    """Составление адреса жительства по европейскому стандарту"""
    street_number_and_name: str = ' '.join([str(location_dict["street"]["number"]), location_dict["street"]["name"]])
    city_name_and_state_name: str = ', '.join([location_dict["city"], location_dict["state"]])
    country_name_and_postcode: str = ', '.join([str(location_dict["postcode"]), location_dict["country"]])

    address_str = ', '.join([street_number_and_name, city_name_and_state_name, country_name_and_postcode])
    return address_str


def get_photo_from_url(url: str, number_of_file: int):
    """Сохранение фотографий на диск, для дальнейшего пуша в БД"""
    image_response = requests.get(url, stream=True)
    if image_response.status_code == 200:
        with open(f"photos/user-photo-{number_of_file}.jpg", "wb") as fl:
            for part in image_response.iter_content(8192):
                fl.write(part)
    else:
        print(f"Loading is failed: {image_response.status_code}")


def get_photo_from_disk(filename: str):
    """Чтение файл с изображениями для пуша в БД"""
    try:
        with open(filename, "rb") as fl:
            photo_data = fl.read()
        return photo_data
    except FileNotFoundError:
        print("Файл не существует.")
        return b''
    except Exception as e:
        print(e)
        return b''
