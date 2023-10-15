import numpy as np
import cv2

from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui


def cvImgToQtImg(cvImage, W=150):
    """This function converts images in the form of 3D ndarray into objects in the form of QTLabel.
    In the process of converting, the image may be resized as needed.

    :param 3D-ndarray cvImage: 3D ndarray type data, which has image data.
    :param int W: Width of the image. Resize the image according to this variable.

    :returns: QTLabel Instance

    """

    # resize cvImage according to W varibale
    cvImage = resizeCVIMG(cvImage, W)

    # convert cvimage (3D-ndarray) to QT Pixmap instance
    pixmap = cvImgToPixmap(cvImage)

    # Create new QLabel Instance
    label = QLabel()

    # Set pixmap of new created QLABEL to the pixmap converted cvImage
    label.setPixmap(pixmap)

    # Set label size as the same as pixmap size
    label.resize(pixmap.width(), pixmap.height())

    return label


def resizeCVIMG(cvImage, W=150):
    """This function resizes the image in the form of a 3D-ndarray.

    :param 3D-ndarray cvImage: 3D ndarray type data, which has image data.
    :param int W: Width of the image. Resize the image according to this variable.

    :returns: resized 3D-ndarray cvImage
    """

    # Get Ratio of cvImage
    ratio = W / cvImage.shape[1]

    # Get dimension size
    dim = (W, int(cvImage.shape[0] * ratio))

    # perform the actual resizing of the image
    cvImage = cv2.resize(cvImage, dim, interpolation=cv2.INTER_AREA)

    return cvImage


def cvImgToPixmap(cvImage):
    """This function converts images in the form of 3D ndarray into objects in the form of QT-Pixmap.

    :param 3D-ndarray cvImage: 3D ndarray type data, which has image data.

    :returns: converted 3D-ndarray cvImage
    """

    # Convert Color of cvImage ( BGR to RBG )
    img = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)

    # Get size of image
    h, w, c = img.shape

    # Create QImage instance for extracting QPixmap
    qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)

    # Get Pixmap
    pixmap = QtGui.QPixmap.fromImage(qImg)

    return pixmap


def draw_detection_boxes(img, pos_list, text,
                         font=cv2.FONT_HERSHEY_SIMPLEX, lineType=cv2.LINE_AA):
    """This function draws a square on the image.

    :param 3D-ndarray img: 3D ndarray type data, which has image data.
    :param list pos_list: List of the lower left and upper right points of the square.
    .. Note:: The pos_list consists of the following list. => [xmin, ymax, xmax, ymin]

    :param str text: Letters to write on the bottom left of a square.
    :param cv2-font-style font: Type of font with letters to write on the bottom left of a square.
    :param cv2-line-type lineType: Types of lines to draw squares.

    :returns: 3D-ndarray img_result ( square & text drawn )

    """

    img_result = img
    
    for pos in pos_list:
        # pos must have the form of [xmin, ymax, xmax, ymin]
        if len(pos) != 4:
            continue

        # draw square & text on image
        img_result = cv2.rectangle(img, (pos[0], pos[1]), (pos[2], pos[3]), (0, 255, 0), 1)
        cv2.putText(img_result, text, (pos[0], pos[1] - 10), font, 0.5, (255, 0, 0), 1,
                    lineType)
        
    return img_result


def draw_area(cvImg, pos_list, dotColor=(255, 0, 0), lineColor=(0, 255, 0)):
    """This function draws a square on the image using four points. Also, each dot is drawn on the image.

    :param 3D-ndarray cvImg: 3D ndarray type data, which has image data.
    :param list pos_list: List of the lower left and upper right points of the square.
    .. Note:: The pos_list consists of the following list. => [xmin, ymax, xmax, ymin]

    :param (int, int, int) dotColor: RGB color of dots.
    :param (int, int, int) lineColor: RGB color of the line of Rectangle.

    :returns: 3D-ndarray img_result ( Rectangle & text drawn )
    """

    # draw dots
    for i in range(len(pos_list)):
        x = pos_list[i][0]
        y = pos_list[i][1]
        cv2.circle(cvImg, (x, y), 5, dotColor, -1)

    # If there are four dots,
    if len(pos_list) == 4:

        # Store an index that counterclockwise aligns the four points.
        x_arg_sort = sort_rectPos(pos_list)

        # Draw a Rectangle counterclockwise.
        for i in range(4):
            start = pos_list[x_arg_sort[i]]
            end = pos_list[x_arg_sort[(i + 1) % 4]]
            cv2.line(cvImg, (start[0], start[1]), (end[0], end[1]), lineColor, 2)

    return cvImg


def isAnyObjectInRect(rectPos, spotList, boxSpot=True):
    """This function receives the vertex coordinates of the square
    and multiple point coordinates to verify that
    any of the multiple point coordinates received exist within the rectangle area.

    :param list rectPos: The rectangle coordinates.
    .. Note:: rectPos must have the form of [[x,y], [x,y], [x,y], [x,y]]

    :param list spotList: List of dots.
    .. Note:: spotList must have the form of [[x,y], [x,y], ...] or [[xmin, ymax, xmax, ymin], ...]
    if spotList have the form of [[xmin, ymax, xmax, ymin], ...], boxSpot Must be True
    if spotList have the form of [[x,y], [x,y], ...], boxSpot Must be False

    :param boolean boxSpot: Whether to use box coordinates.
    .. Note:: box coordinate = [xmin, ymax, xmax, ymin]

    :returns: boolean

    """
    if len(spotList) == 0:
        return False

    # When the vertices of the squares are aligned in counterclockwise order,
    # store the sorted index of the original arrangement according to the aligned arrangement. (like numpy argsort())
    x_arg_sort = sort_rectPos(rectPos)

    p1 = rectPos[x_arg_sort[0]]
    p2 = rectPos[x_arg_sort[1]]
    p3 = rectPos[x_arg_sort[2]]
    p4 = rectPos[x_arg_sort[3]]

    # High Low Low High
    # y = (Ay-By)/(Ax-Bx)*( x - Ax ) + Ay
    for i in range(0, len(spotList)):

        try:

            # Convert From [xmin, ymax, xmax, ymin] To [x,y]
            if boxSpot is True:
                target = [(spotList[i][0] + spotList[i][2]) / 2, spotList[i][1]]
            else:
                target = spotList[i]

            if p1[0] == p2[0]:
                if not p1[0] < target[0]:
                    continue
            else:
                # linear a > 0
                if (p1[1] - p2[1]) / (p1[0] - p2[0]) < 0:
                    if not ((p1[1] - p2[1]) / (p1[0] - p2[0]) * (target[0] - p1[0]) + p1[1]) < target[1]:
                        continue
                # linear a < 0
                else:
                    if not ((p1[1] - p2[1]) / (p1[0] - p2[0]) * (target[0] - p1[0]) + p1[1]) > target[1]:
                        continue

            if not ((p2[1] - p3[1]) / (p2[0] - p3[0]) * (target[0] - p2[0]) + p2[1]) > target[1]:
                continue

            if p3[0] == p4[0]:
                if not p3[0] > target[0]:
                    continue
            else:
                # linear a > 0
                if (p3[1] - p4[1]) / (p3[0] - p4[0]) < 0:
                    if not ((p3[1] - p4[1]) / (p3[0] - p4[0]) * (target[0] - p3[0]) + p3[1]) > target[1]:
                        continue
                # linear a < 0
                else:
                    if not ((p3[1] - p4[1]) / (p3[0] - p4[0]) * (target[0] - p3[0]) + p3[1]) < target[1]:
                        continue

            if not ((p4[1] - p1[1]) / (p4[0] - p1[0]) * (target[0] - p4[0]) + p4[1]) < target[1]:
                continue

        except ZeroDivisionError as e:
            return False

        return True

    return False


def sort_rectPos(rectPos):
    """This function returns the sorted index of the original array according to the sorted array
    if the vertices of the squares are sorted in counterclockwise order. (like numpy argsort())

    :param list rectPos: The rectangle coordinates.
    .. Note:: rectPos must have the form of [[x,y], [x,y], [x,y], [x,y]]

    :returns: sorted index number list

    """
    x_arg_sort = np.argsort(rectPos, 0)[:, 0]

    if rectPos[x_arg_sort[0]][1] > rectPos[x_arg_sort[1]][1]:
        temp = x_arg_sort[0]
        x_arg_sort[0] = x_arg_sort[1]
        x_arg_sort[1] = temp

    if rectPos[x_arg_sort[2]][1] < rectPos[x_arg_sort[3]][1]:
        temp = x_arg_sort[3]
        x_arg_sort[3] = x_arg_sort[2]
        x_arg_sort[2] = temp

    try:
        a = (rectPos[x_arg_sort[3]][1] - rectPos[x_arg_sort[0]][1]) / (
                rectPos[x_arg_sort[3]][0] - rectPos[x_arg_sort[0]][0])
        result1 = a * (rectPos[x_arg_sort[2]][0] - rectPos[x_arg_sort[3]][0]) + rectPos[x_arg_sort[3]][1] - \
                 rectPos[x_arg_sort[2]][1]
    except ZeroDivisionError:
        result1 = -1

    try:
        a = (rectPos[x_arg_sort[1]][1] - rectPos[x_arg_sort[2]][1]) / (
                rectPos[x_arg_sort[1]][0] - rectPos[x_arg_sort[2]][0])
        result2 = a * (rectPos[x_arg_sort[0]][0] - rectPos[x_arg_sort[1]][0]) + rectPos[x_arg_sort[1]][1] - \
                  rectPos[x_arg_sort[0]][1]
    except ZeroDivisionError:
        result2 = -1

    if result1*result2 > 0:
        temp = x_arg_sort[2]
        x_arg_sort[2] = x_arg_sort[3]
        x_arg_sort[3] = temp

    return list(x_arg_sort)
