from pprint import pprint
import requests

TOKEN = ""


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def _create_folder(self, dir_name):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self.get_headers()
        params = {"path": dir_name, "overwrite": "true"}
        response = requests.put(upload_url, headers=headers, params=params)
        if response.status_code == 201:
            print("Directory was created successfully")
        pprint(response.json())
        # return response.json()
        return response.status_code

    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        disk_file_path = "netology/upload.txt"
        dir_name = disk_file_path.rstrip(file_path)
        resp = self._create_folder(dir_name=dir_name)
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    # path_to_file = os.path.join(os.getcwd(), "upload.txt")
    path_to_file = "upload.txt"
    uploader = YaUploader(token=TOKEN)
    result = uploader.upload(path_to_file)
