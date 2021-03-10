import argparse
from pathlib import Path
import PIL.Image
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2

"""
"/home/mbernardi/extra/async/ipcv/pdbr/labs/2/datasets/busStation/in000716.jpg"; (76, 61, 37, 117):-0.2346, (186, 11, 38, 118):-0.8941, (60, 21, 58, 161):-1.3409;
"""

'''
We have to add the path of dataset images
'''

def main(args):
    in_folder = Path(args.in_folder)
    ds_folder = Path(args.ds_folder)
    out_filename = Path(args.out_filename)

    print("Saving in", out_filename)
    ignores = {"Head": 0, "Extinguisher": 0}

    with open(out_filename, "w") as out_file:
        for filename,imgname in zip(sorted(in_folder.iterdir()),sorted(ds_folder.glob('*.jpg'))):
            if filename.suffix != ".txt":
                print("Ignored strange file named", filename)
                continue
            if imgname.suffix != '.jpg':
                print("Ignored strange file named", imgname)
                continue
            with open(filename) as in_file:
                detections = []
                for line in in_file:
                    # First strip() to remove endlines
                    cls, x, y, w, h, score = line.strip().split(" ")
                    if cls == "0":
                        detections.append((x, y, w, h, score))
                    else:
                        print("Seen an object of class", cls)

                line, ignores = format_line(imgname, detections, ignores)
                out_file.write(line)

    print(ignores)

def ignore_detection(x, y, w, h):
    """
    Returns true if the detection should be ignored

    Example of fire extinguisher: (671, 352, 20, 45):0.561148,
    """
    # Extinguisher coordinates
    ext_x = 671
    ext_y = 352
    ext_w = 20
    ext_h = 45

    # Threshold of similar coordinates to consider
    ext_th = 5 # allow +/- 5 pixels

    if abs(x - ext_x) < ext_th \
            and abs(y - ext_y) < ext_th \
            and abs(w - ext_w) < ext_th \
            and abs(h - ext_h) < ext_th:
        return True, "Extinguisher"

    # Ignore squares (heads)
    ratio = w / h

    # if ratio > 0.9 and ratio < 1.1 and w < 30:
        # return True, "Head"

    return False, None

def convert_to_BBox(size, box):
    '''
    Info. of Yolo format: https://www.kaggle.com/pabloberhauser/creating-label-files-for-use-in-yolov4
    
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = float(box[0])
    y = float(box[1])
    w = float(box[2])
    h = float(box[3])
    x = (x / dw) * 2.0
    w = w / dw
    y = (y / dh) * 2.0
    h = h / dh
    BB_1 = int(math.floor((w + x) / 2.0))
    BB_0 = int(math.floor(BB_1 - w))
    BB_3 = int(math.floor((h + y) / 2.0))
    BB_2 = int(math.floor(BB_3 - h))
    return [BB_0, BB_2, BB_1, BB_3]
    '''
    # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
    # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
    dw = size[0]
    dh = size[1]
    x = float(box[0])
    y = float(box[1])
    w = float(box[2])
    h = float(box[3])
    l = int((x - w / 2) * dw) #Most Left point
    r = int((x + w / 2) * dw) #Most right point
    t = int((y - h / 2) * dh) #Most top point
    b = int((y + h / 2) * dh) #Most bottom point
    
    if l < 0:
        l = 0
    if r > dw - 1:
        r = dw - 1
    if t < 0:
        t = 0
    if b > dh - 1:
        b = dh - 1

    return l,t,r-l,b-t

def format_line(img_path, detections, ignores):
    """
    Format a line for the output idl file, from a list of detections and the
    name of the txt file.

    Each detection is a tuple of (x, y, w, h, score).

    Adds an endline at the end
    """

    line = f'"{img_path}";'
    # Load image size to extract Bounding Box information
    image = PIL.Image.open(img_path)
    img_w, img_h = image.size
    detected_person = False
    for i, detection_tuple in enumerate(detections):
        x, y, w, h, score = detection_tuple
        x, y, w, h = convert_to_BBox((img_w,img_h),(x,y,w,h))

        ignore, reason = ignore_detection(x, y, w, h)
        if ignore:
            ignores[reason] += 1
            continue
        '''
        # Create figure and axes
        fig, ax = plt.subplots()

        # Display the image
        ax.imshow(image)

        # Create a Rectangle patch
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
        print(img_path)
        print(x,y,w,h)
        # Add the patch to the Axes
        ax.add_patch(rect)
        plt.show()
        '''
        if i > 0:
            line += ","
        line += f' ({x}, {y}, {w}, {h}):{score}'
        detected_person = True

    if detected_person:
        line += ";"

    return line + "\n", ignores

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_folder', type=str,
            help='Input folder with "inXXXXX.txt" files')
    parser.add_argument('ds_folder', type=str,
            help='Input folder with "inXXXXX..jpg" files')
    parser.add_argument('out_filename', type=str,
            help='Output .idl filename')
    args = parser.parse_args()

    main(args)
