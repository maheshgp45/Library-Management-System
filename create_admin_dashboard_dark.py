"""
Create a dark mode admin dashboard background for Library Management System
Features:
- Navy blue and dark charcoal gradient
- Faint glowing line icons (books, reports, database, analytics)
- Smooth abstract curved shapes
- Professional modern SaaS UI style
- High resolution PNG
"""

from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
import random

# Configuration
WIDTH = 1920
HEIGHT = 1080
OUTPUT_PATH = 'static/uploads/admin_dashboard_dark_bg.png'

def create_gradient_background(width, height):
    """Create navy blue to dark charcoal gradient"""
    img = Image.new('RGB', (width, height))
    pixels = np.array(img, dtype=np.uint8)
    
    for y in range(height):
        progress = y / height
        
        # Navy blue to dark charcoal
        r = int(20 + (40 - 20) * progress)      # 20 to 40
        g = int(30 + (50 - 30) * progress)      # 30 to 50
        b = int(60 + (80 - 60) * progress)      # 60 to 80
        
        pixels[y, :] = [r, g, b]
    
    return Image.fromarray(pixels)

def draw_curved_shapes(img, width, height):
    """Draw smooth abstract curved shapes in background"""
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw smooth curved shapes with low opacity
    curves = [
        # Top-left curve
        {
            'center': (width * 0.1, height * 0.1),
            'radius': width * 0.3,
            'color': (100, 150, 255, 8),
            'offset': -50
        },
        # Top-right curve
        {
            'center': (width * 0.9, height * 0.15),
            'radius': width * 0.25,
            'color': (150, 100, 255, 10),
            'offset': -40
        },
        # Bottom-left curve
        {
            'center': (width * 0.15, height * 0.85),
            'radius': width * 0.28,
            'color': (100, 200, 255, 8),
            'offset': -45
        },
        # Bottom-right curve
        {
            'center': (width * 0.85, height * 0.9),
            'radius': width * 0.3,
            'color': (150, 120, 255, 12),
            'offset': -50
        },
    ]
    
    for curve in curves:
        cx, cy = curve['center']
        radius = curve['radius']
        color = curve['color']
        
        # Draw multiple layers for smooth effect
        for i in range(3):
            r = radius - (i * radius * 0.12)
            draw.ellipse(
                [cx - r, cy - r, cx + r, cy + r],
                fill=color,
                outline=None
            )

def draw_book_icon(draw, x, y, size, opacity=40):
    """Draw a faint glowing line icon of a book"""
    # Book spine outline
    draw.rectangle(
        [x - size//2, y - size//2, x + size//2, y + size//2],
        outline=(100, 180, 255, opacity),
        width=2
    )
    
    # Book pages (vertical lines)
    page_x = x - size//3
    for i in range(3):
        draw.line(
            [page_x, y - size//2, page_x, y + size//2],
            fill=(100, 180, 255, opacity // 2),
            width=1
        )
        page_x += size//6

def draw_database_icon(draw, x, y, size, opacity=40):
    """Draw a faint glowing database/cylinder icon"""
    # Cylinder top (ellipse)
    draw.ellipse(
        [x - size//2, y - size//3, x + size//2, y],
        outline=(120, 200, 255, opacity),
        width=2
    )
    
    # Cylinder sides
    draw.line([x - size//2, y, x - size//2, y + size//2],
              fill=(120, 200, 255, opacity), width=2)
    draw.line([x + size//2, y, x + size//2, y + size//2],
              fill=(120, 200, 255, opacity), width=2)
    
    # Cylinder bottom
    draw.ellipse(
        [x - size//2, y + size//2, x + size//2, y + size//3 + size//2],
        outline=(120, 200, 255, opacity),
        width=2
    )

def draw_analytics_icon(draw, x, y, size, opacity=40):
    """Draw a faint glowing analytics/chart icon"""
    # Chart lines
    bar_width = size // 6
    bar_x = x - size // 2 + bar_width
    
    bars = [
        (bar_x, y + size//4, bar_x + bar_width, y + size//2),
        (bar_x + bar_width + 4, y, bar_x + bar_width * 2 + 4, y + size//2),
        (bar_x + bar_width * 2 + 8, y + size//6, bar_x + bar_width * 3 + 8, y + size//2),
    ]
    
    for bar in bars:
        draw.rectangle(bar, outline=(180, 150, 255, opacity), fill=(180, 150, 255, opacity // 2), width=2)
    
    # Trending line
    draw.line([x - size//2, y + size//2, x + size//2, y - size//4],
              fill=(180, 150, 255, opacity), width=2)

def draw_report_icon(draw, x, y, size, opacity=40):
    """Draw a faint glowing report icon"""
    # Document outline
    draw.rectangle(
        [x - size//2, y - size//2, x + size//2, y + size//2],
        outline=(150, 180, 255, opacity),
        width=2
    )
    
    # Document lines (text representation)
    line_y = y - size//3
    for i in range(3):
        draw.line(
            [x - size//3, line_y, x + size//3, line_y],
            fill=(150, 180, 255, opacity // 2),
            width=1
        )
        line_y += size // 6

def add_glow_effect(img, radius=2):
    """Add subtle glow effect to the image"""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))

def create_admin_dashboard_bg():
    """Create the complete dark admin dashboard background"""
    
    # Create gradient background
    bg = create_gradient_background(WIDTH, HEIGHT)
    
    # Convert to RGBA for drawing with opacity
    bg = bg.convert('RGBA')
    
    # Draw curved shapes
    draw_curved_shapes(bg, WIDTH, HEIGHT)
    
    # Add icons in all four corners
    draw = ImageDraw.Draw(bg, 'RGBA')
    
    # Icon positions and types
    icon_positions = [
        # Top-left area
        {'pos': (100, 100), 'type': 'book', 'opacity': 35},
        {'pos': (200, 150), 'type': 'database', 'opacity': 30},
        
        # Top-right area
        {'pos': (WIDTH - 100, 80), 'type': 'analytics', 'opacity': 35},
        {'pos': (WIDTH - 200, 160), 'type': 'report', 'opacity': 30},
        
        # Bottom-left area
        {'pos': (120, HEIGHT - 100), 'type': 'database', 'opacity': 35},
        {'pos': (200, HEIGHT - 150), 'type': 'report', 'opacity': 30},
        
        # Bottom-right area
        {'pos': (WIDTH - 120, HEIGHT - 120), 'type': 'book', 'opacity': 35},
        {'pos': (WIDTH - 220, HEIGHT - 160), 'type': 'analytics', 'opacity': 30},
        
        # Middle sides (subtle)
        {'pos': (50, HEIGHT // 2), 'type': 'report', 'opacity': 20},
        {'pos': (WIDTH - 50, HEIGHT // 2), 'type': 'analytics', 'opacity': 20},
    ]
    
    for icon in icon_positions:
        x, y = icon['pos']
        icon_type = icon['type']
        opacity = icon['opacity']
        
        if icon_type == 'book':
            draw_book_icon(draw, x, y, 60, opacity)
        elif icon_type == 'database':
            draw_database_icon(draw, x, y, 65, opacity)
        elif icon_type == 'analytics':
            draw_analytics_icon(draw, x, y, 60, opacity)
        elif icon_type == 'report':
            draw_report_icon(draw, x, y, 55, opacity)
    
    # Add subtle glow
    bg = bg.filter(ImageFilter.GaussianBlur(radius=1))
    
    return bg

def main():
    """Generate and save the admin dashboard background"""
    print("🌙 Creating dark mode admin dashboard background...")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    
    # Create the background
    background = create_admin_dashboard_bg()
    
    # Save the image
    background.save(OUTPUT_PATH, 'PNG')
    
    file_size = len(background.tobytes()) / (1024 * 1024)
    print(f"✓ Admin dashboard background saved to: {OUTPUT_PATH}")
    print(f"✓ File size: {file_size:.2f} MB")
    print(f"\nFeatures:")
    print(f"  • Navy blue to dark charcoal gradient")
    print(f"  • Faint glowing line icons (books, reports, database, analytics)")
    print(f"  • Smooth abstract curved shapes")
    print(f"  • Low opacity design elements")
    print(f"  • Professional modern SaaS UI style")
    print(f"  • Center area optimized for dashboard content")

if __name__ == '__main__':
    main()
