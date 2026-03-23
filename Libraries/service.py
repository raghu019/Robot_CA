
import pyautogui
import pygetwindow as gw
from pywinauto import Application
import os
import sys
import io
import time
from pywinauto.timings import Timings
from robot.libraries.BuiltIn import BuiltIn
import datetime
from pywinauto.timings import wait_until_passes
from pywinauto import Desktop
from Screenshot import capture_failure_screenshot  
from datetime import datetime 
import pyperclip
import subprocess



class MyHP:
    TIMEOUT = 5
 
    def __init__(self):
        self.application = None
        self.main_window = None
        self.app_title = "HP"
        self.baseline_folder = r"C:\Users\CanopyR\Documents\Robot\Libraries\Identifiers"
        # if not os.path.exists(self.baseline_folder):
        #     os.makedirs(self.baseline_folder)

    def _log_result(self, test_name, status, message=""):
            """
            Central logger.
            Automatically captures screenshot on FAILURE.
            Logs to console and Robot Framework.
            """
            result = "PASS" if status else "FAIL"
            screenshot_path = None

            if not status:
                # Capture screenshot
                try:
                    screenshot_dir = os.path.join(os.getcwd(), "screenshots")
                    os.makedirs(screenshot_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    safe_name = test_name.replace(" ", "_").replace("/", "_")
                    screenshot_path = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")

                    pyautogui.screenshot(screenshot_path)
                    print(f"[SCREENSHOT] Saved: {screenshot_path}")

                    # Log to Robot Framework
                    try:
                        BuiltIn().log(
                            f"{result}: {test_name} - {message}<br>"
                            f"Screenshot: <a href='{screenshot_path}'>{screenshot_path}</a>",
                            html=True
                        )
                    except Exception as e:
                        print(f"[ROBOT LOGGING FAILED] {e}")

                except Exception as e:
                    print(f"[SCREENSHOT ERROR] {e}")

            # Console output
            if screenshot_path:
                print(f"[{result}] {test_name}: {message} | Screenshot: {screenshot_path}")
            else:
                print(f"[{result}] {test_name}: {message}")

    def _log_debug(self, message):
                """
                Debug logger.
                Prints debug messages to console and Robot Framework log.
                """
                print(f"[DEBUG] {message}")
                try:
                    BuiltIn().log(f"[DEBUG] {message}")
                except Exception:
                    pass



    # ---------------- Open Services and Maximize ----------------

    def open_services_and_maximize(self):
        """Open Services and maximize the window"""

        try:
            # Open Services console
            subprocess.Popen("services.msc", shell=True)
            time.sleep(5)

            # Connect to MMC (Services runs under mmc.exe)
            app = Application(backend="win32").connect(path="mmc.exe")

            # Get top window
            services_window = app.top_window()

            # Save main window for later use
            self.main_window = services_window

            # Focus window
            services_window.set_focus()
            time.sleep(1)

            # Maximize window
            pyautogui.hotkey("win", "up")

            self._log_result("Open Services", True, "Services window maximized")
            return True

        except Exception as e:
            self._log_result("Open Services", False, str(e))
            return False


    #     # ---------------- Dump UI Tree to File ----------------

    # def dump1_ui_tree_to_file(self):
    #     """Dump the full UI tree of the current window to a text file."""

    #     if not self.main_window:
    #         self._log_result("Dump UI Tree", False, "Application not connected")
    #         return False

    #     try:
    #         dump_path = os.path.join(self.baseline_folder, "ui_dump.txt")

    #         with open(dump_path, "w", encoding="utf-8") as f:

    #             buffer = io.StringIO()
    #             sys.stdout = buffer

    #             # Dump UI tree
    #             self.main_window.print_control_identifiers()

    #             sys.stdout = sys.__stdout__

    #             f.write(buffer.getvalue())
    #             buffer.close()

    #         self._log_result("Dump UI Tree", True, f"Saved to {dump_path}")
    #         return True

    #     except Exception as e:
    #         sys.stdout = sys.__stdout__
    #         self._log_result("Dump UI Tree", False, str(e))
    #         return False




    def stop_hp_app_helper_service(self):
        """Open properties → reliably click Stop"""

        if not self.main_window:
            self._log_result("HP Service Action", False, "Application not connected")
            return False

        try:
            self.main_window.set_focus()
            time.sleep(1)

            # Focus ListView
            list_view = self.main_window.child_window(class_name="SysListView32")
            list_view.wait("exists ready", timeout=10)
            list_view.set_focus()
            list_view.click_input()
            time.sleep(1)

            # Select service
            pyautogui.write("HP App Helper HSA Service", interval=0.05)
            time.sleep(2)

            # Open Properties
            pyautogui.press('enter')
            time.sleep(2)

            # Connect to Properties window
            app = Application(backend="win32").connect(title_re=".*Properties.*")
            prop_window = app.top_window()

            prop_window.wait("exists ready", timeout=6)
            prop_window.set_focus()
            time.sleep(1)

            # Get Stop button
            stop_button = prop_window.child_window(title="Stop")

            # Force focus on Stop button
            try:
                stop_button.set_focus()
                time.sleep(1)
            except:
                pass

            # ry clicking
            try:
                stop_button.click_input()
                time.sleep(2)
                self._log_result("HP Service Action", True, "Stop clicked using click_input")
            except:
                try:
                    stop_button.click()
                    time.sleep(2)
                    self._log_result("HP Service Action", True, "Stop clicked using click()")
                except:
                    
                    # FINAL fallback (keyboard)
                    pyautogui.press('tab')  # navigate to Stop
                    pyautogui.press('tab')
                    pyautogui.press('space')
                    time.sleep(3)
                    self._log_result("HP Service Action", True, "Stop triggered using keyboard fallback")

            # Close window
            prop_window.close()

            return True

        except Exception as e:
            self._log_result("HP Service Action", False, str(e))
            return False








#    # ---------------- Run all steps in sequence ----------------

    def run_steps(self):
        steps = [
            self.open_services_and_maximize,
            self.stop_hp_app_helper_service
            
        ]

        overall_status = True  # Track final result

        for step in steps:
            print(f"[INFO] Running: {step.__name__}")
            try:
                result = step()
                if not result:
                    print(f"[FAIL] {step.__name__}")
                    overall_status = False
                else:
                    print(f"[PASS] {step.__name__}")
            except Exception as e:
                print(f"[ERROR] {step.__name__}: {e}")
                overall_status = False

        return overall_status



    # ---------------- Main ----------------
   
if __name__ == "__main__":
    hp_app = MyHP()

    if hp_app.run_steps():
        print("All tests completed.")
    else:
        print("OVERALL TEST RESULT : FAIL")
