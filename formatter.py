import numpy as np 
from cv2 import cv2 as cv
from matplotlib import pyplot as plt
import time

# SOBEL_K=3

# c = cv.imread("resources/circle1.jpg")


# c_gray=cv.cvtColor(c,cv.COLOR_BGR2GRAY)
# c_blur=cv.GaussianBlur(c_gray,(9,9),0)

# c_sobelx_x64f = cv.Sobel(c_blur,cv.CV_64F,1,0,ksize=SOBEL_K)
# abs_c_sobelx_x64f = np.absolute(c_sobelx_x64f)
# c_sobelx = np.uint8(abs_c_sobelx_x64f)

# c_sobely_x64f=cv.Sobel(c_blur,cv.CV_64F,0,1,ksize=SOBEL_K)
# abs_c_sobely_x64f = np.absolute(c_sobely_x64f)
# c_sobely = np.uint8(abs_c_sobely_x64f)

# c_sobelz_float = np.sqrt(c_sobelx_x64f**2 + c_sobely_x64f**2)
# c_sobelz = c_sobelz_float.astype(int)

# max_elem_indices = np.where(c_sobelz == np.amax(c_sobelz))
# coord = list(zip(max_elem_indices[0],max_elem_indices[1]))

# for x in coord:
#     print(x)

# c_angle = np.arctan(c_sobely/c_sobelx)
# # cv.imshow("Blur",c_blur)
# # cv.imshow("Gray",c_gray)

# cv.imshow("X",c_sobelx)
# cv.imshow("Y",c_sobely)

class Formatter:

    # do io excpetion handling
    def __init__(self,image):
        self.im = cv.imread(image)

    # maybe prompt for parameters
    def configSobel(self):
        while True:
            blur = int(input("Enter a value for blur dimensions: "))
            if blur <= 0 or blur % 2 == 0:
                print("Please enter odd numbers greater than 1 for blur kernal size.")
            else:
                self.BLUR_RADIUS = blur
                break
        while True:
            sobel = int(input("Enter a value for Sobel kernal size: "))
            if sobel <= 0 or sobel % 2 == 0:
                print("Please enter odd numbers greater than 1 for Sobel kernal size.")
            else:
                self.K_SIZE = sobel
                break
    
    def imshow(self,im,gray=True):
        if gray:
            plt.imshow(im,cmap='gray')
        else:
            plt.imshow(im)
        plt.show()

    def calcSobel(self):
        self.configSobel()
        gray=cv.cvtColor(self.im,cv.COLOR_BGR2GRAY)
        blur=cv.GaussianBlur(gray,(self.BLUR_RADIUS,self.BLUR_RADIUS),0)

        sobelx_x64f = cv.Sobel(blur,cv.CV_64F,1,0,ksize=self.K_SIZE)
        abs_sobelx_x64f = np.absolute(sobelx_x64f)
        self.sobelx = np.uint8(abs_sobelx_x64f) # may not need

        sobely_x64f=cv.Sobel(blur,cv.CV_64F,0,1,ksize=self.K_SIZE)
        abs_sobely_x64f = np.absolute(sobely_x64f)
        self.sobely = np.uint8(abs_sobely_x64f) # may not need

        sobelz_float = np.sqrt(sobelx_x64f**2 + sobely_x64f**2)
        self.sobelz = sobelz_float.astype(int)

        # catch exceptions with dividing by zero
        self.sobel_angles = np.arctan(self.sobely/self.sobelx)

    def findStart(self):
        max_elem_indices = np.where(self.sobelz == np.amax(self.sobelz))
        coords = list(zip(max_elem_indices[0],max_elem_indices[1]))
        return coords[0]

    def inMat(self,coord,shape):
        if coord[0] < 0 or coord[0] >= shape[0] or coord[1] < 0 or coord[1] >= shape[1]:
            return False
        return True

    # - return coordinates
    # - threshholding may remove the need for min and max
    def checkMove(self,mat,angle,coord,length,min):
        # might add checkCoord here
        new_coord = (coord[0] + int(length*np.sin(angle)), coord[1] + int(length*np.cos(angle)))
        # if not self.inMat(new_coord,mat.shape):
        #     if length > 1:
        #         return self.checkMove(mat,angle,coord,length-1,min)
        #     else:
        #         # implement something to check whether or not it should add or subtract
        #         return self.checkMove(mat,angle+0.196,coord,length,min)
        new_val = mat[new_coord[0]][new_coord[1]]
        # make sure it doesn't go back in the same direction

        # if new_val < min:
        #     self.checkMove(mat,angle+0.196,coord,length,min)

        return new_coord

    # Create a list of coordinate pairs for the skribbl api to draw
    # 
    def generateVertices(self):
        lst = []
        start = self.findStart()
        cfrom = start
        LENGTH = 4
        MIN = 150
        while True:
            cto = self.checkMove(self.sobelz,self.sobel_angles[cfrom[0]][cfrom[1]]+np.pi/2,cfrom,LENGTH,MIN)
            print((cfrom,cto))
            time.sleep(1)
            lst.append((cfrom,cto))
            cfrom = cto
            if cto == start:
                return lst
    
fmt=Formatter('resources/circle1.jpg')
fmt.calcSobel()
start = fmt.findStart()
# print(start)
# fmt.imshow(fmt.sobelz)
lst = fmt.generateVertices()
print(lst)

# phase_shift = np.ones(c.shape) * np.pi/2
# print(phase_shift)
# plt.imshow(c_angle,cmap='gray')
# plt.show()

############### this phase shifting works
# plt.imshow(np.add(c_angle, np.pi/2),cmap='gray')
# plt.show() 


# plt.subplot(1,3,3),plt.imshow(c_sobelz,cmap = 'gray')
# plt.title('Sobel abs(CV_64F)'), plt.xticks([]), plt.yticks([])
# plt.show()

# cv.imshow("Z",c_sobelz)

# im = cv.imread("resources/image.jpeg")
# im_gray=cv.cvtColor(im,cv.COLOR_BGR2GRAY)
# im_blur=cv.GaussianBlur(im_gray,(17,17),0)
# im_sobelx=cv.Sobel(im_blur,cv.CV_64F,1,0,ksize=3)
# im_sobely=cv.Sobel(im_blur,cv.CV_64F,0,1,ksize=3)
# cv.imshow("X",im_sobelx)
# cv.imshow("Y",im_sobely)

cv.waitKey(0)
cv.destroyAllWindows()

