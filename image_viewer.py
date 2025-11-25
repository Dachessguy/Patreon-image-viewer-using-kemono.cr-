import requests
import json
import cv2
import os
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import hashlib

MAX_WIDTH = 1280
MAX_HEIGHT = 720
CACHE_FOLDER = 'cache'

if not os.path.exists(CACHE_FOLDER):
    os.makedirs(CACHE_FOLDER)

def url_to_filename(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest() + '.jpg'

def resize_image(img):
    width, height = img.size
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        aspect_ratio = width / height
        if width > height:
            new_width = MAX_WIDTH
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = MAX_HEIGHT
            new_width = int(new_height * aspect_ratio)
        img = img.resize((new_width, new_height), Image.Resampling.NEAREST)
    return img

def cache_all_images(image_urls):
    cached_images = []
    for url in image_urls:
        filename = url_to_filename(url)
        filepath = os.path.join(CACHE_FOLDER, filename)

        if not os.path.exists(filepath):
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = resize_image(img)
            img.save(filepath)

        cached_images.append(filepath)
    return cached_images

class ImageViewer(tk.Tk):
    def __init__(self, image_urls):
        
        #self.title(data["post"]["title"])
        
        super().__init__()

        self.image_urls = image_urls
        self.current_index = 0
        self.cached_images = cache_all_images(image_urls)

        self.img = Image.open(self.cached_images[self.current_index])
        self.img_tk = ImageTk.PhotoImage(self.img)

        self.geometry(f"{self.img.width}x{self.img.height}")
        self.label = tk.Label(self, image=self.img_tk)
        self.label.pack()

        self.prev_button = tk.Button(self, text="←", command=self.show_prev, font=('Arial', 20))
        self.prev_button.place(relx=0.05, rely=0.5, anchor='center')

        self.next_button = tk.Button(self, text="→", command=self.show_next, font=('Arial', 20))
        self.next_button.place(relx=0.95, rely=0.5, anchor='center')

        self.counter_label = tk.Label(self, text=f"{self.current_index + 1}/{len(self.cached_images)}", font=('Arial', 12))
        self.counter_label.place(relx=0.5, rely=0.9, anchor='center')

        self.title("Image Viewer")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()

    def show_prev(self):
        self.current_index = (self.current_index - 1) % len(self.cached_images)
        self.update_image()

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.cached_images)
        self.update_image()

    def update_image(self):
        self.img = Image.open(self.cached_images[self.current_index])
        self.img_tk = ImageTk.PhotoImage(self.img)
        self.label.config(image=self.img_tk)
        self.label.image = self.img_tk
        self.counter_label.config(text=f"{self.current_index + 1}/{len(self.cached_images)}")

    def on_close(self):
        for filename in os.listdir(CACHE_FOLDER):
            file_path = os.path.join(CACHE_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        self.destroy()

# --------- PUBLIC FUNCTION TO CALL FROM PAGINATION -------- #

def open_image_viewer(service, user_id, post_id):
    service = service.strip()
    user_id = str(user_id).strip()
    post_id = str(post_id).strip()

    url = f"https://kemono.cr/api/v1/{service}/user/{user_id}/post/{post_id}"
    
    os.system("cls" if os.name == "nt" else "clear")
    
    print("[DEBUG] Fetching:", url)

    headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/css"
    }

    response = requests.get(url, headers=headers)

    print("[DEBUG] STATUS:", response.status_code)
    #print("[DEBUG] CONTENT-TYPE:", response.headers.get("content-type"))
    #print("[DEBUG] BODY:", response.text[:200])


    if response.status_code != 200:
        print("[ERROR] Status:", response.status_code)
        print("Response:", response.text[:300])
        return
        
        
    data = response.json()

    print("[DEBUG] PREVIEW COUNT:", len(data.get("previews", [])))
    
    print("LOADING IMAGES . . . ")
    
    # Extract URLs
    image_urls = [img["path"] for img in data.get("previews", [])]

    # Full absolute URLs
    base = "https://kemono.cr"
    image_urls = [base + u for u in image_urls]

    #print("[DEBUG] IMAGE URLS:", image_urls)

    # Open viewer
    ImageViewer(image_urls)

