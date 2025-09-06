import os
import subprocess
import numpy as np
from .logging_config import get_logger

logger = get_logger(__name__)

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
  try:
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_frame, _ = process.communicate()
    width, height = 2688, 1512
    
    if len(raw_frame) == 0:
      logger.warning("No frame data received from RTSP stream")
      return None
    
    expected_size = height * width * 3
    if len(raw_frame) != expected_size:
      logger.warning(f"Frame size mismatch. Expected {expected_size} bytes, got {len(raw_frame)} bytes")
      return None
    
    return np.frombuffer(raw_frame, np.uint8).reshape((height, width, 3))
  except Exception as e:
    logger.error(f"Error reading RTSP stream: {e}")
    return None
