data_1_1 = '''
import cv2 as cv

img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\clg.jpg')

cv.imshow('SKK',img)
cv.waitKey(0)
'''
data_1_2 = '''
import cv2 as cv
import numpy as np
capture = cv.VideoCapture('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\vid.mp4')
while(True):
    rec, frame = capture.read()
    if rec:    
        cv.imshow('output', frame)
        if cv.waitKey(10) & 0xFF==ord('d'):
            break            
    else:
        break
capture.release()
cv.destroyAllWindows()
'''
data_2_1 = '''
import cv2 as cv

create = int(input("Create your Password:"))
pwd = int(input("Password:"))

if pwd == create:
    img = cv.imread('c:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_2\\Input\\clg.jpg')
else:
    print("Passcode is incorrect")
    exit()

cv.imshow('Kkw',img)

cv.waitKey(0)
'''
data_2_2 = '''
import cv2 as cv
import numpy as np

capture = cv.VideoCapture('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_2\\Input\\video.gif')
pause_frame = int(input("Enter Number of Frame: "))
frame_count =0
while frame_count < pause_frame:
    rec, frame = capture.read()
    cv.imshow('output', frame)
    cv.waitKey(20)
    frame_count +=1
    capture.set(1, pause_frame)
    while True:
        ch = 0xFF & cv.waitKey(1)
        if ch == 27:
            break
    
capture.release()
cv.destroyAllWindows()
'''
data_3_1 = '''
import cv2 as cv
import numpy as np

img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_3\\Input\\clg.jpg')
cv.imshow('Kkw',img)
#Translation
def translate(img,x,y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimension = (img.shape[1],img.shape[0])
    return cv.warpAffine(img,transMat,dimension)
translate = translate(img, -50,50)
cv.imshow('Translated',translate)

#Rotation
def rotate(img,angle, rptPoint=None):
    (height,width) = img.shape[:2]
    if rptPoint is None:
        rptPoint = (width//2,height//2)
    rotMat = cv.getRotationMatrix2D(rptPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, -45)
cv.imshow('Rotated', rotated)

rotated_rotated = rotate(img, -90)
cv.imshow('Rotated Rotated', rotated_rotated)
 

cv.waitKey(0)
'''
data_3_2 = '''
import cv2 as cv
import numpy as np

img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_3\\Input\\clg.jpg')
cv.imshow('Kkw',img)
rows,cols,ch = img.shape
# define four points on input image
pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
# define the corresponding four points on output image
pts2 = np.float32([[100,50],[300,0],[0,300],[300,300]])
M = cv.getPerspectiveTransform(pts1,pts2)
dst = cv.warpPerspective(img,M,(cols, rows))
cv.imshow('Transformed Image', dst)
cv.waitKey(0)
'''
data_4_1 = '''
import cv2 as cv
import numpy as np
#reading a image from computer and taking dimensions
img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_4\\Input\\paris.jfif')
rows, cols = img.shape[:2]

#gaussian Blur 
output_gaus = cv.GaussianBlur(img, (5,5), 0)

#median Bur (reduction of noise)
output_med = cv.medianBlur(img, 5)

#Bilateral filtering (Reduction of noise + Preserving of edges)
output_bil = cv.bilateralFilter(img, 5, 6, 6)
cv.imshow('Gaussian', output_gaus)
cv.imshow('Bilateral', output_bil)
cv.imshow('Median Blur', output_med)
cv.imshow('Original', img)
cv.waitKey(0)
'''
data_4_2 = '''
import cv2 as cv
import numpy as np
#Reading the image
img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_4\\Input\\paris.jfif')

#Gauusian kernel for sharpening
gaussian_blur = cv.GaussianBlur(img, (7,7), 2)

#Sharpening using addweighted()
sharpened1 = cv.addWeighted(img,1.5, gaussian_blur, -0.5, 0)
sharpened2 = cv.addWeighted(img,3.5, gaussian_blur, -2.5, 0)
sharpened3 = cv.addWeighted(img,7.5, gaussian_blur, -6.5, 0)

#Showing the sharpened Images
cv.imshow('Sharpened 3', sharpened3)
cv.imshow('Sharpened 2', sharpened2)
cv.imshow('Sharpened 1', sharpened1)
cv.imshow('original', img)
cv.waitKey(0)
'''
data_4_3 = '''
import cv2 as cv
import os
img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_4\\Input\\paris.jfif')
cv.imwrite('lossless_compressed_image.png', img)
# A value between 0 and 100 (higher means better quality, but larger file size)
jpeg_quality = 90  
cv.imwrite('lossy_compressed_image.jpg', img, [cv.IMWRITE_JPEG_QUALITY, jpeg_quality])

original_size = os.path.getsize('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_4\\Input\\paris.jfif')
lossless_size = os.path.getsize('lossless_compressed_image.png')
lossy_size = os.path.getsize('lossy_compressed_image.jpg')

print(f'Original image size: {original_size} bytes')
print(f'Lossless compressed image size: {lossless_size} bytes')
print(f'Lossy compressed image size: {lossy_size} bytes')

lossless_img = cv.imread('lossless_compressed_image.png')
lossy_img = cv.imread('lossy_compressed_image.jpg')

cv.imshow('Original Image', img)
cv.imshow('Lossless Compressed Image', lossless_img)
cv.imshow('Lossy Compressed Image', lossy_img)
cv.waitKey(0)
cv.destroyAllWindows()
'''
data_5_1 = '''
import cv2 as cv
import numpy as np

img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_5\\Input\\og.jpg')
cv.imshow('Park', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

# Laplacian
lap = cv.Laplacian(gray, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow('Laplacian', lap)

# Sobel 
sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0)
sobely = cv.Sobel(gray, cv.CV_64F, 0, 1)
combined_sobel = cv.bitwise_or(sobelx, sobely)

cv.imshow('Sobel X', sobelx)
cv.imshow('Sobel Y', sobely)
cv.imshow('Combined Sobel', combined_sobel)

# Canny Algorithm / Canny Edge Detector
canny = cv.Canny(gray, 150, 175)
cv.imshow('Canny', canny)
cv.waitKey(0)
'''
data_6_1 = '''
import cv2 as cv
import numpy as np

# Load image
img = cv.imread('C:\\Users\\DELL\\OneDrive\\Desktop\\MVS_34\\Practical_6\\Input\\shapes.jpg')
imgGrey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Thresholding
_, thrash = cv.threshold(imgGrey, 240, 255, cv.THRESH_BINARY)

# Find contours
contours, _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

# Show original image
cv.imshow("img", img)

for contour in contours:
    approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
    cv.drawContours(img, [approx], 0, (0, 0, 0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5
    
    # Identify shape
    if len(approx) == 3:
        cv.putText(img, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 4:
        x1, y1, w, h = cv.boundingRect(approx)
        aspectRatio = float(w) / h
        print(aspectRatio)
        if 0.95 <= aspectRatio <= 1.05:
            cv.putText(img, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        else:
            cv.putText(img, "Rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 5:
        cv.putText(img, "Pentagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) == 10:
        cv.putText(img, "Star", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    else:
        cv.putText(img, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

# Display the final image with shapes identified
cv.imshow("shapes", img)
cv.waitKey(0)
cv.destroyAllWindows()
'''
data_6_2 = '''
import cv2 as cv
import numpy as np

# Read the image
image = cv.imread('C:\\Users\\ROBOTICS&AUTOMATION\\Desktop\\MVS_34\\Photos\\6.2.jpg')

# Convert the image to HSV color space
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

# Define color ranges for the colors you want to identify (e.g., blue)
lower_blue = np.array([90, 50, 50])  # Lower HSV value for blue
upper_blue = np.array([130, 255, 255])  # Upper HSV value for blue

# Create a mask to isolate the desired color
mask = cv.inRange(hsv, lower_blue, upper_blue)

# Find contours in the mask
contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Iterate through the detected contours and identify color
for contour in contours:
    area = cv.contourArea(contour)
    if area > 100:  # Filter out small contours
        # Draw the contour on the original image
        cv.drawContours(image, [contour], -1, (0, 255, 0), 2)
        
        # Get the centroid of the contour
        M = cv.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])         
            
            # Identify and label the color
            color = "Blue"  # You can add more color ranges and labels as needed
            cv.putText(image, color, (cx - 20, cy - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the result
cv.imshow('Color Identification', image)
cv.waitKey(0)
cv.destroyAllWindows()
'''

def get(code):
    if code == "img processing":
        return data_1_1
    elif code == "video processing":
        return data_1_2
    elif code == "frames":
        return data_2_1
    elif code == "password encrypted":
        return data_2_2
    elif code == "translation rotation":
        return data_3_1
    elif code == "transformed":
        return data_3_2
    elif code == "blurring":
        return data_4_1
    elif code == "sharpening":
        return data_4_2
    elif code == "compression":
        return data_4_3
    elif code == "canny":
        return data_5_1
    elif code == "edge":
        return data_6_1
    elif code == "color":
        return data_6_2
    else:
        return 'Enter from: [img processing\nvideo processing\nframes\npassword encrypted\ntranslation rotation\ntransformed\nblurring\nsharpening\ncompression\ncanny\nedge\ncolor]'