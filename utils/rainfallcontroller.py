from utils.seoulopenapi import SeoulOpenApi
import requests, json


class RainFallController(SeoulOpenApi):
    def __init__(self, gu_name):
        super(RainFallController, self).__init__()
        self.function_name = "ListRainfallService/"

        if gu_name[-1] == "구":
            self.gu_name = gu_name
        else:
            self.gu_name = gu_name + "구"

    def set_RAINGAUGE_CODE_to_set(self, row):
        """
        Rain Fall set RAINGAUGE_CODE
        """
        set_RAINGAUGE_CODE = set()
        count_RAINGAUGE_CODE = 0

        for i in row:
            set_RAINGAUGE_CODE.add(i.get("RAINGAUGE_CODE"))
            if count_RAINGAUGE_CODE != len(set_RAINGAUGE_CODE):
                count_RAINGAUGE_CODE = len(set_RAINGAUGE_CODE)
            else:
                break

        return set_RAINGAUGE_CODE

    def get_url(self):
        """
        서울 강우량 Url 생성
        """
        return f"{self.host + self.key + self.type + self.function_name + self.start + self.end + self.gu_name}/"

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

        response_datas = rainfall.get_response_data_row(url)

        RAINGAUGE_CODE_set = rainfall.set_RAINGAUGE_CODE_to_set(response_datas)
        RAINGAUGE_CODE_len = len(RAINGAUGE_CODE_set) + 1

        # 최신 데이터 추출
        resluts = []

        for row in response_datas[: RAINGAUGE_CODE_len - 1]:
            data = rainfall.get_json_data(row)
            resluts.append(data)

        return resluts
