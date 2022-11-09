class DrainPipe:
    def __init__(self, data, gu_name):
        self.IDN = data.get("IDN")
        self.GUBN = data.get("GUBN")
        self.GUBN_NAM = gu_name
        self.MEA_YMD = data.get("MEA_YMD")
        self.MEA_WAL = data.get("MEA_WAL")
        self.SIG_STA = data.get("SIG_STA")
        self.REMARK = data.get("REMARK")

    def __str__(self):
        return (
            f"IDN: {self.IDN}, GUBN: {self.GUBN}, GUBN_NAM: {self.GUBN_NAM}, "
            f"MEA_YMD: {self.MEA_YMD}, MEA_WAL: {self.MEA_WAL}, "
            f"SIG_STA: {self.SIG_STA}, REMARK: {self.REMARK},"
        )
