'''
A little framework to make
kernel testing simple.

Comman line:
    python filter_framework.py <path_to_image>

Usage:
    Write square matrix of numbers.
    Press 'Apply'. That's it! 
    It's possible to apply normalization 
    for an inputed matrix, so that 
    sum of all the values in that matrix
    will be equal to 1.
    ! Matrix must have odd size. 
'''

import cv2
import imutils
import numpy as np
from tkinter import Tk, Text, Button, END,  Checkbutton, IntVar
import argparse


class FilterFramework:
    '''
    With use of this class (framework)
    it's convinient to test different
    kinds of kernels.
    '''
    # TODO: provide ability to save and load kernels

    def __init__(self, image):
        # we same initial image
        # so we can reapply new filters
        self.__initial_image = image
        self.image = image

        # GUI section
        self.gui_root = Tk()

        # here user type the kernel
        self.text_area = Text(self.gui_root)
        self.text_area.pack()

        self.apply_button = Button(self.gui_root, text='Apply',
                                   command=self.__apply_filter)
        self.apply_button.pack()

        # if flag is on then we
        # try to normalize the
        # image so that sum of
        # numbers in array is equal to 1
        self.flag_normalize = IntVar()
        self.button_normalize = Checkbutton(
            self.gui_root, text='Normalize', variable=self.flag_normalize)
        self.button_normalize.pack()

    def __apply_filter(self):
        def parse_kernel(text_to_parse: str):
            '''
            @param text_to_parse: text from text area representing a kernel
            @retval: (bool, kernel) - bool is True is parsing succeed, else False. 
                kernal is np.array having the same odd number of rows and columns
            '''

            # parse string into 2d array
            lines = [line for line in text_to_parse.split('\n') if line]
            numbers = []
            for line in lines:
                row_of_numbers = [int(x) for x in line.split(' ') if x != '']
                numbers.append(row_of_numbers)
            numbers = np.array(numbers)

            # invariant
            if len(numbers) == 0 or len(numbers) != len(numbers[0]) or len(numbers) % 2 == 0:
                return False, None

            # trial to normalize the array
            if self.flag_normalize.get():
                try:
                    numbers = numbers / np.sum(numbers)
                except ZeroDivisionError:
                    print('[INFO] Cannot normalize. Division by zero!')

            return True, numbers

        text_from_input = self.text_area.get('1.0', END)
        ret, kernel = parse_kernel(text_from_input)
        if ret is False:
            print('[INFO] Cannot parse kernel')
            return
        self.image = cv2.filter2D(
            self.__initial_image, -1, kernel).astype('uint8')

    def update(self):
        '''
        One iteration of the main_loop
        '''
        cv2.imshow('Image', self.image)
        self.gui_root.update()

    def main_loop(self):
        '''
        Updating Tk and cv2 gui
        '''
        while True:
            cv2.imshow('Image', self.image)
            self.gui_root.update()
            if cv2.waitKey(20) == ord('q'):
                break
        self.gui_root.destroy()


if __name__ == "__main__":
    # get path to image
    # from arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', dest='path_to_image',
                        help='path to image to apply filtering on')
    args = parser.parse_args()
    path_to_image = args.path_to_image
    if path_to_image is None:
        print('[INFO] Path to image is missed. Using default...')
        path_to_image = 'img/japan_sun.jpg'

    # load image and check
    # if it's loaded correctly
    image = cv2.imread(path_to_image)
    if image is None:
        print('[INFO] Invalid path.')
        exit(-1)

    # Convert to gray and resize
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = imutils.resize(image, width=600)

    # Run the framework
    ff = FilterFramework(image)
    ff.main_loop()
