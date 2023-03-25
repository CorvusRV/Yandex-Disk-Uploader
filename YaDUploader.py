import requests
import os.path

class YaDUploader:
    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url
        
    def connection_test(self, headers: dict):
        """Метод проверяет соединение с сервером"""
        resp = requests.get(f"{self.url}/v1/disk", headers=headers)
        return resp.status_code

    def upload(self, file_path: str, headers: dict):
        """Метод загружает файл на яндекс диск"""
        params = {"path": file_path}
        resp = requests.get(f"{self.url}/v1/disk/resources/upload", headers=headers, params=params)
        if 'error' in resp.json():
            return "Ошибка загрузки"
        else:
            down_url = resp.json()['href']
            resp = requests.put(down_url, headers=headers, params=params)
        return "Файл загружен"
    
    def uploader (self, file_list: list, headers: dict):
        """Метод позволяет загрузить последовательно несколкьо файлов на яндекс диск"""
        for file in file_list:
            print(self.upload(file, headers))
                
    def list_of_uploaded_files (self):
        """Метод создает список адресов загружаемых файлов"""
        file_list = []
        print("""Инструкция: последовательно введите адреса всех файлов, которые планируете загрузить на диск.
        После того, как ввели адрес, нажмите Enter. Если вы ввели адреса всех файлов, которые планировали загрузить, 
        нажмите Enter.""")
        while file := input():
            if os.path.exists(file): #проверка наличия файла
                file_list.append(file)
            else:
                print("Файл не найден")
        return file_list

error_dict = {400: "Некорректные данные",
              401: "Не авторизован",
              403: "Не достаточно прав для изменения данных в общей папке",
              404: "Не удалось найти запрошенный ресурс",
              406: "Ресурс не может быть представлен в запрошенном формате",
              412: "При дозагрузке файла был передан неверный диапазон в заголовке",
              413: "Загрузка файла недоступна. Файл слишком большой",
              423: "Загрузка файлов недоступна, можно только просматривать и скачивать. Вы достигли ограничения по загрузке файлов",
              429: "Слишком много запросов",
              500:"Ошибка сервера, попробуйте повторить загрузку",
              503: "Сервис временно недоступен", 
              507: "Для загрузки файла не хватает места на Диске пользователя"
             }

url = "https://cloud-api.yandex.net"
token = "token"
uploader = YaDUploader(token, url)
headers = {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {uploader.token}"
          }
test_result = uploader.connection_test(headers)
if test_result == 200:
    file_list = uploader.list_of_uploaded_files()
    uploader.uploader(file_list, headers)
elif test_result in error_dict:
    print(error_dict[test_result])
else:
    print("Неизвестная ошибка")