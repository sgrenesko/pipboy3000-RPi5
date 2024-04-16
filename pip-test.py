import tkinter as tk
from PIL import Image, ImageTk

class ImageSwitcher(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Pip-Boy 3000")
        
        #Initial image and index setup
        self.current_image_index = 0
        self.images = ["image1.gif", "image2.png", "image3.png", "image4.png"]
        
        self.load_images()
        
        #Get the maximum dimensions of all images
        max_width = max(max(img.width() for img in img_list) for img_list in self.image_objects)
        max_height = max(max(img.height() for img in img_list) for img_list in self.image_objects)
        
        # Create a label to display the image
        self.image_label = tk.Label(self, width=max_width, height=max_height)
        self.image_label.pack()
        self.image_label.config(image=self.image_objects[self.current_image_index][0])
        
        #Start the animation
        self.animate()
        
        #Bind mouse scroll to switch between image1 and image2 and bind left mouse click to switch image on specific areas
        self.image_label.bind("<MouseWheel>", self.on_scroll)
        self.image_label.bind("<Button-1>", self.on_click)
        
    #Loads images, and if a .gif, loads and animates
    def load_images(self):
        self.image_objects = []
        for img_path in self.images:
            if img_path.lower().endswith('.gif'):
                gif = Image.open(img_path)
                frames = []
                try:
                    while True:
                        frame = ImageTk.PhotoImage(gif.copy().resize((1200, 675)))  #Dimension of initial gif for uniformity
                        frames.append(frame)
                        gif.seek(len(frames))  
                except EOFError:
                    pass 
                self.image_objects.append(frames)
            else:
                #Load static image
                img = Image.open(img_path)
                img_resized = img.resize((1200, 675))
                self.image_objects.append([ImageTk.PhotoImage(img_resized)])
        
    #Functionality for clicking to switch between sub menus
    def on_click(self, event):
        #Check if click is within a specific area for image3 and if image2 is current image
        if event.x > 550 and event.x < 600 and event.y < 100 and event.y > 30 and self.current_image_index == 1:
            self.current_image_index = 2
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
        #Check if click is within a specific area for image4 and if image1 is current image
        elif event.x > 450 and event.x < 525 and event.y < 100 and event.y > 75 and self.current_image_index == 0:
            self.current_image_index = 3
            self.image_label.config(image=self.image_objects[self.current_image_index][0])
            self.animate()
    
    #Fucntionality for scrolling to switch between menus
    def on_scroll(self, event):
        #Scroll up to switch to image2
        if event.delta > 0:
            self.current_image_index = 1
        #Scroll down to switch to image1
        else:
            self.current_image_index = 0 
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
