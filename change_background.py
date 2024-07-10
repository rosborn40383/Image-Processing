import ctypes
import os
import random
from PIL import Image
from screeninfo import get_monitors

def set_wallpaper(image_path, monitor_index):
    # Open the image and resize it to the monitor's resolution
    monitor = get_monitors()[monitor_index]
    img = Image.open(image_path)
    img = img.resize((monitor.width, monitor.height), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
    temp_image_path = f"temp_wallpaper_{monitor_index}.bmp"
    img.save(temp_image_path, "BMP")

    # Set the wallpaper using the Windows API
    ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(temp_image_path), 3)

    # Delete the temporary BMP file after setting the wallpaper
    os.remove(temp_image_path)

def main():
    image_folder = r'C:\Users\richard.osborn\64bit\image_proccessing\described'
    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith('.png')]

    # Get the list of monitors
    monitors = get_monitors()

    # Randomly select an image for each monitor
    for i in range(len(monitors)):
        selected_image = random.choice(image_files)
        set_wallpaper(selected_image, i)

if __name__ == "__main__":
    main()
