import datetime as dt
import os
from picamera import PiCamera

# GLOBAL VARS
VIDEO_W = 1280 # vid width
VIDEO_H = 720 # vid height
VIDEO_LEN = 20 # vid length in seconds
VIDEO_FPS = 15 # vid fps
REC_BASE_DIR = "/home/pi/recordings/"

def createFilenames():
    '''
        returns filenames for video file and respective log file
    '''
    now = dt.datetime.now()
    date = "%0.4d-%0.2d-%0.2d" % (now.year, now.month, now.day)
    time = "%0.2dh-%0.2dm-%0.2ds" % (now.hour, now.minute, now.second)

    if not os.path.exists(REC_BASE_DIR + date):
        os.makedirs(REC_BASE_DIR + date)
    vid_filename = REC_BASE_DIR + date + "/VID_" + time + ".h264"
    log_filename = REC_BASE_DIR + date + "/VID_" + time + ".log"

    return vid_filename, log_filename

def convertToMP4(filename):
    '''
        FFMPEG convert to mp4
    '''
    mp4_filename = os.path.splitext(filename)[0] + ".mp4" # remove original extension and add ".mp4"
    os.system("ffmpeg -i {} -c copy -r {} {}".format(filename, VIDEO_FPS, mp4_filename)) # run
    os.remove(filename) # remove old file


def main():
    camera = PiCamera()
    camera.resolution = (VIDEO_W, VIDEO_H)
    camera.framerate = VIDEO_FPS
    camera.annotate_background = True
    camera.annotate_text_size = 24

    try:
        while True:
            rec_start = dt.datetime.now()
            vid_file, log_file = createFilenames()

            print("started recording " + vid_file)
            camera.start_recording(vid_file)
            while (dt.datetime.now() - rec_start).seconds < VIDEO_LEN:

                # TODO: GRAB OBDII DATA HERE
                speed = 000
                throttle_pct = 00
                brake_pct = 00

                # data overlay
                text = "speed: {}kph | throttle: {}% | brake: {}%".format(speed, throttle_pct, brake_pct)
                camera.annotate_text = text
            
            print("stopped recording " + vid_file)
            camera.stop_recording()
            print("converting to mp4...")
            convertToMP4(vid_file)
            print("finished converting to mp4")

    except (KeyboardInterrupt, SystemExit):
        print("\nDone.\nExiting.")

if __name__ == "__main__":
    main()