"""
Create a clean student dashboard background for Library Management System
Features:
- Soft green and white gradient
- Subtle low-opacity illustrations (books, graduation cap, study desk, library shelves)
- Center area clean for dashboard content
- Light, friendly, academic feel
- Minimal modern web app style
- High resolution PNG
"""

from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math

# Configuration
WIDTH = 1920
HEIGHT = 1080
OUTPUT_PATH = 'static/uploads/student_dashboard_bg.png'

def create_gradient_background(width, height):
    """Create soft green to white gradient"""
    img = Image.new('RGB', (width, height))
    pixels = np.array(img, dtype=np.uint8)
    
    for y in range(height):
        progress = y / height
        
        # Soft green to white
        r = int(245 + (200 - 245) * progress)   # 245 to 200
        g = int(250 + (235 - 250) * progress)   # 250 to 235
        b = int(245 + (200 - 245) * progress)   # 245 to 200
        
        pixels[y, :] = [r, g, b]
    
    # Add subtle green tint
    for y in range(height):
        progress = y / height
        if pixels[y, 0, 1] > 200:  # Green channel
            pixels[y, :, 1] = np.clip(pixels[y, :, 1] + int(20 * (1 - progress)), 0, 255)
    
    return Image.fromarray(pixels)

def draw_soft_shapes(img, width, height):
    """Draw soft abstract shapes in background"""
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Soft green circles/blobs
    shapes = [
        {'center': (width * 0.1, height * 0.1), 'radius': width * 0.2, 'color': (144, 200, 120, 12)},
        {'center': (width * 0.9, height * 0.12), 'radius': width * 0.18, 'color': (120, 180, 100, 10)},
        {'center': (width * 0.15, height * 0.85), 'radius': width * 0.22, 'color': (150, 210, 130, 12)},
        {'center': (width * 0.88, height * 0.88), 'radius': width * 0.2, 'color': (130, 190, 110, 10)},
    ]
    
    for shape in shapes:
        cx, cy = shape['center']
        radius = shape['radius']
        color = shape['color']
        
        # Draw soft circles
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            fill=color,
            outline=None
        )

def draw_book_illustration(draw, x, y, size, opacity=50):
    """Draw a subtle book illustration"""
    color = (100, 150, 80, opacity)
    
    # Book spine
    draw.rectangle(
        [x - size//2, y - size//3, x + size//2, y + size//3],
        fill=color,
        outline=(120, 170, 100, opacity),
        width=2
    )
    
    # Book pages detail
    for i in range(3):
        offset = (i - 1) * (size // 6)
        draw.line(
            [x - size//2 + 8 + offset, y - size//3, x - size//2 + 8 + offset, y + size//3],
            fill=(140, 180, 120, opacity // 2),
            width=1
        )

def draw_graduation_cap(draw, x, y, size, opacity=50):
    """Draw a subtle graduation cap illustration"""
    color = (100, 150, 80, opacity)
    
    # Cap top (outer part)
    draw.polygon(
        [
            (x - size//2, y),
            (x, y - size//2),
            (x + size//2, y),
            (x, y + size//4)
        ],
        fill=color,
        outline=(120, 170, 100, opacity)
    )
    
    # Cap bill (visor)
    draw.ellipse(
        [x - size//2 - 10, y + size//4 - 5, x + size//2 + 10, y + size//4 + 15],
        fill=color,
        outline=(120, 170, 100, opacity),
        width=1
    )
    
    # Tassel
    draw.line(
        [x, y + size//4, x - size//4, y + size//2],
        fill=(100, 150, 80, opacity),
        width=2
    )

def draw_study_desk(draw, x, y, size, opacity=50):
    """Draw a subtle study desk illustration"""
    color = (100, 150, 80, opacity)
    
    # Desk surface
    draw.rectangle(
        [x - size//2, y, x + size//2, y + size//4],
        fill=color,
        outline=(120, 170, 100, opacity),
        width=2
    )
    
    # Desk legs
    draw.line([x - size//2 + 10, y, x - size//2 + 10, y + size//2],
              fill=color, width=2)
    draw.line([x + size//2 - 10, y, x + size//2 - 10, y + size//2],
              fill=color, width=2)
    
    # Lamp on desk
    draw.ellipse(
        [x - 15, y - 20, x + 5, y + 5],
        fill=(150, 190, 120, opacity),
        outline=(120, 170, 100, opacity),
        width=1
    )
    draw.line([x - 5, y - 20, x - 5, y - 30],
              fill=(120, 170, 100, opacity), width=2)

def draw_library_shelves(draw, x, y, size, opacity=50):
    """Draw subtle library shelves illustration"""
    color = (100, 150, 80, opacity)
    
    # Shelves (horizontal lines)
    for i in range(4):
        shelf_y = y - size//2 + (i * size//4)
        draw.line(
            [x - size//2, shelf_y, x + size//2, shelf_y],
            fill=color,
            width=2
        )
    
    # Shelves support (vertical lines)
    draw.line([x - size//2, y - size//2, x - size//2, y + size//2],
              fill=color, width=2)
    draw.line([x + size//2, y - size//2, x + size//2, y + size//2],
              fill=color, width=2)
    
    # Books on shelves (small rectangles)
    book_colors = [
        (120, 170, 100, opacity),
        (110, 160, 90, opacity),
        (130, 180, 110, opacity)
    ]
    
    for shelf in range(3):
        shelf_y = y - size//2 + (shelf * size//4)
        for book in range(4):
            book_x = x - size//2 + 15 + (book * size//6)
            draw.rectangle(
                [book_x, shelf_y - 10, book_x + 12, shelf_y + 8],
                fill=book_colors[book % 3]
            )

def create_student_dashboard_bg():
    """Create the complete student dashboard background"""
    
    # Create gradient background
    bg = create_gradient_background(WIDTH, HEIGHT)
    
    # Convert to RGBA for drawing with opacity
    bg = bg.convert('RGBA')
    
    # Draw soft shapes
    draw_soft_shapes(bg, WIDTH, HEIGHT)
    
    # Add illustrations
    draw = ImageDraw.Draw(bg, 'RGBA')
    
    # Illustration positions
    positions = [
        # Top-left area
        {'pos': (120, 110), 'type': 'book', 'opacity': 40},
        {'pos': (280, 150), 'type': 'graduation_cap', 'opacity': 38},
        
        # Top-right area
        {'pos': (WIDTH - 140, 100), 'type': 'library_shelves', 'opacity': 40},
        {'pos': (WIDTH - 280, 160), 'type': 'study_desk', 'opacity': 38},
        
        # Bottom-left area
        {'pos': (150, HEIGHT - 130), 'type': 'graduation_cap', 'opacity': 40},
        {'pos': (300, HEIGHT - 160), 'type': 'library_shelves', 'opacity': 38},
        
        # Bottom-right area
        {'pos': (WIDTH - 120, HEIGHT - 130), 'type': 'book', 'opacity': 40},
        {'pos': (WIDTH - 270, HEIGHT - 160), 'type': 'study_desk', 'opacity': 38},
        
        # Subtle corners
        {'pos': (60, HEIGHT // 2), 'type': 'book', 'opacity': 25},
        {'pos': (WIDTH - 60, HEIGHT // 2), 'type': 'graduation_cap', 'opacity': 25},
    ]
    
    for item in positions:
        x, y = item['pos']
        item_type = item['type']
        opacity = item['opacity']
        
        if item_type == 'book':
            draw_book_illustration(draw, x, y, 55, opacity)
        elif item_type == 'graduation_cap':
            draw_graduation_cap(draw, x, y, 50, opacity)
        elif item_type == 'study_desk':
            draw_study_desk(draw, x, y, 58, opacity)
        elif item_type == 'library_shelves':
            draw_library_shelves(draw, x, y, 70, opacity)
    
    # Add very subtle glow
    bg = bg.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return bg

def main():
    """Generate and save the student dashboard background"""
    print("📚 Creating student dashboard background...")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    
    # Create the background
    background = create_student_dashboard_bg()
    
    # Save the image
    background.save(OUTPUT_PATH, 'PNG')
    
    file_size = len(background.tobytes()) / (1024 * 1024)
    print(f"✓ Student dashboard background saved to: {OUTPUT_PATH}")
    print(f"✓ File size: {file_size:.2f} MB")
    print(f"\nFeatures:")
    print(f"  • Soft green and white gradient")
    print(f"  • Subtle low-opacity illustrations")
    print(f"  • Books, graduation cap, study desk, library shelves")
    print(f"  • Light, friendly, academic feel")
    print(f"  • Minimal modern web app style")
    print(f"  • Center area clean for dashboard content")

if __name__ == '__main__':
    main()
