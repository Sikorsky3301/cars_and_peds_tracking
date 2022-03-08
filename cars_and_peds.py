import cv2
video = cv2.VideoCapture('peds_and_cars.mp4')

#Our pre-trained car and peds classifiers
Car_tracker_File = 'cars.xml'
pedestrians_tracker_file = 'haarcascade_fullbody.xml'

#create car Classifier
car_tracker = cv2.CascadeClassifier(Car_tracker_File)

#Create Full body Classifier
pedestrians_tracker = cv2.CascadeClassifier(pedestrians_tracker_file)

#Run forever until car stops or something 
while True:
    #Read the current frame
    (read_successful, frame) = video.read()

    #safe coding 
    if read_successful:
        #Must convert to grayscale
        grayscaled_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    else:
        break

    #detect cars and Pedestrians
    cars = car_tracker.detectMultiScale(grayscaled_frame)
    pedestrians = pedestrians_tracker.detectMultiScale(grayscaled_frame)

    #Draw rectangles around the cars
    for (x,y,w,h) in cars:
        cv2.rectangle(frame, (x+1, y+1), (x+w, y+h), (0, 0, 255), 2 )
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2 )

    #Draw rectangles around the Pedestrians
    for (x,y,w,h) in pedestrians:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2 )
    

    #Display the image with the faces spotted
    cv2.imshow('Car and Pedestrians detector', frame )

    #Autoclose disabled with the help of wait key
    key= cv2.waitKey(1)

    print("Code Completed")

    if key==75 or key==107:
        break

#Release the Video
video.release()
