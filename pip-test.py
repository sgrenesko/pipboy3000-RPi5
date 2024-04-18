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
        self.images = os.listdir(self.image_folder)
        
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
        
        # Bind mouse scroll to switch between image1 and image2 and bind left mouse click to switch image on specific areas
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
        
    #Functionality for clicking to switch between sub menus
    def on_click(self, event):
        #Check if click is on the "SPECIAL" tab of the STATS menu or the Strength sub tab then switches accordingly
        if (event.x > 450 and event.x < 550 and event.y > 65 and event.y < 100 and self.current_image_index == 0) or (event.x > 200 and event.x < 525 and event.y < 200 and event.y > 100 and self.current_image_index == 6):
            self.current_image_index = 5
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
        #Check if click is on the Perception sub tab then switches accordingly
        elif event.x > 200 and event.x < 700 and event.y < 300 and event.y > 200 and self.current_image_index == 5:
            self.current_image_index = 6
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
    
    #Fucntionality for scrolling to switch between menus
    def on_scroll(self, event):
        # Scroll up to switch to the next image
        if event.delta > 0:
            self.current_image_index = (self.current_image_index + 1) % 5
        # Scroll down to switch to the previous image
        else:
            self.current_image_index = (self.current_image_index - 1) % 5
            
        self.image_label.config(image=self.image_objects[self.current_image_index][0])
        self.animate()

    #gif animation functionality
    def animate(self, frame=0):
        if len(self.image_objects[self.current_image_index]) > 1:
            frame %= len(self.image_objects[self.current_image_index])
            self.image_label.config(image=self.image_objects[self.current_image_index][frame])
            frame += 1
            self.after(100, lambda: self.animate(frame))
        else:
            self.after(100, self.animate)

#Loops program indefinitely
if __name__ == "__main__":
    app = ImageSwitcher()
    app.mainloop()
