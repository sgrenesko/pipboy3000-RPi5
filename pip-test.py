import tkinter as tk
from PIL import Image, ImageTk

class ImageSwitcher(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Image Switcher")
        
        # Initial image
        self.current_image_index = 0
        self.images = ["image1.gif", "image2.png", "image3.png"]  # List of image file paths
        
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
        
        # Bind left mouse click to switch image on specific areas
        self.image_label.bind("<Button-1>", self.on_click)
        
    def load_images(self):
        self.image_objects = []
        for img_path in self.images:
            if img_path.lower().endswith('.gif'):
                # Load animated gif frames using Pillow
                gif = Image.open(img_path)
                frames = []
                try:
                    while True:
                        frame = ImageTk.PhotoImage(gif.copy().resize((1200, 675)))  # Resize to desired dimensions
                        frames.append(frame)
                        gif.seek(len(frames))  # Move to next frame
                except EOFError:
                    pass  # End of frames
                self.image_objects.append(frames)  # Animated gif frames
            else:
                # Load static image
                img = Image.open(img_path)
                img_resized = img.resize((1200, 675))  # Resize to desired dimensions
                self.image_objects.append([ImageTk.PhotoImage(img_resized)])
        
    def on_click(self, event):
        if event.x<400 and event.x>200 and event.y<50:
            self.current_image_index = 0
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
        # Check if click is within a specific area for image2
        if event.x < 500 and event.x > 400 and event.y < 50:
            self.current_image_index = 1  # Index of "image2.png"
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
        # Check if click is within a specific area for image3
        elif event.x > 550 and event.x < 600 and event.y<100 and event.y>30:
            self.current_image_index = 2  # Index of "image3.png"
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
    
    def animate(self, frame=0):
        if len(self.image_objects[self.current_image_index]) > 1:  # Check if animated GIF
            frame %= len(self.image_objects[self.current_image_index])
            self.image_label.config(image=self.image_objects[self.current_image_index][frame])
            frame += 1
            self.after(100, lambda: self.animate(frame))
        else:
            self.after(100, self.animate)

if __name__ == "__main__":
    app = ImageSwitcher()
    app.mainloop()
