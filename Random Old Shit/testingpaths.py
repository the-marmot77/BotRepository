import os
import pyautogui
import time

# Change this to the image filename you want to test
IMAGE_NAME = "MahogPlank.png"

# Get the full path to the image file
image_path = os.path.join(os.getcwd(), IMAGE_NAME)

def verify_image_path(image):
    """Check if the image file exists and print its absolute path."""
    if os.path.exists(image):
        print(f"✅ Image file found: {image}")
        return True
    else:
        print(f"❌ ERROR: Image file '{image}' NOT found in {os.getcwd()}")
        return False

def search_for_image(image):
    """Attempt to locate the image on the screen and print the result."""
    print("🔍 Searching for the image on screen...")
    
    # Pause briefly to allow user to adjust the screen
    time.sleep(2)

    found_location = pyautogui.locateOnScreen(image, confidence=0.6)
    
    if found_location:
        print(f"✅ Image found at: {found_location}")
    else:
        print(f"❌ Image '{image}' NOT found on the screen. Try adjusting confidence or recapturing the image.")

if __name__ == "__main__":
    print("🔎 Running image verification test...\n")
    
    if verify_image_path(image_path):
        search_for_image(image_path)
    
    print("\n✅ Test complete.")
