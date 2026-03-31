"""
Jungle Background Animation Generator for Library Management System Login
Creates an animated jungle scene with:
- Wild jungle environment
- Cows having food
- Deer running
- Big tree with students reading books
- Students playing games
"""

import numpy as np
from PIL import Image, ImageDraw
import os
import math
import random

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("OpenCV not found, will try imageio")

try:
    import imageio
    HAS_IMAGIO = True
except ImportError:
    HAS_IMAGIO = False
    print("ImageIO not found")

# Configuration
WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 5  # 5 seconds loop for faster generation
FRAME_COUNT = FPS * DURATION
OUTPUT_PATH = 'static/uploads/login_background.gif'
FRAMES_DIR = 'static/uploads/frames'

os.makedirs(FRAMES_DIR, exist_ok=True)

# Colors
SKY_BLUE = (135, 206, 235)
SKY_DARK = (25, 25, 112)
GRASS_GREEN = (34, 139, 34)
GRASS_DARK = (0, 100, 0)
TREE_BROWN = (101, 67, 33)
LEAF_GREEN = (0, 100, 0)
LEAF_LIGHT = (34, 139, 34)
COW_COLOR = (255, 255, 255)
COW_SPOTS = (0, 0, 0)
DEER_COLOR = (139, 69, 19)
STUDENT_SHIRT = (255, 100, 100)
BOOK_COLOR = (139, 90, 43)

def draw_tree(draw, x, y, scale=1.0):
    """Draw a big tree"""
    # Trunk
    trunk_width = int(60 * scale)
    trunk_height = int(200 * scale)
    draw.rectangle([x - trunk_width//2, y, x + trunk_width//2, y + trunk_height], 
                   fill=TREE_BROWN)
    
    # Foliage (multiple layers)
    foliage_size = int(180 * scale)
    draw.ellipse([x - foliage_size, y - foliage_size//2, x + foliage_size, y + foliage_size//2], 
                 fill=LEAF_GREEN)
    draw.ellipse([x - foliage_size*0.8, y - foliage_size, x + foliage_size*0.8, y + foliage_size*0.3], 
                 fill=LEAF_LIGHT)
    draw.ellipse([x - foliage_size*0.6, y - foliage_size*1.2, x + foliage_size*0.6, y + foliage_size*0.1], 
                 fill=LEAF_GREEN)

def draw_cow(draw, x, y, frame, scale=1.0):
    """Draw a cow with slight animation"""
    # Body
    body_width = int(80 * scale)
    body_height = int(50 * scale)
    draw.ellipse([x - body_width//2, y - body_height//2, x + body_width//2, y + body_height//2], 
                 fill=COW_COLOR)
    
    # Spots
    draw.ellipse([x - 20, y - 15, x - 5, y + 5], fill=COW_SPOTS)
    draw.ellipse([x + 10, y - 10, x + 25, y + 10], fill=COW_SPOTS)
    
    # Head
    head_x = x - body_width//2 - int(20 * scale)
    draw.ellipse([head_x - 15, y - 20, head_x + 15, y + 15], fill=COW_COLOR)
    
    # Legs (animated)
    leg_offset = int(3 * math.sin(frame * 0.2))
    draw.rectangle([x - 25, y + body_height//2, x - 15, y + body_height//2 + 25 + leg_offset], fill=COW_COLOR)
    draw.rectangle([x + 5, y + body_height//2, x + 15, y + body_height//2 + 25 - leg_offset], fill=COW_COLOR)

def draw_deer(draw, x, y, frame, scale=1.0):
    """Draw a running deer"""
    # Body
    body_width = int(70 * scale)
    body_height = int(40 * scale)
    draw.ellipse([x - body_width//2, y - body_height//2, x + body_width//2, y + body_height//2], 
                 fill=DEER_COLOR)
    
    # Neck
    neck_x = x + body_width//2
    draw.rectangle([neck_x, y - 25, neck_x + 20, y + 5], fill=DEER_COLOR)
    
    # Head
    draw.ellipse([neck_x + 10, y - 35, neck_x + 30, y - 10], fill=DEER_COLOR)
    
    # Antlers
    antler_y = y - 35
    draw.line([neck_x + 15, antler_y, neck_x + 5, antler_y - 20], fill=DEER_COLOR, width=3)
    draw.line([neck_x + 25, antler_y, neck_x + 35, antler_y - 20], fill=DEER_COLOR, width=3)
    
    # Legs (running animation)
    leg_move = int(15 * math.sin(frame * 0.5))
    draw.line([x - 20, y + body_height//2, x - 30, y + body_height//2 + 30 + leg_move], fill=DEER_COLOR, width=4)
    draw.line([x + 20, y + body_height//2, x + 10, y + body_height//2 + 30 - leg_move], fill=DEER_COLOR, width=4)

def draw_student_reading(draw, x, y, frame, scale=1.0):
    """Draw a student reading book sitting under tree"""
    # Sitting body
    body_width = int(30 * scale)
    body_height = int(45 * scale)
    draw.ellipse([x - body_width//2, y - body_height, x + body_width//2, y], 
                 fill=STUDENT_SHIRT)
    
    # Head
    draw.ellipse([x - 12, y - body_height - 25, x + 12, y - body_height - 5], 
                 fill=(255, 200, 170))
    
    # Legs (sitting)
    draw.rectangle([x - 15, y, x - 5, y + 20], fill=(50, 50, 150))
    draw.rectangle([x + 5, y, x + 15, y + 20], fill=(50, 50, 150))
    
    # Arms holding book
    draw.rectangle([x - 25, y - 35, x - 10, y - 20], fill=(255, 200, 170))
    
    # Book
    book_width = int(20 * scale)
    book_height = int(25 * scale)
    draw.rectangle([x - book_width, y - 40, x, y - 40 + book_height], fill=BOOK_COLOR)
    # Book pages
    draw.rectangle([x - book_width + 3, y - 37, x - 3, y - 7], fill=(255, 255, 255))

def draw_student_playing(draw, x, y, frame, scale=1.0):
    """Draw a student playing (running/jumping)"""
    # Running animation
    jump = int(10 * math.sin(frame * 0.3))
    
    # Body
    draw.ellipse([x - 15, y - 30 + jump, x + 15, y + jump], fill=(100, 200, 255))
    
    # Head
    draw.ellipse([x - 10, y - 50 + jump, x + 10, y - 30 + jump], fill=(255, 200, 170))
    
    # Arms (swinging)
    arm_swing = int(10 * math.sin(frame * 0.4))
    draw.line([x - 15, y - 25 + jump, x - 25, y - 15 + jump + arm_swing], fill=(255, 200, 170), width=5)
    draw.line([x + 15, y - 25 + jump, x + 25, y - 15 + jump - arm_swing], fill=(255, 200, 170), width=5)
    
    # Legs (running)
    leg_swing = int(15 * math.sin(frame * 0.5))
    draw.line([x - 10, y + jump, x - 15, y + 25 + leg_swing], fill=(50, 50, 150), width=5)
    draw.line([x + 10, y + jump, x + 15, y + 25 - leg_swing], fill=(50, 50, 150), width=5)

def create_frame(frame_num, total_frames):
    """Create a single frame of the jungle animation"""
    time_progress = frame_num / total_frames
    
    # Create base image
    img = Image.new('RGB', (WIDTH, HEIGHT), SKY_BLUE)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Sky gradient
    for y in range(HEIGHT // 2):
        progress = y / (HEIGHT // 2)
        r = int(SKY_BLUE[0] * (1 - progress) + SKY_DARK[0] * progress * 0.3)
        g = int(SKY_BLUE[1] * (1 - progress) + SKY_DARK[1] * progress * 0.3)
        b = int(SKY_BLUE[2] * (1 - progress) + SKY_DARK[2] * progress * 0.3)
        draw.rectangle([0, y, WIDTH, y+1], fill=(r, g, b))
    
    # Distant mountains/hills
    for i in range(5):
        hill_x = i * 400 - 100
        hill_y = HEIGHT // 2 + 50
        draw.ellipse([hill_x, hill_y, hill_x + 500, HEIGHT], fill=(50, 100, 50))
    
    # Ground/grass
    grass_colors = [(34, 139, 34), (0, 100, 0), (50, 120, 50)]
    for i, color in enumerate(grass_colors):
        y_start = HEIGHT // 2 + 100 + i * 30
        draw.rectangle([0, y_start, WIDTH, y_start + 40], fill=color)
    
    # Draw big tree on the left side (under which students read)
    draw_tree(draw, 300, HEIGHT - 150, scale=1.5)
    
    # Draw students reading books under the tree
    # Student 1
    draw_student_reading(draw, 250, HEIGHT - 180, frame_num, scale=1.0)
    # Student 2
    draw_student_reading(draw, 320, HEIGHT - 175, frame_num, scale=1.0)
    # Student 3
    draw_student_reading(draw, 380, HEIGHT - 178, frame_num, scale=0.9)
    
    # Draw student playing games (running around)
    play_x = 600 + int(100 * math.sin(time_progress * 2 * math.pi))
    play_y = HEIGHT - 100
    draw_student_playing(draw, play_x, play_y, frame_num, scale=1.0)
    
    # Second playing student
    play2_x = 750 + int(80 * math.sin(time_progress * 2 * math.pi + 1))
    draw_student_playing(draw, play2_x, play_y + 20, frame_num + 10, scale=0.9)
    
    # Draw cows (grazing)
    cow_positions = [
        (1100, HEIGHT - 120, 0),
        (1300, HEIGHT - 130, 5),
        (1500, HEIGHT - 115, 10),
    ]
    for cx, cy, offset in cow_positions:
        draw_cow(draw, cx, cy, frame_num + offset, scale=1.0)
    
    # Draw deer (running across)
    deer_x = int((frame_num * 8) % (WIDTH + 200) - 100)
    if deer_x < WIDTH:
        draw_deer(draw, deer_x, HEIGHT - 200, frame_num, scale=1.0)
    
    # Second deer
    deer2_x = int((frame_num * 6 + 300) % (WIDTH + 200) - 100)
    if deer2_x < WIDTH:
        draw_deer(draw, deer2_x, HEIGHT - 220, frame_num + 5, scale=0.8)
    
    # Add some jungle plants/bushes
    bush_positions = [(100, HEIGHT - 80), (1700, HEIGHT - 90), (900, HEIGHT - 100)]
    for bx, by in bush_positions:
        draw.ellipse([bx - 40, by - 30, bx + 40, by + 20], fill=(0, 80, 0))
        draw.ellipse([bx - 25, by - 45, bx + 25, by + 10], fill=(34, 139, 34))
    
    # Add sun
    sun_x = WIDTH - 150
    sun_y = 120
    draw.ellipse([sun_x - 60, sun_y - 60, sun_x + 60, sun_y + 60], fill=(255, 220, 100))
    draw.ellipse([sun_x - 40, sun_y - 40, sun_x + 40, sun_y + 40], fill=(255, 250, 150))
    
    # Add some clouds
    cloud_positions = [
        (200 + int(50 * math.sin(time_progress * 2 * math.pi)), 80),
        (600 + int(80 * math.sin(time_progress * 2 * math.pi + 1)), 100),
        (1200 + int(60 * math.sin(time_progress * 2 * math.pi + 2)), 60),
    ]
    for cx, cy in cloud_positions:
        draw.ellipse([cx - 50, cy - 20, cx + 50, cy + 20], fill=(255, 255, 255, 200))
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 10], fill=(255, 255, 255, 200))
    
    # Add birds
    for i in range(3):
        bird_x = 500 + i * 100 + int(30 * math.sin(time_progress * 4 * math.pi + i))
        bird_y = 150 + i * 20
        # Simple bird shape
        draw.ellipse([bird_x - 10, bird_y - 3, bird_x + 10, bird_y + 3], fill=(50, 50, 50))
        draw.line([bird_x - 5, bird_y, bird_x - 10, bird_y - 8], fill=(50, 50, 50), width=2)
        draw.line([bird_x + 5, bird_y, bird_x + 10, bird_y - 8], fill=(50, 50, 50), width=2)
    
    return img

def create_video():
    """Generate all frames and create GIF animation"""
    print(f"Generating {FRAME_COUNT} frames for jungle animation...")
    
    frames = []
    for i in range(FRAME_COUNT):
        if i % 30 == 0:
            print(f"Progress: {i}/{FRAME_COUNT} frames")
        frame = create_frame(i, FRAME_COUNT)
        frames.append(frame)
    
    # Save as GIF
    print(f"Saving animation to {OUTPUT_PATH}...")
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000/FPS),
        loop=0
    )
    print(f"Animation saved to {OUTPUT_PATH}")
    print("Done!")

if __name__ == '__main__':
    create_video()
