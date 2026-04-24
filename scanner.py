import os

import PIL.ImageGrab
import PIL.Image
import cv2
import numpy as np
import webbrowser
import time
import datetime
import pyautogui
import requests

from dotenv import load_dotenv

load_dotenv()

# Get the secrets
TOKEN = os.getenv("TELEGRAM_API")
CHAT_ID = os.getenv("TELEGRAM_ID")

def send_telegram_msg(message):
    if not TOKEN or not CHAT_ID:
        print("telegram disabled")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def is_color_near(current_color, target_color, tolerance=10):
    """
    Checks if current_color is within +/- tolerance of target_color
    """
    r_curr, g_curr, b_curr = current_color
    r_targ, g_targ, b_targ = target_color

    return (abs(r_curr - r_targ) <= tolerance and
            abs(g_curr - g_targ) <= tolerance and
            abs(b_curr - b_targ) <= tolerance)


def scan_screen_with_opencv(click_x, click_y, x1, y1, x2, y2):
    bbox = (x1, y1, x2, y2)

    detector = cv2.QRCodeDetector()

    clickable_color = (216, 72, 109)

    disable_color = (21, 51, 205)

    last_url = None

    clicked = False

    sleep_time = 10
    try:
        while True:
            # 1. click
            screenshot_click = PIL.ImageGrab.grab(bbox=(click_x, click_y, click_x + 2, click_y + 2)).convert('RGB')
            r, g, b = screenshot_click.getpixel((0, 0))
            print(r, g, b)
            if is_color_near((r, g, b), clickable_color) and clicked == False:
                print(datetime.datetime.now(),":button clickable")
                send_telegram_msg(str(datetime.datetime.now()) + "\nbutton clickable")
                pyautogui.click(click_x,click_y,60,0.05)
                clicked = True
                sleep_time = 1

            elif is_color_near((r, g, b), disable_color):
                clicked = False
                sleep_time = 30

            # 2. scan QR code
            screenshot = PIL.ImageGrab.grab(bbox=bbox)

            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            data, bbox_array, _ = detector.detectAndDecode(frame)

            if data:
                if data != last_url:
                    print(datetime.datetime.now(),":qr code appeared")
                    send_telegram_msg(str(datetime.datetime.now()) + "\nqr code appeared")
                    webbrowser.open(data)
                    time.sleep(20)
                    # switch back to chrome page
                    pyautogui.keyDown("command")
                    pyautogui.press("tab")
                    pyautogui.keyUp("command")

                    last_url = data

            # Sleep to save CPU
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nScanner stopped.")


if __name__ == "__main__":
    # Pull cursor to top right to escape
    pyautogui.FAILSAFE = True
    # QR Code location
    START_X = 0
    START_Y = 0
    END_X = 165
    END_Y = 400
    # Click location 165 400
    CLICK_X = 1236
    CLICK_Y = 757
    # Click position
    scan_screen_with_opencv(CLICK_X, CLICK_Y, START_X, START_Y, END_X, END_Y)