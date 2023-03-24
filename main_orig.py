import pyautogui as pg
import pynput
import time
import os

year = 1922
publication = 1


def set_topic():
    global year, publication
    well_passed = False
    print('Hello! You are entering the screen prog!\n')
    while not well_passed:
        inp_year = input('Enter year\n').strip()
        inp_publication = input('Enter publication\n').strip()
        try:
            int(year)
            int(publication)
        except ValueError:
            print('Reenter values\n')
            continue
        finally:
            year = inp_year
            publication = inp_publication
            well_passed = True
            break
    print(f'Year set to {year}, publication set to {publication}\n')


set_topic()

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

    print(f'Screenshot saved at {full_name}')




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
    '<ctrl>+<alt>+4': set_topic}) as hotkeys:
    hotkeys.join()

#####################################

