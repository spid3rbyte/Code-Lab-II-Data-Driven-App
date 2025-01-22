from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Root window setup
root = Tk()
root.title("Data Driven App")
root.geometry("1118x688")

# Function to fetch Pokémon data
def pokemon_data(pokemon_name):
    """Fetch data from the PokéAPI based on Pokémon name or ID."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to switch frames
def switch_frame(frame):
    """Switch to a different frame."""
    frame.tkraise()

# Function to search for a Pokémon and display details
def search_pokemon():
    """Fetch and display Pokémon details based on user input."""
    pokemon_name = entry.get().strip()
    if not pokemon_name:
        result_label.config(text="Please enter a Pokémon name or ID.")
        return

    data = pokemon_data(pokemon_name)
    if "error" in data:
        result_label.config(text=f"Error: {data['error']}")
        sprite_label.config(image="")  # Clear image if there's an error
        return

    # Extract Pokémon details
    name = data["name"].capitalize()
    types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
    abilities = ", ".join(a["ability"]["name"].capitalize() for a in data["abilities"])
    stats = {stat["stat"]["name"].capitalize(): stat["base_stat"] for stat in data["stats"]}

    # Display details
    details = (f"Name: {name}\nType(s): {types}\nAbilities: {abilities}\n"
               f"Stats:\n{stats}")
    result_label.config(text=details)

    # Load and display sprite image
    sprite_url = data["sprites"]["front_default"]
    if sprite_url:
        sprite_response = requests.get(sprite_url)
        sprite_image = Image.open(BytesIO(sprite_response.content))
        sprite_photo = ImageTk.PhotoImage(sprite_image)
        sprite_label.config(image=sprite_photo)
        sprite_label.image = sprite_photo  # Prevent garbage collection
    else:
        sprite_label.config(image="")

# Create the main frames
home_frame = Frame(root)
home_frame.place(relwidth=1, relheight=1)

# image for the home frame
bg_image_home = Image.open("pokemon2.png")  
bg_photo_home = ImageTk.PhotoImage(bg_image_home)

bg_label_home = Label(home_frame, image=bg_photo_home)
bg_label_home.place(relwidth=1, relheight=1)

# search input
entry = Entry(home_frame, 
              font=("Arial", 16), 
              width=35, 
              bg="#FFEDED")
entry.place(x=550, y=234, anchor=CENTER)

# search button
search_button = Button(home_frame, 
                       text="search", 
                       font=("Arial", 14), 
                       command=search_pokemon, 
                       bg="#FFEDED")
search_button.place(x=835, y=234, anchor=CENTER)

# Label to display Pokémon sprite
sprite_label = Label(home_frame)
sprite_label.place(relx=0.5, rely=0.4, anchor=CENTER)

# Label to display Pokémon details
result_label = Label(home_frame, text="", font=("Arial", 14), justify=LEFT, wraplength=500)
result_label.place(relx=0.5, rely=0.6, anchor=CENTER)

# Raise the home frame to display it
switch_frame(home_frame)

# Run the GUI
root.mainloop()
