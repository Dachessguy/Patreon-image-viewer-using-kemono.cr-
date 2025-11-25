import requests
import json
import cv2

import os
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import hashlib

# Maximum width and height for resizing
MAX_WIDTH = 1280
MAX_HEIGHT = 720

# Cache folder path
CACHE_FOLDER = 'cache'

# Ensure the cache folder exists
if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)



print("Only patreon and Onlyfans is supported currently")


domain = "kemono.cr"

service = input("Service: ")
user_id = input("User ID: ")
post_id = input("Post ID: ")

url = "https://"+domain+"/api/v1/"+service+"/user/"+user_id+"/post/"+post_id

headers = {
    "Accept": "text/css"
}

response = requests.get(url, headers=headers)

data = json.loads(response.text)

#-----simple 1 image-----
#server_url = data["previews"][0]["server"]
#path_url = data["previews"][0]["path"]

#print(server_url + "/data" + path_url)

#-----displays all info for previews-----
#for i, preview in enumerate(data["previews"]):
    #print(f"Image {i+1}:")
    #print(f"  Type: {preview['type']}")
    #print(f"  Server: {preview['server']}")
    #print(f"  Name: {preview['name']}")
    #print(f"  Path: {preview['path']}\n")
    
image_urls = []
    
for preview in data["previews"]:
    preview["full_url"] = preview["server"] + "/data" + preview["path"]

for i, preview in enumerate(data["previews"]):
    print(f"Attachment {i+1}: {preview['full_url']}")
    image_urls.append(preview['full_url'])


# Function to create a unique filename based on URL
def url_to_filename(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest() + '.jpg'

# Function to download, resize and cache all images at once
def cache_all_images(image_urls):
    cached_images = []
    
    for url in image_urls:
        # Create a unique filename for the image based on its URL
        filename = url_to_filename(url)
        filepath = os.path.join(CACHE_FOLDER, filename)

        # Check if the image is already in the cache
        if not os.path.exists(filepath):
            # If not in cache, download, process, and cache it
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            # Resize the image
            img = resize_image(img)
            
            # Save the image to cache
            img.save(filepath)
        
        # Load the image from cache
        cached_images.append(filepath)
    
    return cached_images

# Function to resize the image while maintaining the aspect ratio
def resize_image(img):
    width, height = img.size

    # Calculate the scaling factor based on the maximum dimensions
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        aspect_ratio = width / height
        if width > height:
            new_width = MAX_WIDTH
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = MAX_HEIGHT
            new_width = int(new_height * aspect_ratio)

        # Use NEAREST or BILINEAR for faster resizing
        img = img.resize((new_width, new_height), Image.Resampling.NEAREST)
    
    return img

# Class for the Image Viewer
class ImageViewer(tk.Tk):
    def __init__(self, image_urls):
        super().__init__()

        self.image_urls = image_urls
        self.current_index = 0
        
        # Cache all images at once
        self.cached_images = cache_all_images(image_urls)
        
        # Load the first image from the cache
        self.img = Image.open(self.cached_images[self.current_index])
        self.img_tk = ImageTk.PhotoImage(self.img)
        
        # Set window size based on the image size
        self.window_width = self.img.width
        self.window_height = self.img.height
        self.geometry(f"{self.window_width}x{self.window_height}")
        
        # Create the label for the image
        self.label = tk.Label(self, image=self.img_tk)
        self.label.pack()

        # Create the navigation buttons (they will stay on top of the image)
        self.prev_button = tk.Button(self, text="←", command=self.show_prev, font=('Arial', 20))
        self.prev_button.place(relx=0.05, rely=0.5, anchor='center')

        self.next_button = tk.Button(self, text="→", command=self.show_next, font=('Arial', 20))
        self.next_button.place(relx=0.95, rely=0.5, anchor='center')

        # Create the counter label (like "3/15")
        self.counter_label = tk.Label(self, text=f"{self.current_index + 1}/{len(self.cached_images)}", font=('Arial', 12))
        self.counter_label.place(relx=0.5, rely=0.9, anchor='center')

        # Window settings
        self.title("Image Viewer")

        # When the program exits, delete cached images
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.mainloop()

    def show_prev(self):
        """Show the previous image"""
        self.current_index = (self.current_index - 1) % len(self.cached_images)
        self.update_image()

    def show_next(self):
        """Show the next image"""
        self.current_index = (self.current_index + 1) % len(self.cached_images)
        self.update_image()

    def update_image(self):
        """Update the image displayed in the window"""
        self.img = Image.open(self.cached_images[self.current_index])
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.label.config(image=self.img_tk)
        self.label.image = self.img_tk  # Keep a reference to the image
        
        # Update the counter label with the new image index
        self.counter_label.config(text=f"{self.current_index + 1}/{len(self.cached_images)}")

    def on_close(self):
        """Clean up by deleting all cached images when the program closes"""
        for filename in os.listdir(CACHE_FOLDER):
            file_path = os.path.join(CACHE_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
        
        # Now close the application
        self.destroy()


# Create and run the Image Viewer
image_viewer = ImageViewer(image_urls)
