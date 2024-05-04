import cv2
import numpy as np
import sys,os



def crop_image(img_path, output_path):
    print("Your Image Is Under Crop Module...")
    img_name = str(img_path)
    img_name = img_name.split('_')[1].split('.')[0]
    print(f'Saving Croped Image as cropped_image_{img_name}.jpg')
    img = cv2.imread(img_path)
    width, height = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 245, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    eroded = cv2.erode(thresh, kernel, iterations=1)
    eroded_c = cv2.bitwise_not(eroded)
    contours, _ = cv2.findContours(eroded_c,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    suitable_contours = list()
    img_area = width * height
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > 0.2 * img_area:
            suitable_contours.append(contour)
    
    bounding_boxes = [cv2.boundingRect(contour) for contour in suitable_contours]
    for i, bbox in enumerate(bounding_boxes):
        x, y, w, h = bbox
        if w>130 and h>130:
            cropped_img = img[y:y+h, x:x+w]
            
            cv2.imwrite(f"{output_path}/cropped_image_{img_name}_{i}.png", cropped_img)








if __name__ == '__main__':
    try:
        input_image_path = sys.argv[1]
        print(input_image_path)
    except:
        print("Please Run this Script like 'python your_file.py your_input_image_path your_output_directory_name'")
    
    try:
        output_directory = sys.argv[2]
    except:
        print("Please Run this Script like 'python your_file.py your_input_image_path your_output_directory_name'")
    os.makedirs(output_directory, exist_ok=True)
    crop_image(input_image_path,output_directory)