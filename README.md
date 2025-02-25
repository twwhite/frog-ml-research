![screenshot](https://raw.githubusercontent.com/twwhite/frog-ml-research/refs/heads/main/img/screenshot.png)

Tools used:
- label-studio
- YOLO
- FFMPEG

2025-02-23
What's working:
- The output of the YOLOv10n model trained on 1000 pre-labeled images is working *GREAT*!
- Todo: IR night-mode, multi-frog, batch pipeline
- Work on appropriate frame rates to speed up predictions

Project Structure:
- img/ : Supporting images for documentation
- models/ : Output models from training
- pipeline/ : Sequential steps for raw, grouped input video to processed, individual videos
- tools/ : Command line utils for working with bulk videos
- yolo/ : Working directory for training including dataset images/videos (.gitignored)