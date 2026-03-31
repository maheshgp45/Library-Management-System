"""
Library Background Animation Generator for Student Dashboard
Creates an animated library scene with:
- Bookshelves with books
- Students reading at desks
- Floating book particles
- Animated library atmosphere
"""

import numpy as np
from PIL import Image, ImageDraw
import os
import math
import random

# Configuration
WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 8  # 8 seconds loop
FRAME_COUNT = FPS * DURATION
OUTPUT_PATH = 'static/uploads/student_dashboard_library.gif'

# Colors
WALL_COLOR = (240, 235, 225)  # Warm cream
FLOOR_COLOR = (101, 67, 33)   # Wood brown
BOOKSHELF_COLOR = (120, 80, 50)
BOOK_COLORS = [
    (180, 50, 50),   # Red
    (50, 100, 180),  # Blue
    (50, 150, 50),   # Green
    (180, 150, 50),  # Yellow
    (150, 50, 150),  # Purple
    (180, 100, 50),  # Orange
    (50, 50, 150),   # Dark Blue
    (100, 180, 100), # Light Green
]
DESK_COLOR = (139, 90, 43)
LAMP_COLOR = (255, 220, 100)

def draw_bookshelf(draw, x, y, width, height):
    """Draw a bookshelf with books"""
    # Shelf background
    draw.rectangle([x, y, x + width, y + height], fill=BOOKSHELF_COLOR)
    
    # Shelves
    shelf_height = height // 4
    for i in range(4):
        shelf_y = y + i * shelf_height
        draw.rectangle([x, shelf_y, x + width, shelf_y + 5], fill=(100, 60, 30))
        
        # Books on shelf
        book_x = x + 10
        while book_x < x + width - 20:
            book_height = random.randint(int(shelf_height * 0.6), int(shelf_height * 0.9))
            book_width = random.randint(8, 15)
            color = random.choice(BOOK_COLORS)
            draw.rectangle([book_x, shelf_y - book_height + 5, book_x + book_width, shelf_y + 3], fill=color)
            book_x += book_width + 2

def draw_desk(draw, x, y, width, height):
    """Draw a study desk"""
    # Desk top
    draw.rectangle([x, y, x + width, y + 10], fill=DESK_COLOR)
    # Desk legs
    draw.rectangle([x + 10, y + 10, x + 20, y + height], fill=DESK_COLOR)
    draw.rectangle([x + width - 20, y + 10, x + width - 10, y + height], fill=DESK_COLOR)

def draw_lamp(draw, x, y):
    """Draw a desk lamp"""
    # Lamp base
    draw.ellipse([x - 15, y - 5, x + 15, y + 5], fill=(80, 80, 80))
    # Lamp stand
    draw.rectangle([x - 3, y - 50, x + 3, y - 5], fill=(100, 100, 100))
    # Lamp shade
    draw.polygon([(x - 25, y - 50), (x + 25, y - 50), (x + 15, y - 35), (x - 15, y - 35)], fill=(100, 200, 100))
    # Light glow
    draw.ellipse([x - 40, y - 30, x + 40, y + 10], fill=(255, 255, 150, 30))

def draw_student_reading(draw, x, y, frame, scale=1.0):
    """Draw a student reading at desk"""
    # Body
    body_width = int(35 * scale)
    body_height = int(50 * scale)
    draw.ellipse([x - body_width//2, y - body_height, x + body_width//2, y], 
                 fill=(100, 150, 255))
    
    # Head
    draw.ellipse([x - 14, y - body_height - 28, x + 14, y - body_height - 5], 
                 fill=(255, 220, 190))
    
    # Hair
    draw.ellipse([x - 15, y - body_height - 35, x + 15, y - body_height - 15], 
                 fill=(60, 40, 20))
    
    # Arms on desk
    draw.rectangle([x - 25, y - 20, x - 10, y - 5], fill=(255, 220, 190))
    draw.rectangle([x + 10, y - 20, x + 25, y - 5], fill=(255, 220, 190))
    
    # Book on desk
    book_x = x - 20
    book_y = y - 15
    draw.rectangle([book_x, book_y, book_x + 40, book_y + 8], fill=(200, 50, 50))
    draw.rectangle([book_x + 2, book_y + 2, book_x + 38, book_y + 6], fill=(255, 255, 255))

def draw_library_sign(draw, x, y, frame):
    """Draw a 'LIBRARY' sign with glow"""
    # Sign background
    draw.rectangle([x - 80, y - 25, x + 80, y + 25], fill=(180, 140, 80))
    draw.rectangle([x - 85, y - 30, x + 85, y + 30], outline=(100, 70, 30), width=3)
    
    # The word "LIBRARY" will be drawn as simple shapes
    # L
    draw.line([x - 60, y - 15, x - 60, y + 10], fill=(60, 30, 10), width=4)
    draw.line([x - 60, y + 10, x - 40, y + 10], fill=(60, 30, 10), width=4)
    # I
    draw.line([x - 25, y - 15, x - 25, y + 10], fill=(60, 30, 10), width=4)
    # B
    draw.line([x - 10, y - 15, x - 10, y + 10], fill=(60, 30, 10), width=4)
    draw.ellipse([x - 10, y - 15, x + 10, y - 2], fill=(60, 30, 10))
    draw.ellipse([x - 10, y - 2, x + 12, y + 10], fill=(60, 30, 10))
    # R
    draw.line([x + 18, y - 15, x + 18, y + 10], fill=(60, 30, 10), width=4)
    draw.ellipse([x + 18, y - 15, x + 35, y - 2], fill=(60, 30, 10))
    draw.line([x + 28, y - 2, x + 38, y + 10], fill=(60, 30, 10), width=3)
    # A
    draw.polygon([(x + 50, y + 10), (x + 60, y - 15), (x + 70, y + 10)], fill=(60, 30, 10))
    draw.line([x + 55, y - 2, x + 65, y - 2], fill=(60, 30, 10), width=3)
    # R
    draw.line([x + 75, y - 15, x + 75, y + 10], fill=(60, 30, 10), width=4)
    draw.ellipse([x + 75, y - 15, x + 92, y - 2], fill=(60, 30, 10))
    draw.line([x + 85, y - 2, x + 95, y + 10], fill=(60, 30, 10), width=3)
    # Y
    draw.line([x + 100, y - 15, x + 110, y], fill=(60, 30, 10), width=4)
    draw.line([x + 110, y, x + 120, y - 15], fill=(60, 30, 10), width=4)
    draw.line([x + 105, y + 2, x + 115, y + 10], fill=(60, 30, 10), width=4)

def create_frame(frame_num, total_frames):
    """Create a single frame of the library animation"""
    time_progress = frame_num / total_frames
    
    # Create base image
    img = Image.new('RGB', (WIDTH, HEIGHT), WALL_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Floor
    draw.rectangle([0, HEIGHT - 200, WIDTH, HEIGHT], fill=FLOOR_COLOR)
    # Floor boards
    for i in range(10):
        x = i * (WIDTH // 10)
        draw.line([x, HEIGHT - 200, x, HEIGHT], fill=(80, 50, 20), width=2)
    
    # Wall decorations - picture frames
    frame_positions = [(200, 200), (600, 200), (1000, 200), (1400, 200), (1700, 200)]
    for fx, fy in frame_positions:
        draw.rectangle([fx - 40, fy - 30, fx + 40, fy + 30], outline=(100, 70, 30), width=4)
        draw.rectangle([fx - 35, fy - 25, fx + 35, fy + 25], fill=(200, 180, 150))
    
    # Draw bookshelves on the back wall
    draw_bookshelf(draw, 100, 250, 350, 400)
    draw_bookshelf(draw, 500, 250, 350, 400)
    draw_bookshelf(draw, 900, 250, 350, 400)
    draw_bookshelf(draw, 1300, 250, 300, 400)
    draw_bookshelf(draw, 1650, 250, 200, 400)
    
    # Draw library sign
    draw_library_sign(draw, WIDTH // 2, 180, frame_num)
    
    # Draw desks with students
    desk_positions = [(400, HEIGHT - 100), (800, HEIGHT - 100), (1200, HEIGHT - 100), (1600, HEIGHT - 100)]
    for dx, dy in desk_positions:
        draw_desk(draw, dx - 60, dy - 60, 120, 60)
        draw_lamp(draw, dx + 40, dy - 60)
        draw_student_reading(draw, dx, dy - 60, frame_num, scale=1.0)
    
    # Add floating book particles
    for i in range(8):
        float_x = (i * 250 + int(50 * math.sin(time_progress * 2 * math.pi + i))) % WIDTH
        float_y = 400 + int(30 * math.sin(time_progress * 3 * math.pi + i * 0.5))
        
        # Draw floating book
        draw.rectangle([float_x - 15, float_y - 20, float_x + 15, float_y + 5], 
                       fill=random.choice(BOOK_COLORS))
        draw.rectangle([float_x - 12, float_y - 17, float_x + 12, float_y], fill=(255, 255, 255))
    
    # Add warm light effect
    for i in range(5):
        light_x = 300 + i * 350
        draw.ellipse([light_x - 150, 350, light_x + 150, 600], 
                     fill=(255, 240, 200, 10))
    
    return img

def create_video():
    """Generate all frames and create GIF"""
    print(f"Generating {FRAME_COUNT} frames for library animation...")
    
    frames = []
    for i in range(FRAME_COUNT):
        if i % 30 == 0:
            print(f"Progress: {i}/{FRAME_COUNT} frames")
        frame = create_frame(i, FRAME_COUNT)
        frames.append(frame)
    
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
