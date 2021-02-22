import argparse
from pathlib import Path

"""
"/home/mbernardi/extra/async/ipcv/pdbr/labs/2/datasets/busStation/in000716.jpg"; (76, 61, 37, 117):-0.2346, (186, 11, 38, 118):-0.8941, (60, 21, 58, 161):-1.3409;
"""

def main(args):
    in_folder = Path(args.in_folder)
    out_filename = Path(args.out_filename)

    with open(out_filename, "w") as out_file:
        for filename in sorted(in_folder.iterdir()):
            if filename.suffix != ".txt":
                print("Ignored strange file named", filename)
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

                out_file.write(format_line(filename, detections))


def format_line(img_path, detections):
    """
    Format a line for the output idl file, from a list of detections and the
    name of the txt file.

    Each detection is a tuple of (x, y, w, h, score).

    Adds a endline at the end
    """

    line = f'"{img_path}";'
    for i, detection_tuple in enumerate(detections):
        x, y, w, h, score = detection_tuple
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
    parser.add_argument('out_filename', type=str,
            help='Output .idl filename')
    args = parser.parse_args()

    main(args)
