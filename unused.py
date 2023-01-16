def get_image_path():
    # create a tkinter root window
    root = tk.Tk()
    # hide the window
    root.withdraw()
    # open a dialog to select a file
    path = filedialog.askopenfilename()
    # return the selected file's path
    return path

def get_folder_path():
    # create a tkinter root window
    root = tk.Tk()
    # hide the window
    root.withdraw()
    # open a dialog to select a folder
    path = filedialog.askdirectory()
    # return the selected folder's path
    return path

def create_histogram(picture_path):
    # flatten the image into a 1D array
    flat_image = picture_path.flatten()
    # create a histogram
    plt.hist(flat_image, 1000, color="g", histtype="step") 
    plt.xlabel("Gray values")
    plt.ylabel("Number of pixels")
    plt.show()

def import_image(picture_path):
    # Loads image as 1D-Grayscale-image
    image = cv2.imread(picture_path, cv2.COLOR_BGR2GRAY)
    return image

def show_picture(picture_path):
    # displays a given image 
    plt.imshow(picture_path)
    plt.show()
   
def e_mail(address, results):
    # set up email server and login
    port = 465  # SSL
    smtp_server = "mx2fa8.netcup.net"
    sender_email = "fertigungstechnik@coldsense.de"  
    receiver_email = address
    # message to send
    subject = "Die Auswertung ist da!"
    message = f"Subject: {subject}\n\n"
    for result in results:
        message += "Datei: " + result[0] + ", Dichte: " + str(result[1]) + " %\n"
    # set up a ssl connection to the email server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message)
        
def take_webcam_screenshot(webcam_path):
    # access default webcam
    cam = cv2.VideoCapture(0)
    # create a window 
    cv2.namedWindow("Camera")
    # read image from webcam
    success, frame = cam.read()
    if success: 
        # display the image in the window
        cv2.imshow("Camera", frame)
        # generate a filename for the image
        img_name = "opencv_frame.png"
        # save the image
        cv2.imwrite(os.path.join(webcam_path, img_name), frame)
        print("{} written!".format(img_name))
    else:  
        print("Failed to grab frame.")

    # generate the path to new image
    path_to_new_file = os.path.join(webcam_path, img_name)

    # release the webcam and destroy the window
    cam.release()
    cv2.destroyAllWindows()

    # print the path to the saved image
    print("Webcam image written to: ", path_to_new_file)
    # return the path to the saved image
    return path_to_new_file

