import tkinter as tk
from tkinter import colorchooser, filedialog

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Program")

        # Create canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create frame for shape selection
        shape_frame = tk.Frame(root, bg="black", width=100, height=400)
        shape_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Add shape selection radiobuttons
        self.selected_shape = tk.StringVar()
        shapes = [("Line", "line"), ("Rectangle", "rectangle"), ("Oval", "oval"), ("Circle", "circle")]
        for text, shape in shapes:
            tk.Radiobutton(shape_frame, text=text, variable=self.selected_shape, value=shape, bg="black", fg="white").pack(anchor=tk.W)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Initialize variables
        self.selected_shape_id = None
        self.start_x, self.start_y = None, None
        self.start_shape_x, self.start_shape_y = None, None
        self.color = "black"
        self.thickness = 2
        self.rect_width = 50
        self.rect_height = 50
        self.oval_width = 50
        self.oval_height = 50
        self.circle_radius = 20

        # Create buttons
        color_button = tk.Button(root, text="Select Color", command=self.choose_color, bg="black", fg="white")
        color_button.pack(side=tk.TOP, pady=10)

        thickness_label = tk.Label(root, text="Thickness:", bg="black", fg="white")
        thickness_label.pack()
        self.thickness_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_thickness)
        self.thickness_scale.set(self.thickness)
        self.thickness_scale.pack()

        self.create_shape_sliders(root)

        save_button = tk.Button(root, text="Save", command=self.save, bg="black", fg="white")
        save_button.pack(side=tk.BOTTOM, pady=10)

        clear_button = tk.Button(root, text="Clear", command=self.clear, bg="black", fg="white")
        clear_button.pack(side=tk.BOTTOM, pady=10)

    def create_shape_sliders(self, root):
        self.rect_width_scale = tk.Scale(root, label="Rect Width", from_=1, to=200, orient=tk.HORIZONTAL)
        self.rect_width_scale.pack()
        self.rect_height_scale = tk.Scale(root, label="Rect Height", from_=1, to=200, orient=tk.HORIZONTAL)
        self.rect_height_scale.pack()
        self.oval_width_scale = tk.Scale(root, label="Oval Width", from_=1, to=200, orient=tk.HORIZONTAL)
        self.oval_width_scale.pack()
        self.oval_height_scale = tk.Scale(root, label="Oval Height", from_=1, to=200, orient=tk.HORIZONTAL)
        self.oval_height_scale.pack()
        self.circle_radius_scale = tk.Scale(root, label="Circle Radius", from_=1, to=100, orient=tk.HORIZONTAL)
        self.circle_radius_scale.pack()

    def create_line(self, x1, y1, x2, y2):
        return self.canvas.create_line(x1, y1, x2, y2, width=self.thickness, fill=self.color)

    def create_rectangle(self, x1, y1, x2, y2):
        return self.canvas.create_rectangle(x1, y1, x2, y2, width=self.thickness, outline=self.color)

    def create_oval(self, x1, y1, x2, y2):
        return self.canvas.create_oval(x1, y1, x2, y2, width=self.thickness, outline=self.color)

    def create_circle(self, x, y, radius):
        return self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, width=self.thickness, outline=self.color)

    def on_canvas_click(self, event):
        shape = self.selected_shape.get()
        if shape == "circle":
            self.start_x, self.start_y = event.x, event.y
            self.circle_radius = self.circle_radius_scale.get()
            self.selected_shape_id = self.create_circle(self.start_x, self.start_y, self.circle_radius)
        elif shape == "rectangle":
            self.start_x, self.start_y = event.x, event.y
            self.rect_width = self.rect_width_scale.get()
            self.rect_height = self.rect_height_scale.get()
            self.selected_shape_id = self.create_rectangle(self.start_x, self.start_y, self.start_x + self.rect_width, self.start_y + self.rect_height)
        elif shape == "oval":
            self.start_x, self.start_y = event.x, event.y
            self.oval_width = self.oval_width_scale.get()
            self.oval_height = self.oval_height_scale.get()
            self.selected_shape_id = self.create_oval(self.start_x, self.start_y, self.start_x + self.oval_width, self.start_y + self.oval_height)
        elif shape == "line":
            self.start_x, self.start_y = event.x, event.y
            self.selected_shape_id = self.create_line(self.start_x, self.start_y, self.start_x, self.start_y)

        if self.selected_shape_id:
            self.start_shape_x, self.start_shape_y = event.x, event.y

    def on_canvas_drag(self, event):
        if self.selected_shape_id:
            if self.selected_shape.get() == "line":
                self.canvas.coords(self.selected_shape_id, self.start_x, self.start_y, event.x, event.y)
            else:
                dx = event.x - self.start_shape_x
                dy = event.y - self.start_shape_y
                self.canvas.move(self.selected_shape_id, dx, dy)
                self.start_shape_x, self.start_shape_y = event.x, event.y

    def on_canvas_release(self, event):
        self.selected_shape_id = None

    def choose_color(self):
        self.color = colorchooser.askcolor()[1]

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.canvas.postscript(file=filename + ".eps", colormode='color')
            # convert .eps file to .png or .jpg as needed

    def clear(self):
        self.canvas.delete("all")

    def change_thickness(self, value):
        self.thickness = int(value)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
