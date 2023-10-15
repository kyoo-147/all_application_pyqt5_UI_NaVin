import os
import face_recognition
import cv2
from Data import *
from PIL import Image
import numpy as np


def encode_and_store_values(division='SE CMPN A'):
    images = os.listdir('Student Images/' + division + "/")

    # Opening the text files in w+ mode, so entire text file will be rewritten and if it doesnt exist
    # then a new file will be created
    input_encoding_file = open('Student Images/' + division + '/' + '#Encodings.txt', 'w+')
    input_ids = open('Student Images/' + division + '/' + '#Encoding Id.txt', 'w+')

    # Iterating through the database and writing encoding and id to text files
    # images[2:] because the first two files in each folder are the #Encodings.txt & #Encoding Id.txt which we skip
    for image in images[2:]:

        ''' 
        # This block is if we want to store encoding of grayscale images
        img_gray = img_new.convert('L')
        print("Grayscale image created")
        img_gray.save('Gray_Temp.jpg')
        current_image = face_recognition.load_image_file('Gray_Temp.jpg')
        print(img_gray.mode)
        '''

        current_image = face_recognition.load_image_file("Student Images/" + division + "/" + image)
        current_image_encoded = face_recognition.face_encodings(current_image, None, 15)[0]
        # known_face_encodings.append(current_image_encoded)
        # known_face_ids.append(image.split('.')[0])  # Adding Roll Numbers to the list
        print(image + " scanned")
        print(image.split('.')[0])
        print(current_image_encoded)

        # Converting current encoding to str and separating each element by ' ' and no [] or \n will be written
        input_encoding_file.write(' '.join(map(str, current_image_encoded)))
        # After each encoding vector written add a ',' so that we can ez split it later
        input_encoding_file.write(',')
        # add the roll number to the input_ids text file and add \n, for splitlines() later
        input_ids.write(image.split('.')[0]+'\n')
    input_encoding_file.close()
    input_ids.close()


def face_detect_and_recognize(image_paths, lecture_details):

    # Path for folder of known images
    images = os.listdir('Student Images/' + lecture_details['year_branch_div'] + "/")

    # Converting image to grayscale (works now :D)
    '''
    img_new = Image.open(img)
    img_gray = img_new.convert('L')
    print("Grayscale image created")
    img_gray.save('GrayOut.jpg')
    img_gray.show()
    print(img_gray.mode)
    '''

    # Old filthy way to encode images
    # Fill known face encodings and their names in respective lists
    '''
    for image in images:
        current_image = face_recognition.load_image_file("Student Images/"+division+"/" + image)
        current_image_encoded = face_recognition.face_encodings(current_image, None, 15)[0]
        known_face_encodings.append(current_image_encoded)
        known_face_id.append(image.split('.')[0])  # Adding Roll Numbers to the list
        print(image + " scanned")
        print(current_image_encoded)
    '''

    # New and improved way to read encodings
    # Reading from encoding and adding it to known_encodings

    # Initializing lists
    known_face_encodings = []
    current_encoding = []
    known_face_ids = []
    matched_ids = []
    image_counter = 1

    input_encoding_file = open('Student Images/' + lecture_details['year_branch_div'] + '/' + '#Encodings.txt', 'r')
    input_ids = open('Student Images/' + lecture_details['year_branch_div'] + '/' + '#Encoding Id.txt', 'r')

    # Encodings.txt contains the encoding vectors for each image in the database
    # Each vector is ended by a ',' which is why we used that split
    # Encoding Id.txt contains the roll numbers of the images, one on each line, hence splitlines()

    for encoding, current_id in zip(input_encoding_file.read().split(','), input_ids.read().splitlines()):
        # you need to split the current vector into individual elements to be able to add them to the list
        # which is why encoding.split() exists
        for encoding_value in encoding.split():
            current_encoding.append(encoding_value)
        print(current_id)
        known_face_ids.append(current_id)

        # The PIECE DE RESISTANCE
        # Converting the current_encoding list into an np array with each element in it of dtype float64
        current_encoding = np.array(current_encoding, dtype='float64')
        # print(current_encoding.shape, 'dype: ', current_encoding.dtype)
        known_face_encodings.append(current_encoding)
        # Resetting the value of the current_encoding to use for the next encoding vector
        current_encoding = []

    print("Finished compiling database")

    input_encoding_file.close()
    input_ids.close()

    # Perform encoding for each image to check using image_paths which is a list of path of images provided
    for img_path in image_paths:
        img = Image.open(img_path)
        print("Image opened")
        img.save('New Image.jpg')
        print("Image saved")
        image_to_scan = face_recognition.load_image_file('New Image.jpg')
        print("Imaged loaded")

        '''
        # Converting to grayscale block
        img = Image.open(img_path)
        print("Image opened")
        img_gray = img.convert('L')
        img_gray.save('GrayOut.jpg')
        print("Image saved")
        image_to_scan = face_recognition.load_image_file('GrayOut.jpg')
        print("Imaged loaded")
        '''

        face_locations = face_recognition.face_locations(image_to_scan)
        print("Face locations found")
        face_encodings = face_recognition.face_encodings(image_to_scan, face_locations, 15)
        print("Current image encoded")

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.45)
            # 0.48 best, 0.47 more accurate, 0.5 gets results atleast
            print(matches)
            name = "Unknown"
            roll_number = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                roll_number = known_face_ids[first_match_index]
                name = get_name(roll_number)
                print(name)
                matched_ids.append(roll_number)

            # Draw rectangle on OG image and not grayscale
            # Draw a box around the face
            cv2.rectangle(image_to_scan, (left, top), (right + 10, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image_to_scan, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        print("Recognised all faces")

        # Convert BGR to RGB
        image_to_scan = image_to_scan[:, :, ::-1]

        print("About to display")

        '''
        # Resizing the image so that it matches the dimensions of the cv2.imshow() output window
        small_image = cv2.resize(image_to_scan, (800, 600))

        # Display image on output screen and save scanned image as Output.jpg
        while True:
            cv2.imshow('Output', small_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        '''

        # Save output of current image to subject directory of class as
        # current_date + lecture_time + lecture_type + 1,2,3... .jpg

        path = 'Output Images/' + lecture_details['year_branch_div'] + '/' + lecture_details['subject'] + '/'
        if 'time' in lecture_details.keys():
            # Replacing : by . because file names cannot have :, but lecture_time has : in it so yeah
            lecture_details['time'] = lecture_details['time'].replace(':', '.')
            img_name = lecture_details['date'] + ' ' + lecture_details['time'] + ' ' + lecture_details['type'] + ' ' + str(image_counter) + '.jpg'
        else:
            img_name = lecture_details['date'] + ' ' + lecture_details['type'] + ' ' + str(image_counter) + '.jpg'
        print(path + img_name)
        # Only save image if a face was detected
        if len(matched_ids) > 0 :
            cv2.imwrite(path + img_name, image_to_scan)
            print("Image saved")
        # Saving temporary output so we can use startfile with it
        cv2.imwrite('Output.jpg', image_to_scan)
        # Display image
        os.startfile('Output.jpg')
        image_counter += 1

    return matched_ids


# face_detect_and_recognize(['New Image.jpg'])


# RUN THIS FUCKING FUNCTION ONCE
# THEN COMMENT IT OUT AND EVERYTHING SHOULD WORK FINE
# encode_and_store_values()
