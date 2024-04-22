import tkinter as tk
from tkinter import Canvas, Button, Spinbox, StringVar, Event, Label


def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    center1 = ((x1 + x2) / 2, (y1 + y2) / 2)
    center2 = ((x3 + x4) / 2, (y3 + y4) / 2)
    radius1 = abs(x2 - x1) / 2
    radius2 = abs(x4 - x3) / 2
    distance = ((center2[0] - center1[0]) ** 2 + (center2[1] - center1[1]) ** 2) ** 0.5

    return distance < (radius1 + radius2)


class App:
    def __init__(self, root):
        root.title("Лабораторная работа 4. Вариант 9")
        width, height = 800, 500
        canvas_w, canvas_h = 500, 500

        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.canvas = Canvas(bg="white", width=canvas_w, height=canvas_h)
        self.canvas.pack(anchor="nw")
        self.canvas.bind("<Button-1>", self.DrawCircleEvent)
        self.canvas.bind("<Motion>", self.UpdateCoords)

        self.findIntersections_btn = Button(
            text="Найти окружность", command=self.ChangeColorOfCircle
        )
        self.findIntersections_btn.place(x=510, y=10)

        raduis_label = Label(text="Радиус: ")
        raduis_label.place(x=510, y=50)
        self.radiusSelector_sb = Spinbox(
            from_=2.0, to=100, textvariable=StringVar(value="50")
        )
        self.radiusSelector_sb.place(x=570, y=50)

        self.clean_btn = Button(
            text="Очистить холст", command=lambda: self.canvas.delete("all")
        )
        self.clean_btn.place(x=510, y=80)

        x_label = Label(text="x: ")
        x_label.place(x=510, y=120)
        self.xSelector_sb = Spinbox(
            from_=0.0, to=500, textvariable=StringVar(value="50")
        )
        self.xSelector_sb.place(x=570, y=120)

        y_label = Label(text="y: ")
        y_label.place(x=510, y=150)
        self.ySelector_sb = Spinbox(
            from_=0.0, to=500, textvariable=StringVar(value="50")
        )
        self.ySelector_sb.place(x=570, y=150)

        self.placeCircle_btn = Button(
            text="Разместить",
            command=lambda: self.DrawCircle(
                int(self.xSelector_sb.get()), int(self.ySelector_sb.get())
            ),
        )
        self.placeCircle_btn.place(x=510, y=180)

        self.xPos_label = Label()
        self.yPos_label = Label()
        self.xPos_label.place(x=510, y=470)
        self.yPos_label.place(x=570, y=470)

    def UpdateCoords(self, event: Event):
        self.xPos_label.config(text=f"x={event.x}")
        self.yPos_label.config(text=f"y={event.y}")

    def DrawCircle(self, x, y):
        radius = int(self.radiusSelector_sb.get())
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, outline="black", width=2
        )

    def DrawCircleEvent(self, event: Event):
        x, y = event.x, event.y
        radius = int(self.radiusSelector_sb.get())
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, outline="black", width=2
        )

    def CheckIntersections(self):
        circles = self.canvas.find_all()
        max_intersections = 0
        circle_with_max_intersections = None

        for circle in circles:
            x1, y1, x2, y2 = self.canvas.coords(circle)
            intersections = 0

            for other_circle in circles:
                if circle != other_circle:
                    x3, y3, x4, y4 = self.canvas.coords(other_circle)
                    if intersect(x1, y1, x2, y2, x3, y3, x4, y4):
                        intersections += 1

            if intersections > max_intersections:
                max_intersections = intersections
                circle_with_max_intersections = circle

        return circle_with_max_intersections

    def ChangeColorOfCircle(self):
        circle = self.CheckIntersections()
        if circle:
            self.canvas.itemconfig(circle, outline="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
