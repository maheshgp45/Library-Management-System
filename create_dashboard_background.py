"""
Create a glassmorphism-style admin dashboard background for Library Management System
Generates a high-resolution PNG with transparent background, blurred gradients, and floating cards
"""

from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math
from io import BytesIO

# Configuration
WIDTH = 1920
HEIGHT = 1080
OUTPUT_PATH = 'static/uploads/admin_dashboard_bg.png'

def create_base_image():
    """Create the base transparent image"""
    return Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))

def create_gradient_overlay(width, height, color1, color2, blur_strength=30):
    """Create a blurred gradient overlay"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()
    
    for y in range(height):
        for x in range(width):
            # Diagonal gradient
            progress = (x + y) / (width + height)
            
            r = int(color1[0] * (1 - progress) + color2[0] * progress)
            g = int(color1[1] * (1 - progress) + color2[1] * progress)
            b = int(color1[2] * (1 - progress) + color2[2] * progress)
            alpha = int(color1[3] * (1 - progress) + color2[3] * progress)
            
            pixels[x, y] = (r, g, b, alpha)
    
    return img.filter(ImageFilter.GaussianBlur(radius=blur_strength))

def draw_book_icon(draw, x, y, size, alpha=80):
    """Draw a subtle book icon"""
    # Book spine
    draw.rectangle([x - size//2, y - size//2, x + size//2, y + size//2], 
                   outline=(100, 150, 255, alpha), width=2)
    # Book pages indicator
    draw.line([x - size//3, y - size//2, x - size//3, y + size//2], 
              fill=(100, 150, 255, alpha), width=1)

def draw_database_icon(draw, x, y, size, alpha=80):
    """Draw a subtle database/cylinder icon"""
    # Cylinder top
    draw.ellipse([x - size//2, y - size//3, x + size//2, y], 
                 outline=(150, 100, 255, alpha), width=2)
    # Cylinder body
    draw.rectangle([x - size//2, y, x + size//2, y + size//2], 
                   outline=(150, 100, 255, alpha), width=2)
    # Cylinder bottom
    draw.ellipse([x - size//2, y + size//2, x + size//2, y + size//3 + size//2], 
                 outline=(150, 100, 255, alpha), width=2)

def draw_floating_card(img, x, y, width, height, blur_radius=10, opacity=40):
    """Draw a semi-transparent floating card with glassmorphism effect"""
    card = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    
    # Light blue/white glass background
    card_draw.rounded_rectangle(
        [0, 0, width, height],
        radius=20,
        fill=(255, 255, 255, opacity),
        outline=(200, 220, 255, int(opacity * 1.5))
    )
    
    # Add slight internal border for glass effect
    card_draw.rounded_rectangle(
        [2, 2, width - 2, height - 2],
        radius=18,
        outline=(255, 255, 255, int(opacity * 0.7)),
        width=1
    )
    
    # Blur the card for glassmorphism effect
    card = card.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # Paste onto main image
    img.paste(card, (x, y), card)

def create_dashboard_background():
    """Create the complete dashboard background"""
    base = create_base_image()
    
    # Create gradient overlay (blue to violet)
    gradient1 = create_gradient_overlay(
        WIDTH, HEIGHT,
        (100, 150, 255, 80),      # Blue
        (180, 100, 255, 80),      # Violet
        blur_strength=50
    )
    
    # Create second gradient overlay (offset)
    gradient2 = create_gradient_overlay(
        WIDTH, HEIGHT,
        (150, 100, 255, 60),      # Violet
        (200, 150, 255, 60),      # Light purple
        blur_strength=40
    )
    
    # Composite gradients
    base = Image.alpha_composite(base, gradient1)
    base = Image.alpha_composite(base, gradient2)
    
    # Draw subtle background icons (low opacity)
    draw = ImageDraw.Draw(base)
    
    # Scatter book and database icons in background
    # Top-left area
    draw_book_icon(draw, 100, 80, 60, alpha=40)
    draw_database_icon(draw, 250, 150, 70, alpha=35)
    
    # Top-right area
    draw_database_icon(draw, WIDTH - 150, 100, 70, alpha=40)
    draw_book_icon(draw, WIDTH - 300, 180, 60, alpha=35)
    
    # Bottom-left area
    draw_book_icon(draw, 150, HEIGHT - 150, 60, alpha=40)
    draw_database_icon(draw, 320, HEIGHT - 100, 70, alpha=35)
    
    # Bottom-right area
    draw_database_icon(draw, WIDTH - 200, HEIGHT - 180, 70, alpha=40)
    draw_book_icon(draw, WIDTH - 350, HEIGHT - 120, 60, alpha=35)
    
    # Add floating cards (glassmorphism style)
    # Top-left card
    draw_floating_card(base, 80, 120, 280, 200, blur_radius=15, opacity=35)
    
    # Top-right card
    draw_floating_card(base, WIDTH - 360, 100, 280, 180, blur_radius=15, opacity=30)
    
    # Bottom-left card
    draw_floating_card(base, 100, HEIGHT - 220, 250, 180, blur_radius=15, opacity=30)
    
    # Bottom-right card
    draw_floating_card(base, WIDTH - 330, HEIGHT - 240, 280, 200, blur_radius=15, opacity=35)
    
    # Add some floating accents (small circles/dots)
    accent_draw = ImageDraw.Draw(base)
    accents = [
        (200, 300, 15),
        (WIDTH - 200, 350, 12),
        (300, HEIGHT - 300, 18),
        (WIDTH - 250, HEIGHT - 200, 15),
        (WIDTH // 2 - 150, 200, 10),
        (WIDTH // 2 + 150, HEIGHT - 300, 10),
    ]
    
    for x, y, size in accents:
        # Draw semi-transparent circles
        accent_draw.ellipse(
            [x - size, y - size, x + size, y + size],
            fill=(100, 150, 255, 25),
            outline=(150, 120, 255, 40)
        )
    
    return base

def main():
    """Generate and save the dashboard background"""
    print("Creating glassmorphism admin dashboard background...")
    print(f"Resolution: {WIDTH}x{HEIGHT}")
    
    # Create the background
    background = create_dashboard_background()
    
    # Save the image
    background.save(OUTPUT_PATH, 'PNG')
    print(f"✓ Dashboard background saved to: {OUTPUT_PATH}")
    print(f"✓ File size: {len(background.tobytes()) / (1024*1024):.2f} MB")
    print("\nFeatures:")
    print("  • Transparent background (RGBA)")
    print("  • Blurred blue to violet gradient overlays")
    print("  • Floating semi-transparent glassmorphic cards")
    print("  • Subtle book and database icons with low opacity")
    print("  • Empty center space for dashboard widgets")
    print("  • Modern SaaS style design")

if __name__ == '__main__':
    main()
