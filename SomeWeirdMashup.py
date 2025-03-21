import os

image_path = "PlankMake\\BotImages\\Rapid_Heal.png"
if os.path.exists(image_path):
    print(f"✅ Image file found: {image_path}")
else:
    print(f"❌ Image file NOT found: {image_path}")
