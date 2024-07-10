import os
import shutil
import tensorflow as tf
import numpy as np
from PIL import Image
import tensorflow_hub as hub

print("Loading model...")
# Load the pre-trained model
model = hub.load("https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/5")
print("Model loaded successfully.")

# Load labels
labels_path = tf.keras.utils.get_file('ImageNetLabels.txt', 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())
print("Labels loaded successfully.")

def describe_image(image_path):
    print(f"Describing image: {image_path}")
    img = Image.open(image_path).resize((224, 224)).convert('RGB')
    img_array = np.array(img) / 255.0
    img_array = img_array[np.newaxis, ...].astype(np.float32)  # Ensure the array is of dtype float32

    # Run the image through the model
    predictions = model(img_array)
    predictions_np = predictions.numpy()  # Convert the tensor to a NumPy array
    predicted_index = np.argmax(predictions_np, axis=-1)
    predicted_label = imagenet_labels[predicted_index][0]

    # Return top 3 predictions
    top_3_indices = predictions_np[0].argsort()[-3:][::-1]
    top_3_labels = [imagenet_labels[i] for i in top_3_indices]
    print(f"Predicted label: {predicted_label}, Top 3 labels: {top_3_labels}")
    return predicted_label, top_3_labels

def copy_images_with_descriptions(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    print(f"Processing images in directory: {directory}")

    for filename in os.listdir(directory):
        if filename.lower() == 'thumbs.db':
            continue  # Skip Thumbs.db file
        print(f"Found file: {filename}")
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(directory, filename)
            print(f"Processing image: {input_path}")
            try:
                predicted_label, top_3_labels = describe_image(input_path)
                new_filename = f"{predicted_label}_{'_'.join(top_3_labels)}.png"
                output_path = os.path.join(output_directory, new_filename)
                shutil.copy(input_path, output_path)
                print(f"Copied {input_path} to {output_path}")
            except Exception as e:
                print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    directory = r'C:\Users\first.last\64bit\image_proccessing\compressed'
    output_directory = r'C:\Users\first.last\64bit\image_proccessing\described'
    print(f"Starting copying process. Input directory: {directory}, Output directory: {output_directory}")
    copy_images_with_descriptions(directory, output_directory)
    print("Copying process completed.")
