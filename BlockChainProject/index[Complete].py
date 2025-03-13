import hashlib
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pyperclip  # Used for copying to the clipboard
from PIL import Image, ImageTk

# Function to calculate SHA-256 hash of an image
def image_to_hash(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        sha256_hash = hashlib.sha256(image_data).hexdigest()
    return sha256_hash

# Function to open the file dialog and load an image
def load_image():
    global image_path
    # Ask user to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    
    if file_path:
        image_path.set(file_path)  # Update the StringVar
        # Display the image hash
        display_image_hash(file_path)
        show_image(file_path)

# Function to display the SHA-256 hash of the selected image
def display_image_hash(image_path):
    image_hash = image_to_hash(image_path)
    hash_label.configure(text=f"SHA-256 Hash: {image_hash}")
    image_hash_entry.delete(0, 'end')
    image_hash_entry.insert(0, image_hash)

# Function to display the image in the Tkinter window
def show_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((250, 250), Image.Resampling.LANCZOS)  # Resize image to fit in the window
        img_tk = ImageTk.PhotoImage(img)
        image_label.configure(image=img_tk)
        # image_label.image = img_tk  # Keep a reference to the image
    except Exception as e:
        messagebox.showerror("Error", f"Error opening image: {e}")

# Function to search for an image using its hash
def search_image_by_hash():
    user_hash = image_hash_entry.get()
    
    if not user_hash:
        messagebox.showerror("Error", "Please enter a hash value.")
        return
    
    found_image = None
    
    # Loop through all images in the directory to find a match
    for image_name in os.listdir(image_directory):
        image_path = os.path.join(image_directory, image_name)
        
        if os.path.isfile(image_path) and image_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
            image_hash = image_to_hash(image_path)
            
            if image_hash == user_hash:
                found_image = image_path
                break
    
    if found_image:
        show_image(found_image)
        messagebox.showinfo("Success", f"Image found: {os.path.basename(found_image)}")
    else:
        messagebox.showerror("Not Found", "No image found with the specified hash.")

# ----------------------------------------------------------------------------------------------------------------------------------------- #

# Function to copy the hash to the clipboard
def copy_hash():
    hash_value = image_hash_entry.get()
    if hash_value:
        pyperclip.copy(hash_value)  # Copy the hash to clipboard
        messagebox.showinfo("Success", "Hash copied to clipboard!")
    else:
        messagebox.showerror("Error", "No hash to copy.")

# Function to paste the hash from the clipboard
def paste_hash():
    hash_value = pyperclip.paste()  # Get text from clipboard
    if hash_value:
        image_hash_entry.delete(0, 'end')
        image_hash_entry.insert(0, hash_value)  # Paste it into the entry field
    else:
        messagebox.showerror("Error", "No hash found in clipboard.")

# Function to clear the hash in the entry field
def clear_hash():
    image_hash_entry.delete(0, 'end')  # Clear the text field
    hash_label.configure(text=f"SHA-256 Hash: ")
    image_label.configure(image=None)
    
# -------------------------------------------------------------------------------------------------------------------------------------------------    
    
    

# GUI Setup
app = ctk.CTk()  # Create the CTk window
app.title("Image Hash and Viewer")
app.geometry("500x700")
ctk.set_appearance_mode("dark")  # Set appearance mode

# Global variables
image_path = ctk.StringVar()  # Corrected StringVar usage

# UI Elements
ctk.CTkLabel(app, text="Select an Image and Generate Hash", font=("Arial", 14)).pack(pady=10)

# Button to load the image
load_image_button = ctk.CTkButton(app, text="Load Image", command=load_image, font=("Arial", 12), corner_radius=32)
load_image_button.pack(pady=10)

# Label to display the image hash
hash_label = ctk.CTkLabel(app, text="SHA-256 Hash: ", font=("Arial", 12),corner_radius=5,fg_color="white",text_color="black")
hash_label.pack(pady=10)

# Entry field for the image hash (also for searching by hash)
image_hash_entry = ctk.CTkEntry(app, width=40, font=("Arial", 12))
image_hash_entry.pack(pady=10)

# Button to search for image by hash
search_button = ctk.CTkButton(
    app, 
    text="Search Image by Hash", 
    command=search_image_by_hash, 
    font=("Arial", 12), 
    corner_radius=10,  # Optional: Adds rounded corners
    fg_color="SpringGreen4",  # Optional: Set the button color
    width=200  # Optional: Set button width
)
search_button.pack(pady=10)

# Buttons for Copy, Paste, and Clear functionality
copy_button = ctk.CTkButton(
    app, 
    text="Copy Hash", 
    command=copy_hash, 
    font=("Arial", 12), 
    corner_radius=10,
    fg_color="royalblue"
)
copy_button.pack(pady=5)

paste_button = ctk.CTkButton(
    app, 
    text="Paste Hash", 
    command=paste_hash, 
    font=("Arial", 12), 
    corner_radius=10,
    fg_color="DarkGoldenrod3"
)
paste_button.pack(pady=5)

clear_button = ctk.CTkButton(
    app, 
    text="Clear Hash", 
    command=clear_hash, 
    font=("Arial", 12), 
    corner_radius=10,
    fg_color="tomato3"
)
clear_button.pack(pady=5)

# Label to display the image
image_label = ctk.CTkLabel(app,text="")
image_label.pack(pady=20)

# Set the directory where the images are located (change this as needed)
image_directory = r'C:\Users\drago\Downloads\Desktop\folder\Image'

# Run the CTk main loop
app.mainloop()
