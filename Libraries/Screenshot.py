import pyautogui
import os
from datetime import datetime
from robot.libraries.BuiltIn import BuiltIn

def capture_failure_screenshot(test_name):
    """
    Capture desktop screenshot on failure.
    Save to disk and log to Robot Framework.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshot_dir = os.path.join(base_dir, "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = test_name.replace(" ", "_").replace("/", "_")

        file_path = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")
        pyautogui.screenshot(file_path)

        # Log to Robot Framework
        try:
            BuiltIn().log(f"Screenshot captured: <a href='{file_path}'>{file_path}</a>", html=True)
        except Exception as e:
            print(f"[ROBOT LOGGING FAILED] {e}")

        print(f"[SCREENSHOT] Saved: {file_path}")
        return file_path

    except Exception as e:
        print(f"[SCREENSHOT ERROR] {e}")
        return None
