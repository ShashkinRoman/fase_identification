"""
Человек подходит к камере, его распознает, записывает в журнал вход или выход
"""
import face_recognition
import cv2
import numpy as np
from monitoring_system.models import User, Journal
from transliterate import translit
from time import sleep
from collections import Counter

# todo продумать ситуацию, когда человек при выходе неправильно опознался

video_capture = cv2.VideoCapture(0)


def load_users():
    """
    Грузит всех пользователей из базы и возвращает списки для использования в распознавании
    :return:  known_face_encodings, known_face_names
    """
    users = User.objects.all()

    known_face_encodings = []
    known_face_names = []

    for user in users:
        # Load a sample picture and learn how to recognize it.
        user_image = face_recognition.load_image_file(user.path_photo.path)
        user_face_encoding = face_recognition.face_encodings(user_image)[0]
        known_face_encodings.append(user_face_encoding)
        # Create arrays of known face encodings and their names
        known_face_names.append(translit(f'{user.id}){user.first_name} {user.second_name}', reversed=True))
    return known_face_encodings, known_face_names


frame_counter = 0
face_list_controller = []


known_face_encodings, known_face_names = load_users()


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            if name != "Unknown":
                frame_counter += 1
                face_list_controller.append(name)
            if frame_counter > 0 and frame_counter % 20 == 0:
                # Getting key with maximum value in dictionary
                final_name = max(Counter(face_list_controller), key=Counter(face_list_controller).get)
                Journal.objects.create(status=True, userid=User.objects.get(id=int(final_name.split(')')[0])))
                print("Дверь открыта!")
                frame_counter = 0
                face_list_controller = []
                sleep(3)


            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

def video_flow(video_source):
    """Считывает видеопоток из источника """
    video_capture = cv2.VideoCapture(0)
    pass


def statuses_load():
    """
     Подтягивает из бд статусы
    :return:
    """


def write_journal():
    """
    ЗАписывает информацию в журнал, в зависимости от того с какого сигнала пришло видео
    :return:
    """


def time_calculate():
    """
    Показывает сколько времени осталось сегодня человеку пройти
    :return:
    """


def start_wideo_flow():
    """
    Старт видео потока возвращение результатов
    :return:
    """