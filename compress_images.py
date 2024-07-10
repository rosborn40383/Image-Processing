from PIL import Image
import os

def compress_image(input_path, output_path, quality=85):
    # Open an image file
    with Image.open(input_path) as img:
        # Convert to RGB if necessary
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        # Save the image with the specified quality
        img.save(output_path, "JPEG", quality=quality)

def compress_images_in_directory(directory, output_directory, quality=85):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, f'compressed_{filename[:-4]}.jpg')
            compress_image(input_path, output_path, quality)
            print(f'Compressed {filename} and saved as {output_path}')

if __name__ == "__main__":
    directory = r'J:\Investments\Richard\Random Graphics\Background'  # Replace with your directory
    output_directory = os.path.join(directory, 'compressed')
    compress_images_in_directory(directory, output_directory, quality=85)
