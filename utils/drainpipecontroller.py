from utils.seoulopenapi import SeoulOpenApi
import requests, json

from utils.util import Util


class DrainPipeController(SeoulOpenApi):
    GUBN_CODE = {
        "종로": "01",
        "중": "02",
        "용산": "03",
        "성동": "04",
        "광진": "05",
        "동대문": "06",
        "중랑": "07",
        "성북": "08",
        "강북": "09",
        "도봉": "10",
        "노원": "11",
        "은평": "12",
        "서대문": "13",
        "마포": "14",
        "양천": "15",
        "강서": "16",
        "구로": "17",
        "금천": "18",
        "영등포": "19",
        "동작": "20",
        "관악": "21",
        "서초": "22",
        "강남": "23",
        "송파": "24",
        "강동": "25",
    }

    def __init__(self, gu_name):
        super(DrainPipeController, self).__init__()
        self.function_name = "DrainpipeMonitoringInfo/"
        self.gu_name = gu_name

    def set_IDN_to_set(self, row):
        """
        Drain Pipe set IDN
        """
        set_IDN = set()
        count_IDN = 0

        for i in row:
            set_IDN.add(i.get("IDN"))
            if count_IDN != len(set_IDN):
                count_IDN = len(set_IDN)
            else:
                break

        return set_IDN

    def get_url(self):
        """
        서울 하수관로 Url 생성
        """
        return f"{self.host + self.key + self.type + self.function_name + self.start + self.end + self.GUBN_CODE.get(self.gu_name)}/{Util().get_latest_date_hour()}"

    def get_response_data_row(self, url):
        """
        row data 추출
        """
        response = requests.get(url)
        response_json = response.json()
        return response_json.get("DrainpipeMonitoringInfo").get("row")

    def get_json_data(self, data):
        """
        row data to json
        """
        dumps_json = json.dumps(data)
        return json.loads(dumps_json)

    def get_result(self):
        drain = DrainPipeController(self.gu_name)

        url = drain.get_url()

        response_datas = drain.get_response_data_row(url)

        IDN_set = drain.set_IDN_to_set(response_datas)
        IDN_len = len(IDN_set) + 1

        # 최신 추출 데이터
        resluts = []

        for row in response_datas[:-IDN_len:-1]:
            data = drain.get_json_data(row)
            resluts.append(data)

        return resluts
