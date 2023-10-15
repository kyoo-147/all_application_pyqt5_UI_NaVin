import time, math
import numpy as np
import triggers

class Benchmark:
    def __init__(self, name):
        self.name = name
        self.executionInitTime = time.time()
        self.initTime = None
        self.detectionTimeList = np.ndarray((0,))

    def startTimer(self):
        self.initTime = time.time()

    def stopTimer(self, bPrint=False):
        if self.initTime is None:
            raise Exception('(Benchmark) stopTimer was called before startTimer')

        timeElapsed = time.time() - self.initTime
        
        self.detectionTimeList = np.append(self.detectionTimeList, timeElapsed)
        self.initTime = None

        if bPrint:
            print(f'BENCHMARK [{self.name}] | Time elapsed: {round(timeElapsed, 3)}s')

        return timeElapsed

    def restartExecutionTime(self):
        self.executionInitTime = time.time()

    def printStatistics(self):
        if len(self.detectionTimeList) == 0:
            print('[BENCHMARK] Detection list is empty')
            return

        executionTime = time.time() - self.executionInitTime
        acuracia = triggers.triggersList[0].stayedTime / executionTime * 100
        acuraciaStr = str(round(acuracia, 2)).replace('.', ',')

        print(f'----------BENCHMARK [{self.name}]----------')
        print(f'Average time\tMax time\tMin times')
        print(int(self.detectionTimeList.min() * 1000),
              int(self.detectionTimeList.mean() * 1000),
              int(self.detectionTimeList.max() * 1000))
        # print(f'Average time:\t{round(self.detectionTimeList.mean(), 3)}s')
        # print(f'Max time:\t{round(self.detectionTimeList.max(), 3)}s')
        # print(f'Min time:\t{round(self.detectionTimeList.min(), 3)}s')
        print(f'Total execution time:\t{round(executionTime, 3)}s')
        print(f'Max Stay Time: {triggers.triggersList[0].stayedTime}')
        print(f'Accuracy: {acuraciaStr}%')