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

from deep_translator import GoogleTranslator

class Subtitle:
    def __init__(self):
        self.audio_tmpfile = NamedTemporaryFile().name + ".mp3"
        self.srt_tmpfile = None

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

    def __result_to_subtitle(self, fname = None):
        if self.recognise_result == None or self.video_file == None:
            return

        srt_wr = get_writer("srt", os.path.dirname(self.video_file))
        filename = "{}.{}.srt".format(Path(os.path.basename(self.video_file)).stem, self.lang)

        if fname != None:
            filename = os.path.basename(fname)

        print("save subtitle to file {}".format(filename))
        srt_wr(self.recognise_result, filename)

    def __lang_map(self, lang):
        if lang == None:
            return "en"
        elif lang == "zh":
            return "zh-TW"
        elif lang == "jp":
            return "ja"
        else:
            return "en"

    def __translate(self, lang, file):
        if file == None or not os.path.exists(file):
            return ""

        result = ""

        lang = self.__lang_map(lang)
        src_lang = self.__lang_map(self.lang)
        gt = GoogleTranslator(source = src_lang, target = lang)

        with open(file, "r", encoding="utf-8") as ori_file:
            for line in ori_file:
                res = gt.translate(line) + "\n"
                result += res

        return result

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
            print("create subtitle file ...")
            self.__result_to_subtitle()
            return
        elif lang == "zh" or lang == "en" or lang == "jp":
            print("start translate process...")
        else:
            return

        print("create tmp subtitle file ...")
        self.srt_tmpfile = os.path.basename(NamedTemporaryFile().name) + ".srt"
        self.__result_to_subtitle(self.srt_tmpfile)

        result = self.__translate(lang, self.srt_tmpfile)
        if len(os.path.dirname(self.video_file)) == 0:
            filename = "{}.{}.srt".format(Path(os.path.basename(self.video_file)).stem, lang)
        else:
            filename = "{}/{}.{}.srt".format(os.path.dirname(self.video_file), Path(os.path.basename(self.video_file)).stem, lang)
        print("create subtitle file {} ...".format(filename))
        f = open(filename, 'w', encoding="utf-8")
        f.write(result)
        f.close()

    def close(self):
        print("remove tmp files....")
        if os.path.exists(self.audio_tmpfile):
            os.remove(self.audio_tmpfile)

        if os.path.exists(self.srt_tmpfile):
            os.remove(self.srt_tmpfile)

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
