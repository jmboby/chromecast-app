import os
import time
from PIL import Image


# Function to display an image
def cast_image(image_path):
    image = Image.open(image_path)
    image.show()

def main():
    photo_dir = '/Volumes/GoPro Media/iMac Export Max Quality/4 January 2008/'  # Replace with your photo directory
    
    # Iterate over files in the media directory
    for filename in os.listdir(photo_dir):
        file_path = os.path.join(photo_dir, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Displaying image: {file_path}")
            cast_image(file_path)
            time.sleep(10)  # Display each image for 10 seconds
        elif filename.lower().endswith(('.mp4', '.mkv', '.avi')):
            print(f"Displaying video: {file_path}")
            #//TODO

    print("Finished casting media.")

if __name__ == "__main__":
    main()