from datetime import datetime

from utils.rainfall import RainFall
from utils.seoulopenapi import SeoulOpenApi
import requests

from utils.util import Util


class RainFallController(SeoulOpenApi):
    def __init__(self, gu_name):
        super(RainFallController, self).__init__()
        self.function_name = "ListRainfallService/"
        self.gu_name = Util().get_gu_name(gu_name)

    def set_RAINGAUGE_CODE_to_set(self, row):
        """
        Rain Fall set RAINGAUGE_CODE
        """
        set_RAINGAUGE_CODE = set()
        count_RAINGAUGE_CODE = 0

        for data in row:
            set_RAINGAUGE_CODE.add(data.get("RAINGAUGE_CODE"))
            if count_RAINGAUGE_CODE != len(set_RAINGAUGE_CODE):
                count_RAINGAUGE_CODE = len(set_RAINGAUGE_CODE)
            else:
                break

        return set_RAINGAUGE_CODE

    def get_url(self):
        """
        서울 강우량 Url 생성
        """
        return f"{self.host + self.key + self.type + self.function_name + str(self.start) + '/' + str(self.end) + '/' + self.gu_name}/"

    def get_response_data_row(self, url):
        """
        row data 추출
        """
        response = requests.get(url)
        response_json = response.json()
        return response_json.get("ListRainfallService").get("row")

    def get_datas_set_len(self, url):
        """
        데이터의 set 개수
        """
        response_data = self.get_response_data_row(url)

        raingauge_code_set = self.set_RAINGAUGE_CODE_to_set(response_data)
        raingauge_code_len = len(raingauge_code_set)

        return response_data, raingauge_code_len

    def get_result(self, datas, set_len):
        # 최신 데이터 리스트
        result = list(map(lambda x: RainFall(x), datas[:set_len]))

        return result

    def get_today_result(self, datas, set_len):
        """
        현재 시간 * 6(한 시간에 6번 데이터가 쌓임) * set 한 아이디 개수
        """
        year, month, day, hour, minute = Util().set_year_month_day_hour_minute()

        now_data_count = hour * 6 * set_len

        today_date = datetime(year, month, day).strftime("%Y-%m-%d")

        result_list = list(map(lambda x: RainFall(x), datas[:now_data_count]))
        result = list(filter(lambda x: today_date in x.RECEIVE_TIME, result_list))

        return result
