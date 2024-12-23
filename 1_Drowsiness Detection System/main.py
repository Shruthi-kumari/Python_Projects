# for basic image processing functions
import cv2

# for deep learning based Modules and face landmark detection
import dlib

# for basic operations of conversion
from imutils import face_utils

# for audio playing
from playsound import playsound

#for calculating distance between 2 coodinates
from scipy.spatial import distance as distance

# Initializing the camera and taking the instance
#capture the real time video of the driver
cap = cv2.VideoCapture(0)


# Initializing the face detector and landmark detector

# Get the coordinates,used in detecting the face in a frame or image. 
detector = dlib.get_frontal_face_detector()


#a tool that takes in an image region containing some object and outputs 
# a set of point locations that define the pose of the object.
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# status marking for current state
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)


# Compute Eulidean distance
def compute(ptA, ptB):
    Euclidean_d = distance.euclidean(ptA,ptB)
    return Euclidean_d

# Compute EAR
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up/(2.0*down)

    # Checking if it is blinked
    if (ratio > 0.2):
        return 1
    else:
        return 0


while True:
    _, frame = cap.read()

    # RGB to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    # detected face in faces array
    # coordinates of the face in the video
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    landmarks = predictor(gray, face)
    landmarks = face_utils.shape_to_np(landmarks)

    # The numbers are actually the landmarks which will show eye
    left_blink = blinked(landmarks[36], landmarks[37],
                         landmarks[38], landmarks[41], landmarks[40], landmarks[39])
    right_blink = blinked(landmarks[42], landmarks[43],
                          landmarks[44], landmarks[47], landmarks[46], landmarks[45])

    # Now judge what to do for the eye blinks

    if (left_blink == 0 or right_blink == 0):

        drowsy += 1
        active = 0

        if (drowsy > 6):
            status = "Drowsy!"
            color = (0, 0, 255)
            cv2.putText(frame, status, (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            playsound('Wake_up.mp3')

    else:
        drowsy = 0

        active += 1
        if (active > 6):
            status = "Active "
            color = (0, 255, 0)
            
            cv2.putText(frame, status, (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
		        break

cv2.destroyAllWindows()
cap.release()







