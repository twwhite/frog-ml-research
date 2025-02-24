
from ffmpeg import FFmpeg
from pathlib import Path
import argparse
import sys
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='crop_to_specimen.py',
        description='Takes an input video and top-left/bottom-right coordinates and crops the video to the specified region'
    )

    parser.add_argument('filename')
    parser.add_argument('-t', '--x-top-left')      # option that takes a value
    parser.add_argument('-u', '--y-top-left')      # option that takes a value
    parser.add_argument('-v', '--x-bottom-right')      # option that takes a value
    parser.add_argument('-w', '--y-bottom-right')      # option that takes a value
    parser.add_argument('-n', '--nvidia-hardware-acceleration', action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.filename:
        filename = args.filename
        filename_stem = Path(filename).stem
        if not os.path.exists(filename):
            print(f"File {filename} does not exist")
            sys.exit(1)
        
    
    for arg in [args.x_top_left, args.y_top_left, args.x_bottom_right, args.y_bottom_right]:
        if arg and not arg.isdigit():
            print(f"Invalid value for {arg}")
            sys.exit(1)

    x_top_left = int(args.x_top_left)
    y_top_left = int(args.y_top_left)
    x_bottom_right = int(args.x_bottom_right)
    y_bottom_right = int(args.y_bottom_right)

    ffmpeg = (
        FFmpeg()
        .hwaccel('cuda') if args.nvidia_hardware_acceleration else FFmpeg()
        .input(filename)
        .output(
            f"{filename_stem}-crop.mp4",
            vf = f"crop={x_bottom_right - x_top_left}:{y_bottom_right - y_top_left}:{x_top_left}:{y_top_left}"
        )
    )

    ffmpeg.execute()
