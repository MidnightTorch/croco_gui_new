import pyautogui as pg
import pynput
import time
import tkinter as tk
import os

year = 1922
publication = 1


def write_configs():
    global year, publication
    entered_year_label.config(text='Year - {}'.format(year))
    entered_publication_label.config(text='Publication - {}'.format(publication))

def show_error():
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_label = tk.Label(error_window, text="Error while entering data")
    error_label.pack(padx=10, pady=10)


def success_win(success_text):
    error_window = tk.Toplevel(root)
    error_window.title("Success")
    error_label = tk.Label(error_window, text=success_text)
    error_label.pack(padx=10, pady=10)

def submit_meta():
    global year, publication
    try:
        int(year_entry.get())
        int(pub_entry.get())
    except ValueError:
        show_error()
    finally:
        year = year_entry.get()
        publication = pub_entry.get()
        write_configs()

root = tk.Tk()
root.title("Publication Info")


entered_year_label = tk.Label(root, text="year")
entered_year_label.grid(row=3, column=0, padx=5, pady=5)

entered_publication_label = tk.Label(root, text="publication")
entered_publication_label.grid(row=4, column=0, padx=5, pady=5)

year_label = tk.Label(root, text="Year:")
year_label.grid(row=0, column=0, padx=5, pady=5)

year_entry = tk.Entry(root)
year_entry.grid(row=0, column=1, padx=5, pady=5)

pub_label = tk.Label(root, text="Publication:")
pub_label.grid(row=1, column=0, padx=5, pady=5)

pub_entry = tk.Entry(root)
pub_entry.grid(row=1, column=1, padx=5, pady=5)

submit_button = tk.Button(root, text="Submit", command=submit_meta)
submit_button.grid(row=2, column=1, padx=5, pady=5)





# Лютое колесо - нужно зарефакторить
def screenshot_mode():
    with pynput.mouse.Events() as events:
        for event in events:
            if type(event) == pynput.mouse.Events.Click:
                if event.button == pynput.mouse.Button.left:
                    return pg.position()

def create_screenshot(first, second, width, height):
    name = 1
    path_to_next_screen = f'screens/{year}/{publication}'
    if os.path.exists(path_to_next_screen):
        if os.listdir(path_to_next_screen) == []: pass
        else:
            name = max([int(i.rstrip('.jpg')) for i in os.listdir(path_to_next_screen)]) + 1
    if not os.path.exists(path_to_next_screen):
        os.makedirs(path_to_next_screen)

    full_name = path_to_next_screen + '/' + str(name) + '.jpg'

    if first[0] > second[0]:
        pg.screenshot(full_name, (first[0], first[1], width, height))
    if first[0] < second[0]:
        pg.screenshot(full_name, (first[0], first[1], abs(second[0] - first[0]), abs(second[1] - first[1])))

    success_win(f'Screenshot saved at {full_name}')


def on_activate():
    print('Screenshot mode activated!')
    first = screenshot_mode()
    time.sleep(1)
    second = screenshot_mode()
    width = abs(first[0] - second[0])
    height = abs(first[1] - second[1])
    create_screenshot(first, second, width, height)


#####################################
# Ниже часть, которая отвечает за работу хоткея - тоже колесо

with pynput.keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+3': on_activate,
    '<ctrl>+<alt>+4': submit_meta}) as hotkeys:
    root.mainloop()
    hotkeys.join()
