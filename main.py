from tkinter import *
import random


class SnakeGame:
    def __init__(self):
        # Инициализация главного окна и основных параметров игры
        self.root = Tk()
        self.root.title("Змейка by MMG")
        self.grid = 20  # Размер одной клетки сетки
        self.root.resizable(False, False)  # Запрет изменения размера окна

        # Настройки размеров окна и скоростей
        self.set_size = ["600x400", "800x600", "1000x800", "400x200"]
        self.set_speed = ["200", "150", "100", "75", "50"]

        # Изменяемые параметры игры
        self.changable_param = {
            "width": 600,
            "height": 400,
            "speed": 75
        }

        # Цветовая схема игры
        self.colors = {
            "snake_head": "#FF0000",
            "snake_body": "#8a0000",
            "apple": "#9ACD32",
            "menu_bg": "#521E05",
            "btn": "#853D1B",
            "active_bg": "#FF4500",
            "grid": "#333333"
        }

        # Шрифты для текста
        self.T_font = ("Arial", 14, "bold")  # Заголовочный шрифт
        self.t_font = ("Arial", 14)  # Основной шрифт
        self.o_font = ("Arial", 10)  # шрифт для OptionMenu

        # Стиль кнопок
        self.btn_style = {
            "font": self.t_font,
            "bg": self.colors["btn"],
            "fg": "white",
            "activebackground": self.colors["active_bg"],
            "relief": "raised"
        }

        # Разрешение экрана (для центрирования окон)
        self.swidth = 1920
        self.sheight = 1080

        # Создание главного меню
        self.create_menu()

    def create_menu(self):
        """Создание главного меню игры"""
        # Очистка текущего содержимого окна
        for w in self.root.winfo_children():
            w.destroy()

        # Настройка фона окна
        self.root.configure(bg=self.colors["menu_bg"])

        # Заголовок игры
        t_label = Label(self.root, text="ЗМЕЙКА by MMG", bg=self.colors["menu_bg"],
                        fg="white", font=self.T_font)
        t_label.pack(pady=15)

        # Кнопка начала игры
        pl_btn = Button(self.root, text="🐍", command=self.start_game, **self.btn_style, width=20, height=2)
        pl_btn.pack(padx=170)

        # Кнопка настроек
        sett_btn = Button(self.root, text="⚙️", command=self.settings_menu, **self.btn_style, width=20, height=2)
        sett_btn.pack(padx=170, pady=5)

        # Кнопка выхода
        ex_btn = Button(self.root, text="🔙", command=self.root.quit, **self.btn_style, width=20, height=2)
        ex_btn.pack(padx=170)

    def settings_menu(self):
        """Создание меню настроек"""
        # Очистка текущего содержимого окна
        for w in self.root.winfo_children():
            w.destroy()

        self.root.configure(bg=self.colors["menu_bg"])

        # Заголовок меню настроек
        Label(self.root, text="НАСТРОЙКИ", font=self.T_font, fg="white", bg=self.colors["menu_bg"]).pack(pady=15)

        # Выбор размера окна
        Label(self.root, text="Размер окна игры: ", font=self.t_font, fg="white", bg=self.colors["menu_bg"]).pack(
            pady=2)
        self.size_var = StringVar(value=f"{self.changable_param['width']}x{self.changable_param['height']}")
        size_menu = OptionMenu(self.root, self.size_var, *self.set_size)
        size_menu.config(font=self.o_font, fg="white", bg=self.colors["menu_bg"], width=10)
        size_menu.pack(pady=5)

        # Выбор скорости
        Label(self.root, text="Скорость: ", font=self.t_font, fg="white", bg=self.colors["menu_bg"]).pack()
        self.speed_var = StringVar(value=f"{self.changable_param['speed']}")
        speed_menu = OptionMenu(self.root, self.speed_var, *self.set_speed)
        speed_menu.config(font=self.o_font, fg="white", bg=self.colors["menu_bg"], width=10)
        speed_menu.pack(pady=5)

        # Фрейм для кнопок
        btn_frame = Frame(self.root, bg=self.colors["menu_bg"])
        btn_frame.pack(pady=15)

        # Кнопка сохранения настроек
        save_btn = Button(btn_frame, text="💾", command=self.save_settings, **self.btn_style)
        save_btn.pack(side="left", padx=5)

        # Кнопка возврата в меню
        back_btn = Button(btn_frame, text="🔙", command=self.create_menu, **self.btn_style)
        back_btn.pack(side="left", padx=5)

        # Кнопка сброса настроек
        reset_btn = Button(btn_frame, text="🔄", command=self.reset_settings, **self.btn_style)
        reset_btn.pack(side="left", padx=5)

    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        self.size_var.set("600x400")
        self.speed_var.set("75")

    def save_settings(self):
        """Сохранение выбранных настроек"""
        try:
            new_width, new_height = map(int, self.size_var.get().split('x'))
            self.changable_param["width"] = new_width
            self.changable_param["height"] = new_height
            self.changable_param["speed"] = int(self.speed_var.get())
        except Exception as e:
            print(f"Ошибка при сохранении настроек: {e}")

    def initial_state(self):
        """Инициализация начального состояния игры"""
        # Начальная позиция змеи (центр экрана)
        self.snake = [(self.changable_param["width"] // 2, self.changable_param["height"] // 2)]
        self.direction = (self.grid, 0)  # Начальное направление (вправо)
        self.food = self.food_gen()  # Генерация первой еды
        self.score = 0  # Начальный счет
        self.speed = self.changable_param["speed"]  # Скорость игры
        self.game_running = False  # Флаг состояния игры

    def draw_game(self):
        """Отрисовка игрового поля и интерфейса"""
        # Очистка окна
        for w in self.root.winfo_children():
            w.destroy()

        # Центрирование игрового окна
        sgx = (self.swidth - self.changable_param["width"]) // 2
        sgy = (self.sheight - self.changable_param["height"]) // 2 - 100
        self.root.geometry(f"{self.changable_param['width']}x{self.changable_param['height'] + 100}+{sgx}+{sgy}")

        # Создание игрового поля (канвас)
        self.can = Canvas(self.root, width=self.changable_param["width"],
                          height=self.changable_param["height"], background="black")
        self.can.pack()

        # Создание фрейма для интерфейса
        fr = Frame(self.root, bg=self.colors["menu_bg"])
        fr.pack(fill="x", padx=5, pady=5)

        # Метка счета
        self.score_label = Label(fr, text="СЧЕТ: 0", font=self.T_font,
                                 fg="white", bg=self.colors["menu_bg"])
        self.score_label.pack()

        # Отрисовка сетки
        for x in range(0, self.changable_param["width"], self.grid):
            self.can.create_line(x, 0, x, self.changable_param["height"], fill=self.colors["grid"])
        for y in range(0, self.changable_param["height"], self.grid):
            self.can.create_line(0, y, self.changable_param["width"], y, fill=self.colors["grid"])

        # Фрейм для кнопки паузы (левый нижний угол)
        left_frame = Frame(fr, bg=self.colors["menu_bg"], width=300, height=80)
        left_frame.pack(side="left")
        left_frame.pack_propagate(False)

        pause_btn = Button(left_frame, text="⏸️", command=self.pause_func, **self.btn_style)
        pause_btn.pack(anchor="e", padx=15)

        # Фрейм для кнопки выхода (правый нижний угол)
        right_frame = Frame(fr, bg=self.colors["menu_bg"], width=300, height=80)
        right_frame.pack(side="right")
        right_frame.pack_propagate(False)

        ex_btn = Button(right_frame, text="🔙", command=self.back_to_menu, **self.btn_style, width=3)
        ex_btn.pack(anchor="w", padx=15)

        # Установка фокуса на канвас для обработки клавиш
        self.can.focus_set()

        # Отрисовка начального состояния
        self.draw_snake_and_food()

    def draw_snake_and_food(self):
        """Отрисовка змеи и еды на игровом поле"""
        self.can.delete("all")  # Очищаем канвас

        # Рисуем сетку
        for x in range(0, self.changable_param["width"], self.grid):
            self.can.create_line(x, 0, x, self.changable_param["height"], fill=self.colors["grid"])
        for y in range(0, self.changable_param["height"], self.grid):
            self.can.create_line(0, y, self.changable_param["width"], y, fill=self.colors["grid"])

        # Рисуем змею
        for i, (x, y) in enumerate(self.snake):
            if i == 0:  # Голова
                self.draw_snake_head(x, y)
            else:  # Тело
                self.draw_snake_body(x, y)

        # Рисуем еду
        x, y = self.food
        food_size = self.grid
        self.can.create_oval(x, y, x + food_size, y + food_size,
                             fill=self.colors["apple"])

    def draw_snake_head(self, x, y):
        """Отрисовка головы змеи"""
        self.can.create_rectangle(x, y, x + self.grid, y + self.grid,
                                  fill=self.colors["snake_head"])

    def draw_snake_body(self, x, y):
        """Отрисовка тела змеи"""
        self.can.create_rectangle(x, y, x + self.grid, y + self.grid,
                                  fill=self.colors["snake_body"])

    def food_gen(self):
        """Генерация новой позиции для еды"""
        while True:
            # Случайная позиция в пределах игрового поля
            x = random.randrange(0, self.changable_param["width"] - self.grid, self.grid)
            y = random.randrange(0, self.changable_param["height"] - self.grid, self.grid)
            food_pos = (x, y)

            # Проверка, что еда не появилась на змее
            if food_pos not in self.snake:
                return food_pos

    def pause_func(self):
        """Функция паузы/возобновления игры"""
        self.paused = not self.paused
        if self.paused:
            self.pause_overlay()
        else:
            self.hide_pause_overlay()
            self.game_loop()

    def pause_overlay(self):
        """Отображение текста паузы"""
        self.pause_text = self.can.create_text(
            self.changable_param["width"] // 2, self.changable_param["height"] // 2,
            text="ПАУЗА", font=("Arial", 36, "bold"), fill="white"
        )

    def hide_pause_overlay(self):
        """Скрытие текста паузы"""
        if hasattr(self, 'pause_overlay'):
            self.can.delete(self.pause_text)

    def start_game(self):
        """Запуск новой игры"""
        self.initial_state()  # Инициализация состояния
        self.draw_game()  # Отрисовка игрового поля
        self.game_running = True
        self.paused = False
        # Привязка обработчиков клавиш
        self.root.bind('<KeyPress>', self.on_key_press)
        self.game_loop()  # Запуск игрового цикла

    def game_loop(self):
        """Основной игровой цикл"""
        if not self.game_running or self.paused:
            return

        try:
            # Расчет новой позиции головы
            head_x, head_y = self.snake[0]
            dir_x, dir_y = self.direction
            new_head = (head_x + dir_x, head_y + dir_y)

            # Проверка столкновений с границами и самой собой
            if (new_head[0] < 0 or new_head[0] >= self.changable_param["width"] or
                    new_head[1] < 0 or new_head[1] >= self.changable_param["height"] or
                    new_head in self.snake):
                self.game_over()
                return

            # Добавление новой головы
            self.snake.insert(0, new_head)

            # Проверка съедания еды
            if new_head == self.food:
                self.score += 25
                self.food = self.food_gen()
                self.score_label.config(text=f"СЧЕТ: {self.score}")
                # Увеличение скорости каждые 100 очков
                if self.score % 100 == 0 and self.speed > 30:
                    self.speed -= 10
            else:
                # Удаление хвоста если еда не съедена
                self.snake.pop()

            # Перерисовка игры
            self.draw_snake_and_food()

            # Продолжение игрового цикла
            self.root.after(self.speed, self.game_loop)

        except Exception as e:
            print(f"Ошибка в игровом цикле: {e}")

    def on_key_press(self, event):
        """Обработка нажатий клавиш"""
        key = event.keysym
        # Управление направлением (с проверкой на противоположное направление)
        if key == 'Up' and self.direction != (0, self.grid):
            self.direction = (0, -self.grid)
        elif key == 'Down' and self.direction != (0, -self.grid):
            self.direction = (0, self.grid)
        elif key == 'Left' and self.direction != (self.grid, 0):
            self.direction = (-self.grid, 0)
        elif key == 'Right' and self.direction != (-self.grid, 0):
            self.direction = (self.grid, 0)
        elif key == 'Escape':  # Выход в меню
            self.back_to_menu()
        elif key == 'p':  # Пауза
            self.pause_func()

    def game_over(self):
        """Обработка окончания игры"""
        self.game_running = False

        # Создание окна окончания игры
        overlay = Toplevel(self.root)
        overlay.resizable(False, False)
        overlay.title("Игра окончена")
        # Центрирование окна
        overlay.geometry(
            f"236x220+{self.root.winfo_x() + self.changable_param['width'] // 2 - 118}+{self.root.winfo_y() + self.changable_param['height'] // 2 - 110}")
        overlay.configure(bg=self.colors["menu_bg"])
        overlay.transient(self.root)
        overlay.grab_set() 

        # Текст окончания игры
        Label(overlay, text="ИГРА ОКОНЧЕНА",
              font=self.T_font, fg="white", bg=self.colors["menu_bg"]).pack(pady=20)

        # Отображение счета
        Label(overlay, text=f"Ваш счет: {self.score}",
              font=self.T_font, fg="white", bg=self.colors["menu_bg"]).pack(pady=10)

        # Фрейм для кнопок
        btn_frame = Frame(overlay, bg=self.colors["menu_bg"])
        btn_frame.pack(pady=20)

        # Кнопка перезапуска игры
        Button(btn_frame, text="🔄",
               command=self.start_game,
               **self.btn_style).pack(side="left", padx=10)

        # Кнопка возврата в меню
        Button(btn_frame, text="🔙",
               command=self.back_to_menu,
               **self.btn_style).pack(side="left", padx=10)

    def back_to_menu(self):
        """Возврат в главное меню"""
        self.game_running = False
        # Очистка окна
        for w in self.root.winfo_children():
            w.destroy()
        self.create_menu()
        # Возврат к размеру окна меню
        sx = (self.swidth - 400) // 2
        sy = (self.sheight - 300) // 2 - 100
        self.root.geometry(f"400x300+{sx}+{sy}")

    def run(self):
        """Запуск приложения"""
        # Центрирование окна меню
        sx = (self.swidth - 400) // 2
        sy = (self.sheight - 300) // 2 - 100
        self.root.geometry(f"400x300+{sx}+{sy}")
        self.root.mainloop()  # Запуск главного цикла приложения


if __name__ == "__main__":
    game = SnakeGame()
    game.run()