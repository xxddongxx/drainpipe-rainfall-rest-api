from config import settings


class SeoulOpenApi:
    def __init__(self):
        self.host = "http://openapi.seoul.go.kr:8088/"
        self.key = settings.SEOUL_OPEN_API_KEY + "/"
        self.function_name = ""
        self.type = "json/"
        self.start = 1
        self.end = 1000
        self.gu_name = ""
