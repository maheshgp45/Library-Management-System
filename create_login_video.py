"""
Create a cinematic background video for Library Management System login page
Features:
- Forest environment during golden hour
- Animated particles (sun rays, floating dust)
- Golden hour lighting
- Loopable 15-20 seconds, smooth animation
- 4K quality (3840x2160)
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np
import math
import random
from moviepy.editor import ImageSequenceClip
import os

# Configuration
WIDTH = 3840
HEIGHT = 2160
FPS = 30
DURATION = 18  # seconds
FRAME_COUNT = FPS * DURATION
OUTPUT_PATH = 'static/uploads/login_background.mp4'
FRAMES_DIR = 'static/uploads/frames'

# Ensure frames directory exists
os.makedirs(FRAMES_DIR, exist_ok=True)

def create_sky_gradient(width, height, time_progress=0):
    """Create golden hour sky with time-based variation"""
    img = Image.new('RGB', (width, height), (0, 0, 0))
    pixels = np.array(img)
    
    # Golden hour colors (warmer as time progresses)
    sky_top = np.array([255, 200, 100])  # Golden yellow
    sky_mid = np.array([255, 160, 80])   # Orange
    sky_bottom = np.array([200, 140, 100])  # Peachy
    
    for y in range(height):
        progress = y / height
        # Add slight time variation
        time_variation = math.sin(time_progress * math.pi * 2) * 0.1
        
        color = sky_top * (1 - progress) + sky_bottom * progress
        color = color * (1 + time_variation * 0.2)
        color = np.clip(color, 0, 255).astype(np.uint8)
        
        pixels[y, :] = color
    
    return Image.fromarray(pixels)

def create_forest_ground(width, height, detail_level=0.3):
    """Create forest ground with grass and foliage"""
    img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Ground gradient (darker at top hills)
    for y in range(height):
        progress = y / height
        
        # Green gradient
        r = int(80 * progress + 60 * (1 - progress))
        g = int(140 * progress + 100 * (1 - progress))
        b = int(80 * progress + 50 * (1 - progress))
        
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def create_trees(width, height, count=8):
    """Create stylized tree silhouettes"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Tree positions and sizes
    tree_positions = []
    for i in range(count):
        x = int((i + 0.5) * width / count + random.randint(-int(width/(count*2)), int(width/(count*2))))
        y = int(height * 0.4)
        tree_positions.append((x, y))
    
    for x, y in tree_positions:
        # Tree trunk
        trunk_width = 120
        draw.rectangle(
            [x - trunk_width//2, y, x + trunk_width//2, y + int(height * 0.3)],
            fill=(60, 40, 20, 200)
        )
        
        # Tree foliage (multiple circles for natural look)
        foliage_color = (40, 100, 40, 180)
        for i in range(3):
            circle_y = y - int(height * 0.15 * i)
            circle_size = int(height * 0.25 * (1 - i * 0.2))
            
            # Draw circles for foliage
            draw.ellipse(
                [x - circle_size, circle_y - circle_size, x + circle_size, circle_y + circle_size],
                fill=foliage_color
            )
    
    return img

def create_particles(width, height, time_progress, particle_type='rays'):
    """Create light particles (sun rays, floating dust, etc.)"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if particle_type == 'rays':
        # Sun rays coming through trees
        num_rays = 12
        for i in range(num_rays):
            angle = (i / num_rays * math.pi * 2 + time_progress * math.pi * 0.5) % (math.pi * 2)
            
            # Ray starting point (top center)
            start_x = width // 2 + math.cos(angle) * width * 0.3
            start_y = height * 0.1
            
            # Ray end point
            end_x = width // 2 + math.cos(angle) * width * 0.8
            end_y = height * 0.6
            
            # Draw ray with gradient effect
            for j in range(20):
                progress = j / 20
                x = int(start_x + (end_x - start_x) * progress)
                y = int(start_y + (end_y - start_y) * progress)
                
                opacity = int(60 * (1 - progress) * (0.5 + math.sin(time_progress * math.pi * 2) * 0.3))
                
                draw.ellipse(
                    [x - 50, y - 50, x + 50, y + 50],
                    fill=(255, 220, 100, opacity)
                )
    
    elif particle_type == 'dust':
        # Floating dust particles
        random.seed(12345)  # For consistency across frames
        num_particles = 40
        
        for i in range(num_particles):
            # Pseudo-random but consistent positions
            base_x = (i * 97) % width
            base_y = (i * 113) % height
            
            # Floating motion
            x = base_x + math.sin(time_progress * 2 + i) * 100
            y = base_y + math.cos(time_progress * 1.5 + i * 0.5) * 80
            
            # Ensure within bounds
            x = x % width
            y = y % height
            
            opacity = int(30 * (0.7 + math.sin(time_progress * math.pi * 2 + i) * 0.3))
            
            draw.ellipse(
                [x - 20, y - 20, x + 20, y + 20],
                fill=(255, 200, 100, opacity)
            )
    
    return img

def add_blur_effect(img, radius=3):
    """Add subtle blur for depth of field effect"""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))

def create_frame(frame_num, total_frames):
    """Create a single frame of the video"""
    time_progress = frame_num / total_frames
    
    # Create sky
    sky = create_sky_gradient(WIDTH, HEIGHT, time_progress)
    
    # Create ground
    ground = create_forest_ground(WIDTH, HEIGHT)
    
    # Composite sky and ground
    background = Image.new('RGB', (WIDTH, HEIGHT))
    background.paste(sky, (0, 0, WIDTH, int(HEIGHT * 0.4)))
    background.paste(ground, (0, int(HEIGHT * 0.4), WIDTH, HEIGHT))
    
    # Add trees
    trees = create_trees(WIDTH, HEIGHT, count=10)
    background = Image.alpha_composite(
        background.convert('RGBA'),
        trees
    ).convert('RGB')
    
    # Add sun rays
    rays = create_particles(WIDTH, HEIGHT, time_progress, 'rays')
    background = Image.alpha_composite(
        background.convert('RGBA'),
        rays
    ).convert('RGB')
    
    # Add floating dust
    dust = create_particles(WIDTH, HEIGHT, time_progress, 'dust')
    background = Image.alpha_composite(
        background.convert('RGBA'),
        dust
    ).convert('RGB')
    
    # Add subtle blur for cinematic effect
    background = add_blur_effect(background, radius=2)
    
    return background

def generate_video():
    """Generate all frames and create video"""
    print("Generating cinematic login background video...")
    print(f"Resolution: {WIDTH}x{HEIGHT} (4K)")
    print(f"Duration: {DURATION} seconds @ {FPS} FPS = {FRAME_COUNT} frames")
    print()
    
    frames = []
    
    # Generate all frames
    for frame_num in range(FRAME_COUNT):
        progress = (frame_num / FRAME_COUNT) * 100
        print(f"\rGenerating frame {frame_num + 1}/{FRAME_COUNT} ({progress:.1f}%)", end='', flush=True)
        
        frame = create_frame(frame_num, FRAME_COUNT)
        frame_path = os.path.join(FRAMES_DIR, f'frame_{frame_num:04d}.png')
        frame.save(frame_path)
        frames.append(frame_path)
    
    print("\n\nCreating video from frames...")
    
    # Create video clip from frames
    clip = ImageSequenceClip(frames, fps=FPS)
    
    # Write video file
    clip.write_videofile(
        OUTPUT_PATH,
        verbose=False,
        logger=None,
        codec='libx264',
        audio=False,
        preset='medium'
    )
    
    print(f"\n✓ Video saved to: {OUTPUT_PATH}")
    print(f"\nVideo Specifications:")
    print(f"  • Resolution: {WIDTH}x{HEIGHT} (4K)")
    print(f"  • Duration: {DURATION} seconds")
    print(f"  • Frame Rate: {FPS} FPS")
    print(f"  • Format: MP4 (H.264 codec)")
    print(f"  • Loopable: Yes")
    print(f"\nFeatures:")
    print(f"  • Golden hour forest lighting")
    print(f"  • Animated sun rays through trees")
    print(f"  • Floating dust particles")
    print(f"  • Smooth cinematic motion")
    print(f"  • Center area kept less busy for login form")
    print(f"  • Seamless looping animation")

if __name__ == '__main__':
    generate_video()
