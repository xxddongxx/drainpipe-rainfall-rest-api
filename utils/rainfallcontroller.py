from utils.seoulopenapi import SeoulOpenApi
import requests, json

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

    def get_json_data(self, data):
        """
        row data to json
        """
        dumps_json = json.dumps(data)
        return json.loads(dumps_json)

    def get_result(self):
        rainfall = RainFallController(self.gu_name)

        url = rainfall.get_url()

        response_data = rainfall.get_response_data_row(url)

        raingauge_code_set = rainfall.set_RAINGAUGE_CODE_to_set(response_data)
        raingauge_code_len = len(raingauge_code_set) + 1

        # 최신 데이터 리스트
        result = []

        for data in response_data[: raingauge_code_len - 1]:
            json_data = rainfall.get_json_data(data)
            result.append(json_data)

        return result
