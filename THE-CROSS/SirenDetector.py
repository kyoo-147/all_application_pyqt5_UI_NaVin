import threading

import tensorflow_hub as hub
import sounddevice as sd
import numpy as np

siren_classesNum = [316, 317, 318, 319, 390, 391]
"""The siren classification number list used by yamnet."""


class SirenDetector(threading.Thread):
    """This class is for recognizing the siren sound of an emergency vehicle.
    """

    def __init__(self):
        """A function to initialize the SirenDetector class
        Create and store objects to use the yamnet model of the tensorflow-hub module.
        Save setting values for receiving sound input.
        Create a flag variable that determines whether the siren detection function operates.
        Importantly, Create an 'self.isSirenDetected' variable in the SirenDetector
        so that MainClass can access whether a siren is detected.
        """

        super().__init__()
        self.model = hub.load('https://tfhub.dev/google/yamnet/1')
        self.fs = 16000
        self.duration = 2  # seconds
        self.isRun = True
        self.isSirenDetected = False

    def run(self):
        """This function is a function that detects sirens.
        While constantly detecting the siren,
        change the isSerenDetected variable depending on whether Siren is detected or not.

        If there is a siren among the top five classification results predicted by yamnet, the siren detection model,
        we implemented that the siren sound detected.
        """

        self.isRun = True
        while self.isRun:
            result = sd.rec(self.duration * self.fs, samplerate=self.fs, channels=1, dtype=np.float32).reshape(-1)
            sd.wait()
            scores, embeddings, log_mel_spectrogram = self.model(result)
            prediction = np.mean(scores, axis=0)
            top5 = np.argsort(prediction)[::-1][:5]

            siren_result = False
            for wavNum in top5:
                if wavNum in siren_classesNum:
                    siren_result = True

            self.isSirenDetected = siren_result

    def isSiren(self):
        """This function returns whether a siren is detected.
        """
        return self.isSirenDetected

    def stop(self):
        """This function stops the siren detector.
        """
        self.isRun = False
