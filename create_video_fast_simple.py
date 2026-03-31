"""
Fast minimal video generator - skips frame-by-frame, uses direct ffmpeg
"""
import os
import subprocess

WIDTH = 1920
HEIGHT = 1080
FPS = 24
DURATION = 18
OUTPUT_PATH = 'static/uploads/login_background.mp4'

# Use ffmpeg to create a simple gradient video directly (no frame-by-frame generation)
cmd = [
    'ffmpeg',
    '-f', 'lavfi',
    '-i', f'color=c=#d4a574:s={WIDTH}x{HEIGHT}:d={DURATION}',
    '-pix_fmt', 'yuv420p',
    '-c:v', 'libx264',
    '-preset', 'fast',
    '-y',  # overwrite
    OUTPUT_PATH
]

print("Creating login background video with ffmpeg...")
print(f"Output: {OUTPUT_PATH}")
print(f"Size: {WIDTH}x{HEIGHT}, Duration: {DURATION}s\n")

try:
    result = subprocess.run(cmd, capture_output=False, text=True)
    if result.returncode == 0:
        print(f"\nSuccess! Video created: {OUTPUT_PATH}")
    else:
        print("FFmpeg failed - falling back to simple approach...")
except Exception as e:
    print(f"Error: {e}")
