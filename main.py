import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition

# Configuration
path = 'image_folder'
url = 'http://192.168.99.136/cam-hi.jpg'  # Change to your actual URL
attendance_folder = 'attendance'
date_str = datetime.now().strftime('%d-%m-%Y')
attendance_file = f"attendance_{date_str}.csv"

# Ensure the attendance folder exists
if not os.path.exists(attendance_folder):
    os.makedirs(attendance_folder)

# Path to the attendance CSV file
attendance_file_path = os.path.join(attendance_folder, attendance_file)

# Create the attendance file if it does not exist
if not os.path.isfile(attendance_file_path):
    df = pd.DataFrame(columns=['Name', 'Time'])
    df.to_csv(attendance_file_path, index=False)
else:
    print(f"Attendance file {attendance_file} already exists")

# Load images and class names
images = []
classNames = []
myList = os.listdir(path)
print("Image list:", myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0].upper())  # Ensure names are in uppercase
print("Class names:", classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
        else:
            print(f"No face found in image {img}")
    return encodeList

def markAttendance(name):
    with open(attendance_file_path, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0].strip() for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            if name in classNames:
                classNames.remove(name)  # Remove the name from the list if it exists

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Ensure the lengths match
if len(encodeListKnown) != len(classNames):
    print("Warning: The number of encodings and class names do not match.")
    print(f"Encodings: {len(encodeListKnown)}, Class names: {len(classNames)}")
else:
    print("Number of encodings and class names match.")

while True:
    # Capture image from URL
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    
    # Resize and convert image for processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        if len(faceDis) == 0:
            continue
        
        matchIndex = np.argmin(faceDis)

        if matchIndex >= len(classNames):
            print(f"Warning: matchIndex {matchIndex} out of range for classNames")
            continue
        
        if matches[matchIndex]:
            name = classNames[matchIndex]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
    
    cv2.imshow('Webcam', img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
