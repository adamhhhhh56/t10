# === Standard library ===
import os
import wget
import time
import json
import math
import torch
import torch.nn as nn
import copy
import numpy as np
import requests
from omegaconf import open_dict
from pydub import AudioSegment
from nemo.collections.asr.models import ASRModel

# === Imports ===
exec(open("audioupload.py").read())
exec(open("parakeet.py").read())
exec(open("canary.py").read())

# Data
response = {
    "idn": "W74WCS02P70EZXRI7VQU",
    "task": "transcription",
    "lang": "en",
    "length": "1468",
    "file": "http://qweasdzxc.fun/50.wav"
}
data = response

# Transcription
if data["task"] == "transcription":
    
    # Audio download
    def_audioupload(data["idn"], data["file"])

    #  Transcription
    if data["lang"] == "en":
        
        # Audio cut (--transcription)
        segments = def_audiocut(data["idn"], f'_temp/{data["idn"]}/{data["idn"]}.wav', int(data["length"]), int(600), int(60), 'transcription')

        # Transcription
        for seg in segments["segments"]:
            #seg["words"], seg["time"] = def_parakeet(seg["file"], modelparakeet)

            seg["words"], seg["time"]   = def_canary(seg["file"], modelcanary, data["lang"], data["lang"])


            



    total_time = 0
    for seg in segments["segments"]:
        total_time += seg.get("time", 0) 
    
    print(total_time)

        
    #print(segments)


























    

 