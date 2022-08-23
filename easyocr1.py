import csv
import os
import re
import sqlite3
from datafill import *
# import dateutil.parser as dparser

from easyocr import Reader
import argparse
import cv2
from threading import *
from datafill import *

class aadharocr(Thread):
    def __init__(self, aadhar_info, location, un, room, arraived, amount, event):
        super().__init__()
        self.stopped = event
        # self.thread2 = datathread
        self.args = aadhar_info
        self.currentlocation = location
        self.username = un
        self.room = room
        self.arrive = arraived
        self.amount = amount

    def cleanup_text(self, text):
        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV
        return "".join([c if ord(c) < 128 else "" for c in text]).strip()

    def find_adhar_number(self, ocr_text):
        """Function to find adhar number inside the image

		Args:
		ocr_text (list): text from the ocr

		Returns:
		str: 12 digit aadhaar number
		"""
        adhar_number_patn = '[0-9]{4}\s[0-9]{4}\s[0-9]{4}'
        match = re.search(adhar_number_patn, ocr_text)
        if match:
            return match.group()

    def find_name(self, ocr_text):
        """Function to find adhar name inside the image

		Args:
		ocr_text (list): text from the ocr

		Returns:
		str: name on the aadhar card
		"""
        adhar_name_patn = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\s[A-Z][a-z]+$'
        split_ocr = ocr_text.split('\n')
        for ele in split_ocr:
            match = re.search(adhar_name_patn, ele)
            if match:
                return match.group()

    def find_dob(self, ocr_text):
        """Function to find date of birth inside the image

		Args:
		ocr_text (list): text from the ocr

		Returns:
		str: Date of birth
		"""
        dob_patn = '\d+[-/]\d+[-/]\d+'
        yob_patn = '[0-9]{4}'
        DateOfBirth = ''
        # print("check ocr_text",ocr_text)
        if 'DOB' in ocr_text:
            match = re.search(dob_patn, ocr_text)
            DateOfBirth = match.group()
        if 'Year of Birth' in ocr_text:
            match = re.search(yob_patn, ocr_text)
            DateOfBirth = match.group()
        return DateOfBirth

    def find_gender(self, ocr_text):
        """Function to find Gender inside the image

		Args:
		ocr_text (list): text from the ocr

		Returns:
		str: Gender
		"""
        if 'Male' in ocr_text or 'MALE' in ocr_text:
            GENDER = 'Male'
        elif 'Female' in ocr_text or 'FEMALE' in ocr_text:
            GENDER = 'Female'
        else:
            GENDER = 'NAN'
        return GENDER

    def find_address(self, ocr_text):
        """Function to find address inside the image

		Args:
		ocr_text (list): text from the ocr

		Returns:
		str: address on the aadhaar card
		"""

        # ocr_text = pytesseract.image_to_string(
        # 	backimg, config=f'-l eng --psm 6 --oem 3 ')
        # # print(ocr_text)

        try:
            address_start = ocr_text.find('Address')
            address = ocr_text[address_start:]
            pinpatn = r'[0-9]{6}'
            address_end = 0
            pinloc = re.search(pinpatn, address)
            if pinloc:
                address_end = pinloc.end()
            else:
                print('Pin code not found in address')
                address = re.sub('\n', ' ', address[:address_end])
            address = address.split(':')[1]
            return address
        except:
            address = re.sub('\n', ' ', ocr_text)
            pinpatn = re.compile(r'[0-9]{6}')
            pincode = re.search(pinpatn, address)
            # print(pincode.group())
            return pincode.group()

    def run(self):
        print("ocr thread is running!!")

        langs = self.args["langs"].split(",")
        print("[INFO] OCR'ing with the following languages: {}".format(langs))
        # load the input image from disk
        image = cv2.imread(self.args["image"])
        # OCR the input image using EasyOCR
        print("[INFO] OCR'ing input image...")
        reader = Reader(langs, gpu=self.args["gpu"] > 0)
        results = reader.readtext(image)
        # print("results---->",results)

        textlist = []

        for (bbox, text, prob) in results:
            # display the OCR'd text and associated probability
            # print("[INFO] {:.4f}: {}".format(prob, text))
            # unpack the bounding box
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            # cleanup the text and draw the box surrounding the text along
            # with the OCR'd text itself
            text = self.cleanup_text(text)
            # print("text -->",text)
            textlist.append(text)
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            cv2.putText(image, text, (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        # show the output image
        # print(textlist)
        print(" ".join(textlist))
        texts = " ".join(textlist)
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)
        aadhar_number = self.find_adhar_number(texts)
        print(aadhar_number)
        name = self.find_name(texts)
        print(name)
        dob = self.find_dob(texts)
        print(dob)
        gender = self.find_gender(texts)
        print(gender)
        # ## dump data into database
        sqlconnection = sqlite3.Connection(self.currentlocation + '/login.db')
        cursor = sqlconnection.cursor()
        # # # print(cursor)
        query1 = "INSERT INTO GuestDetails (Username,RoomNo,Amount,Arrive,GuestName,UID,DOB,Gender) VALUES ('{usn}','{rn}','{am}','{fm}','{gn}','{uid}','{db}','{gd}');".format(
            usn=self.username, rn=self.room, am=self.amount, fm=self.arrive, gn=name, uid=aadhar_number, db=dob,
            gd=gender)
        cursor.execute(query1)
        sqlconnection.commit()
        sqlconnection.close()
        print("connection closed")
        # datathread = datafillup()
        # datathread.start()
        # self.thread2.start()
    # fillform = datafillup()
    # fillform.start()

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image",  default="aad43.jpg",
# 	help="path to input image to be OCR'd")
# ap.add_argument("-l", "--langs", type=str, default="en",
# 	help="comma separated list of languages to OCR")
# ap.add_argument("-g", "--gpu", type=int, default=-1,
# 	help="whether or not GPU should be used")
#
# # args = vars(ap.parse_args())
# # print("check args ",args)
# # # aadhar_ocr(args)
# # aadhar_val = aadharocr(args)
# # aadhar_val.start()
