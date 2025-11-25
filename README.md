📦 Patreon-Image-Viewer

Patreon-Image-Viewer is a Python tool for browsing Kemono posts with a smooth paginated interface and an advanced Tkinter-based image viewer.
It makes navigating large creator archives easy by showing posts in pages, caching images locally, and providing fast, simple navigation.

✨ Features
🔹 Post Pagination

View posts in pages with a clean console UI

Navigate using:

↑ / ↓ — Scroll through pages

Number keys — Open a post

Q — Go back to the previous screen

🔹 Kemono API Integration

Fetches full post data from:

https://kemono.cr/api/v1/<service>/user/<user_id>/post/<post_id>


Supports:

Patreon

-- working on OF

🔹 Tkinter Image Viewer

Navigate attachments using onscreen arrows

Resizes images to max 1280×720

Displays counters like 2 / 14

Cleans up cached images automatically

Window title updates dynamically

🔹 Loading Screen

A separate Tkinter loading window is displayed while images are being cached.

🔹 Smart Caching

Downloads each attachment only once

Saves images to /cache/

Removes temporary files on close

🛠 Installation
1. Clone the Repository
git clone https://github.com/yourusername/Patreon-image-viewer.git
cd Patreon-image-viewer

2. Install Dependencies
pip install -r requirements.txt


Dependencies include:

requests

Pillow

tkinter (preinstalled on Windows/Linux)

hashlib

opencv-python (optional)

▶️ Usage

Start the pagination browser:

python list_creators.py


Scroll through posts

Select a post by number

A loading screen appears

The image viewer opens when caching is complete

📁 Project Structure
Patreon-image-viewer/
 ├── list_creators.py        # Post browsing + pagination
 ├── image_viewer.py         # Tkinter image viewer + caching
 ├── post_image.py           # image_viewer but for the list_creators program
 ├── main.py                 # main program to run to use UI
 ├── cache/                  # Auto-generated image cache
 └── README.md

🧠 How It Works
1. Pagination

Prints posts page-by-page and waits for user input to switch pages or open a post.

2. API Fetch

Uses custom headers to bypass Kemono's scraper protections:

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/css"
}

3. Download + Cache

All images from a selected post are downloaded once, resized, and saved to /cache/.

4. Image Viewer

A Tkinter window displays cached images with arrow-button navigation and a dynamic window title.

5. Cleanup

When the viewer closes, the cache folder is emptied to prevent storage buildup.

⚠ Disclaimer

This tool interacts with Kemono’s publicly available API endpoints.
Users are responsible for following all applicable laws and terms of service.
This project is for educational purposes only.

💡 Future Plans

Optional persistent cache

Bulk post/image downloads

Thumbnail grid view

Sorting and filtering options

Dark mode for the viewer

🤝 Contributing

Contributions are welcome!
Submit a pull request or open an issue with suggestions or bug reports.

📄 License

MIT License — free to use and modify.
