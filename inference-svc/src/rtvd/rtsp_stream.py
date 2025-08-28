import os
import subprocess
import numpy as np

RTSP_CONTROLLER_URL = os.environ.get('RTSP_CONTROLLER_URL')
RTSP_ID = os.environ.get('RTSP_ID')

ffmpeg_command = [
    'ffmpeg',
    '-rtsp_transport', 'tcp',
    '-i', f'{RTSP_CONTROLLER_URL}/{RTSP_ID}', 
    '-frames', '1',
    '-f', 'rawvideo',
    '-pix_fmt', 'bgr24',
    'pipe:1'
]

def get_frame():
  process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  raw_frame, _ = process.communicate()
  width, height = 2688, 1512
  return np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))