import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.filters import (threshold_otsu, threshold_niblack,
                             threshold_sauvola)
import pyrebase

try:
    #Config Firebase
    config ={
    "apiKey": "AIzaSyAAR8u71dKG9dqYYtgZmhAwwcsN_pWgmMI",
    "authDomain": "ulul-1010.firebaseapp.com",
    "databaseURL":"https://ulul-1010-default-rtdb.firebaseio.com/",
    "projectId": "ulul-1010",
    "storageBucket": "ulul-1010.appspot.com",
    "messagingSenderId": "547305753399",
    "appId": "1:547305753399:web:7239dfba925311164668b2",
    "measurementId": "G-VBYDY91Z9G"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    databases = firebase.database()
    logging.info("Berhasil Melakukan config firebase")
except:
    logging.error("Error Config Firebase")

try:
    error = databases.child("Push").child("Push").get()
    error = error.val()
    logging.info("Nilai Sekarang %s", error)
except:
    logging.error("Error melakukan get hasil")

logging.info("Program still Running")
while error == 0:
    try:
        error = databases.child("Push").child("Push").get()
        error = error.val()
        logging.info("Nilai Sekarang %s", error)
    except:
        logging.error("Error melakukan get hasil")
    if error == 1:
        #Download
        path_on_cloud = "images/hasil3.jpg"
        storage.child(path_on_cloud).download("Images/img_1.png")
        logging.info("berhasil melakukan Download. Path : Images/img_1.png")

        matplotlib.rcParams['font.size'] = 9
        original = Image.open("Images/img_1.png")
        img = Image.open("Images/img_1.png").convert('L')
        image = np.array(img)
        binary_global = image > threshold_otsu(image)
        logging.info("Berhasil Melakukan binary_global")

        window_size = 25
        Koofesien = 0.8
        thresh_niblack = threshold_niblack(image, window_size=window_size, k=Koofesien)
        logging.info("Berhasil Melakukan binary_niblack, Window Size : %s", window_size)
        logging.info("Berhasil Melakukan binary_niblack, Koofesien : %s", Koofesien)

        thresh_sauvola = threshold_sauvola(image, window_size=window_size)
        logging.info("Berhasil Melakukan binary_sauvola, Window Size : %s", window_size)

        binary_niblack = image > thresh_niblack
        binary_sauvola = image > thresh_sauvola
        TNS = binary_niblack + binary_sauvola / 2
        logging.info("Berhasil Melakukan binary_TNS")

        plt.figure(figsize=(8, 7))
        plt.subplot(2, 2, 1)
        plt.imshow(original, cmap=plt.cm.gray)
        plt.title('Original')
        plt.axis('off')

        plt.subplot(2, 2, 2)
        plt.title('TNS')
        plt.imshow(TNS, cmap=plt.cm.gray)
        plt.axis('off')

        plt.subplot(2, 2, 3)
        plt.imshow(binary_niblack, cmap=plt.cm.gray)
        plt.title('Niblack Threshold')
        plt.axis('off')

        plt.subplot(2, 2, 4)
        plt.imshow(binary_sauvola, cmap=plt.cm.gray)
        plt.title('Sauvola Threshold')
        plt.axis('off')

        plt.savefig("Images/hasil3.png")
        logging.info("Berhasil menyimpan gambar hasil Binary")

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        path_local = "Images/hasil3.png"
        storage.child(path_on_cloud).put(path_local)
        logging.info("Berhasil Mengupload gambar ke firebase")
        try:
            data = {"Push":0}
            #databases.push(data)
            databases.child("Push").update(data)
            logging.info("berhasil Mengirimkan 0 pada Push, %s", data)
        except:
            logging.error("gagal Melakukan Push Data")
