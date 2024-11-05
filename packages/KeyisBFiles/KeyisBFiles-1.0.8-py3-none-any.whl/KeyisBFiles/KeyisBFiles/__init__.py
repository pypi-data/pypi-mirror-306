
import json




class load:
    @staticmethod
    def json(path:str) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except:
            data = {}
        return data
    @staticmethod
    def file(path:str) -> str:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                data = file.read()
        except Exception as e:
            data = ''
            print(e)
        return data
