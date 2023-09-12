import tkinter as tk
from tkinter import messagebox
import openai
from PIL import Image, ImageTk
from io import BytesIO
import os, requests

    def __init__(self, root):
        self.root = root
        self.root.title("OpenAI Image Generator")

        # OpenAI API Key Entry
        self.api_label = tk.Label(root, text="OpenAI API Key:")
        self.api_label.pack(pady=10)
        self.api_entry = tk.Entry(root, width=50)
        self.api_entry.pack(pady=10)

        # Description Entry
        self.desc_label = tk.Label(root, text="Enter Description:")
        self.desc_label.pack(pady=10)
        self.desc_entry = tk.Entry(root, width=50)
        self.desc_entry.pack(pady=10)

        # Frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Frame for Generate Image Button
        self.generate_frame = tk.Frame(self.button_frame)
        self.generate_frame.pack(side=tk.LEFT, padx=5)
        self.generate_btn = tk.Button(self.generate_frame, text="Generate Image", command=self.generate_image)
        self.generate_btn.pack()

        # Frame for Save Image Button
        self.save_frame = tk.Frame(self.button_frame)
        self.save_frame.pack(side=tk.LEFT, padx=5)
        self.save_btn = tk.Button(self.save_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)  # Initially disabled
        self.save_btn.pack()

        # Image Label
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=20)

        

    def generate_image(self):
        api_key = self.api_entry.get()
        description = self.desc_entry.get()

        # Set the OpenAI API key
        openai.api_key = api_key

        try:
            # Generate the image using OpenAI's API
            response = openai.Image.create(
                prompt=description,
                n=1,  # Let's just get one image for simplicity
                size="1024x1024"
            )

            # Extracting image URL from the response
            image_url = response.data[0]['url']

            # Fetch the image from the URL
            image_response = requests.get(image_url)
            image_response.raise_for_status()  # Raise an error for bad responses

            self.current_image = Image.open(BytesIO(image_response.content))  # Store the image in the current_image attribute
            photo = ImageTk.PhotoImage(self.current_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate image. Error: {e}")

        # Enable the save button once an image is generated
        self.save_btn.config(state=tk.NORMAL)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.current_image.save(file_path)  # Assuming you've stored the PIL Image object in self.current_image


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenAIApp(root)
    root.mainloop()
