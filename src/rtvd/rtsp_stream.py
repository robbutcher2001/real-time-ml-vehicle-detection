import subprocess
import numpy as np

ffmpeg_command = [
    'ffmpeg',
    '-rtsp_transport', 'tcp',
    '-i', '<camera_rtsp_url>',
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