import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
customDetector = tf.saved_model.load('customDetector/saved_model')

# ================== [ CONFIG ] ================

DETECTION_PRECISION = 0.5
DETECTION_CLASS = [1]
CUSTOM_DETECTOR_PRECISION = 0.3

WHEELCHAIR_COLOR = (204, 51, 000)
BABY_CARRIAGE_COLOR = (204, 51, 000)
CANE_COLOR = (204, 51, 000)
AMBULANCE_COLOR = (255, 51, 000)

WHEELCHAIR_TEXT = "Wheelchair"
BABY_CARRIAGE_TEXT = "Baby_carriage"
CANE_TEXT = "Cane"
AMBULANCE_TEXT = "Ambulance"

WHEELCHAIR_CLASS = 0
BABY_CARRIAGE_CLASS = 1
CANE_CLASS = 2
AMBULANCE_CLASS = 3

# Please Check :: LabelMap Index = Object detection Model's Class Number - 1
LabelMap = [[WHEELCHAIR_TEXT, WHEELCHAIR_COLOR],
            [BABY_CARRIAGE_TEXT, BABY_CARRIAGE_COLOR],
            [CANE_TEXT, CANE_COLOR],
            [AMBULANCE_TEXT, AMBULANCE_COLOR]]


# ===============================================

def Detector(image):
    """This function detects objects in the image using the tensorflow-hub module. And return the detection result.

    :param 3D-ndarray image: 3D ndarray type data, which has image data.

    :returns: 2D list [[xmin, ymax, xmax, ymin], [..], ..]
    """

    # Convert 3D ndarray image into tensor array ( 3D array = RBG )
    rgb_tensor = cvImgToRGBTensor(image)

    # Save object detection result using tensorflow-hub module
    boxes, scores, classes, num_detections = detector(rgb_tensor)

    pred_labels = classes.numpy().astype('int')[0]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]

    # Create variable to return
    pos_result = []

    # The pos_result list stores the object location only when the detected object is one of DETECTION_CLASS.
    for score, (ymin, xmin, ymax, xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < DETECTION_PRECISION or label not in DETECTION_CLASS:
            continue

        pos_result.append([int(xmin), int(ymax), int(xmax), int(ymin)])

    return pos_result


def CustomDetector(image):
    """This function detects objects in the image using the Transfer learned Object Detection Model.
    And return the detection result.

    :param 3D-ndarray image: 3D ndarray type data, which has image data.

    :returns: 3D list [ [[xmin, ymax, xmax, ymin], [..], ..], [[xmin, ymax, xmax, ymin], [..], ..], ..]
    """

    # Convert 3D ndarray image into tensor array ( 3D array = RBG )
    rgb_tensor = cvImgToRGBTensor(image)

    # Save object detection result using customDetector ( which is Transfer learned Object Detection Model. )
    output_dict = customDetector(rgb_tensor)

    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

    pred_labels = output_dict['detection_classes']
    pred_boxes = output_dict['detection_boxes']
    pred_scores = output_dict['detection_scores']

    # Save the resolution of the image to calculate detected object's position
    h, w, c = image.shape

    # Create variable to return
    pos_result = []

    for i in range(0, len(LabelMap)):
        pos_result.append([])

    # The pos_result list stores the object location
    for score, (ymin, xmin, ymax, xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < CUSTOM_DETECTOR_PRECISION:
            continue

        y_min = int(ymin * h)
        x_min = int(xmin * w)
        y_max = int(ymax * h)
        x_max = int(xmax * w)

        pos_result[label - 1].append([int(x_min), int(y_max), int(x_max), int(y_min)])

    return pos_result


def cvImgToRGBTensor(image):
    """This function converts 3D-ndarray data into tensor-array data. ( 3D Array = RGB )

    :param 3D-ndarray image: 3D ndarray type data, which has image data.

    :returns: tensor-array data ( 3D Array = RGB )

    """
    # Convert img to RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Is optional but i recommend (float conversion and convert img to tensor image)
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)

    # Add dims to rgb_tensor
    rgb_tensor = tf.expand_dims(rgb_tensor, 0)

    return rgb_tensor
