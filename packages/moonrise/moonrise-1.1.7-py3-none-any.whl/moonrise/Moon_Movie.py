import threading
import time
from datetime import datetime
import os
import ffmpeg
from colorama import Fore, Style, init
init(convert=True)

class VideoThread(threading.Thread):
    """Creates a new thread that handles the creation of video recordings for browser sessions.
    """
    def __init__(self, driver, shutter_speed):
        """Receives a webdriver to create an additional thread where screenshots are taken during test execution.
           These screenshots are converted to an mp4 file when the webdriver is killed or after the moonrise test execution has completed.
        """
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.driver = driver
        self.video_folder = None
        self.shutter_speed = shutter_speed
        self.start()

    def run(self):
        while not self.stop_event.is_set():
            try:
                timestamp = str(datetime.now()).replace(" ", "_").replace(":", "_")
                self.driver.save_screenshot(f"{self.video_folder}/{timestamp}.png")
                time.sleep(self.shutter_speed)
            except Exception:
                self.stop()

    def stop(self):
        self.stop_event.set()

    def create_video_from_pngs(self, output_file):

        # Get a list of PNG files in the folder
        png_files = [file for file in os.listdir(self.video_folder) if file.endswith('.png')]

        # Sort the files in ascending order based on their names
        png_files.sort()

        # Set up the FFmpeg input file list
        input_file_list = os.path.join(self.video_folder, 'input.txt')
        with open(input_file_list, 'w') as f:
            for i, png_file in enumerate(png_files):
                file_path = os.path.join(self.video_folder, png_file)
                f.write(f"file '{file_path}'\nduration 0.1\n")

        print(f"\n{Fore.YELLOW}{datetime.now()} | {f"Creating video file, reports{str(output_file).split("reports")[1]}..."}{Style.RESET_ALL}")
        
        ffmpeg.input(input_file_list, format='concat', safe=0, loglevel='quiet').output(
            output_file,
            r=10,  # Set framerate to 10 frames per second (adjust as needed)
            start_number=0  # Set the start number of the input files
        ).overwrite_output().run()

        print(f"\n{Fore.YELLOW}{datetime.now()} | {f"Video file, reports{str(output_file).split("reports")[1]} created"}{Style.RESET_ALL}")
