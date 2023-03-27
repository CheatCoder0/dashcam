import datetime as dt
import os
import logging
import threading
from picamera import PiCamera

# GLOBAL VARS
VIDEO_W = 1280 # vid width
VIDEO_H = 720 # vid height
VIDEO_LEN = 20 # vid length in seconds
VIDEO_FPS = 15 # vid fps
REC_BASE_DIR = "/home/pi/recordings/"
ANNOTATE_TXT_SIZE = 24

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

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

def convertToMP4(thread_num, filename):
    '''
        FFMPEG convert to mp4
    '''
    mp4_filename = os.path.splitext(filename)[0] + ".mp4" # remove original extension and add ".mp4"
    logging.info("FFMPEG{} : converting {} to mp4...".format(thread_num, filename))
    os.system("ffmpeg -i {} -c copy -r {} {}".format(filename, VIDEO_FPS, mp4_filename)) # run
    os.remove(filename) # remove old file
    logging.info("FFMPEG{} : done.".format(thread_num))


def main():
    camera = PiCamera()
    camera.resolution = (VIDEO_W, VIDEO_H)
    camera.framerate = VIDEO_FPS
    camera.annotate_background = True
    camera.annotate_text_size = ANNOTATE_TXT_SIZE

    logging.info("Main    : program start!")

    try:
        while True:
            rec_start = dt.datetime.now()
            vid_file, log_file = createFilenames()

            camera.start_recording(vid_file)
            logging.info("Main    : started recording " + vid_file)
            while (dt.datetime.now() - rec_start).seconds < VIDEO_LEN:

                # TODO: GRAB OBDII DATA HERE
                speed = 000
                throttle_pct = 000
                brake_pct = 000

                # data overlay
                text = "speed: {}kph | throttle: {}% | brake: {}%".format(speed, throttle_pct, brake_pct)
                camera.annotate_text = text
            
            camera.stop_recording()
            logging.info("Main    : stopped recording " + vid_file)
            ffmpeg_thread = threading.Thread(target=convertToMP4, args=(threading.activeCount(), vid_file))
            ffmpeg_thread.start()
            #convertToMP4(vid_file)
            #ffmpeg_thread.join()

    except (KeyboardInterrupt, SystemExit):
        print("\nDone.\nExiting.")

if __name__ == "__main__":
    main()