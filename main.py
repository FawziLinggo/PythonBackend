import logging

import cv2
logging.basicConfig(level=logging.INFO)

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.filters import (threshold_otsu, threshold_niblack,
                             threshold_sauvola)
import pyrebase
angle = 45
try:
    #Config Firebase
    config ={
    "apiKey": "AIzaSyAAR8u71dKG9dqYYtgZmhAwwcsN_pWgmMI",
    "authDomain": "ulul-1010.firebaseapp.com",
    "databaseURL":"https://ulul-1010-default-rtdb.firebaseio.com",
    "projectId": "ulul-1010",
    "storageBucket": "ulul-1010.appspot.com",
    "messagingSenderId": "547305753399",
    "appId": "1:547305753399:web:7239dfba925311164668b2",
    "measurementId": "G-VBYDY91Z9G"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    databases = firebase.database()
    logging.error("Berhasil Melakukan config firebase")
except:
    logging.error("Error Config Firebase")

try:
    error = databases.child("Push").child("Push").get()
    error = error.val()
    logging.error("Nilai Sekarang ss %s", error)
except:
    logging.error("Error melakukan get hasil")

logging.error("Program still Running")
while True:
    try:
        error = databases.child("Push").child("Push").get()
        error = error.val()
    except:
        logging.error("Error melakukan get hasil")
    if error == 1:
        #Download
        path_on_cloud = "image.jpg"
        storage.child("image.jpg").download(filename="image.jpg",path="")
        logging.error("berhasil melakukan Download. Path : image.jpg")

        matplotlib.rcParams['font.size'] = 9
        original = Image.open("image.jpg")
        img = Image.open("image.jpg").convert('L')
        # img.rotate(90)
        image = np.array(img)
        binary_global = image > threshold_otsu(image)

        window_size = 25
        Koofesien = 0.8
        thresh_niblack = threshold_niblack(image, window_size=window_size, k=Koofesien)

        thresh_sauvola = threshold_sauvola(image, window_size=window_size)

        binary_niblack = image > thresh_niblack
        binary_sauvola = image > thresh_sauvola
        TNS = (binary_niblack + binary_sauvola) / 2
        logging.error("Berhasil Melakukan binary_TNS")

        # # plt.figure(figsize=(8, 7))
        # new_data = ndimage.rotate(TNS, angle, reshape=True)
        # plt.imshow(new_data, cmap=plt.cm.gray)
        # plt.axis('off')

        # plt.savefig("image.jpg")
        plt.imsave('image.jpg', TNS,cmap=plt.cm.gray)
        Original_Image = Image.open("image.jpg")
        # rotatecmap=plt.cm.gray
        rotated_image2 = Original_Image.transpose(Image.ROTATE_270)
        rotated_image2.save("image.jpg")
        logging.error("Berhasil menyimpan gambar hasil Binary")

        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()

        path_local = "image.jpg"
        storage.child(path_on_cloud).put(path_local)
        logging.error("Berhasil Mengupload gambar ke firebase")
        try:
            data = {"Push":0}
            databases.child("Push").update(data)
            logging.error("berhasil Mengirimkan 0 pada Push, %s", data)
        except:
            logging.error("gagal Melakukan Push Data")
