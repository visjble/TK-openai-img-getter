import tkinter as tk
from tkinter import filedialog, messagebox
import openai
from PIL import Image, ImageTk
from io import BytesIO
import os
import requests

class OpenAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenAI Image Generator")

        self.root.geometry("512x800")
        self.root.configure(bg="#2E2E2E")  # Dark gray background

        # Frame for API Key with dark gray background
        api_frame = tk.Frame(root, bg="#2E2E2E")
        api_frame.pack(pady=10, fill=tk.X)

        # OpenAI API Key Entry with light gray text
        self.api_label = tk.Label(api_frame, text="OpenAI API Key:", width=15, bg="#2E2E2E", fg="#D8D8D8")
        self.api_label.pack(side=tk.LEFT, padx=5)
        self.api_entry = tk.Entry(api_frame, width=50, show="*", bg="#3C3C3C", fg="#D8D8D8")
        self.api_entry.pack(side=tk.RIGHT, padx=5)

        # Frame for Description with dark gray background
        desc_frame = tk.Frame(root, bg="#2E2E2E")
        desc_frame.pack(pady=10, fill=tk.X)

        # Description Entry with light gray text
        self.desc_label = tk.Label(desc_frame, text="Prompt:", width=15, bg="#2E2E2E", fg="#D8D8D8")
        self.desc_label.pack(side=tk.LEFT, padx=5)
        self.desc_entry = tk.Entry(desc_frame, width=50, bg="#3C3C3C", fg="#D8D8D8")
        self.desc_entry.pack(side=tk.RIGHT, padx=5)

        

        # Bind the Enter key to the generate_image function
        self.api_entry.bind('<Return>', self.generate_image)


        # Frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        # Frame for Generate Image Button
        self.generate_frame = tk.Frame(self.button_frame)
        self.generate_frame.pack(side=tk.LEFT, padx=5)
        self.generate_btn = tk.Button(self.generate_frame, text="Generate Image", command=self.generate_image, bg="#4B4B4B", fg="#D8D8D8", activebackground="#5A5A5A", activeforeground="#D8D8D8")
        self.generate_btn.pack(pady=5)

        # Frame for Save Image Button
        self.save_frame = tk.Frame(self.button_frame)
        self.save_frame.pack(side=tk.LEFT, fill=tk.X, padx=5)
        self.save_btn = tk.Button(self.save_frame, text="Save Image", command=self.save_image, state=tk.DISABLED, bg="#4B4B4B", fg="#D8D8D8", activebackground="#5A5A5A", activeforeground="#D8D8D8")  # Initially disabled
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
    root.geometry("512x800")
    app = OpenAIApp(root)
    root.mainloop()
