import pyautogui as pg
import pynput
import time
import tkinter as tk
import os

year = 1
publication = 1


def change_mode_status(status):
    mode_status_label.config(text=status)

def write_configs():
    global year, publication
    entered_year_label.config(text='Year - {}'.format(year))
    entered_publication_label.config(text='Publication - {}'.format(publication))

def show_error():
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("300x100+1500+50")
    error_label = tk.Label(error_window, text="Error while entering data")
    error_label.pack(padx=10, pady=10)


def success_win(success_text):
    success_window = tk.Toplevel(root)
    success_window.title("Success")
    success_window.geometry("300x100+1500+50")
    error_label = tk.Label(success_window, text=success_text)
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
root.title("Sreenshooter")
root.geometry("400x200+1500+50")

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

entered_year_label = tk.Label(root, text="year")
entered_year_label.grid(row=3, column=0, padx=5, pady=5)

entered_publication_label = tk.Label(root, text="publication")
entered_publication_label.grid(row=4, column=0, padx=5, pady=5)

mode_status_label = tk.Label(root)
mode_status_label.grid(row=5, column=1, padx=5, pady=5)


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

# pass_arg is needed just to lock standard Tkinter bind call with 1 argument
def activate_screenshot_mode(pass_arg=None):
    change_mode_status('Screenshot mode activated!')
    print('Screenshot mode activated')
    first = screenshot_mode()
    second = screenshot_mode()
    width = abs(first[0] - second[0])
    height = abs(first[1] - second[1])
    create_screenshot(first, second, width, height)
    # change_mode_status('Screenshot mode inactive!')


root.focus_set()
root.bind("<Escape>", activate_screenshot_mode)
root.mainloop()
