import taglib
import datetime 
from cv2 import cv2
import os

class Video:

    def __init__(self, directory, file_name, extension, name=None):
        self.directory = directory
        self.file_name = file_name
        self.extension = extension
        self.path = directory + "/" + file_name + "." + extension
        self.duration = self._get_duration()
        self.preview = file_name + ".jpg"
        if name == None:
            self.name = self.__get_title()[0]
        else:
            self.name = name
            self.__set_title()
        self._create_preview()

    def __set_title(self):
        video = taglib.File(self.path)
        video.tags["TITLE"] = [self.name]
        video.save()

    def __get_title(self):
        video = taglib.File(self.path)
        return video.tags["TITLE"]

    def _get_duration(self):
        video = cv2.VideoCapture(self.path)
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        seconds = int(frames / fps)
        duration = str(datetime.timedelta(seconds=seconds))
        time = duration.split(":")
        if int(time[0]) == 0:
            return time[1] + ":" + time[2]
        return duration

    def _create_preview(self):
        path = self.directory + "/" + self.preview
        if not os.path.isfile(path):
            video = cv2.VideoCapture(self.path)
            ret, frame = video.read()
            ratio = frame.shape[0] / frame.shape[1]
            width = 150
            height = int(width * ratio)
            dimensions = (width, height)

            frame = cv2.resize(frame, dimensions)
            cv2.imwrite(path, frame)

    def print(self):
        video = {"file_name": self.file_name + "." + self.extension,
                 "name": self.name,
                 "duration": self.duration,
                 "preview": self.preview}
        return video
