"""
Admin Dashboard Background Animation Generator
Creates a professional library admin environment with:
- Book inventory visualization
- Desk with computer
- Admin staff
- Floating data/book icons
- Professional dark theme
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
OUTPUT_PATH = 'static/uploads/admin_dashboard_library.gif'

# Colors - Dark Professional Theme
WALL_COLOR = (30, 35, 50)  # Dark blue-gray
FLOOR_COLOR = (20, 25, 35)   # Darker floor
DESK_COLOR = (40, 45, 60)
COMPUTER_COLOR = (60, 70, 90)
SCREEN_COLOR = (100, 150, 200)
ACCENT_COLOR = (100, 150, 255)
BOOK_COLORS = [
    (180, 80, 80),   # Red
    (80, 130, 200),  # Blue
    (80, 180, 100),  # Green
    (200, 180, 80),  # Yellow
    (180, 80, 180),  # Purple
]

def draw_computer(draw, x, y):
    """Draw a computer workstation"""
    # Desk
    draw.rectangle([x - 100, y + 50, x + 100, y + 60], fill=(60, 65, 80))
    draw.rectangle([x - 90, y + 60, x - 80, y + 120], fill=(50, 55, 70))
    draw.rectangle([x + 80, y + 60, x + 90, y + 120], fill=(50, 55, 70))
    
    # Monitor
    draw.rectangle([x - 60, y - 30, x + 60, y + 50], fill=(40, 45, 60))
    # Screen
    draw.rectangle([x - 50, y - 20, x + 50, y + 40], fill=(30, 80, 150))
    # Screen content - simple bars
    for i in range(5):
        bar_width = random.randint(10, 30)
        draw.rectangle([x - 40, y - 15 + i * 10, x - 40 + bar_width, y - 10 + i * 10], 
                       fill=(100, 180, 255, 150))
    
    # Keyboard
    draw.rectangle([x - 40, y + 55, x + 40, y + 65], fill=(50, 55, 70))
    
    # Mouse
    draw.ellipse([x + 50, y + 52, x + 65, y + 67], fill=(50, 55, 70))

def draw_admin_person(draw, x, y, frame):
    """Draw an admin staff person"""
    # Body
    draw.ellipse([x - 25, y - 50, x + 25, y], fill=(80, 100, 150))
    
    # Head
    draw.ellipse([x - 18, y - 75, x + 18, y - 50], fill=(255, 220, 190))
    
    # Hair
    draw.ellipse([x - 20, y - 85, x + 20, y - 65], fill=(40, 30, 20))
    
    # Glasses
    draw.ellipse([x - 15, y - 68, x - 5, y - 62], outline=(80, 80, 80), width=2)
    draw.ellipse([x + 5, y - 68, x + 15, y - 62], outline=(80, 80, 80), width=2)
    draw.line([x - 5, y - 65, x + 5, y - 65], fill=(80, 80, 80), width=2)
    
    # Arms on desk
    draw.rectangle([x - 40, y - 30, x - 20, y - 10], fill=(255, 220, 190))
    draw.rectangle([x + 20, y - 30, x + 40, y - 10], fill=(255, 220, 190))

def draw_bookshelf(draw, x, y, width, height):
    """Draw a bookshelf"""
    # Shelf background
    draw.rectangle([x, y, x + width, y + height], fill=(50, 55, 70))
    
    # Shelves
    shelf_height = height // 4
    for i in range(4):
        shelf_y = y + i * shelf_height
        draw.rectangle([x, shelf_y, x + width, shelf_y + 5], fill=(40, 45, 55))
        
        # Books
        book_x = x + 10
        while book_x < x + width - 15:
            book_height = random.randint(int(shelf_height * 0.5), int(shelf_height * 0.8))
            book_width = random.randint(8, 12)
            color = random.choice(BOOK_COLORS)
            draw.rectangle([book_x, shelf_y - book_height + 5, book_x + book_width, shelf_y + 3], fill=color)
            book_x += book_width + 2

def draw_floating_icon(draw, x, y, icon_type, alpha):
    """Draw floating icons"""
    if icon_type == 'book':
        draw.rectangle([x - 10, y - 15, x + 10, y + 10], fill=(200, 100, 100, alpha))
        draw.rectangle([x - 8, y - 12, x + 8, y + 7], fill=(255, 255, 255, alpha))
    elif icon_type == 'user':
        draw.ellipse([x - 10, y - 15, x + 10, y], fill=(100, 150, 200, alpha))
        draw.ellipse([x - 6, y - 20, x + 6, y - 10], fill=(100, 150, 200, alpha))
    elif icon_type == 'chart':
        # Bar chart
        for i in range(3):
            bar_height = 15 + i * 10
            draw.rectangle([x - 15 + i * 10, y + 10 - bar_height, x - 8 + i * 10, y + 10], 
                          fill=(100, 200, 150, alpha))

def create_frame(frame_num, total_frames):
    """Create a single frame"""
    time_progress = frame_num / total_frames
    
    # Create base
    img = Image.new('RGB', (WIDTH, HEIGHT), WALL_COLOR)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Floor
    draw.rectangle([0, HEIGHT - 180, WIDTH, HEIGHT], fill=FLOOR_COLOR)
    
    # Wall pattern - subtle lines
    for i in range(5):
        y = 100 + i * 150
        draw.line([0, y, WIDTH, y], fill=(50, 55, 70), width=1)
    
    # Bookshelves
    draw_bookshelf(draw, 100, 200, 250, 350)
    draw_bookshelf(draw, 400, 200, 250, 350)
    draw_bookshelf(draw, 700, 200, 250, 350)
    draw_bookshelf(draw, 1000, 200, 250, 350)
    draw_bookshelf(draw, 1300, 200, 250, 350)
    draw_bookshelf(draw, 1600, 200, 200, 350)
    
    # Draw admin desk with computer
    draw_computer(draw, WIDTH // 2, HEIGHT - 150)
    
    # Draw admin person
    draw_admin_person(draw, WIDTH // 2 - 80, HEIGHT - 150, frame_num)
    
    # Floating icons
    for i in range(12):
        float_x = (i * 180 + int(40 * math.sin(time_progress * 2 * math.pi + i))) % WIDTH
        float_y = 150 + int(30 * math.sin(time_progress * 3 * math.pi + i * 0.7))
        alpha = int(150 + 50 * math.sin(time_progress * 4 * math.pi + i))
        icon_type = ['book', 'user', 'chart'][i % 3]
        draw_floating_icon(draw, float_x, float_y, icon_type, alpha)
    
    # Glowing effect at bottom
    for i in range(5):
        glow_x = 200 + i * 400
        draw.ellipse([glow_x - 100, HEIGHT - 180, glow_x + 100, HEIGHT - 50], 
                     fill=(100, 150, 255, 8))
    
    return img

def create_gif():
    """Generate all frames and create GIF"""
    print(f"Generating {FRAME_COUNT} frames for admin animation...")
    
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
    create_gif()
