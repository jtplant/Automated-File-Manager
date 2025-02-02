import logging
import sys
import time

from os import scandir, rename, makedirs
from os.path import splitext, exists, join

from shutil import move

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler\

source_dir = "/Users/INSERT_USERNAME/Downloads"
document_dir = "/Users/INSERT_USERNAME/Desktop/Documents"
image_dir = "/Users/INSERT_USERNAME/Desktop/Images"
audio_dir = "/Users/INSERT_USERNAME/Desktop/Audio"
video_dir = "/Users/INSERT_USERNAME/Desktop/Videos"

video_types = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",".mp4", ".mp4v", ".m4v", ".avi",".wmv", 
               ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_types = [".mp3", ".m4a", ".flac", ".wav", ".wma", ".aac"]

image_types = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2",
            ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf",
            ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico",".png", ".gif", ".webp", ".nrw"]

document_types = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"]

makedirs(source_dir, exist_ok=True)
makedirs(document_dir, exist_ok=True)
makedirs(image_dir, exist_ok=True)
makedirs(audio_dir, exist_ok=True)
makedirs(video_dir, exist_ok=True)

class FileManager(FileSystemEventHandler):

    def on_created(self, event):
        with scandir(source_dir) as files:
            for file in files:
                name = file.name
                self.check_for_docs(name, file)
                self.check_for_video(name, file)
                self.check_for_images(name, file)
                self.check_for_audio(name, file)

    def on_modified(self, event):
        with scandir(source_dir) as files:
            for file in files:
                name = file.name
                self.check_for_docs(name, file)
                self.check_for_video(name, file)
                self.check_for_images(name, file)
                self.check_for_audio(name, file)
        

    def check_for_docs(self, name, file):  
        for audio_type in audio_types:
            if name.endswith(audio_type) or name.endswith(audio_type.upper()):
                handle_duplicate(document_dir, name)
                move(file, audio_dir)
                logging.info(f"Moved audio file to Desktop: {name}")

    def check_for_video(self, name, file): 
        for video_type in video_types:
            if name.endswith(video_type) or name.endswith(video_type.upper()):
                handle_duplicate(video_dir, name)
                move(file, video_dir)
                logging.info(f"Moved video file to Desktop: {name}")

    def check_for_images(self, name, file):  
        for image_type in image_types:
            if name.endswith(image_type) or name.endswith(image_type.upper()):
                handle_duplicate(image_dir, name)
                move(file, image_dir)
                logging.info(f"Moved image file to Desktop: {name}")

    def check_for_audio(self, name, file):  
        for document_type in document_types:
            if name.endswith(document_type) or name.endswith(document_type.upper()):
                handle_duplicate(document_dir, name)
                move(file, document_dir)
                logging.info(f"Moved document file to Desktop: {name}")

def handle_duplicate(dest, name):
    if exists(f"{dest}/{name}"):
        old_name = join(dest, name)
        new_name = join(dest, unique_name(dest, name))
        rename(old_name, new_name)

def unique_name(dest, name):
    filename, type = splitext(name)
    counter = 1
    
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){type}"
        counter += 1

    return name



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = FileManager()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()