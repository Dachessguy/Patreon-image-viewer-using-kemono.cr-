import requests
import json
import image_viewer
import keyboard
import os

print("YOU ARE CURRENTLY USING LIST CREATORS\n")

domain = "kemono.cr"

service = input("Service: ")
user_id = input("User ID: ")

url = "https://"+domain+"/api/v1/"+service+"/user/"+user_id+"/posts"

headers = {
    "Accept": "text/css"
}

response = requests.get(url, headers=headers)
#print(response)

data = json.loads(response.text)
#print(data)

#for i, preview in enumerate(data):
    #print(f"Post {i+1}:")
    #print(f" Title: {preview["title"]}")



def clear():
    os.system("cls" if os.name == "nt" else "clear")

#---- paginate posts without link ----#

#def paginate_posts(data, page_size=5):
    #page = 0
    #max_page = (len(data) - 1) // page_size

    #while True:
        #clear()
        #print(f"Posts Page {page+1}/{max_page+1}")
        #print("-" * 40)

        # ---- only show posts from this page ----
        #start = page * page_size
        #end = start + page_size

        #for i, preview in enumerate(data[start:end], start=start):
            #print(f"Post {i+1}:")
            #print(f" Title: {preview['title']}")
            #print(f" Post ID {preview['id']}")
            #print()

        #print("↑ previous | ↓ next | q back")

        #event = keyboard.read_event()
        #if event.event_type == keyboard.KEY_DOWN:

            #if event.name == "down" and page < max_page:
                #page += 1

            #elif event.name == "up" and page > 0:
                #page -= 1

            #elif event.name == "q":
                #return  # ← go back to previous screen

#paginate_posts(data)

#-------------------------------------#

def paginate_posts(data, page_size=5):
    page = 0
    max_page = (len(data) - 1) // page_size

    while True:
        clear()
        print(f"Posts Page {page+1}/{max_page+1}")
        print("-" * 40)

        # only show posts for the current page
        start = page * page_size
        end = start + page_size
        page_items = data[start:end]

        for idx, preview in enumerate(page_items):
            print(f"{idx+1}. {preview['title']}")   # give each a number

        print("\n↑ previous | ↓ next | 1-5 select post | q back")

        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:

            # page navigation
            if event.name == "down" and page < max_page:
                page += 1
            elif event.name == "up" and page > 0:
                page -= 1
            elif event.name == "q":
                return  # go back to previous menu

            # --- selecting post (the “link”) ---
            elif event.name in ["1", "2", "3", "4", "5"]:
                num = int(event.name)
                if num <= len(page_items):
                    post = page_items[num - 1]

                    service = post["service"]
                    user_id = post["user"]
                    post_id = post["id"]
                
                    image_viewer.open_image_viewer(service, user_id, post_id) #opens image viewer

paginate_posts(data)