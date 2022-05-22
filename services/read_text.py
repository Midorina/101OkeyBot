import time

import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

sift = cv2.SIFT_create()


def read_text(text_image):
    # start = time.time()

    text = pytesseract.image_to_string(improve_image_for_ocr(text_image))
    # text = pytesseract.image_to_string(text_image)

    # time_it_took = time.time() - start
    # print(f"time it took to read the text: {time_it_took}")

    return text


def images_are_equal(im1, im2) -> bool:
    # start = time.time()

    im1, im2 = np.array(im1), np.array(im2)

    # remove the ALPHA channel if its there
    if im1.shape != im2.shape:
        im2 = im2[:, :, :3]

    difference = cv2.subtract(im1, im2)
    b, g, r = cv2.split(difference)
    # print(f"time it took to check if images are equal: {time.time() - start}")

    print(cv2.countNonZero(b), cv2.countNonZero(g), cv2.countNonZero(r))

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        return True
    else:
        return False


def images_are_similar(im1, im2) -> bool:
    im1, im2 = np.array(im1), np.array(im2)

    kp_1, desc_1 = sift.detectAndCompute(im1, None)
    kp_2, desc_2 = sift.detectAndCompute(im2, None)

    # print("kp1:", len(kp_1))
    # print("kp2:", len(kp_2))

    number_keypoints = len(kp_1) if len(kp_1) <= len(kp_2) else len(kp_2)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good_points.append(m)

    similarity_percentage = len(good_points) / number_keypoints * 100

    # print("Keypoints 1ST Image: " + str(len(kp_1)))
    # print("Keypoints 2ND Image: " + str(len(kp_2)))
    # print("GOOD Matches:", len(good_points))
    print("How good it's the match: ", similarity_percentage)

    return similarity_percentage > 75


def take_screenshot(coords):
    while True:
        try:
            return ImageGrab.grab(bbox=coords)
        except OSError:
            print("Screen grab failed. Trying again in 1 second...")
            time.sleep(1)


def wait_until_screen_changes(coords):
    im1 = take_screenshot(coords)
    im2 = take_screenshot(coords)

    while images_are_equal(im1, im2):
        im1 = im2
        im2 = take_screenshot(coords)

    return im2


def improve_image_for_ocr(image):
    image = np.array(image, dtype='uint8')

    return cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
