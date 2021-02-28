import argparse
from pathlib import Path
import PIL.Image
import math
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

                out_file.write(format_line(imgname, detections))

def convert_to_BBox(size, box):
    '''
    Info. of Yolo format: https://www.kaggle.com/pabloberhauser/creating-label-files-for-use-in-yolov4
    '''
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

def format_line(img_path, detections):
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
    for i, detection_tuple in enumerate(detections):
        x, y, w, h, score = detection_tuple
        x, y, w, h = convert_to_BBox((img_w,img_h),(x,y,w,h))
        if i > 0:
            line += ","
        line += f' ({x}, {y}, {w}, {h}):{score}'

    if detections:
        line += ";"

    return line + "\n"

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
