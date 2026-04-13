import sys
import random
from PIL import Image
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, Qt
import ctypes
import os

if not os.path.exists("images"):
    os.makedirs("images")

# taskbar icon doesn't update without this, no idea why
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("company.app.1")


class Direction:
    direction = (1, 0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Taskbar snake")

        central = QWidget(self)
        layout = QVBoxLayout(central)

        label = QLabel("Look at the taskbar icon")
        font = label.font()
        font.setPointSize(30)
        label.setFont(font)
        label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(label)

        label2 = QLabel("(this window has to be focused for input)")
        font2 = label2.font()
        font2.setPointSize(15)
        label2.setFont(font2)
        label2.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(label2)

        self.setCentralWidget(central)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W and Direction.direction != (0, 1):
            Direction.direction = (0, -1)
        elif event.key() == Qt.Key.Key_A and Direction.direction != (1, 0):
            Direction.direction = (-1, 0)
        elif event.key() == Qt.Key.Key_S and Direction.direction != (0, -1):
            Direction.direction = (0, 1)
        elif event.key() == Qt.Key.Key_D and Direction.direction != (-1, 0):
            Direction.direction = (1, 0)

        event.accept()


app = QApplication(sys.argv)
window = MainWindow()
window.resize(500, 200)
window.show()

game_size = 8
snake = [(game_size / 2, game_size / 2)]
food = None
frame = 0


def spawn_food():
    while True:
        pos = (random.randint(0, game_size - 1), random.randint(0, game_size - 1))
        if pos not in snake:
            return pos


food = spawn_food()


def save_png():
    global frame

    img = Image.new("RGB", (game_size, game_size), (0, 0, 0))
    pixels = img.load()

    for x, y in snake:
        pixels[x, y] = (0, 255, 0)

    fx, fy = food
    pixels[fx, fy] = (255, 0, 0)

    img = img.resize((32, 32), Image.Resampling.NEAREST)
    img.save(f"images/frame_{frame}.png")

    frame = 1 if frame == 0 else 0


def update_icon():
    icon = QIcon(f"images/frame_{frame}.png")
    app.setWindowIcon(icon)
    window.setWindowIcon(icon)


def update_game():
    global food

    head_x, head_y = snake[0]
    dx, dy = Direction.direction
    new_head = ((head_x + dx) % game_size, (head_y + dy) % game_size)

    if new_head in snake:
        print("Game over!")
        exit()

    snake.insert(0, new_head)

    if new_head == food:
        food = spawn_food()
    else:
        snake.pop()

    save_png()
    update_icon()


timer = QTimer()
timer.timeout.connect(update_game)
timer.start(230)

app.exec()
