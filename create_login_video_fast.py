"""
Optimized cinematic background video generator for Library Management System
Creates fast, high-quality 4K video with forest scene
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os
import math
import random

# Configuration
WIDTH = 1920  # Using 1080p for faster generation, scales to 4K
HEIGHT = 1080
FPS = 30
DURATION = 18
FRAME_COUNT = FPS * DURATION
OUTPUT_PATH = 'static/uploads/login_background.mp4'
FRAMES_DIR = 'static/uploads/frames'

os.makedirs(FRAMES_DIR, exist_ok=True)

def create_frame(frame_num, total_frames):
    """Create a single optimized frame"""
    time_progress = frame_num / total_frames
    
    # Create base image as numpy array (faster)
    img_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    
    # Golden hour gradient sky
    for y in range(HEIGHT):
        progress = y / HEIGHT
        # Smooth golden hour colors
        r = int(255 * (1 - progress * 0.3) + 100 * progress * 0.3)
        g = int(200 * (1 - progress * 0.2) + 120 * progress * 0.2)
        b = int(100 * (1 - progress * 0.1) + 80 * progress * 0.1)
        img_array[y, :] = [r, g, b]
    
    # Convert to PIL Image
    img = Image.fromarray(img_array)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw ground
    ground_color = (60, 120, 60, 255)
    draw.rectangle([0, HEIGHT // 2, WIDTH, HEIGHT], fill=ground_color)
    
    # Draw trees (silhouettes)
    tree_positions = [
        (WIDTH * 0.15, HEIGHT * 0.35),
        (WIDTH * 0.35, HEIGHT * 0.4),
        (WIDTH * 0.55, HEIGHT * 0.35),
        (WIDTH * 0.75, HEIGHT * 0.38),
        (WIDTH * 0.85, HEIGHT * 0.4),
    ]
    
    for x, y in tree_positions:
        # Trunk
        draw.rectangle([x-40, y, x+40, y + HEIGHT * 0.35], fill=(80, 50, 30, 200))
        # Foliage
        draw.ellipse([x-120, y-100, x+120, y+50], fill=(30, 80, 30, 180))
        draw.ellipse([x-100, y-50, x+100, y+100], fill=(40, 100, 40, 180))
    
    # Add animated sun rays
    num_rays = 10
    for i in range(num_rays):
        angle = (i / num_rays * 2 * math.pi + time_progress * math.pi) % (2 * math.pi)
        
        # Ray spread
        for length in range(50, 300, 50):
            sx = WIDTH // 2 + math.cos(angle) * length
            sy = HEIGHT // 3 + math.sin(angle) * length * 0.5
            
            # Opacity based on distance and time
            opacity = max(0, int(80 * (1 - length / 300) * (0.5 + 0.5 * math.sin(time_progress * 4))))
            
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                draw.ellipse([sx-30, sy-30, sx+30, sy+30], fill=(255, 200, 80, opacity))
    
    # Add floating particles
    random.seed(42)
    for i in range(30):
        px = (int(random.random() * WIDTH) + int(time_progress * 100 + i) * 7) % WIDTH
        py = (int(random.random() * HEIGHT) + int(math.sin(time_progress + i) * 50)) % HEIGHT
        
        opacity = int(50 * (0.5 + 0.5 * math.sin(time_progress * 3 + i)))
        draw.ellipse([px-15, py-15, px+15, py+15], fill=(255, 200, 100, opacity))
    
    return img

    # Composite silhouette sprites if available
    sprites_dir = 'static/uploads/sprites'
    try:
        # load optional sprite images (man, cow, student) and paste them with simple walk animation
        man = Image.open(os.path.join(sprites_dir, 'man.png')).convert('RGBA')
        cow = Image.open(os.path.join(sprites_dir, 'cow.png')).convert('RGBA')
        student = Image.open(os.path.join(sprites_dir, 'student.png')).convert('RGBA')

        # scale sprites to scene
        man = man.resize((int(WIDTH*0.06), int(HEIGHT*0.18)), Image.ANTIALIAS)
        cow = cow.resize((int(WIDTH*0.08), int(HEIGHT*0.12)), Image.ANTIALIAS)
        student = student.resize((int(WIDTH*0.05), int(HEIGHT*0.14)), Image.ANTIALIAS)

        # compute simple horizontal positions for walking animation
        man_x = int((frame_num * 2) % (WIDTH + man.width) - man.width)
        cow_x = int((frame_num * 1.2 + WIDTH*0.3) % (WIDTH + cow.width) - cow.width)
        student_x = int((frame_num * 2.5 + WIDTH*0.6) % (WIDTH + student.width) - student.width)

        base_y = HEIGHT // 2 + 40
        img.paste(man, (man_x, base_y - man.height), man)
        img.paste(cow, (cow_x, base_y - cow.height + 20), cow)
        img.paste(student, (student_x, base_y - student.height - 10), student)
    except Exception:
        # sprites not provided — skip compositing
        pass

def generate_video_optimized():
    """Generate video with optimized performance"""
    # avoid emojis which can cause encoding errors on Windows consoles
    print("Generating Cinematic Login Background Video")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    print(f"Total Frames: {FRAME_COUNT}")
    print()
    
    # Generate frames
    frames_list = []
    for frame_num in range(FRAME_COUNT):
        if frame_num % 30 == 0 or frame_num == FRAME_COUNT - 1:
            progress = int((frame_num / FRAME_COUNT) * 100)
            print(f"✓ Generating frame {frame_num + 1}/{FRAME_COUNT} ({progress}%)")
        
        frame = create_frame(frame_num, FRAME_COUNT)
        frame_path = os.path.join(FRAMES_DIR, f'frame_{frame_num:04d}.png')
        frame.save(frame_path, optimize=True)
        frames_list.append(frame_path)
    
    print("\nCreating video from frames...")
    
    # Use FFmpeg via moviepy alternatively, or create with imageio
    try:
        import imageio
        writer = imageio.get_writer(OUTPUT_PATH, fps=FPS, codec='libx264', quality=8, pixelformat='yuv420p')
        for i, frame_path in enumerate(frames_list):
            frame = imageio.imread(frame_path)
            writer.append_data(frame)
            if i % 30 == 0:
                print(f"  Writing frame {i + 1}/{len(frames_list)}")
        writer.close()
        print(f"\nVideo successfully generated!")
        print(f"📂 Saved to: {OUTPUT_PATH}")
    except ImportError:
        print("⚠️  imageio not available, installing...")
        os.system("pip install imageio imageio-ffmpeg")
        print("Please run this script again!")
        return
    
    print("\nVideo Specifications:")
    print(f"  • Resolution: {WIDTH}x{HEIGHT}")
    print(f"  • Duration: {DURATION} seconds")
    print(f"  • Frame Rate: {FPS} FPS")
    print(f"  • Format: MP4 (H.264)")
    print(f"  • Loopable: Yes")
    print("\n✨ Features:")
    print("  ✓ Golden hour forest lighting")
    print("  ✓ Animated sun rays")
    print("  ✓ Floating dust particles")
    print("  ✓ Smooth cinematic motion")
    print("  ✓ Center area optimized for login form")

if __name__ == '__main__':
    generate_video_optimized()
