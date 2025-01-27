import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


# Программа для создания изображений на основе TKinter
class DrawingApp:
    def __init__(self, root):
        self.option_var = None
        self.brush_size_scale = None
        self.root = root    # Это корневой виджет Tkinter, который служит контейнером для всего интерфейса приложения.
        self.root.title("Рисовалка с сохранением в PNG")    # - Устанавливается заголовок окна приложения.

        self.image = Image.new("RGB", (600, 400), "white")  # - Создается объект изображения.
        self.draw = ImageDraw.Draw(self.image)  # Инициализируется объект, позволяющий рисовать на объекте изображения.

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')    # Виджет отображает интерфейс для рисования.
        self.canvas.pack()

        self.setup_ui()  # - Вызывается метод self.setup_ui(), который настраивает элементы управления интерфейса.

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):     # Этот метод отвечает за создание и расположение виджетов управления:
        """Добавлен функционал - Выбор размера кисти из списка"""
        sizes = ["1", "2", "4", "8", "16", "32"]    # Размеры кисти
        self.option_var = tk.StringVar(value="1")   # Размер кисти по умолчанию
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)
        # - Кнопки "Очистить", "Выбрать цвет" и "Сохранить" позволяют пользователю очищать холст,
        # выбирать цвет кисти и сохранять текущее изображение соответственно.
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)
        # Выпадающий список для изменения размера кисти дает возможность выбирать толщину линии в пикселях.
        selected_label = tk.Label(control_frame, text="Толщина кисти")     # Текст рядом со списком
        selected_label.pack(side=tk.LEFT)       # Положение текста
        self.brush_size_scale = tk.OptionMenu(control_frame, self.option_var, *sizes)   # Добавляет список
        self.brush_size_scale.config(indicatoron=False)  # Убирает лишнюю черту
        self.brush_size_scale.pack(side=tk.LEFT)       # Положение списка

    def paint(self, event):     # Вызывается при движении мыши с нажатой левой кнопкой по холсту.
        # - event: Событие содержит координаты мыши, которые используются для рисования.
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=int(self.option_var.get()), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=int(self.option_var.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):     # Сбрасывает последние координаты кисти.
        self.last_x, self.last_y = None, None

    def clear_canvas(self):     # Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw.
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):     # Открывает диалоговое окно выбора цвета и устанавливает выбранный цвет кисти.
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):       # Позволяет пользователю сохранить изображение. Поддерживает только формат PNG.
        # В случае успешного сохранения выводится сообщение об успешном сохранении.
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
