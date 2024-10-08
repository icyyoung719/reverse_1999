import cv2
import pyautogui
import numpy as np
import time
import json


def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def find_template(template, screenshot):
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val, max_loc


def click_on_image(template_path, similar=0.8, click_offset=None):
    if click_offset is None:
        click_offset = [0, 0]
    template = cv2.imread(template_path)
    screenshot = capture_screen()

    max_val, max_loc = find_template(template, screenshot)

    if max_val > similar:
        template_height, template_width, _ = template.shape
        center_x = max_loc[0] + template_width // 2 + click_offset[0]
        center_y = max_loc[1] + template_height // 2 + click_offset[1]

        pyautogui.click(center_x, center_y)
        print(f"Clicked on {template_path} at ({center_x}+{click_offset[0]}, {center_y}+{click_offset[1]})")
        return center_x, center_y
    else:
        print("Image not found on the screen.")
        return False


def wait_until_image_show(template_path, similar=0.8, timeout=40, interval=1):
    start_time = time.time()

    while time.time() - start_time < timeout:
        template = cv2.imread(template_path)
        screenshot = capture_screen()

        max_val, max_loc = find_template(template, screenshot)

        if max_val > similar:
            template_height, template_width, _ = template.shape
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2

            print(f"Image found at ({center_x}, {center_y})")
            return center_x, center_y

        print(f"waiting----- {template_path}")
        time.sleep(interval)

    print(f"Image not found within {timeout} seconds.")
    return False


def detect_image(template_path, similar=0.8):
    template = cv2.imread(template_path)
    screenshot = capture_screen()

    max_val, max_loc = find_template(template, screenshot)

    if max_val > similar:
        # template_height, template_width, _ = template.shape
        # center_x = max_loc[0] + template_width // 2
        # center_y = max_loc[1] + template_height // 2
        return True
    else:
        return False


def scroll_down(template_path,similar=0.8, click_offset = None ):
    # if not wait_until_image_show(template_path):
    #     print(f"Image not found within 30 seconds.")
    #     return False
    center_x, center_y = wait_until_image_show(template_path, similar)
    center_x = click_offset[0] + center_x
    center_y = click_offset[1] + center_y
    pyautogui.moveTo(center_x, center_y)
    pyautogui.scroll(-1)
    return True


def save_json(config_data):
    with open('config.json', 'w') as f:
        # 使用dump函数将配置数据写入文件
        json.dump(config_data, f, indent = 4)  # indent=4 使输出更美观，不是必需的


def load_json():
    try:
        with open('config.json', 'r') as f:
            config_data = json.load(f)
        return config_data
    except FileNotFoundError:
        print("欢迎初次使用")
    except json.JSONDecodeError:
        print("配置文件config.json格式错误，无法解析。")
    except Exception as e:
        print(f"读取配置文件时发生错误：{e}")
    return None