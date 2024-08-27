import tkinter as tk
from tkinter import simpledialog, messagebox


class Object2D:
    def __init__(self, name, obj_type, x1, y1, x2=None, y2=None):
        self.name = name
        self.obj_type = obj_type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        x1, y1 = to_screen_coords(
            self.x1, self.y1, canvas.winfo_width(), canvas.winfo_height()
        )
        if self.obj_type == "point":
            canvas.create_rectangle(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill="black")
        elif self.obj_type == "line":
            x2, y2 = to_screen_coords(
                self.x2, self.y2, canvas.winfo_width(), canvas.winfo_height()
            )
            canvas.create_line(x1, y1, x2, y2, fill="black")


def to_screen_coords(x, y, canvas_width, canvas_height):
    return (canvas_width // 2 + int(x), canvas_height // 2 - int(y))


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Básico 2D | João Vitor Thomazoni Borrachini |")
        self.geometry(f"{WIDTH}x{HEIGHT}")

        self.objects = []

        # Canvas
        self.canvas = tk.Canvas(self, bg="white", width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self, width=200, bg="lightgray")
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox
        self.listbox = tk.Listbox(self.sidebar, bg="white")
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Buttons
        self.button_frame = tk.Frame(self.sidebar)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(
            self.button_frame, text="Adicionar Ponto", command=self.add_point
        ).pack(side=tk.TOP, padx=5, pady=5)
        tk.Button(
            self.button_frame, text="Adicionar Linha", command=self.add_line
        ).pack(side=tk.TOP, padx=5, pady=5)
        tk.Button(
            self.button_frame, text="Remover Objeto", command=self.remove_object
        ).pack(side=tk.TOP, padx=5, pady=5)

        self.update_viewport()

        # Bind selection event
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

    def add_point(self):
        name = simpledialog.askstring("Nome do Ponto", "Nome do ponto:")
        x = simpledialog.askfloat("Coordenada X", "Coordenada X:")
        y = simpledialog.askfloat("Coordenada Y", "Coordenada Y:")
        if name and x is not None and y is not None:
            obj = Object2D(name, "point", x, y)
            self.objects.append(obj)
            self.update_viewport()
            self.update_listbox()

    def add_line(self):
        name = simpledialog.askstring("Nome da Linha", "Nome da linha:")
        x1 = simpledialog.askfloat("Coordenada X1", "Coordenada X1:")
        y1 = simpledialog.askfloat("Coordenada Y1", "Coordenada Y1:")
        x2 = simpledialog.askfloat("Coordenada X2", "Coordenada X2:")
        y2 = simpledialog.askfloat("Coordenada Y2", "Coordenada Y2:")
        if (
            name
            and x1 is not None
            and y1 is not None
            and x2 is not None
            and y2 is not None
        ):
            obj = Object2D(name, "line", x1, y1, x2, y2)
            self.objects.append(obj)
            self.update_viewport()
            self.update_listbox()

    def remove_object(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum objeto selecionado.")
            return

        selected_name = self.listbox.get(selected_index)
        self.objects = [obj for obj in self.objects if obj.name != selected_name]
        self.update_viewport()
        self.update_listbox()

    def update_viewport(self):
        self.canvas.delete("all")
        for obj in self.objects:
            obj.draw(self.canvas)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for obj in self.objects:
            if obj.obj_type == "point":
                entry = f"{obj.name}: ({obj.x1}, {obj.y1})"
            elif obj.obj_type == "line":
                entry = f"{obj.name}: ({obj.x1}, {obj.y1}) - ({obj.x2}, {obj.y2})"
            self.listbox.insert(tk.END, entry)

    def on_listbox_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index)
            # Extract the name from the selected item
            selected_name = selected_text.split(":")[0]
            for obj in self.objects:
                if obj.name == selected_name:
                    self.canvas.delete("all")
                    obj.draw(self.canvas)
                    break


if __name__ == "__main__":
    WIDTH, HEIGHT = 800, 600
    app = Application()
    app.mainloop()
