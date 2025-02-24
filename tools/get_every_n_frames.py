import cv2
from pathlib import Path
import argparse
import sys
import os


if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        prog='get_every_n_frames.py',
        description='Takes an input video and extracts every n frames, saves to specified output directory.'
    )

    parser.add_argument('filename')
    parser.add_argument('-n', '--n_frames')      # option that takes a value
    parser.add_argument('-o', '--output-dir')      # option that takes a value
    parser.add_argument('-t', '--target-num-frames', help="Target number of frames in output video. If specified, n_frames will be calculated as length//target_num_frames")

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

    if args.output_dir:
        output_dir = args.output_dir
        if not os.path.exists(output_dir):
            print(f"Directory {output_dir} does not exist")
            sys.exit(1)

    if args.n_frames and not args.n_frames.isdigit():
        print(f"Invalid value for {args.n_frames}")
        sys.exit(1)

    if args.n_frames:
        n_frames = int(args.n_frames)

    if args.n_frames and args.target_num_frames:
        print("Cannot use both n_frames and target_num_frames at the same time")
        sys.exit(1)
    
    if args.target_num_frames and not args.target_num_frames.isdigit():
        print(f"Invalid value for {args.target_num_frames}")
        sys.exit(1)

    if args.target_num_frames:
        target_num_frames = int(args.target_num_frames)

    cap = cv2.VideoCapture(filename)
    count = 0

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if target_num_frames > 0:
        n_frames = length//target_num_frames

    print(f"Num frames in video: {length}")
    print(f"Extracting every {n_frames} frames")
    print(f"Output directory: {output_dir}")
    print(f"Total output frames: {length//n_frames}")
    input('Press Enter to begin extraction...')
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(f"{output_dir}/{filename_stem}_{count}.jpg", frame)
            count += n_frames
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            print(f"Progress: {count}/{length}  {round((count/length)*100) }%                ", end="\r")

        else:
            cap.release()
            break
