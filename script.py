import numpy as np 
import matplotlib.pyplot as plt 
import os
import cv2
import sys
import tkinter as tk
import tkinter.messagebox
import smtplib, ssl
import shutil
import datetime
from tkinter import filedialog
from PIL import Image, ImageTk
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from ast import ExceptHandler

# global variables for sample analysis

threshold_gray = 150
threshold_color = 80

threshold_contour_length = 130
threshold_contour_area = 500

cropping_offset = 50 

password = "yourpassword"

def calculate_density(flat_image, threshold_gray):
    # count black pixels as impurities
    black_pixels = np.sum(flat_image <= threshold_gray)
    # count white pixels as dense material
    white_pixels = np.sum(flat_image == 255)

    # calculating Density
    density = (white_pixels / (black_pixels + white_pixels))

    return density # Return density 

def crop_image_five(image_path, Filename):
    # open the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # get image dimensions
    height, width = img.shape
    # set the dimensions of the crops and the offset from the corners
    crop_width = int((width-2*cropping_offset)//2.5)
    print(crop_width)
    crop_height = int((height-2*cropping_offset)//2.5)

    offset = cropping_offset
    # calculate the center coordinates of the image
    center_x, center_y = width // 2, height // 2
    
    cropped_images = []
    
    # crop and save center image
    cropped_center = img[center_y - crop_height // 2:center_y + crop_height // 2, center_x - crop_width // 2:center_x + crop_width // 2]
    cv2.imwrite("cropped_center-{}".format(Filename), cropped_center)
    cropped_images.append(cropped_center)
    # crop and save top left image
    cropped_top_left = img[offset:offset + crop_height, offset:offset + crop_width]
    cv2.imwrite("cropped_top_left-{}".format(Filename), cropped_top_left)
    cropped_images.append(cropped_top_left)
    # crop and save top right image
    cropped_top_right = img[offset:offset + crop_height, width - offset - crop_width:width - offset]
    cv2.imwrite("cropped_top_right-{}".format(Filename), cropped_top_right)
    cropped_images.append(cropped_top_right)
    # crop and save bottom left image
    cropped_bottom_left = img[height - offset - crop_height:height - offset, offset:offset + crop_width]
    cv2.imwrite("cropped_bottom_left-{}".format(Filename), cropped_bottom_left)
    cropped_images.append(cropped_bottom_left)
    # crop and save bottom right image
    cropped_bottom_right = img[height - offset - crop_height:height - offset, width - offset - crop_width:width - offset]
    cv2.imwrite("cropped_bottom_right-{}".format(Filename), cropped_bottom_right)
    cropped_images.append(cropped_bottom_right)
    
    return cropped_images

def convert_image(image, Filename):

    # converts image to grayscale (array)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply threshold to grayscale image
    density = calculate_density(gray, threshold_gray)
    if density*100 < 50:
        print("## INFO ## Es wurde ein dunkles Bild erkannt. Wandle das Bild um...\n")
        _, binary_image = cv2.threshold(gray, threshold_color, 255, cv2.THRESH_BINARY)
        gray = binary_image

        gray = cv2.bitwise_not(gray)
    else:
        print("## INFO ## Das verwendete Bild entspricht dem Standard. Fahre fort.\n")

    # create a Sobel mask to highlight edges
    sobel_x = cv2.Sobel(gray , cv2.CV_64F, 1, 0, ksize=1)
    sobel_y = cv2.Sobel(gray , cv2.CV_64F, 0, 1, ksize=1)

    # calculate the gradient
    gradient = np.sqrt(np.square(sobel_x) + np.square(sobel_y))

    # convert the gradient to an 8-bit integer
    gradient = np.uint8(255 * (gradient / np.max(gradient)))

    # cv2.imwrite("AfterSobel.png", gradient)

    # perform contour detection
    # Note: hierarchy "not used" but necessary!
    contours, hierarchy = cv2.findContours(gradient, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # go through all contours and remove those longer than 130 pixels or smaller than 500px area
    for c in contours:
        if len(c) > threshold_contour_length:
            cv2.drawContours(gradient, [c], -1, (255,255,255), -1)

        if cv2.contourArea(c) < threshold_contour_area:
            cv2.drawContours(gradient, [c], -1, (0,0,0), -1)

    # save the image with removed scratches
    cv2.imwrite("Erkannte_Kratzer-{}".format(Filename), gradient)

    # overriding recognized scratches 
    CorrectedImage = cv2.add(gradient, gray)

    # saving corrected file
    cv2.imwrite("Korrigiert-{}".format(Filename), CorrectedImage)

    return CorrectedImage

def e_mail(address, results):
    # set up email server and login
    port = 465  # SSL
    smtp_server = "your.smtp.tld"
    sender_email = "your@domail.tld"  
    receiver_email = address
    # create message
    message = MIMEMultipart()
    message["Subject"] = "Die Auswertung ist da!"
    message["From"] = sender_email
    message["To"] = receiver_email
    for result in results:
        text = f"Datei: {result[0]}, Dichte: {result[1]} %"
        message.attach(MIMEText(text))
        image_path = f"{result[0]}"
        # check if the image exists in the local directory
        if os.path.exists(image_path):
            # open image in binary mode
            with open(image_path, "rb") as image_file:
                image = MIMEBase("application", "octet-stream")
                image.set_payload(image_file.read())
            # encode the image and add header with pdf name
            encoders.encode_base64(image)
            image.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(image_path)}",
            )
            # add the image to the message
            message.attach(image)
        else:
            pass
    # set up a ssl connection to the email server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

def save_image():
    # get the current webcam frame
    ret, frame = webcam.read()

    # get the current date and time
    now = datetime.datetime.now()
    file_name = "Probe_" + now.strftime("%Y-%m-%d %H-%M-%S") + ".jpg"

    file_path = os.path.join(os.getcwd(), file_name)

    # save the image to the working directory
    cv2.imwrite(file_path, frame)
    tk.messagebox.showinfo("Info","Das Foto wurde zur Analyse-Warteschlange hinzugefuegt! Sie koennen nun ein weiteres Foto aufnehmen oder die Analyse starten.")

def copy_images():
    # open a file dialog to select one or more images
    selected_files = filedialog.askopenfilenames()

    # iterate over the selected files
    for file_path in selected_files:
        # generate file name with date and time
        now = datetime.datetime.now()
        file_name = "Probe_" + now.strftime("%Y-%m-%d %H-%M-%S") + ".jpg"
        new_file_path = os.path.join(os.getcwd(), file_name)

        # copy the selected files to the working directory
        shutil.copy2(file_path, new_file_path)
        tk.messagebox.showinfo("Info","Das Foto wurde zur Analyse-Warteschlange hinzugefuegt! Sie koennen nun ein weiteres Foto aufnehmen oder die Analyse starten.")

def display_webcam_feed():
    # get webcam image
    ret, frame = webcam.read()

    # converting image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(img)
    
    # display webcam feed
    webcam_canvas.create_image(0, 0, image=img, anchor=tk.NW)
    webcam_canvas.image = img
    
    # Repeat the process after a delay
    root.after(20, display_webcam_feed)

# this is main

results = []

if __name__ == "__main__":
    try:
        # create a new tkinter window
        root = tk.Tk()
        root.title("Webcam GUI")

        # create a canvas to display webcam
        webcam_canvas = tk.Canvas(root, width=640, height=480)
        webcam_canvas.pack(side=tk.TOP)

        # create a button for a screenshot
        capture_button = tk.Button(root, text="Bild Aufnehmen", command=save_image)
        capture_button.pack(side=tk.BOTTOM)

        # create a button for searching local files
        select_button = tk.Button(root, text="Dateien durchsuchen...", command=copy_images)
        select_button.pack(side=tk.BOTTOM)

        # create a button for starting the script
        close_button = tk.Button(root, text="Analyse starten", command=root.quit)
        close_button.pack(side=tk.BOTTOM)

        # shows the webcam image
        webcam = cv2.VideoCapture(0)
        display_webcam_feed()

        root.mainloop()

        # loop through all files in the current directory
        for file in os.listdir():
             # check if the file starts with "Probe_"
            if file.startswith("Probe_"):
                # saving Filename for naming files
                Filename = str(file)
                print("Lese Datei:\n", file)
                # read the image 
                image = cv2.imread(file)
                print("Bearbeite die Datei:\n", file,"\n")
                try:
                    convert_image(image, Filename)
                    # loop through all files in the current directory
                    for file in os.listdir():
                        count = 0
                        density_sum = 0
                        # check if the file starts with "Korrigiert"
                        if file.startswith("Korrigiert-{}".format(Filename)):
                            # crop the image into 5 arrays
                            arrays = crop_image_five(file, Filename)
                            for array in arrays:
                                # calculate the density of the image
                                density = calculate_density(array, threshold_gray)
                                if density*100 > 95:
                                     print("Dichte des Bildes",count,"von", Filename, ":" ,round(density*100,2), "%")
                                     density_sum += density
                                     count += 1
                                else:
                                    print("Dichte des Bildes",count,"von", Filename, ":" ,round(density*100,2), "%", " [NICHT VERWENDET!]")
                            try:
                                mean_density = (density_sum / count)*100
                            except:
                                print("\n## INFO ## Die Auswertung wurde uebersprungen\n")
                                print("########################################################################\n")
                                continue
                            print("\nDer Mittelwert der Dichten betraegt:", round(mean_density,2), "%\n")
                            print("########################################################################\n")

                            # adding results to the list
                            results.append((Filename, round(mean_density,2)))
                # file is corrupted or different than expected, ignoring it
                except:
                    print("\n\n### WARNUNG ##")
                    print("### Die Datei", Filename, "konnte nicht analysiert werden. Fahre mit der naechsten Datei fort ###")
                    print("### WARNUNG ##\n\n")
                    print("\n########################################################################\n")
                    continue

        print("\n## INFO ## Die Auswertung wurde abgeschlossen")

        # email sent flag
        email_sent = False

        while True:
            # checking if email was sent
            if email_sent:
                # if yes, ending script
                break
            else:
                # if not, asking if a email is wished
                print("\n## INFO ## Wollen Sie die Resultate auch als E-Mail erhalten?")
                print("## INFO ## Fuer ja, geben sie ""ja"" ein. Wenn nicht, geben Sie ""nein"" ein\n")
                # get users input 
                answer = input()
                if answer.lower() == "ja":
                        print("\n## INFO ## Geben Sie Ihre Email Adresse an\n")
                        address = input()
                        while True:
                            # confirm choice
                            print("\n## INFO ## Ist", address, "richtig? (Ja/Nein)\n")
                            answer = input()
                            if answer.lower() == "ja":
                                try:
                                    # sending mails with the results
                                    e_mail(address, results)
                                    print("\n## INFO ## Die E-Mail wurde verschickt")
                                except:
                                    # email is wrong and email couldn't be sent
                                    print("\n## INFO ## Die E-Mail Adresse ist ungueltig oder konnte nicht verschickt werden")
                                print("\n## INFO ## Das Programm wird nun beendet\n")
                                # set flag for exit
                                email_sent = True
                                break
                            if answer.lower() == "nein":
                                print("\n## INFO ## Geben Sie Ihre Email Adresse an\n")
                                address = input()
                                # going back to the beginning
                                continue
                # user dont want an email
                elif answer.lower() == "nein":
                    # confirming choice
                    print("\n## INFO ## Sind Sie sich sicher? (Ja/Nein)\n")
                    answer = input()
                    if answer.lower() == "ja":
                        # ending program
                        break
                    if answer.lower() == "nein":
                        # going back to the beginning
                        continue
                else:
                    print("Die Antwort ist ungueltig")
    except KeyboardInterrupt:
        sys.exit(0)




    








   


