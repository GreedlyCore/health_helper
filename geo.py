#широта долгота
def geo_to_url(latitude, longitude):
    answer = f"https://yandex.ru/maps/?ll={str(longitude)}%2C{str(latitude)}&mode=search&sll={str(longitude)}%2C{str(latitude)}&text={str(latitude)}%2C{str(longitude)}&z=14"
    return answer
