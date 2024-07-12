import os
import time
import pychromecast
from flask import Flask, send_file
import threading
import local_ip

# Configuration
CHROMECAST_NAME = 'Living Room TV'
#CHROMECAST_NAME = 'Xiaomi TV Box'
MEDIA_DIR = '/Volumes/GoPro Media/2015-01-02/HERO5 Black 1/'  # Replace with the path to your media directory
PORT = 8080
LOCAL_IP = local_ip.get_local_ip()

app = Flask(__name__)

@app.route('/media/<filename>')
def serve_file(filename):
    try:
        return send_file(os.path.join(MEDIA_DIR, filename))
    
    except Exception as e:
        return f"Error serving file: {e}", 500


def start_server():
    app.run(host='0.0.0.0', port=PORT, threaded=True)

def find_chromecast(device_name):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
    if not chromecasts:
        print(f"No Chromecast with name '{device_name}' found")
        return None
    return chromecasts[0]

def cast_media(cast, media_url, media_type):
    mc = cast.media_controller
    mc.play_media(media_url, media_type)
    mc.block_until_active()

    # Print the status of the media
    print(f"Casting to {cast.name}")
    print(f"Status: {mc.status}")

def main():
    # Start the local server in a separate thread
    threading.Thread(target=start_server).start()
    time.sleep(1)  # Give the server a second to start

    # Find the Chromecast device
    cast = find_chromecast(CHROMECAST_NAME)
    if not cast:
        return

    cast.wait()
   
    # Loop over files in the media directory
    for filename in os.listdir(MEDIA_DIR):
        file_path = os.path.join(MEDIA_DIR, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            media_type = 'image/jpeg'
        elif filename.lower().endswith(('.mp4', '.mkv', '.avi')):
            media_type = 'video/mp4'  # Adjust the MIME type if necessary
        else:
            continue  # Skip unsupported file types

        media_url = f'http://{LOCAL_IP}:{PORT}/media/{filename}'
        print(f"Casting {media_type}: {media_url}")
        cast_media(cast, media_url, media_type)

        # Wait until the current media finishes playing
        if media_type.startswith('video'):
            time.sleep(30)
            #while cast.media_controller.status.player_state == 'PLAYING':
                #time.sleep(1)
        else:
            time.sleep(5)  # Display each image for 10 seconds

if __name__ == '__main__':
    main()

