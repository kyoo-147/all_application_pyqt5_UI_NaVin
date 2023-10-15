import cv2
import numpy as np

class BlobSizeTester:
    personTesterImg = cv2.imread(
        './assets/blob-size-person-tester.png',
        cv2.IMREAD_UNCHANGED)
    aspectRatio = (float(personTesterImg.shape[1]) / personTesterImg.shape[0])
    testersList = []

    def addTesterToList(pos):
        BlobSizeTester.testersList.append(pos)

    def drawPeople(frame, size):
        for pos in BlobSizeTester.testersList:
            frame = BlobSizeTester.drawPerson(frame, size, pos)
        return frame

    def drawPerson(frame, size, pos):
        frameHeight, frameWidth = frame.shape[:2]
        posInPixels = (int(pos[0] * frameWidth),
                        int(pos[1] * frameHeight))

        size = (int(size), int(size / BlobSizeTester.aspectRatio))
        if (size[0] / 2 + posInPixels[0] >= frame.shape[1]
            or posInPixels[0] - size[0] / 2 < 0
            or size[1] / 2 + posInPixels[1] >= frame.shape[0]
            or posInPixels[1] - size[1] / 2 < 0):
            return frame
        personTesterImgResized = cv2.resize(BlobSizeTester.personTesterImg, size)

        alphaPerson = personTesterImgResized[:, :, 3] / 255.0
        alphaPerson = alphaPerson[:, :, np.newaxis]
        alphaFrame = 1.0 - alphaPerson

        frameCrop = frame[
            posInPixels[1] - int(size[1] / 2) : posInPixels[1] + size[1] - int(size[1] / 2),
            posInPixels[0] - int(size[0] / 2) : posInPixels[0] + size[0]- int(size[0] / 2),
        ]

        frameCrop[:] = personTesterImgResized[:, :, :3] * alphaPerson + frameCrop * alphaFrame

        return frame