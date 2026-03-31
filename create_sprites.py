from PIL import Image, ImageDraw
import os
os.makedirs('static/uploads/sprites', exist_ok=True)

W, H = 400, 400

# Man silhouette (standing)
img = Image.new('RGBA', (W, H), (0,0,0,0))
d = ImageDraw.Draw(img)
# head
d.ellipse((170,40,230,100), fill=(0,0,0,255))
# body
d.rectangle((185,100,215,220), fill=(0,0,0,255))
# left arm
d.rectangle((140,110,185,135), fill=(0,0,0,255))
# right arm holding book (small rectangle)
d.rectangle((215,110,260,135), fill=(0,0,0,255))
d.rectangle((260,120,295,140), fill=(80,80,255,255))
# legs
d.rectangle((185,220,200,340), fill=(0,0,0,255))
d.rectangle((200,220,215,340), fill=(0,0,0,255))
img.save('static/uploads/sprites/man.png')

# Cow silhouette
img = Image.new('RGBA', (W, H), (0,0,0,0))
d = ImageDraw.Draw(img)
# body
d.ellipse((60,150,340,260), fill=(0,0,0,255))
# head
d.ellipse((300,120,360,170), fill=(0,0,0,255))
# legs
d.rectangle((100,250,120,340), fill=(0,0,0,255))
d.rectangle((160,250,180,340), fill=(0,0,0,255))
d.rectangle((240,250,260,340), fill=(0,0,0,255))
d.rectangle((300,250,320,340), fill=(0,0,0,255))
# tail
d.rectangle((50,180,70,190), fill=(0,0,0,255))
img.save('static/uploads/sprites/cow.png')

# Student silhouette (walking with book)
img = Image.new('RGBA', (W, H), (0,0,0,0))
d = ImageDraw.Draw(img)
# head
d.ellipse((160,30,220,90), fill=(0,0,0,255))
# body
d.rectangle((175,90,205,200), fill=(0,0,0,255))
# left leg (forward)
d.rectangle((170,200,185,320), fill=(0,0,0,255))
# right leg (back)
d.rectangle((195,220,210,320), fill=(0,0,0,255))
# left arm holding book
d.rectangle((120,110,170,140), fill=(0,0,0,255))
d.rectangle((90,120,140,150), fill=(80,80,255,255))
# right arm swinging
d.rectangle((205,110,240,140), fill=(0,0,0,255))
img.save('static/uploads/sprites/student.png')

print('Sprites generated: man.png, cow.png, student.png')