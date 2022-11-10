import time
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

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
        날짜 시간 부분은 요청마다 달라지므로 따로 분리해서 관리
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
        return f"{self.host + self.key + self.type + self.function_name + str(self.start) + '/' + str(self.end) + '/' + self.GUBN_CODE.get(self.gu_name)}/"  # {Util().get_latest_date_hour()}"

    def get_latest_url(self):
        """
        default url을 받아와 최신 url을 결합
        결과물로 최신 url 생성
        """
        default_url = self.get_url()
        latest_date_hour = Util().get_latest_date_hour()
        return default_url + latest_date_hour

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
        print("response_json >>>>> ", response_json)

        # 데이터 개수가 1000개 이상일겨우
        # 최신 데이터를 다시 불러오기 위한 url 생성
        total_count = self.get_response_data_total_count(response_json)

        if self.is_over_total_count(total_count):

            self.start = total_count - (total_count - 999)
            self.end = total_count
            # 새로운 url
            new_url = self.get_latest_url()
            response = requests.get(new_url)
            response_json = response.json()
        return response_json.get("DrainpipeMonitoringInfo").get("row")

    def get_today_data_row(self, url):
        """
        하루 데이터
        """
        response = requests.get(url)
        response_json = response.json()
        return response_json.get("DrainpipeMonitoringInfo").get("row")

    def get_datas_set_len(self, url):
        """
        데이터의 set 개수
        """
        response_data = self.get_response_latest_data_row(url)

        idn_set = self.set_IDN_to_set(response_data)
        idn_len = len(idn_set)

        return response_data, idn_len

    def get_today_result(self, datas):
        result = list(map(lambda x: DrainPipe(x, self.gu_name), datas))
        return result

    def get_result(self, datas, set_len):
        """
        latest 결과값 추출
        """
        result = []
        for data in datas[: -(set_len + 1) : -1]:
            result.append(DrainPipe(data, self.gu_name))

        return result

    def make_today_url_list(self, url):
        """
        TODO
        1. 00시 url -> 리스트에 추가
        2. total_count 어더 end와 비교   => 처음 얻으면 다른 시간데에도 같은 카운트...
        3. end가 크면 다음 시간, enc가 작다면
          3-1. start += 1000, enc += 1000
          3-2. url 리스트에 추가, 다시 3번으로
        4. 다음 시간으로
        """
        # 초기 url로 접근하여 데이터의 총 개수를 받아온다.
        response = requests.get(url)
        response_json = response.json()
        total_data_count = self.get_response_data_total_count(response_json)

        # 00시 부터 현재 시간 까지의 날자 path를 생성하기 위해서
        now_hour = datetime.now().hour

        # 00시 ~ 현재 시간까지의 url을 담아 둔다.
        url_list = []

        for count in range(now_hour):
            count_time_path = Util().make_today_times(count)
            first_url = self.get_url() + count_time_path
            url_list.append(first_url)

            # total_data_count가 크다면 반복, 없으면 페스
            while total_data_count > self.end:
                self.start += 1000
                self.end += 1000
                second_url = self.get_url() + count_time_path
                url_list.append(second_url)

            # 다음 시간 url 생성 전 시작 페이지 다시 설정
            self.start = 1
            self.end = 1000

        return url_list

    def method_in_thread(self, url):
        """
        thread에서 실행할 메소드
        """
        datas = self.get_today_data_row(url)
        result = self.get_today_result(datas)
        return result

    def thread_executor_method(self, url_list):
        """
        thread로 실행하여 시간 단축
        """
        with ThreadPoolExecutor(50) as executor:
            result = sum(executor.map(self.method_in_thread, url_list), [])
        return result
