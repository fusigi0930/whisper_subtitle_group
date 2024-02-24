import io
import os
from pathlib import Path
import whisper
from whisper.utils import get_writer
import torch
import sys
import contextlib

import openai

from tempfile import NamedTemporaryFile
from sys import platform
import time
from datetime import datetime, timedelta
import copy
import random
import re
from moviepy.editor import *

class Subtitle:
    def __init__(self):
        self.audio_tmpfile = NamedTemporaryFile().name + ".mp3"

        self.model = "small"
        self.lang = "en"
        self.video_file = None

        self.whisper_model = whisper.load_model(self.model+"."+self.lang)

        self.recognise_result = None

    def __recognise(self, file):
        try:
            if self.lang == "zh":
                r = self.whisper_model.transcribe(file, language="zh", fp16=torch.cuda.is_available())
            elif self.lang == "jp":
                r = self.whisper_model.transcribe(file, language="Japanese", fp16=torch.cuda.is_available())
            else:
                r = self.whisper_model.transcribe(file, fp16=torch.cuda.is_available())
            self.recognise_result = r
        except:
            self.recognise_result = None

    def __result_to_subtitle(self):
        if self.recognise_result == None or self.video_file == None:
            return

        srt_wr = get_writer("srt", os.path.dirname(self.video_file))
        filename = "{}.{}.srt".format(Path(os.path.basename(self.video_file)).stem, self.lang)
        print("save subtitle to file {}".format(filename))
        srt_wr(self.recognise_result, filename)

    def set_lang(self, lang):
        if lang == "en":
            self.whisper_model = whisper.load_model(self.model+".en")
        elif lang == "zh" or lang == "jp":
            self.whisper_model = whisper.load_model(self.model)
        else:
            return

        self.lang = lang

    def start_recognise(self):
        self.start_recognise_from_file(self.audio_tmpfile)

    def start_recognise_from_file(self, audio_file):
        print("recognise in ai model ...")
        self.__recognise(audio_file)

    def store_to_srt(self, lang = None):
        if lang == None or lang == self.lang:
            print("create substitle file ...")
            self.__result_to_subtitle()
        elif lang == "zh":
            print("TBI")
        elif lang == "en":
            print("TBI")

    def close(self):
        if os.path.exists(self.audio_tmpfile):
            print("remove tmp files....")
            os.remove(self.audio_tmpfile)

        self.recognise_result = None
        self.video_file = None

    def process(self, video_file):
        if not os.path.exists(video_file):
            print("file {} is not exist.".format(video_file))
            exit(1)

        self.video_file = video_file
        v = VideoFileClip(video_file)
        a = v.audio
        print("extract audio from video file")
        a.write_audiofile(self.audio_tmpfile)
        self.start_recognise()
