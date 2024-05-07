import tkinter as tk
from PIL import Image, ImageTk
import os

class ImageSwitcher(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Pip-Boy 3000")
        
        # Initial image and index setup
        self.current_image_index = 0
        self.image_folder = "images"
        self.images = [img for img in os.listdir(self.image_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        
        self.load_images()
        
        # Get the maximum dimensions of all images
        max_width = max(max(img.width() for img in img_list) for img_list in self.image_objects)
        max_height = max(max(img.height() for img in img_list) for img_list in self.image_objects)
        
        # Create a label to display the image
        self.image_label = tk.Label(self, width=max_width, height=max_height)
        self.image_label.pack()
        self.image_label.config(image=self.image_objects[self.current_image_index][0])
        
        # Start the animation
        self.animate()
        
        # Bind mouse scroll to switch between images and bind left mouse click to switch image on specific areas
        self.image_label.bind("<MouseWheel>", self.on_scroll)
        self.image_label.bind("<Button-1>", self.on_click)
        
    # Loads images, and if a .gif, loads and animates
    def load_images(self):
        self.image_objects = []
        for img_file in self.images:
            img_path = os.path.join(self.image_folder, img_file)
            if img_path.lower().endswith('.gif'):
                gif = Image.open(img_path)
                frames = []
                try:
                    while True:
                        frame = ImageTk.PhotoImage(gif.copy().resize((1200, 675)))  # Dimension of initial gif for uniformity
                        frames.append(frame)
                        gif.seek(len(frames))  
                except EOFError:
                    pass 
                self.image_objects.append(frames)
            else:
                # Load static image
                img = Image.open(img_path)
                img_resized = img.resize((1200, 675))
                self.image_objects.append([ImageTk.PhotoImage(img_resized)])
        
    # Functionality for clicking to switch between images
    def on_click(self, event):
        x, y = event.x, event.y
        if 450 < x < 550 and 65 < y < 100 and self.current_image_index == 0:
            self.current_image_index = 5
        elif 200 < x < 300 and 65 < y < 100 and 4 < self.current_image_index < 12:
            self.current_image_index = 0
        elif 4 < self.current_image_index < 12 and 700 > x > 200:
            if 100 < y < 200:
                self.current_image_index = 5
            elif 190 < y < 225:
                self.current_image_index = 6
            elif 230 < y < 265:
                self.current_image_index = 7
            elif 270 < y < 305:
                self.current_image_index = 8
            elif 310 < y < 345:
                self.current_image_index = 10
            elif 350 < y < 385:
                self.current_image_index = 9
            elif 390 < y < 425:
                self.current_image_index = 11
        elif 575 < x < 650 and 65 < y < 100 and self.current_image_index == 1:
            self.current_image_index = 12

        self.image_label.config(image=self.image_objects[self.current_image_index][0])
        self.animate()

        
    # Functionality for scrolling to switch between images
    def on_scroll(self, event):
        # Scroll up to switch to the next image
        if event.delta > 0:
            self.current_image_index = (self.current_image_index + 1) % 5
        # Scroll down to switch to the previous image
        else:
            self.current_image_index = (self.current_image_index - 1) % 5
            
        self.image_label.config(image=self.image_objects[self.current_image_index][0])
        self.animate()

    # GIF animation functionality
    def animate(self, frame=0):
        if len(self.image_objects[self.current_image_index]) > 1:
            frame %= len(self.image_objects[self.current_image_index])
            self.image_label.config(image=self.image_objects[self.current_image_index][frame])
            frame += 1
            self.after(100, lambda: self.animate(frame))
        else:
            self.after(100, self.animate)

# Loops program indefinitely
if __name__ == "__main__":
    app = ImageSwitcher()
    app.mainloop()
