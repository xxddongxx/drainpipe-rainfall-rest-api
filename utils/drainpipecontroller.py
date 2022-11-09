from rest_framework import status
from rest_framework.response import Response

from utils.drainpipe import DrainPipe
from utils.seoulopenapi import SeoulOpenApi
import requests

from utils.util import Util


class DrainPipeController(SeoulOpenApi):
    GUBN_CODE = {
        "종로구": "01",
        "중구": "02",
        "용산구": "03",
        "성동구": "04",
        "광진구": "05",
        "동대문구": "06",
        "중랑구": "07",
        "성북구": "08",
        "강북구": "09",
        "도봉구": "10",
        "노원구": "11",
        "은평구": "12",
        "서대문구": "13",
        "마포구": "14",
        "양천구": "15",
        "강서구": "16",
        "구로구": "17",
        "금천구": "18",
        "영등포구": "19",
        "동작구": "20",
        "관악구": "21",
        "서초구": "22",
        "강남구": "23",
        "송파구": "24",
        "강동구": "25",
    }

    def __init__(self, gu_name):
        super(DrainPipeController, self).__init__()
        self.function_name = "DrainpipeMonitoringInfo/"
        self.gu_name = Util().get_gu_name(gu_name)

    def set_IDN_to_set(self, row):
        """
        Drain Pipe set IDN
        """
        set_IDN = set()
        count_IDN = 0

        for data in row:
            set_IDN.add(data.get("IDN"))
            if count_IDN != len(set_IDN):
                count_IDN = len(set_IDN)
            else:
                break

        return set_IDN

    def get_url(self):
        """
        서울 하수관로 Url 생성
        """
        keys = self.GUBN_CODE.keys()
        if self.gu_name not in keys:
            return Response(
                {
                    "message": "검색한 군 이름이 없습니다.",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "result": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return f"{self.host + self.key + self.type + self.function_name + str(self.start) + '/' + str(self.end) + '/' + self.GUBN_CODE.get(self.gu_name)}/{Util().get_latest_date_hour()}"

    def get_response_data_total_count(self, json_data):
        """
        total count 추출
        """
        return json_data.get("DrainpipeMonitoringInfo").get("list_total_count")

    def is_over_total_count(self, total_count):
        return bool(total_count > 1000)

    def get_response_latest_data_row(self, url):
        """
        최신 row data 추출
        """
        response = requests.get(url)
        response_json = response.json()

        # 데이터 개수가 1000개 이상일겨우
        # 최신 데이터를 다시 불러오기 위한 url 생성
        total_count = self.get_response_data_total_count(response_json)

        if self.is_over_total_count(total_count):

            self.start = total_count - (total_count - 999)
            self.end = total_count
            # 새로운 url
            url = self.get_url()
            response = requests.get(url)
            response_json = response.json()
        return response_json.get("DrainpipeMonitoringInfo").get("row")

    def get_result(self, url):
        response_data = self.get_response_latest_data_row(url)

        idn_set = self.set_IDN_to_set(response_data)
        idn_len = len(idn_set)

        # 최신 데이터 리스트
        result = []

        for data in response_data[: -(idn_len + 1) : -1]:
            result.append(DrainPipe(data, self.gu_name))

        return result
