import hashlib
from PIL import Image
import os

# Function to calculate SHA-256 hash of an image
def image_to_hash(image_path):
    # Open the image file in binary mode ('rb')
    with open(image_path, 'rb') as image_file:
        # Read the file content as binary
        image_data = image_file.read()
        
        # Calculate SHA-256 hash
        sha256_hash = hashlib.sha256(image_data).hexdigest()
    
    return sha256_hash

# Set the directory where the images are located
image_directory = r'C:\Users\drago\Downloads\Desktop\folder\Image'

# Prompt the user to input the image file name
image_name = input("Enter the image file name (e.g., Paper.png): ")

# Construct the full image path by combining the directory and file name
image_path = os.path.join(image_directory, image_name)

# Check if the file exists
if not os.path.exists(image_path):
    print(f"Error: The file '{image_name}' does not exist in the specified directory.")
else:
    # Get the hash of the image
    image_hash = image_to_hash(image_path)

    # Print the SHA-256 hash
    print(f"SHA-256 Hash of the Image: {image_hash}")

    # Display the image using PIL
    try:
        image = Image.open(image_path)
        image.show()  # This will open the image in the default image viewer
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
        
def generate_hashes_for_directory(directory):
    image_hashes = {}
    
    # Loop over all files in the directory
    for image_name in os.listdir(directory):
        image_path = os.path.join(directory, image_name)
        
        # Only process files that are images (you can extend this check)
        if os.path.isfile(image_path) and image_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            # Calculate hash for each image
            image_hash = image_to_hash(image_path)
            image_hashes[image_hash] = image_name  # Map hash to image name
    
    return image_hashes

# Generate the image hashes for the given directory
image_hashes = generate_hashes_for_directory(image_directory)

# Ask user for the hash to search
user_input_hash = input("Enter the SHA-256 hash of the image: ")

# Check if the entered hash exists in the hash dictionary
if user_input_hash in image_hashes:
    # If hash exists, get the image name
    image_name = image_hashes[user_input_hash]
    image_path = os.path.join(image_directory, image_name)

    # Display the image using PIL
    try:
        image = Image.open(image_path)
        image.show()  # This will open the image in the default image viewer
        print(f"Image '{image_name}' displayed successfully.")
    except Exception as e:
        print(f"An error occurred while opening the image: {e}")
else:
    print("No image found with the specified hash.")
