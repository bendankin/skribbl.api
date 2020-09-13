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
        #   - maybe add 1 to sobel x
        # self.sobel_angles = np.arctan(self.sobely/self.sobelx)
        self.sobel_angles = np.arctan(sobely_x64f/sobelx_x64f)

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
    def checkMove(self,coord,length,min):
        perim = {()}
        # might add checkCoord here
        if not self.inMat(coord,self.sobel_angles.shape):
            raise Exception
        else:
            #angle = self.sobel_angles[coord[0]][coord[1]] + np.pi/2
            newCoord = self.findPerimMaxCoord(coord)
            # if new coord isnt within threshold, return previous coord
            if (self.sobelz[newCoord[0]][newCoord[1]] < min):
                return coord
            else:
                return newCoord   
    
    def findPerimMaxCoord(self,coord):
        maxPerimCoord = coord
        maxVal = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if (i != 0 or j != 0):
                    val = self.sobelz[coord[0]+i][coord[1]+j]
                    if maxVal <= val:
                        maxVal = val
                        maxPerimCoord = (coord[0]+i,coord[1]+j)

        return maxPerimCoord

    def checkAngle(self,direction):
        #   Diagram of pixels
        #   3 2 1
        #   4 # 0
        #   5 6 7
        if (5.891 < direction) and (direction <= .393):
            return 0
        elif (0.393 < direction) and (direction <= 1.178):
            return 1
        elif (1.178 < direction) and (direction <= 1.964):
            return 2
        elif (1.964 < direction) and (direction <= 2.749):
            return 3
        elif (2.749 < direction) and (direction <= 3.535):
            return 4
        elif (3.535 < direction) and (direction <= 4.320):
            return 5
        elif (4.320 < direction) and (direction <= 5.105):
            return 6
        else:
            return 7

    # Create a list of coordinate pairs for the skribbl api to draw
    def generateVerticies(self):
        self.test = np.zeros(self.sobelz.shape)
        lst = []
        start = self.findStart()
        cfrom = start
        LENGTH = 4
        MIN = 136

        x = 0
        cfromPending = cfrom
        while True:
            self.test[cfrom[0]][cfrom[1]] = 155
            self.sobelz[cfrom[0]][cfrom[1]] = 0
            cto = self.checkMove(cfrom,LENGTH,MIN)

            print((cfrom,cto), x)
            # time.sleep(1)
            if cto == cfrom:
                return lst 
            if x == LENGTH:
                lst.append((cfromPending,cto))
                cfromPending = cto
                x = 0

            cfrom = cto
            x = x + 1
       
        # while True:
        #     self.test[cfrom[0]][cfrom[1]] = 255
        #     cto = self.checkMove(cfrom,LENGTH,MIN)
        #     print((cfrom,cto))
        #     # time.sleep(1)
        #     lst.append((cfrom,cto))
        #     cfrom = cto
        #     if cto == start:
        #         return lst  

"""
fmt=Formatter('resources/circle1.jpg')
fmt.calcSobel()
# start = fmt.findStart()
# print(start)
# fmt.imshow(fmt.sobelx)
# fmt.imshow(fmt.sobely)
# fmt.imshow(fmt.sobelz, False)
# fmt.imshow(fmt.sobel_angles)

lst = fmt.generateVerticies()
fmt.imshow(fmt.test)
#fmt.imshow(fmt.sobel_angles)
print(lst)

            

# fmt2=Formatter('resources/image.jpeg')
# fmt2.calcSobel()
# fmt2.imshow(fmt2.sobelz)
# fmt2.imshow(fmt2.sobel_angles)
# print(fmt2.im[39][312][:])
# fmt2.imshow(fmt2.im)

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

"""