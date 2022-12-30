import tkinter as tk
from io import BytesIO

import requests
from PIL import Image, ImageTk
import json

"""
FYI THIS WAS MOSTLY CREATED USING CHATGPT SO DON'T EXPECT IT TO BE GOOD QUALITY
"""
# Open the JSON file and load the data
with open("src.json", "r") as f:
    data = json.load(f)
# Create the main window
root = tk.Tk()
root.title("Image Classification")

# Create the label to display the image
image_label = tk.Label(root)
image_label.pack()


# Function to display the image and allow the user to select the categories
def classify_image(data, image_obj, index):
    # Download the image and convert it to a PhotoImage object
    response = requests.get(image_obj["src"])
    image = Image.open(BytesIO(response.content))
    image = ImageTk.PhotoImage(image)
    # Update the label with the new image
    image_label.config(image=image)
    image_label.image = image
    # Create the checkboxes for selecting categories
    dog_var = tk.IntVar()
    nature_var = tk.IntVar()
    assorted_var = tk.IntVar()
    dog_checkbox = tk.Checkbutton(root, text="Dog", variable=dog_var)
    nature_checkbox = tk.Checkbutton(root, text="Nature", variable=nature_var)
    assorted_checkbox = tk.Checkbutton(root, text="Assorted", variable=assorted_var)
    dog_checkbox.pack()
    nature_checkbox.pack()
    assorted_checkbox.pack()
    # Create the submit button
    submit_button = tk.Button(root, text="Submit",
                              command=lambda: update_categories(data, dog_var, nature_var, assorted_var, image_obj,
                                                                index,
                                                                dog_checkbox, nature_checkbox, assorted_checkbox,
                                                                submit_button))
    submit_button.pack()


# Function to update the categories in the JSON object and write the data back to the file
def update_categories(data, dog_var, nature_var, assorted_var, image_obj, index, dog_checkbox, nature_checkbox,
                      assorted_checkbox, submit_button):
    categories = []
    if dog_var.get() == 1:
        categories.append("dog")
    if nature_var.get() == 1:
        categories.append("nature")
    if assorted_var.get() == 1:
        categories.append("assorted")
    # Update the categories in the JSON object
    image_obj["category"] = categories
    data[index] = image_obj
    # Write the data back to the file
    with open("src.json", "w") as f:
        json.dump(data, f)
    # Remove the checkboxes and button from the window
    dog_checkbox.destroy()
    nature_checkbox.destroy()
    assorted_checkbox.destroy()
    submit_button.destroy()
    # Classify the next image in the data
    index += 1
    if index <= len(data) - 1:
        classify_image(data, data[index], index)
    else:
        tk.Label(root, text="No more images to classify").pack()


# Classify datathe first image in the JSON data
classify_image(data, data[0], 0)

# Run the main loop
root.mainloop()
