class RainFall:
    def __init__(self, data):
        self.RAINGAUGE_CODE = data.get("RAINGAUGE_CODE")
        self.RAINGAUGE_NAME = data.get("RAINGAUGE_NAME")
        self.GU_CODE = data.get("GU_CODE")
        self.GU_NAME = data.get("GU_NAME")
        self.RAINFALL10 = data.get("RAINFALL10")
        self.RECEIVE_TIME = data.get("RECEIVE_TIME")

    def __str__(self):
        return (
            f"RAINGAUGE_CODE: {self.RAINGAUGE_CODE}, RAINGAUGE_NAME: {self.RAINGAUGE_NAME}, GU_CODE: {self.GU_CODE}, "
            f"GU_NAME: {self.GU_NAME}, RAINFALL10: {self.RAINFALL10}, RECEIVE_TIME: {self.RECEIVE_TIME}"
        )
