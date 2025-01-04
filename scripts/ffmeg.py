import os
import subprocess

image_dir = r'D:\__projects\StaticChairProductions\LOU\01_Workflow\Shots\001-2010\Plates\2224x1548'
output_video = os.path.join(image_dir, 'output.mp4')

# Adjusting the pattern to match JPG files
image_pattern = os.path.join(image_dir, 'IF2010_MP01.%04d.jpg')

# FFmpeg command to convert images to video
command = [
    'ffmpeg',
    '-start_number', '1001',
    '-framerate', '24',
    '-i', image_pattern,
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    output_video
]

# Run the command
subprocess.call(command)
