# Overview

This project - currently in the "Holy crap! It actually (kinda) works!" phase - intends to help pinball players get better by detecting when you drain, then create a video clip 10 seconds befor and 3 seconds after that drain. The end result is you have videos that you can review for trends, etc.

# Giving credit...

This code is more or less a trimmed down version of the [Home Surveillance and Motion Detection post on PyImageSearch.com](https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/). Adrian has a ton of great info on his site, so visit it... and buy his book! :)

# Usage

I will warn you ahead of time that getting this setup is very fiddly at the moment. If time permits, I'll add the ability to visually specify the detection zone.

The detection zone setting is very important, as any inserts lighting on the playfield will be detected as "motion" by OpenCV. So, we can't just watch the whole playfield. We need to have the code zoom in on the area immediately above the drain. After all, this is all we ultimately care about, right?

In order to use this code, you need to do the following:

0. Clone this repo ;)
1. Have [Python](https://www.python.org/downloads/) installed
2. Run: `python pip install -r requirements.txt` to install any packages the code needs
3. Edit `conf.json` and set `"zoom: false`
3. Run: `python --conf conf.json --video /path/to/your/video`
5. This will play your video, which sets us up for determining the detection zone
6. By mousing over the video, you will see the (x,y) coordinates. Use this to determine the (x,y) coordinates that capture enough of the drain for us to detect the ball, but does not show the flippers.
7. Enter these coordinates in `conf.json`
8. Change `"zoom: false` back to `"zoom: true` in `conf.json`
9. `ctrl-c` in the terminal where you ran Step 5 to stop the processing
10. Re-run  `python --conf conf.json --video /path/to/your/video`. You will see just the rectangle you chose before. Repeat the steps above as needed to tweak the detection zone.
11. When you let the script run to completion, it will save the clips in the `./clips` directory

# Configuration

As mentioned above, there is a file named `conf.json` that controls how the script behaves. Here are some of the more interesting bits:

1. `scrollback_time` (int): The number of seconds before a drain to start the clip.
2. `x\_left`, `x\_right`, `y\_top`, 'y\_bottom` (int): Coordinates for the detection zone.
2. `zoom` (boolean): Whether to zoom in on the detection zone. You need to set this to `true` once you have your detection zone determined, else any change in the video (including any insert lighting up) will trigger a detection.
4. `min\_area`: The minimum area - in pixels - of movement required before determining the motion is worthwhile (e.g.: a 10x10 pixel object would need `min\_area` set to somewhere close to `100`). This helps prevent things like reflections of lights from falsely triggering detection.
4. `show\_video` (boolean): Whether to show the video while processing.

# Two Great Tastes...

If your target videos are on Twitch, I *highly* recommend using [`twitch-dl`](https://github.com/ihabunek/twitch-dl). Super easy - and performant - way to download any stream.
