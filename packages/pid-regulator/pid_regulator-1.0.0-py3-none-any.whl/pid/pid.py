import time


class pid:
    kp: float | int = 1
    ki: float | int = 1
    kd: float | int = 1
    lastCall: float = 0
    lastError: float | int = 0
    target: float | int = 0

    def __init__(self, kp: float | int, ki: float | int, kd: float | int):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def start(self):
        self.timeDel = time.perf_counter()

    def setTarget(self, target: float | int):
        self.target = target

    def tick(self, value: float | int):
        error = self.target - value
        dE = error - self.lastError
        dT = time.perf_counter() - self.lastCall
        self.lastError = error
        self.lastCall = time.perf_counter()
        return self.calculate(error, dT, dE)

    def calculate(self, error: float | int, dT: float | int, dE: float | int) -> float | int:
        return self.calcP(error) + self.calcI(error, dT) + self.calcD( dT, dE)

    def calcP(self, error: float | int):
        return self.kp * error

    def calcI(self, error: float | int, dT: float | int) -> float:
        return self.ki * error*dT

    def calcD(self, dT: float | int, dE: float | int) -> float:
        return self.kd * (dE/dT)
