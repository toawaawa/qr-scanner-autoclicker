import cv2
import webbrowser
import time

import pyautogui

first_button_x = 855
first_button_y = 602
second_button_x = 1073
second_button_y = 710
refresh_x = 888
refresh_y = 60
main_x = 785
main_y = 431
def grab_gift():
    # 1. switch to gifts tab
    time.sleep(3)
    # control + tab
    pyautogui.keyDown("ctrl")
    pyautogui.press("tab")
    pyautogui.keyUp("ctrl")
    # 2. refresh
    pyautogui.click(refresh_x, refresh_y, 1)
    time.sleep(0.2)
    # 3. Put cursor on main page
    pyautogui.click(main_x, main_y, 1)
    # 4. scroll to destination
    time.sleep(0.5)
    pyautogui.scroll(-100)
    # 5. press first and second button
    pyautogui.click(first_button_x, first_button_y, 1)
    time.sleep(0.2)
    pyautogui.click(second_button_x, second_button_y, 1)

def scan_qr_code_on_tv():
    cap = cv2.VideoCapture(0)

    # FIX 1: Lower the resolution to 640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = cv2.QRCodeDetector()

    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                break

            # FIX 2: Only decode every once in a while to save CPU
            # We will process the frame and then immediately sleep
            data, bbox, _ = detector.detectAndDecode(frame)

            if data:
                print(f"✅ Found: {data}")
                webbrowser.open(data)
                grab_gift()
                break

                # Show the window (Optional: you can comment this out to save more power)
            # FIX 4: Add a longer sleep. 0.5 seconds = 2 checks per second.
            # This reduces CPU usage from 90% to 5%.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #time.sleep(0.5)

    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    scan_qr_code_on_tv()