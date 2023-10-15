"""
# To-Do
"""
from configuration_parser import ConfigurationParser
import cv2
import numpy as np

class Detect:
    """
    Detect class
    """
    def __init__(self):
        """
        Detect class constructor
        """
        self._path = 'config/config.yaml'
        self._config_parser = ConfigurationParser(path=self._path,
                                                 module_name='detect')
        self._classes = self._config_parser.getConfigValue('classes')
        self._minimum_confidence = self._config_parser.getMinConfidence()

    def initializeModel(self):
        """
        """
        # Load the model
        model_path = self._config_parser.getModelPath()
        model_config_path = self._config_parser.getModelConfigPath()
        network = cv2.dnn.readNetFromCaffe(model_config_path, model_path)
        print('Model loaded successfully')
        return network

    def detect(self, network, frame=None): 
        """
        """
        HEIGHT, WIDTH = None, None
        if HEIGHT is None and WIDTH is None:
            HEIGHT, WIDTH = frame.shape[:2]
        # Get the blob from the frame
        blob = cv2.dnn.blobFromImage(image=frame,
                                        size=(300, 300),
                                        ddepth=cv2.CV_8U)
        # Set the blob as input to the network
        network.setInput(blob, 
                            scalefactor=1.0 / 127.5,
                            mean=[127.5, 127.5, 127.5])

        # Run the forward pass
        detections = network.forward()
        #print('detections shape: ', detections.shapes

        # Loop over the detections
        for i in range(0, detections.shape[2]):
            # Get the confidence of the prediction
            confidence = detections[0, 0, i, 2]
            # Filter out weak detections
            if confidence > self._minimum_confidence:
                # Extract the class label
                class_label = int(detections[0, 0, i, 1])
                # Extract the class
                class_name = self._classes[class_label]
                print('class name: ', class_name)
                # Extract the bounding box
                box = detections[0, 0, i, 3:7]*np.array([WIDTH, HEIGHT, WIDTH, HEIGHT])
                (startX, startY, endX, endY) = box.astype("int")
                # Draw the bounding box
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                # Draw the label on the bounding box
                label = "{}: {:.2f}%".format(class_name, confidence * 100)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, 
                            label, 
                            (startX, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.5, 
                            (255, 0, 0), 
                            2)
        return frame