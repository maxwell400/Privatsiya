#Import libraries
try:
    from ultralytics import YOLO
    import filetype
    import cv2
    import argparse

    print("Libraries imported successfully.")

except:
    #To fix this, you may downgrade Python version and install libraries again
    print("An error occured while importing libraries.")

#Added arguments for easier usage
ap = argparse.ArgumentParser()

ap.add_argument("-f", "--file", required=True, help="Path to the file.")
ap.add_argument("-s", "--save",  required=True, help="Set the value as 1 if want to save it. 0 to not save it. DO NOT FORGET, this argument used as string, not a boolean.")
ap.add_argument("-n", "--name", required=False, help="If you set the value of --save argument, this parameter must be set too. This parameter value sets name of the blurred file.")

args = vars(ap.parse_args())

def video_file():
    video = cv2.VideoCapture(args["file"])

    yolo = YOLO("yolov8n-face.pt")

    if not video.isOpened():
        print("Unable to load the video.")
        return
    if args["save"] == 1 and args["name"]:
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS) #FPS did not attached as 'int' because of non-integer fps probabilities.

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(args["name"], fourcc, fps, (width, height))

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        face_detection = yolo(frame)
        boxes = face_detection[0].boxes

        for box in boxes:
            x, y, w, h = map(int, box.xyxy[0])
            face = frame[y:h, x:w]
            blurred_face = cv2.GaussianBlur(face, (23,23), cv2.BORDER_DEFAULT)
            frame[y:h, x:w] = blurred_face

        if args["save"] == 1 and args["name"]:
            out.write(frame)
        
        else:
            cv2.imshow("video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    video.release()
    if args["save"] == 1 and args["name"]:
        out.release()
        print(f"Blurred video saved.")

    else:
        cv2.destroyAllWindows()
 
def image_file():
    image = cv2.imread(args["file"]) #Get image path from arguments' list

    yolo = YOLO("yolov8n-face.pt")

    face_detection = yolo(image)

    boxes = face_detection[0].boxes

    for box in boxes:
        x, y, w, h = map(int, box.xyxy[0]) #Rectangle coordinates
        f = image[y:h, x:w] #Face area
        blurred_face = cv2.GaussianBlur(f, (23,23), cv2.BORDER_DEFAULT) #Blur "f" areas
        image[y:h, x:w] = blurred_face #Place the blurred "f" areas to original image

    if str((args["save"])) == "1":
        try:
            if args["name"] == None: #As --name mentioned as empty it is None as value, determined by argparse library
                print("--name argument is empty.")
            else:
                cv2.imwrite(str(args["name"]), image)
                print("Saved successfully.")
        except:
            print("Error occured while saving.")


if "image" in str(filetype.guess(str(args["file"]))):
    print("Image file detected.")
    image_file()

elif "video" in str(filetype.guess(str(args["file"]))):
    print("Video file detected.")
    video_file()

else:
    print("Unrecognised file type. Make sure your file type is acceptable or check your files integration within filetype library.")
