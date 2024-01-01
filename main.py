#Exception handling of importing libs
try:
    import cv2
    import filetype
    import os
    import argparse

except:
    print("Libs are not installed, use 'pip install opencv-python opencv-contrib-python filetype os argparse'")

ap = argparse.ArgumentParser()

#Added arguments for easier usage
ap.add_argument("-i", "--image", required=True, help="Path for the image")

ap.add_argument("-s", "--save", required=True, help="1 for saving the image, 0 for not saving it.")

ap.add_argument("-n", "--name", required=False, help="Determine a name for your blurred image if you want to save your file.")

#Arguments assigned to a variable 
args = vars(ap.parse_args())

#Dataset to detect faces
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def blur_image():
    img = cv2.imread(args["image"])

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Image converted to grayscale for face detection

    fd = cascade.detectMultiScale(
        gray_img,
        scaleFactor = 1.1,
        minNeighbors = 5,
        minSize=(30,30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for(x, y, w, h) in fd:
        #cv2.rectangle(img, (x,y), (x+w , y+h), (255,0,0), 2) #Remove the sharp for showing detection lines
        f = img[y:y+h, x:x+w]
        f = cv2.GaussianBlur(f,(23,23), cv2.BORDER_DEFAULT)

        img[y:y+f.shape[0], x:x+f.shape[1]] = f #Assignation of f is reversed because of the row by row compile 

    cv2.imshow("img", img)
    cv2.waitKey(0)

    if str((args["save"])) == "1":
        try:
            name_input = str((args["name"]))
            if name_input != "":
                cv2.imwrite(name_input, img)
                print("Saved successfully")
            elif name_input == "":
                print("--name argument is empty.")
                exit

        except:
            print("Error occured while saving")

    else:
        print("Quitting...")
        
blur_image()
