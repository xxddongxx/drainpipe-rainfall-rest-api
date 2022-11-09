from datetime import datetime


class Util:
    def __init__(self):
        pass

    def set_year_month_day_hour_minute(self):
        now_date = datetime.now()
        year = now_date.year
        month = now_date.month
        day = now_date.day
        hour = now_date.hour
        minute = now_date.minute
        return year, month, day, hour, minute

    def get_latest_date_hour(self):
        year, month, day, hour, minute = self.set_year_month_day_hour_minute()

        if hour != 0:
            an_hour_ago = (
                datetime(year, month, day, hour - 1).strftime("%Y%m%d%H") + "/"
            )
            latest_hour = datetime(year, month, day, hour).strftime("%Y%m%d%H") + "/"
        else:
            latest_hour = datetime(year, month, day, hour).strftime("%Y%m%d%H") + "/"
            day -= 1
            hour = 23
            an_hour_ago = datetime(year, month, day, hour).strftime("%Y%m%d%H") + "/"

        return an_hour_ago + latest_hour

    def is_last_str(self, text):
        """
        입력받은 구이름에 마지막 문자열이 구인지 확인
        """
        return bool(text[-1] == "구")

    def get_gu_name(self, gu_name):
        """
        '구'가 포함 확인
        """
        if self.is_last_str(gu_name):
            return gu_name
        else:
            return gu_name + "구"
