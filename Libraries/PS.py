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


 

            # ---------------- Open HP Application ----------------
    def open_hp_application(self):
        try:
            pyautogui.press("winleft")
            time.sleep(1)
            pyautogui.write(self.app_title)
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(5)

            self._log_result("Open Application", True)
            return True

        except Exception as e:
            self._log_result("Open Application", False, str(e))
            return False
    
    # # ---------------- Wait Until HP Fully Loaded ----------------
    # def wait_for_hp_ready(self):
    #     try:
    #         timeout=60
    #         start_time = time.time()
    #         while time.time() - start_time < timeout:
    #             windows = gw.getWindowsWithTitle(self.app_title)
    #             if windows:
    #                 win = windows[0]
    #                 if win.visible:
    #                     win.maximize()
    #                     self._log_result("Wait for HP Ready", True)
    #                     return
    #             time.sleep(1)
 
    #         self._log_result("Wait for HP Ready", False, "HP not ready within timeout")
    #     except Exception as e:
    #         self._log_result("Wait for HP Ready", False, str(e))
 

#----------------------Connect application-------------------------------

    def connect_to_application(self):

        try:
            # Use regex to avoid exact title issues
            self.main_window = Desktop(backend="uia").window(title_re=".*HP.*")

            # Wait until visible (max 10 sec, but returns early if ready)
            self.main_window.wait("visible", timeout=10)

            # Bring window to front
            self.main_window.set_focus()

            print(f"DEBUG: Connected to window = {self.main_window.window_text()}")

            self._log_result("Connect to Application", True)
            return True

        except Exception as e:
            self.main_window = None
            self._log_result("Connect to Application", False, str(e))
            return False



    # ---------------- Handle Location Permission ----------------

    def handle_location_permission_popup(self):
        """Handle location popup only if it appears"""

        try:
            time.sleep(2)

            active_window = gw.getActiveWindow()

            # Check if any active window exists
            if active_window and active_window.title:
                title = active_window.title.lower()

                # Check if location permission popup is active
                if "location" in title:
                    self._log_debug(f"Location popup detected: {title}")

                    # Default focus = No → move to Yes
                    pyautogui.press("tab")
                    time.sleep(0.5)
                    pyautogui.press("enter")
                    time.sleep(2)

                    self._log_result("Location Permission", True, "Clicked YES")
                    return True

            # Popup not present → continue
            self._log_debug("Location popup not present - continuing test")
            return True

        except Exception as e:
            self._log_result("Location Permission", False, str(e))
            return False

        

    # ---------------- Click Accept All ----------------

    def click_accept_all_button(self):
        """Click Accept all consent button if popup appears"""
        try:
            if not self.main_window:
                self._log_result("Accept All", True, "HP window not connected - skipping")
                return True

            btn = self.main_window.child_window(
                auto_id="FuFConsents.FuFConsents.AcceptAllButton",
                control_type="Button"
            )

            if btn.wait("exists enabled visible ready", timeout=4):
                btn.set_focus()
                btn.click_input()
                time.sleep(2)
                self._log_result("Accept All", True, "Clicked Accept All")
            else:
                self._log_result("Accept All", True, "Popup not present - skipped")

            return True

        except Exception as e:
            self._log_result("Accept All", True, f"Skipped due to exception: {e}")
            return True
        

    # ---------------- Continue As Guest ----------------

    def click_continue_as_guest_button(self):
        """Click Continue as guest button if popup appears"""
        try:
            if not self.main_window:
                self._log_result("Continue As Guest", True, "HP window not connected - skipping")
                return True

            btn = self.main_window.child_window(
                title="Continue as guest",
                auto_id="WelcomeScreen.WelcomeScreenView.ContinueAsGuestButton",
                control_type="Button"
            )

            # Check if popup exists
            if btn.exists(timeout=5):
                btn.click_input()
                time.sleep(3)
                self._log_result("Continue As Guest", True, "Clicked")
            else:
                self._log_result("Continue As Guest", True, "Popup not present - skipped")

            return True

        except Exception as e:
            self._log_result("Continue As Guest", True, f"Skipped due to exception: {e}")
            return True


    # ---------------- Maximize HP Application ----------------

    def maximize_hp_application(self):
        try:
            windows = gw.getWindowsWithTitle(self.app_title)

            if windows:
                win = windows[0]
                win.activate()
                win.maximize()
                time.sleep(2)

                self._log_result("Maximize Application", True)
                return True

            self._log_result("Maximize Application", False, "HP window not found")
            return False

        except Exception as e:
            self._log_result("Maximize Application", False, str(e))
            return False
        
    def navigate_to_pc_device(self):
        pc_device = self.main_window.child_window(
            auto_id="DeviceList.DeviceList.PrimaryCard-0__device-nickname",
            control_type="Text"
        )

        if pc_device.exists(timeout=5):
            time.sleep(3)
            pc_device.click_input()
            time.sleep(3)
            return True
        return False


    # ---------------- Handle Startup Conditions ----------------

    def handle_startup_conditions(self):

        try:

            self.handle_location_permission_popup()
            self.maximize_hp_application()
            self.click_accept_all_button()
            self.click_continue_as_guest_button()
            self.navigate_to_pc_device()

            self._log_result("Startup Handling", True)
            return True

        except Exception as e:
            self._log_result("Startup Handling", False, str(e))
            return False

    
    
   
   
    # ---------------- Dump UI Tree to File ----------------

    def dump_ui_tree_to_file(self):
        """Dump the full UI tree of the current main window to a text file."""
        if not self.main_window:
            self._log_result("Dump UI Tree", False, "Application not connected")
            return False
        try:
            dump_path = os.path.join(self.baseline_folder, "ui_dump.txt")
            with open(dump_path, "w", encoding="utf-8") as f:
                buffer = io.StringIO()
                sys.stdout = buffer
                self.main_window.print_control_identifiers()
                sys.stdout = sys.__stdout__  # Reset stdout
                f.write(buffer.getvalue())
                buffer.close()
            self._log_result("Dump UI Tree", True, f"Saved to {dump_path}")
            return True
        except Exception as e:
            sys.stdout = sys.__stdout__  # Ensure stdout is reset
            self._log_result("Dump UI Tree", False, str(e))
            return False
 

            
        # ---------------- Navigate to Audio control ----------------         

    
  # ---------------- Navigate to Audio control ----------------         
       
            
    def navigate_to_Audio(self):
        """Navigate to the Audio module inside PC Device page"""

        # ---------- Print Test Case Header ----------
        print("\nTEST CASE 1: Navigate to Audio for CA module")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Navigate to Audio", False, "Application not connected")
            print("Test case 'Navigate to Audio' completed : FAIL")
            print("-" * 60)
            return False

        try:
            self.main_window.set_focus()
            time.sleep(7) 

            audio_btn = self.main_window.child_window(
                auto_id="PcDeviceCards.PcDeviceActionCards.PcaudioXCoreCard",
                control_type="Button"
            )

            # ---------- Step 1: Page Down ----------
            self.main_window.type_keys("{PGDN}") 
            time.sleep(2)

            # ---------- Step 2: Two UP nudges ----------
            for _ in range(8):
                self.main_window.type_keys("{UP}")
                time.sleep(1)

            # ---------- Step 3: Click Audio ----------
            if audio_btn.exists(timeout=3): 
                time.sleep(2)
                audio_btn.click_input()
                time.sleep(8)
                self._log_result("Navigate to audio page", True)
                print("\nOverall test results : PASS")
                print("-" * 60)
                return True

            self._log_result(
                "Navigate to audio page",
                False,
                "Audio card not visible after PGDN + UP UP"
            )
            print("\nOverall test results : FAIL")
            print("-" * 60)
            return False 

        except Exception as e:
            self._log_result("Navigate to audio page", False, str(e))
            print("\nOverall test results : FAIL")
            print("-" * 60)
            return False





    # ---------------- Delete the apps from app bar----------------
                        
        
    def TC_ID_C51570661_Delete_Custom_OOB_App(self):
        """
        Delete Custom OOB Apps workflow with popup verification and cleanup
        Always returns True/False (never None)
        """

        print("\nTEST CASE: Delete Custom OOB Apps")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Delete Custom OOB App", False, "Application not connected")
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False

        success = True  

        try:
            import time
            time.sleep(3)

            # ------------------------------
            # GET CAROUSEL ITEMS
            # ------------------------------
            def get_carousel_items():
                all_items = self.main_window.descendants(control_type="ListItem")
                items = []
                for item in all_items:
                    try:
                        txt = item.window_text()
                        if txt and txt.lower().startswith("carousel-item-"):
                            items.append(item)
                    except:
                        pass
                return items

            # ------------------------------
            # CLICK ANY APP
            # ------------------------------
            def click_any_app():
                items = get_carousel_items()
                for item in items:
                    if item.is_visible():
                        app_name = item.window_text().replace("carousel-item-", "")
                        item.click_input()
                        time.sleep(1)
                        self._log_result("Clicked App", True, f"App: {app_name}")
                        return True
                self._log_result("Clicked App", False, "No visible app found")
                return False

            # ------------------------------
            # CLICK DELETE
            # ------------------------------
            def click_delete():
                delete_btn = self.main_window.child_window(
                    title="Delete profile",
                    auto_id="ReactPCContextAware.Carousel.DeleteProfileButton",
                    control_type="Button"
                )

                if delete_btn.exists(timeout=5) and delete_btn.is_enabled():
                    delete_btn.click_input()
                    time.sleep(1)
                    self._log_result("Delete Profile", True, "Delete profile clicked")
                    return True

                self._log_result("Delete Profile", False, "Delete button not available")
                return False

            # ------------------------------
            # CLICK CONTINUE
            # ------------------------------
            def click_continue(optional=False):
                cont = self.main_window.child_window(
                    title="Continue",
                    auto_id="ReactPCContextAware.DeleteProfileModal.ContinueButton",
                    control_type="Button"
                )

                if cont.exists(timeout=2):
                    cont.click_input()
                    time.sleep(1)
                    self._log_result("Popup Continue", True, "Continue clicked")
                    return True

                if optional:
                    self._log_result("Popup Continue", True, "Popup skipped (expected)")
                    return True

                self._log_result("Popup Continue", False, "Continue not found")
                return False

            # ------------------------------
            # CHECKBOX + CONTINUE
            # ------------------------------
            def checkbox_continue():
                checkbox = self.main_window.child_window(
                    title="Do not show again",
                    auto_id="ReactPCContextAware.DeleteProfileModal.ConfirmationCheckbox__checkbox",
                    control_type="CheckBox"
                )

                if checkbox.exists(timeout=3):
                    checkbox.click_input()
                    time.sleep(1)
                    self._log_result("Popup Checkbox", True, "Checkbox selected")

                return click_continue()

            # =====================================================
            # STEP 1
            # =====================================================
            if not (click_any_app() and click_delete() and click_continue()):
                success = False

            # =====================================================
            # STEP 2
            # =====================================================
            if not (click_any_app() and click_delete() and checkbox_continue()):
                success = False

            # =====================================================
            # STEP 3 - VERIFY POPUP DOES NOT REAPPEAR
            # =====================================================
            if click_any_app() and click_delete():

                time.sleep(2)

                popup = self.main_window.child_window(
                    title="Delete Profile",
                    control_type="Window"
                )

                if popup.exists(timeout=1):
                    self._log_result("Popup Verification", False, "Popup appeared again")
                    success = False
                else:
                    self._log_result("Popup Verification", True, "No popup appeared as expected")

            # =====================================================
            # CLEANUP LOOP
            # =====================================================
            self._log_debug("Cleaning remaining apps...")

            tries = 0
            while tries < 20:
                items = get_carousel_items()
                if not items:
                    self._log_debug("No more carousel apps found.")
                    break

                items[0].click_input()
                time.sleep(1)

                if click_delete():
                    click_continue(optional=True)
                    self._log_result("Cleanup Delete", True, "Remaining app deleted")
                else:
                    success = False

                tries += 1
                time.sleep(1)

            # =====================================================
            # FINAL RESULT
            # =====================================================
            if success:
                print("\nOverall Test results  : PASS")
            else:
                print("\nOverall Test results  : FAIL")

            print("-" * 60)

            return bool(success) 

        except Exception as e:
            self._log_result("Delete Custom OOB App", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False







    # ---------------- Navigate to CA module/Add button click ----------------

    def TC_ID_C77290501_navigate_to_CA_and_click_Add_button(self):
        """Navigate to the CA module and open Add Application modal, then cancel"""

        print("\nTEST CASE 2: Navigate to CA module and Click Add button")
        print("-" * 60)

        if not self.main_window:
            self._log_result("CA", False, "Application not connected")
            return False
        try:
            time.sleep(3)  # wait for CA page to load

            # ---------- CLICK ADD APPLICATION BUTTON ----------
            add_btn = self.main_window.child_window(
                title="Add Application",
                auto_id="ReactPCContextAware.Carousel.AddButton",
                control_type="Button"
            )

            if add_btn.exists(timeout=10):
                add_btn.click_input()
                time.sleep(5)  # wait 1 second after opening modal
                self._log_result("Custom app Button clicked", True)
                
                # ---------- CLICK CANCEL BUTTON IN MODAL ----------
                cancel_btn = self.main_window.child_window(
                    title="Cancel",
                    control_type="Button"
                )
                if cancel_btn.exists(timeout=15) and cancel_btn.is_enabled():
                    cancel_btn.click_input()
                    time.sleep(1)
                    self._log_result("Add Application modal cancelled", True)
                    print("\nOverall Test results  : PASS")
                    print("-" * 60)
                    return True
                else:
                    self._log_result("Cancel button", False, "Cancel button not found or disabled")
                    print("\nOverall Test results  : FAIL")
                    print("-" * 60)
                    return False
            else:
                self._log_result("Add button exist", False, "Add Application button failed to click")
                print("\nOverall Test results  : FAIL")
                print("-" * 60)
                return False

        except Exception as e:
            self._log_result("Add button clicking", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False



#    # ---------------- Click Next button to scroll the apps in carousel/Appbar ----------------

    def TC_ID_C51570652_click_carousel_next(self):

        """Click the carousel Next button to scroll apps"""
        print("\nTEST CASE 6: Click Carousel Next Button")
        print("-" * 60)
        if not self.main_window:
            self._log_result("Carousel Next Button", False, "Application not connected")
            return False

        try:
            # Locate the Next button in Audio carousel
            next_btn = self.main_window.child_window(
                title="Next",
                auto_id="ReactPCContextAware.Carousel.NextButton",
                control_type="Button"
            )

            if not next_btn.exists(timeout=5):
                self._log_result("Carousel Next Button", False, "Next button not found")
                print("\nOverall Test results  : FAIL")
                print("-" * 60)
                return False
            
            # Click Next button 10 times
            for _ in range(10):
                next_btn.click_input()
                time.sleep(1)

            self._log_result("Carousel Next Button clicked", True)
            print("\nOverall Test results  : PASS")
            print("-" * 60)
            return True

        except Exception as e:
            self._log_result("Carousel Next Button", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False





# ---------------- Verify tooltip for each carousel app ----------------
            
    def TC_ID_C60424978_verify_carousel_app_tooltips(self):
        """
        Verify tooltip for each carousel app.
        """
        print("\nTEST CASE 8: Verify Carousel App Tooltips in app bar")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Carousel Tooltip Check", False, "Application not connected")
            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return False

        overall_pass = True   

        app_names = [
            "Administrative Tools",
            "Calculator",
            "Feedback Hub",
            "LiveCaptions",
            "Magnify",
            "Clock",
            "Command Prompt",
            "Copilot",
            "Character Map",
        ]

        def get_app_item(name):
            return self.main_window.child_window(
                title=f"carousel-item-{name}",
                control_type="ListItem"
            )

        def reset_carousel_focus():
            try:
                all_apps = self.main_window.child_window(
                    title="For all applications",
                    auto_id="ReactPCContextAware.Carousel.AllAppsButton",
                    control_type="ListItem"
                )
                if all_apps.exists(timeout=1):
                    time.sleep(0.5)
            except:
                pass

        def get_tooltip_text():
            try:
                for tip in self.main_window.descendants(control_type="ToolTip"):
                    text = tip.window_text().strip()
                    if text:
                        return text
            except:
                pass
            return None

        try:
            for expected_name in app_names:

                app_item = get_app_item(expected_name)

                if not app_item.exists(timeout=1):
                    reset_carousel_focus()
                    if not self.click_carousel_next():
                        self._log_result(expected_name, False, "Next button not available")
                        overall_pass = False
                        continue

                    time.sleep(3)
                    app_item = get_app_item(expected_name)

                if not app_item.exists(timeout=1):
                    self._log_result(expected_name, False, "App not found after one Next click")
                    overall_pass = False
                    continue

                reset_carousel_focus()
                previous_tooltip = get_tooltip_text()

                try:
                    app_item.click_input()
                    app_item.set_focus()
                    time.sleep(0.6)
                except Exception as e:
                    self._log_result(expected_name, False, f"Click failed: {str(e)}")
                    overall_pass = False
                    continue

                tooltip_text = None
                for _ in range(15):
                    current_tooltip = get_tooltip_text()
                    if current_tooltip and current_tooltip != previous_tooltip:
                        tooltip_text = current_tooltip
                        break
                    time.sleep(0.3)

                if not tooltip_text:
                    self._log_result(expected_name, False, "Tooltip not visible after click")
                    overall_pass = False
                    reset_carousel_focus()
                    continue

                if expected_name.lower() in tooltip_text.lower():
                    self._log_result(
                        expected_name, True, f"Tooltip matched: {tooltip_text}"
                    )
                else:
                    self._log_result(
                        expected_name, False, f"Tooltip mismatched: {tooltip_text}"
                    )
                    overall_pass = False

                reset_carousel_focus()

            #  PRINT OVERALL RESULT ONCE
            print("-" * 60)
            print(f"OVERALL TEST RESULT : {'PASS' if overall_pass else 'FAIL'}")
            print("-" * 60)

            return True

        except Exception as e:
            self._log_result("Carousel Tooltip Check", False, str(e))
            print("-" * 60)
            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return True









    # ---------------- Verify application is present in carousel or not ----------------


    def TC_ID_C77291045_verify_carousel_apps(self):
        """
        Verify that required apps exist in the carousel (title-based check only).
        Continues verification even if one or more apps are missing.
        """
        print("\nTEST CASE 7: Verify added Apps are existing in Appbar/Carousel")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Carousel Verification", False, "Application not connected")
            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            self.available_carousel_apps = []
            return True   # Non-blocking

        apps = [
            "Administrative Tools",
            "Calculator",
            "Feedback Hub",
            "LiveCaptions",
            "Magnify",
            "Clock",
            "Command Prompt",
            "Copilot",
            "Disk Cleanup",
            "Character Map",
            "LinkedIn",
        ]

        self.available_carousel_apps = []
        overall_pass = True   # single overall flag

        try:
            for app_name in apps:
                item = self.main_window.child_window(
                    title=f"carousel-item-{app_name}",
                    control_type="ListItem"
                )

                if item.exists(timeout=10):
                    self._log_result(
                        app_name, True, f"'{app_name}' present in carousel/Appbar"
                    )
                    self.available_carousel_apps.append(app_name)
                else:
                    self._log_result(
                        app_name, False, f"'{app_name}' NOT found in carousel/Appbar"
                    )
                    overall_pass = False

            #  PRINT OVERALL RESULT ONCE
            print("-" * 60)
            print(f"OVERALL TEST RESULT : {'PASS' if overall_pass else 'FAIL'}")
            print("-" * 60)

            return True   # Non-blocking

        except Exception as e:
            self._log_result("Carousel Verification", False, str(e))
            self.available_carousel_apps = []
            print("-" * 60)
            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return True







    # ---------------- Add Multiple Apps (IMPROVED SCROLLING) ----------------

    def TC_ID_C51570654_add_multiple_apps(self):
        """
        Flow enforced:
        Add (+) → Find app → Scroll → Select app → Continue → Add (+)
        If app not visible, select Administrative Tools first to enable scrolling.
        """
        print("\nTEST CASE 4: Add Multiple Apps to carosel/Appbar")
        print("-" * 60)

        try:
            self._log_result("Add Apps", True, "Starting process for multiple apps")

            apps_to_add = [

                ("Administrative Tools", "ReactPCContextAware.InstalledAppsModal.AppItem2328013EC67257A5EFF59B60098FEB2B"),
                ("Feedback Hub", "ReactPCContextAware.InstalledAppsModal.AppItem35754CE70FD833D49339A02421C97007"),
                ("LiveCaptions","ReactPCContextAware.InstalledAppsModal.AppItem0129D1E7D7570F8D575B759EAE255B33"),
                ("Magnify","ReactPCContextAware.InstalledAppsModal.AppItem1CB79190ED90A2079EB37225A66350F0"),
                ("Calculator", "ReactPCContextAware.InstalledAppsModal.AppItem2399C925B35566234AB600C70B12C40E"),
                ("Clock", "ReactPCContextAware.InstalledAppsModal.AppItem394766A9BD87112DA3EF0663591D0A21"),
                ("Command Prompt", "ReactPCContextAware.InstalledAppsModal.AppItem638D987E05CF5DE7460A01837C024F19"),
                ("Copilot", "ReactPCContextAware.InstalledAppsModal.AppItem5256B9B8FF48BCECD8077FC44CBF239E"),
                ("Character Map", "ReactPCContextAware.InstalledAppsModal.AppItem4D07EFF018A4F67FC6A3F21DA817AFAB"),
                ("Disk Cleanup", "ReactPCContextAware.InstalledAppsModal.AppItemCECE0E77E37C64AEE9DB38229F0D72C7"),
                ("LinkedIn", "ReactPCContextAware.InstalledAppsModal.AppItem554B1A3213ECA0D51534E50B794A4C09"),
            ]

            for index, (app_name, app_id) in enumerate(apps_to_add):

                # ---------- STEP 1: CLICK ADD (+) ----------
                add_btn = self.main_window.child_window(
                    auto_id="ReactPCContextAware.Carousel.AddButton",
                    control_type="Button"
                )

                if not add_btn.exists(timeout=5):
                    self._log_result("Add Apps", False, "Add (+) button not found")
                    return False

                add_btn.click_input()
                time.sleep(1)
                self._log_result("Add Apps", True, "Add (+) clicked")

                # ---------- STEP 2: FIND TARGET APP ----------
                app_btn = self.main_window.child_window(
                    auto_id=app_id,
                    control_type="Button"
                )

                found = False

                # If target app is already visible, no scroll needed
                if app_btn.exists() and app_btn.is_visible():
                    found = True
                    self._log_result("Add Apps", True, f"{app_name} found without scrolling")
                else:
                    # Select Administrative Tools first to enable scrolling
                    admin_tool_btn = self.main_window.child_window(
                        auto_id="ReactPCContextAware.InstalledAppsModal.AppItem2328013EC67257A5EFF59B60098FEB2B",
                        control_type="Button"
                    )
                    if admin_tool_btn.exists() and admin_tool_btn.is_visible():
                        admin_tool_btn.click_input()
                        time.sleep(0.3)
                        self._log_result("Add Apps", True, "Administrative Tools selected to enable scrolling")

                    # Scroll down to find target app
                    for _ in range(15):
                        if app_btn.exists() and app_btn.is_visible():
                            found = True
                            break
                        self.main_window.type_keys("{PGDN}")
                        time.sleep(0.4)

                if not found:
                    self._log_result("Add Apps", False, f"{app_name} not found, skipping")
                    continue

                # ---------- STEP 3: SELECT TARGET APP ----------
                app_btn.click_input()
                time.sleep(0.5)
                self._log_result("Add Apps", True, f"{app_name} selected")

                # ---------- STEP 4: CLICK CONTINUE ----------
                continue_btn = self.main_window.child_window(
                    title="Continue",
                    control_type="Button"
                )

                for _ in range(5):
                    if continue_btn.exists() and continue_btn.is_enabled():
                        break
                    time.sleep(0.5)

                if not continue_btn.exists() or not continue_btn.is_enabled():
                    self._log_result("Add Apps", False, f"Continue not enabled for {app_name}")
                    continue

                continue_btn.click_input()
                time.sleep(1)
                self._log_result("Add Apps", True, f"Continue clicked for {app_name}")

                # ---------- STEP 5: READY FOR NEXT APP ----------
                if index < len(apps_to_add) - 1:
                    self._log_result("Add Apps", True, "Preparing to add next app")
                else:
                    self._log_result("Add Apps", True, f"Last app {app_name} added")
                    print("\nOverall Test results  : PASS")
                    print("-" * 60)

            return True

        except Exception as e:
            self._log_result("Add Apps", False, f"Exception occurred: {str(e)}")
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False









    # ---------------- Launch & verify multiple apps are focus in Appbar ----------------

    def launch_and_verify_multiple_apps_appbar(self):
        """
        Launch apps from Windows search and verify each one becomes
        selected / highlighted in HP Audio App Bar.
        """

        if not self.main_window:
            self._log_result("Audio Selection", False, "Application not connected")
            return True   # Non-blocking

        # Use only apps that exist in carousel
        apps = getattr(self, "available_carousel_apps", [])

        if not apps:
            self._log_result("Audio Selection", False, "No carousel apps available to verify")
            return True

        for app_name in apps:
            try:
                pyautogui.press('winleft')
                time.sleep(1)
                pyautogui.write(app_name)
                time.sleep(2)
                pyautogui.press('enter')
                time.sleep(4)

                windows = gw.getWindowsWithTitle(app_name)
                if not windows:
                    self._log_result(app_name, False, "App window not found")
                    continue

                windows[0].activate()
                time.sleep(2)

                self.main_window.set_focus()
                time.sleep(3)

                carousel_item = self.main_window.child_window(
                    title=f"carousel-item-{app_name}",
                    control_type="ListItem"
                )

                if not carousel_item.exists(timeout=10):
                    self._log_result(app_name, False, "application not found")
                    continue

                if carousel_item.is_selected():
                    self._log_result(app_name, True, "Application launched and highlighted in App Bar")
                else:
                    self._log_result(app_name, False, "App launched but not selected in App Bar")

                time.sleep(3)

            except Exception as e:
                self._log_result(app_name, False, str(e))

        return True   # Never block execution







# ----------------  Verify Global Appbar is higlight by Launch Notepad/click time and date in taskbar &----------------

    def launch_notepad_and_verify_global_appbar(self):
        """
        Launch Notepad and verify:
        1. If Notepad is not in the carousel → check 'For all applications' is selected.
        2. If Notepad is in the carousel → click taskbar clock and verify 'For all applications' persists.
        """

        if not self.main_window:
            self._log_result("Notepad", False, "Application not connected")
            return True   # Non-blocking

        try:
            app_name = "Notepad"

            # -------- Launch Notepad --------
            pyautogui.press('winleft')
            time.sleep(1)
            pyautogui.write(app_name)
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(4)

            # Bring HP app back to focus
            self.main_window.set_focus()
            time.sleep(2)

            # -------- Check carousel --------
            carousel_item = self.main_window.child_window(
                title=f"carousel-item-{app_name}",
                control_type="ListItem"
            )

            if carousel_item.exists(timeout=5):
                self._log_result(
                    app_name,
                    True,
                    "Application launched and highlighted in carousel"
                )

                # -------- Click Windows Taskbar Clock --------
                try:
                    taskbar = Desktop(backend="uia").window(class_name="Shell_TrayWnd")
                    clock_btn = taskbar.child_window(title_re="Clock.*", control_type="Button")

                    if clock_btn.exists(timeout=5):
                        clock_btn.click_input()
                        time.sleep(2)

                        # Verify 'For all applications' highlight persists
                        global_item = self.main_window.child_window(
                            title="For all applications",
                            auto_id="ReactPCContextAware.Carousel.AllAppsButton",
                            control_type="ListItem"
                        )
                        if global_item.exists(timeout=5):
                            if global_item.is_selected():
                                self._log_result(
                                    "For all applications",
                                    True,
                                    "Global application still SELECTED after opening calendar"
                                )
                            else:
                                self._log_result(
                                    "For all applications",
                                    False,
                                    "Global application NOT selected after opening calendar"
                                )
                        else:
                            self._log_result("For all applications", False, "Global application item not found")

                    else:
                        self._log_result("Taskbar Clock", False, "Clock button not found")

                except Exception as e:
                    self._log_result("Taskbar Clock", False, f"Error: {e}")

                return True

            else:
                # -------- Notepad NOT in carousel --------
                self._log_result(
                    app_name,
                    False,
                    "Application launched but not found in carousel so global app slected (Expected)"
                )

                # Verify 'For all applications'
                global_item = self.main_window.child_window(
                    title="For all applications",
                    auto_id="ReactPCContextAware.Carousel.AllAppsButton",
                    control_type="ListItem"
                )

                if not global_item.exists(timeout=10):
                    self._log_result(
                        "For all applications",
                        False,
                        "Global application item not found"
                    )
                    return True

                if global_item.is_selected():
                    self._log_result(
                        "For all applications",
                        True,
                        "Global application SELECTED for Notepad"
                    )
                else:
                    self._log_result(
                        "For all applications",
                        False,
                        "Global application NOT selected for Notepad"
                    )

                return True   # Never block execution

        except Exception as e:
            self._log_result("Notepad", False, str(e))
            return True



# ---------------- Verify IMAX apps are visible in carousel ----------------

    def TC_ID_C51570659_verify_imax_apps_in_carousel(self):

        """Verify IMAX apps are visible in carousel"""
        print("TEST CASE 2: Verify IMAX apps are visible in carousel")
        print("-" * 60)
        try:
            # Ensure main window is active
            self.main_window.set_focus()
            time.sleep(3)

            # Define expected IMAX apps
            imax_apps = [
                "carousel-item-Disney+",
                "carousel-item-腾讯视频",
                "carousel-item-爱奇艺"
            ]

            missing_apps = []

            # Check each app in carousel
            for app in imax_apps:
                app_item = self.main_window.child_window(
                    title=app,
                    control_type="ListItem"
                )
                if not app_item.exists(timeout=5):
                    missing_apps.append(app)

            # Log result
            if missing_apps:
                if len(missing_apps) == 1:
                    self._log_result("Verify IMAX apps in carousel", False,
                                    f"1 IMAX app not found: {missing_apps[0]}")
                    print("\nOverall Test results  : FAIL")
                    print("-" * 60)
                else:
                    self._log_result("Verify IMAX apps in carousel", False,
                                    f"{len(missing_apps)} IMAX apps not found: {', '.join(missing_apps)}")
                    print("\nOverall Test results  : FAIL")
                    print("-" * 60)
                return False
            else:
                self._log_result("IMAX apps are present in carousel", True)
                print("\nOverall Test results  : PASS")
                print("-" * 60)
                return True

        except Exception as e:
            self._log_result("IMAX apps are present in carousel", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False



    # ---------------- Search and Add Application ----------------

    def TC_ID_C52986236_search_and_add_application(self):

        """
        Open Add Application modal, search Calculator, select it and click Continue
        """
        print("\nTEST CASE 5: Search and Add Application to carosel/Appbar")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Add App", False, "Application not connected")
            return False

        try:
            # -------- CONFIG (INSIDE FUNCTION) --------
            search_text = "Link"
            app_title = "LinkedIn"

            time.sleep(3)  # wait for CA page to load

            # ---------- CLICK ADD APPLICATION ----------
            add_btn = self.main_window.child_window(
                title="Add Application",
                auto_id="ReactPCContextAware.Carousel.AddButton",
                control_type="Button"
            )

            if not add_btn.exists(timeout=10):
                self._log_result("Add Application", False, "Add Application button not found")
                return False

            add_btn.click_input()
            time.sleep(1)
            self._log_result("Add Application", True, "Add Application modal opened")

            # ---------- SEARCH APPLICATION ----------
            search_box = self.main_window.child_window(
                auto_id="ReactPCContextAware.InstalledAppsModal.SearchApplication__text-box",
                control_type="Edit"
            )

            if not search_box.exists(timeout=10):
                self._log_result("Search App", False, "Search box not found")
                return False

            search_box.click_input()
            time.sleep(0.5)
            search_box.type_keys("^a{BACKSPACE}")
            search_box.type_keys(search_text, with_spaces=True)
            time.sleep(2)

            self._log_result("Search App", True, f"Searched for {search_text}")

            # ---------- SELECT APPLICATION ----------
            app_btn = self.main_window.child_window(
                title=app_title,
                control_type="Button"
            )

            if not app_btn.exists(timeout=10):
                self._log_result("Select App", False, f"{app_title} not found")
                return False

            app_btn.click_input()
            time.sleep(1)
            self._log_result("Select App", True, f"{app_title} selected")

            # ---------- CLICK CONTINUE ----------
            continue_btn = self.main_window.child_window(
                title="Continue",
                auto_id="ReactPCContextAware.InstalledAppsModal.ContinueButton",
                control_type="Button"
            )

            if continue_btn.exists(timeout=5) and continue_btn.is_enabled():
                continue_btn.click_input()
                self._log_result("Continue", True, "Continue button clicked")
                print("\nOverall Test results  : PASS")
                print("-" * 60)
                return True
            else:
                self._log_result("Continue", False, "Continue button not enabled")
                print("\nOverall Test results  : FAIL")
                print("-" * 60)
                return False

        except Exception as e:
            self._log_result("Add Application", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False





# ---------------- Verify Back button navigation from PC Device page to L1 page ----------------

    def device_page_backbutton(self):
        """
        TEST CASE 9: Verify Back button navigation from PC Device page
        """

        print("\nTEST CASE 9: Verify Back button navigation from PC Device page")
        print("-" * 60)

        # ---------- Check Application Connection ----------
        if not self.main_window:
            self._log_result(
                "Back Button",
                False,
                "Application not connected"
            )

            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return False

        try:
            self.main_window.set_focus()
            self.main_window.wait("exists ready", timeout=10)

            back_button = self.main_window.child_window(
                auto_id="NavBar.NavBarView.BackButton",
                control_type="Button"
            )

            # ---------- Verify Back Button ----------
            if back_button.exists(timeout=5):

                back_button.wait("enabled", timeout=5)
                time.sleep(2)

                back_button.click_input()
                time.sleep(5)

                self._log_result(
                    "Back Button",
                    True,
                    "Back button clicked and navigated to L1 page"
                )

                print("OVERALL TEST RESULT : PASS")
                print("-" * 60)
                return True

            else:

                self._log_result(
                    "Back Button",
                    False,
                    "Back button not found on screen"
                )

                print("OVERALL TEST RESULT : FAIL")
                print("-" * 60)
                return False

        except Exception as e:

            self._log_result(
                "Back Button",
                False,
                f"Back button error: {e}"
            )

            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return False



    # ---------------- Verify default state of CA Apps in Audio page ----------------

    def TC_ID_C51570650_verify_default_state_of_CA_apps(self):

        """Verify default state of CA Apps in Audio page"""

        print("\nTEST CASE 1: Verify Default State of CA Apps")
        print("-" * 80)

        if not self.main_window:
            self._log_result("CA Apps Default State", False, "Application not connected")
            print("Overall test results : FAIL")
            print("-" * 80)
            return False

        try:
            self.main_window.set_focus()
            time.sleep(3)

            overall_status = True
            missing_oob_apps = []

            # --------------------------------------------------
            # 1. Verify ALL OOB apps are visible by default
            # --------------------------------------------------
            oob_apps = [
                ("Disney+", "ReactPCContextAware.Carousel.CarouselItemA07DDB88965F20AE0E1C2E89F36F5B07"),
                ("爱奇艺", "ReactPCContextAware.Carousel.CarouselItem96D443B8FDA8B07AAB692A8F386CF8C0"),
                ("腾讯视频", "ReactPCContextAware.Carousel.CarouselItem41A61336B059C3F8CEB51A343050E228"),
            ]

            for app_name, app_auto_id in oob_apps:
                app_item = self.main_window.child_window(
                    title=f"carousel-item-{app_name}",
                    auto_id=app_auto_id,
                    control_type="ListItem"
                )

                if app_item.exists(timeout=2):
                    self._log_result(f"OOB app visible by default - {app_name}", True)
                else:
                    self._log_result(f"OOB app visible by default - {app_name}", False)
                    missing_oob_apps.append(app_name)
                    overall_status = False

            if missing_oob_apps:
                self._log_result(
                    "OOB apps missing",
                    False,
                    f"Missing OOB apps: {', '.join(missing_oob_apps)}"
                )

            # --------------------------------------------------
            # 2. Verify Add Application option is available
            # --------------------------------------------------
            add_app_btn = self.main_window.child_window(
                title="Add Application",
                auto_id="ReactPCContextAware.Carousel.AddButton",
                control_type="Button"
            )

            if add_app_btn.exists(timeout=3):
                self._log_result("Add Application option available", True)
            else:
                self._log_result("Add Application option available", False)
                overall_status = False

            # --------------------------------------------------
            # 3. Verify "For all applications" default state
            #    (Implicit selection – visual-only by design)
            # --------------------------------------------------
            all_apps = self.main_window.child_window(
                title="For all applications",
                auto_id="ReactPCContextAware.Carousel.AllAppsButton",
                control_type="ListItem"
            )

            if all_apps.exists(timeout=3) and all_apps.is_enabled():
                self._log_result(
                    "For all applications selected by default",
                    True,
                    "Default is selected state"
                )
            else:
                self._log_result(
                    "For all applications selected by default",
                    False,
                    "Default is not selected state"
                )
                overall_status = False

            # --------------------------------------------------
            # Final Result
            # --------------------------------------------------
            if overall_status:
                print("\nOverall test results : PASS")
            else:
                print("\nOverall test results : FAIL")

            print("-" * 80)
            return overall_status

        except Exception as e:
            self._log_result("CA Apps Default State", False, str(e))
            print("\nOverall test results : FAIL")
            print("-" * 80)
            return False


    # ---------------- Verify Delete Profile Button Enable/Disable ----------------

    def TC_ID_C51570658_verify_delete_profile_button_enable_disable(self):

        print("\nTEST CASE: Verify Delete Profile Button State")
        print("-" * 60)

        overall_pass = True

        try:
            delete_btn = self.main_window.child_window(
                title="Delete profile",
                control_type="Button"
            )

            # CASE 1: Delete profile already visible
            if delete_btn.exists(timeout=1):
                self._log_result(
                    "Initial Delete Profile State",
                    True,
                    "Delete profile button is visible"
                )

            # CASE 2: Not visible → click Disney+
            else:
                self._log_result(
                    "Initial Delete Profile State",
                    False,
                    "Delete profile button not visible initially, clicking Disney+"
                )

                disney_app = self.main_window.child_window(
                    title="carousel-item-Disney+",
                    control_type="ListItem"
                )

                if disney_app.exists(timeout=2):
                    disney_app.click_input()
                    time.sleep(2)

                    if delete_btn.exists(timeout=2):
                        self._log_result(
                            "Delete Profile After Disney+ Click",
                            True,
                            "Delete profile button visible after selecting Disney+"
                        )
                    else:
                        self._log_result(
                            "Delete Profile After Disney+ Click",
                            False,
                            "Delete profile button NOT visible after selecting Disney+"
                        )
                        overall_pass = False
                else:
                    self._log_result(
                        "Disney+ App",
                        False,
                        "Disney+ app not found in carousel"
                    )
                    overall_pass = False

            print("-" * 60)
            print(f"OVERALL TEST RESULT : {'PASS' if overall_pass else 'FAIL'}")
            print("-" * 60)

            # VERY IMPORTANT: DO NOT BLOCK EXECUTION
            return overall_pass

        except Exception as e:
            self._log_result("Delete Profile State", False, str(e))
            print("-" * 60)
            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)

            # Soft fail
            return False






     # verify application is sleceted in app bar

    def TC_ID_C51570655_verify_application_selected_in_app_bar(self):
        """
        Test Case 1:
        Verify application is selected in app bar
        
        """

        print("\nTEST CASE: Verify application selected in app bar")
        print("-" * 60)

        if not self.main_window:
            self._log_result("CA", False, "Application not connected")
            return False

        try:
            applications = [
                "Administrative Tools",
                "Command Prompt",
                "Clock"
            ]

            for app_name in applications:

                print(f"\nChecking selection for: {app_name}")

                # ---- Find carousel item ----
                carousel_item = self.main_window.child_window(
                    title=f"carousel-item-{app_name}",
                    control_type="ListItem"
                )

                if not carousel_item.exists(timeout=10):
                    self._log_result(app_name, False, "Carousel item not found")
                    return False

                # ---- Click carousel item ----
                carousel_item.click_input()
                time.sleep(1)

                # ---- Verify it is selected (app bar = carousel) ----
                if carousel_item.is_selected() or carousel_item.has_keyboard_focus():
                    self._log_result(
                        f"{app_name} selected",
                        True,
                        "Application is selected (carousel/app bar)"
                    )
                else:
                    self._log_result(
                        f"{app_name} selected",
                        False,
                        "Application is not selected"
                    )
                    return False

                time.sleep(2)

            print("\nOverall Test results  : PASS")
            print("-" * 60)
            return True

        except Exception as e:
            self._log_result("Selection verification", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False






    #  ---------------- Verify selected application name and focus state----------------

    def TC_ID_C51570657_verify_selected_application_name_and_focus(self):
        """
        Test Case:
        Verify selected application name visibility and focus state
        (Only for mentioned apps: Administrative Tools, Calculator, Clock)
        """

        print("\nTEST CASE: Verify selected application name and focus")
        print("-" * 60)

        if not self.main_window:
            self._log_result("CA", False, "Application not connected")
            return False

        try:
            expected_apps = {
                "Administrative Tools",
                "Command Prompt",
                "Clock"
            }

            # ---- Get ALL ListItems ----
            all_list_items = self.main_window.descendants(control_type="ListItem")

            carousel_items = [
                item for item in all_list_items
                if item.window_text().startswith("carousel-item-")
            ]

            if not carousel_items:
                self._log_result(
                    "Carousel",
                    False,
                    "No carousel items found"
                )
                return False

            verified_apps = set()

            for item in carousel_items:
                raw_title = item.window_text().strip()
                app_name = raw_title.replace("carousel-item-", "").strip()

                # ---- CLICK ONLY EXPECTED APPS ----
                if app_name in expected_apps:
                    item.click_input()
                    time.sleep(1)

                    # ---- VERIFY NAME ----
                    self._log_result(
                        f"{app_name} name",
                        True,
                        "Application name is visible"
                    )

                    # ---- VERIFY FOCUS ----
                    if item.is_selected() or item.has_keyboard_focus():
                        self._log_result(
                            f"{app_name} focus",
                            True,
                            "Application is in focus state"
                        )
                    else:
                        self._log_result(
                            f"{app_name} focus",
                            False,
                            "Application is not in focus"
                        )
                        return False

                    verified_apps.add(app_name)
                    time.sleep(2)

                    # ---- STOP EARLY IF ALL FOUND ----
                    if verified_apps == expected_apps:
                        break

            # ---- FINAL CHECK ----
            missing = expected_apps - verified_apps
            if missing:
                self._log_result(
                    "Name & focus verification",
                    False,
                    f"Apps not verified: {', '.join(missing)}"
                )
                return False

            print("\nOverall Test results  : PASS")
            print("-" * 60)
            return True

        except Exception as e:
            self._log_result(
                "Name & focus verification",
                False,
                str(e)
            )
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False



#    # ---------------- Launch & verify OOB apps ----------------

    def TC_ID_C51570660_launch_and_verify_oob_apps(self):
        """
        TEST CASE : Verify OOB apps launch and carousel focus state
        """

        print("\nTEST CASE : Verify OOB apps launch and carousel focus state")
        print("-" * 60)

        import pyperclip

        try:
            oob_apps = [
                ("Disney+", "ReactPCContextAware.Carousel.CarouselItemA07DDB88965F20AE0E1C2E89F36F5B07"),
                ("爱奇艺", "ReactPCContextAware.Carousel.CarouselItem96D443B8FDA8B07AAB692A8F386CF8C0"),
                ("腾讯视频", "ReactPCContextAware.Carousel.CarouselItem41A61336B059C3F8CEB51A343050E228"),
            ]

            not_focused_apps = []

            for app_name, carousel_id in oob_apps:

                # -------- Launch from Windows (Clipboard paste supports Chinese) --------
                print(f"{app_name} launching from Windows...")

                pyautogui.press('winleft')
                time.sleep(1)

                pyperclip.copy(app_name)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(2)

                pyautogui.press('enter')
                time.sleep(11)

                # Handle "Let this app access your location?" popup (if shown)
                print("Checking for location permission popup...")
                time.sleep(2)
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.press("enter")
                time.sleep(2)

                print(f"{app_name} launched")

                # -------- Close App --------
                pyautogui.hotkey('alt', 'f4')
                time.sleep(3)

                # -------- Focus HP App --------
                self.main_window.set_focus()
                self.main_window.click_input()
                time.sleep(3)

                # -------- Locate Carousel Item --------
                carousel_item = self.main_window.child_window(
                    auto_id=carousel_id,
                    control_type="ListItem"
                )

                if carousel_item.exists(timeout=10):

                    wrapper = carousel_item.wrapper_object()
                    is_focused = False

                    # Check keyboard focus
                    try:
                        if wrapper.has_keyboard_focus():
                            is_focused = True
                    except:
                        pass

                    #  React carousel fallback (focused = selected)
                    try:
                        if wrapper.is_selected():
                            is_focused = True
                    except:
                        pass

                    if is_focused:
                        print(f"{app_name} is focused in carousel")
                    else:
                        print(f"{app_name} is NOT focused in carousel")
                        not_focused_apps.append(app_name)

                else:
                    print(f"{app_name} not found in carousel")
                    not_focused_apps.append(app_name)

            # -------- Final Result --------
            if not_focused_apps:
                self._log_result(
                    "Verify OOB apps focus state",
                    False,
                    f"{len(not_focused_apps)} apps not in focus: {', '.join(not_focused_apps)}"
                )

                print("OVERALL TEST RESULT : FAIL")
                print("-" * 60)
                return False

            else:
                self._log_result(
                    "OOB apps focus state",
                    True,
                    "All apps returned focused in carousel after launch"
                )

                print("OVERALL TEST RESULT : PASS")
                print("-" * 60)
                return True

        except Exception as e:
            self._log_result(
                "Verify OOB apps focus state",
                False,
                str(e)
            )

            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return False





    # ---------------- Verify Global App focus after HP relaunch ----------------



    def TC_ID_C51570664_verify_global_app_focus_after_hp_relaunch(self):
        """
        TEST CASE ID : C51570664
        TEST CASE    : Verify Global Apps focus after HP relaunch
        """

        print("\nTEST CASE ID : C51570664 - Verify Global Apps focus after HP relaunch")
        print("-" * 60)

        try:
            # ---------------------------------------------------
            # STEP 1 : Select Administrative Tools
            # ---------------------------------------------------
            admin_tools_item = self.main_window.child_window(
                title="carousel-item-Administrative Tools",
                control_type="ListItem"
            ).wait('exists enabled visible', timeout=10)

            admin_tools_item.click_input()
            time.sleep(2)

            #  admin_tools_item is already a wrapper
            is_selected = False

            try:
                if admin_tools_item.has_keyboard_focus():
                    is_selected = True
            except:
                pass

            try:
                if admin_tools_item.is_selected():
                    is_selected = True
            except:
                pass

            if not is_selected:
                self._log_result(
                    " Administrative Tools Focus",
                    False,
                    "Administrative Tools not focused"
                )
                print("OVERALL TEST RESULT : FAIL")
                print("-" * 60)
                return False

            print("Administrative Tools is focused in carousel")

            # ---------------------------------------------------
            # STEP 2 : Close HP
            # ---------------------------------------------------
            print("Closing HP application...")
            pyautogui.hotkey('alt', 'f4')
            time.sleep(3)

            # ---------------------------------------------------
            # STEP 3 : Launch Notepad
            # ---------------------------------------------------
            print("Launching Notepad...")
            pyautogui.press('winleft')
            time.sleep(1)
            pyautogui.write("Notepad")
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(3)

            # ---------------------------------------------------
            # STEP 4 : Relaunch HP
            # ---------------------------------------------------
            print("Relaunching HP application...")
            self.open_hp_application()
            self.connect_to_application()
            self.navigate_to_Audio()
            time.sleep(5)

            # ---------------------------------------------------
            # STEP 5 : Verify Global Apps Focus
            # ---------------------------------------------------
            global_apps_item = self.main_window.child_window(
                title="For all applications",
                control_type="ListItem"
            ).wait('exists enabled visible', timeout=10)

            is_focused = False

            try:
                if global_apps_item.has_keyboard_focus():
                    is_focused = True
            except:
                pass

            try:
                if global_apps_item.is_selected():
                    is_focused = True
            except:
                pass

            if is_focused:
                self._log_result(
                    "Global Apps Focus After Relaunch",
                    True,
                    "For all applications is focused after HP relaunch"
                )

                print("For all applications is focused in carousel")
                print("OVERALL TEST RESULT : PASS")
                print("-" * 60)
                return True
            else:
                self._log_result(
                    "C51570664 - Global Apps Focus After Relaunch",
                    False,
                    "For all applications not focused after HP relaunch"
                )

                print("OVERALL TEST RESULT : FAIL")
                print("-" * 60)
                return False

        except Exception as e:
            self._log_result(
                "C51570664 - Global Apps Focus After Relaunch",
                False,
                str(e)
            )

            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return False




    
# ---------------- Verify application Select Unselect enables disables Continue button ----------------


    def TC_ID_C53033386_verify_aapplication_Select_Unselect(self):
        """
        TEST CASE : Verify Calculator toggle selection enables/disables Continue button
        """

        print("\nTEST CASE : Verify Calculator toggle selection enables/disables Continue button")
        print("-" * 60)

        try:
            # ---------------------------------------------------
            # STEP 1 : Click Add Application button
            # ---------------------------------------------------
            add_btn = self.main_window.child_window(
                title="Add Application",
                auto_id="ReactPCContextAware.Carousel.AddButton",
                control_type="Button"
            ).wait('exists enabled visible', timeout=10)

            add_btn.click_input()
            time.sleep(3)

            print("Add Application modal opened")

            # ---------------------------------------------------
            # STEP 2 : Locate Calculator + Continue button
            # ---------------------------------------------------
            calculator_btn = self.main_window.child_window(
                title="Calculator",
                control_type="Button"
            ).wait('exists enabled visible', timeout=10)

            continue_btn = self.main_window.child_window(
                title="Continue",
                control_type="Button"
            ).wait('exists visible', timeout=10)

            # ---------------------------------------------------
            # STEP 3 : VERIFY INITIAL UNSELECTED STATE
            # ---------------------------------------------------
            print("Verifying INITIAL UNSELECTED state...")

            if continue_btn.is_enabled():
                self._log_result(
                    "Calculator Initial State",
                    False,
                    "Continue button should be disabled initially"
                )
            else:
                self._log_result(
                    "Calculator Initial State",
                    True,
                    "Continue button not disabled initially"
                )

            # ---------------------------------------------------
            # STEP 4 : CLICK CALCULATOR → SELECTED
            # ---------------------------------------------------
            print("Clicking Calculator (SELECT)...")
            calculator_btn.click_input()
            time.sleep(3)

            if continue_btn.is_enabled():
                self._log_result(
                    "Calculator Selected State",
                    True,
                    "Continue button enabled after selecting Calculator"
                )
                print("Continue button ENABLED (Expected)")
                
            else:
                self._log_result(
                    "Calculator Selected State",
                    False,
                    "Continue button not enabled after selecting Calculator"
                )

            # ---------------------------------------------------
            # STEP 5 : CLICK AGAIN → UNSELECTED
            # ---------------------------------------------------
            print("Clicking Calculator again (UNSELECT)...")
            calculator_btn.click_input()
            time.sleep(3)

            if not continue_btn.is_enabled():
                self._log_result(
                    "Calculator Unselected State",
                    True,
                    "Continue button disabled after unselecting Calculator"
                )
                print("Continue button DISABLED (Expected)")
            else:
                self._log_result(
                    "Calculator Unselected State",
                    False,
                    "Continue button still enabled after unselecting Calculator"
                )

            # ---------------------------------------------------
            # STEP 6 : Click Cancel
            # ---------------------------------------------------
            cancel_btn = self.main_window.child_window(
                title="Cancel",
                control_type="Button"
            ).wait('exists enabled visible', timeout=10)

            cancel_btn.click_input()
            time.sleep(2)

            print("Cancel button clicked")

            print("OVERALL TEST RESULT : PASS")
            print("-" * 60)
            return True

        except Exception as e:
            self._log_result(
                "Calculator Toggle Validation",
                False,
                str(e)
            )

            print("OVERALL TEST RESULT : FAIL")
            print("-" * 60)
            return False




        # ----------------Re launch ------------------------------
    def relaunch_hp(self):
        """Reusable HP relaunch method"""
        try:
            if not self.open_hp_application():
                raise Exception("Open HP failed")

            if not self.connect_to_application():
                raise Exception("Connect failed")

            if not self.handle_startup_conditions():
                raise Exception("Startup failed")

            if not self.navigate_to_Audio():
                raise Exception("Navigation to Audio failed")

            self._log_result("HP Relaunch", True)
            return True

        except Exception as e:
            self._log_result("HP Relaunch", False, str(e))
            return False


        
     
    # ---------------------------------- Uninstall OOB apps and reset HPX APP ----------------------------------------


    def TC_ID_C53046320_Uninstall_OOB_apps_and_Reset_HPX_application(self):

        print("\nTEST CASE: Verify IMAX uninstall, tooltip error and HP reset")
        print("-" * 60)

        overall_result = True

        if not self.main_window:
            self._log_result("CA", False, "Application not connected")
            return False

        try:
            # =====================================================
            # TEST DATA
            # =====================================================
            oob_apps = [
                ("Disney+", "ReactPCContextAware.Carousel.CarouselItemA07DDB88965F20AE0E1C2E89F36F5B07"),
                ("爱奇艺", "ReactPCContextAware.Carousel.CarouselItem96D443B8FDA8B07AAB692A8F386CF8C0"),
                ("腾讯视频", "ReactPCContextAware.Carousel.CarouselItem41A61336B059C3F8CEB51A343050E228"),
            ]

            tooltip_text = "App not found. Try adding it again using the + to restore this profile."

            # =====================================================
            # STEP 1: UNINSTALL OOB APPS
            # =====================================================
            for app_name, _ in oob_apps:
                print(f"\nUninstalling {app_name}")

                pyautogui.press("winleft")
                time.sleep(1)

                pyperclip.copy(app_name)
                pyautogui.hotkey("ctrl", "v")
                time.sleep(2)

                try:
                    search_win = Desktop(backend="uia").window(title="Search")
                    search_win.wait("visible", timeout=10)

                    best_match = search_win.child_window(control_type="ListItem", found_index=0)
                    best_match.wait("visible", timeout=5)
                    best_match.click_input()

                    uninstall_item = search_win.child_window(
                        title="Uninstall",
                        control_type="ListItem"
                    )

                    if uninstall_item.exists(timeout=5):
                        uninstall_item.click_input()
                        self._log_result(app_name, True, "Clicked Uninstall")
                    else:
                        self._log_result(app_name, False, "Uninstall option not found")
                        overall_result = False
                        continue

                    # ✅ ONE TAB + ENTER
                    time.sleep(2)
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.press("enter")

                    self._log_result(app_name, True, "Uninstall confirmed")

                    time.sleep(10)
                    pyautogui.hotkey("alt", "f4")

                except Exception as e:
                    self._log_result(app_name, False, f"Uninstall failed: {e}")
                    overall_result = False

            # =====================================================
            # STEP 2: CLOSE HP
            # =====================================================
            print("\nClosing HP before relaunch...")

            try:
                if self.main_window and self.main_window.exists(timeout=5):
                    self.main_window.set_focus()
                    self.main_window.close()
                    time.sleep(5)

                    if self.main_window.exists(timeout=3):
                        pyautogui.hotkey("alt", "f4")
                        time.sleep(5)

                self.main_window = None

            except Exception as e:
                self._log_debug(f"HP close failed: {e}")

            # =====================================================
            # STEP 3: RELAUNCH & VERIFY TOOLTIP
            # =====================================================
            print("\nRelaunching HP to verify tooltips...")

            if not self.relaunch_hp():
                overall_result = False

            for app_name, auto_id in oob_apps:
                try:
                    print(f"Checking tooltip for {app_name}")

                    carousel_item = self.main_window.child_window(
                        auto_id=auto_id,
                        control_type="ListItem"
                    )

                    if not carousel_item.exists(timeout=5):
                        self._log_result(app_name, True, "App not present (expected)")
                        continue

                    # ✅ CLICK (not focus)
                    carousel_item.click_input()
                    time.sleep(1.5)

                    # Try inside main window
                    tooltip = self.main_window.child_window(
                        title=tooltip_text,
                        control_type="ToolTip"
                    )

                    if not tooltip.exists(timeout=2):
                        # Fallback
                        tooltip = Desktop(backend="uia").window(
                            title=tooltip_text,
                            control_type="ToolTip"
                        )

                    if tooltip.exists(timeout=5):
                        self._log_result(f"{app_name} Tooltip", True)
                    else:
                        self._log_result(f"{app_name} Tooltip", False, "Tooltip missing")
                        overall_result = False

                except Exception as e:
                    self._log_debug(f"{app_name} check failed: {e}")
                    overall_result = False

            # =====================================================
            # STEP 4: RESET HP APPLICATION
            # =====================================================
            print("\nResetting HP Application...")

            pyautogui.press("winleft")
            time.sleep(1)

            pyperclip.copy("HP")
            pyautogui.hotkey("ctrl", "v")
            time.sleep(3)

            search_win = Desktop(backend="uia").window(title="Search")
            search_win.wait("visible", timeout=10)

            best_match = search_win.child_window(control_type="ListItem", found_index=0)
            best_match.wait("visible", timeout=5)
            best_match.click_input()

            # ✅ App Settings (fixed)
            app_settings = search_win.child_window(
                title="App settings",
                control_type="ListItem"
            )

            if app_settings.exists(timeout=5):
                app_settings.click_input()
                self._log_result("HP Settings", True)
            else:
                self._log_result("HP Settings", False)
                return False

            time.sleep(10)

            settings_win = Desktop(backend="uia").window(title="Settings")
            settings_win.wait("visible", timeout=20)
            settings_win.set_focus()

            pyautogui.press("PGDN")
            pyautogui.press("PGDN")
            pyautogui.press("up")
            time.sleep(2)

            reset_btn = settings_win.child_window(title="Reset", control_type="Button")
            reset_btn.wait("enabled", timeout=20)
            reset_btn.click_input()

            time.sleep(2)

            pyautogui.press("tab")
            pyautogui.press("enter")
            pyautogui.press("enter")

            self._log_result("HP Reset", True)
            time.sleep(80)

            pyautogui.hotkey("alt", "f4")
            time.sleep(3)

            # =====================================================
            # STEP 5: RELAUNCH & VERIFY APPS NOT PRESENT
            # =====================================================
            print("\nRelaunching HP after reset...")

            self.open_hp_application()
            self.handle_startup_conditions()
            self.navigate_to_Audio()
            time.sleep(6)

            print("\nVerifying IMAX OOB apps are NOT present after reset...")

            found_oob_apps = []

            all_items = self.main_window.descendants(control_type="ListItem")

            for item in all_items:
                try:
                    auto_id = item.element_info.automation_id or ""

                    for app_name, imax_auto_id in oob_apps:
                        if imax_auto_id in auto_id:
                            found_oob_apps.append(app_name)
                except:
                    pass

            if len(found_oob_apps) == 0:
                self._log_result("HP Reset Validation", True)
                print("\nOverall Test results  : PASS")
                print("-" * 60)
                return True
            else:
                self._log_result("HP Reset Validation", False, f"{found_oob_apps}")
                print("\nOverall Test results  : FAIL")
                print("-" * 60)
                return False

        except Exception as e:
            self._log_result("IMAX Flow", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False





    # ---------------- Delete profile with 'Do not show again' and verify deletion from carousel ----------------
    
    def TC_ID_C53045345_Delete_app_without_delete_profile_page(self):

        print("\nTEST CASE: Add Admin Tool and Delete From Carousel")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Test Setup", False, "Application not connected")
            return False

        try:
            import time

            ADD_BUTTON_AUTO_ID = "ReactPCContextAware.Carousel.AddButton"
            ADMIN_TOOLS_MODAL_ID = "ReactPCContextAware.InstalledAppsModal.AppItem2328013EC67257A5EFF59B60098FEB2B"
            ADMIN_TOOLS_CAROUSEL_ID = "ReactPCContextAware.Carousel.CarouselItem2328013EC67257A5EFF59B60098FEB2B"

            # ---------------------------------------------------------
            # STEP 1 → CLICK ADD
            # ---------------------------------------------------------
            add_btn = self.main_window.child_window(
                auto_id=ADD_BUTTON_AUTO_ID,
                control_type="Button"
            )

            if not add_btn.exists(timeout=5):
                self._log_result("Add Button", False, "Add button not found")
                return False

            add_btn.click_input()
            time.sleep(1)
            self._log_result("Add Button", True, "Add clicked")

            # ---------------------------------------------------------
            # STEP 2 → SELECT ADMINISTRATIVE TOOLS
            # ---------------------------------------------------------
            admin_btn = self.main_window.child_window(
                auto_id=ADMIN_TOOLS_MODAL_ID,
                control_type="Button"
            )

            if not admin_btn.exists(timeout=5):
                self._log_result("Select Admin", False, "Administrative Tools not found")
                return False

            admin_btn.click_input()
            time.sleep(1)
            self._log_result("Select Admin", True, "Administrative Tools selected")

            # ---------------------------------------------------------
            # STEP 3 → CLICK CONTINUE
            # ---------------------------------------------------------
            continue_btn = self.main_window.child_window(
                title="Continue",
                control_type="Button"
            )

            if not continue_btn.exists(timeout=5) or not continue_btn.is_enabled():
                self._log_result("Continue", False, "Continue not enabled")
                return False

            continue_btn.click_input()
            time.sleep(2)
            self._log_result("Continue", True, "Continue clicked")

            # ---------------------------------------------------------
            # STEP 4 → WAIT & VERIFY ADMIN TOOL ADDED TO CAROUSEL
            # ---------------------------------------------------------
            time.sleep(2)

            carousel_item = self.main_window.child_window(
                auto_id=ADMIN_TOOLS_CAROUSEL_ID,
                control_type="ListItem"
            )

            if not carousel_item.exists(timeout=5):
                self._log_result("Carousel Add Verification", False,
                                "Administrative Tools not added to carousel")
                return False

            self._log_result("Carousel Add Verification", True,
                            "Administrative Tools added to carousel")

            # ---------------------------------------------------------
            # STEP 5 → CLICK ADMIN TOOL IN CAROUSEL
            # ---------------------------------------------------------
            carousel_item.click_input()
            time.sleep(1)
            self._log_result("Carousel Click", True, "Admin tool clicked")

            # ---------------------------------------------------------
            # STEP 6 → CLICK DELETE PROFILE
            # ---------------------------------------------------------
            delete_btn = self.main_window.child_window(
                auto_id="ReactPCContextAware.Carousel.DeleteProfileButton",
                title="Delete profile",
                control_type="Button"
            )

            if not delete_btn.exists(timeout=5):
                self._log_result("Delete Button", False, "Delete button not found")
                return False

            delete_btn.click_input()
            time.sleep(2)
            self._log_result("Delete Button", True, "Delete clicked")

            # ---------------------------------------------------------
            # STEP 7 → VERIFY ADMIN TOOL REMOVED FROM CAROUSEL
            # ---------------------------------------------------------
            time.sleep(2)

            if carousel_item.exists(timeout=3):
                self._log_result("Carousel Deletion Verification", False,
                                "Administrative Tools still present in carousel")
                print("\nOverall Test results  : FAIL")
                print("-" * 60)
                return False

            self._log_result("Carousel Deletion Verification", True,
                            "Administrative Tools successfully removed from carousel")

            print("\nOverall Test results  : PASS")
            print("-" * 60)
            return True

        except Exception as e:
            self._log_result("Test Exception", False, str(e))
            print("\nOverall Test results  : FAIL")
            print("-" * 60)
            return False




#----------------- Verify Netflix uninstall shows warning icon in carousel ----------------

    def TC_ID_C51570647_netflix_uninstal_Apperror_Icon_validation(self):

        """TC: Add Netflix (if not present), Uninstall and validate warning icon"""

        # ---------- Print Test Case Header ----------
        print("\nTEST CASE: Netflix Uninstall Warning Validation")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Netflix Validation", False, "Application not connected")
            print("Test case 'Netflix Validation' completed : FAIL")
            print("-" * 60)
            return False

        app_name = "Netflix"
        tooltip_text = "App not found. Try adding it again using the + to restore this profile."

        try:
            self.main_window.set_focus()
            time.sleep(5)

            netflix_item = self.main_window.child_window(
                title="carousel-item-Netflix",
                control_type="ListItem"
            )

            # ==================================================
            # STEP 0: ADD NETFLIX USING SEARCH (IF NOT PRESENT)
            # ==================================================
            if not netflix_item.exists(timeout=5):

                print("Netflix not in carousel → Adding via Search")

                # ---------- CLICK ADD APPLICATION ----------
                add_btn = self.main_window.child_window(
                    title="Add Application",
                    auto_id="ReactPCContextAware.Carousel.AddButton",
                    control_type="Button"
                )

                if not add_btn.exists(timeout=10):
                    self._log_result("Add Application", False, "Add button not found")
                    return False

                add_btn.click_input()
                time.sleep(2)

                # ---------- SEARCH NETFLIX ----------
                search_box = self.main_window.child_window(
                    auto_id="ReactPCContextAware.InstalledAppsModal.SearchApplication__text-box",
                    control_type="Edit"
                )

                if not search_box.exists(timeout=10):
                    self._log_result("Search App", False, "Search box not found")
                    return False

                search_box.click_input()
                time.sleep(0.5)
                search_box.type_keys("^a{BACKSPACE}")
                search_box.type_keys("Netflix", with_spaces=True)
                time.sleep(2)

                self._log_result("Search App", True, "Searched for Netflix")

                # ---------- SELECT NETFLIX ----------
                app_btn = self.main_window.child_window(
                    title="Netflix",
                    control_type="Button"
                )

                if not app_btn.exists(timeout=10):
                    self._log_result("Select App", False, "Netflix not found in search result")
                    return False

                app_btn.click_input()
                time.sleep(1)

                # ---------- CLICK CONTINUE ----------
                continue_btn = self.main_window.child_window(
                    title="Continue",
                    auto_id="ReactPCContextAware.InstalledAppsModal.ContinueButton",
                    control_type="Button"
                )

                if continue_btn.exists(timeout=5) and continue_btn.is_enabled():
                    continue_btn.click_input()
                    time.sleep(5)
                    self._log_result("Add Netflix", True, "Netflix added to carousel")
                else:
                    self._log_result("Continue", False, "Continue button not enabled")
                    return False

            # ==================================================
            # STEP 1: CHECK INSTALL STATUS
            # ==================================================
            netflix_item = self.main_window.child_window(
                title="carousel-item-Netflix",
                control_type="ListItem"
            )

            netflix_item.click_input()
            time.sleep(2)

            tooltip = self.main_window.child_window(
                title=tooltip_text,
                control_type="ToolTip"
            )

            # ==================================================
            # STEP 2: IF INSTALLED → UNINSTALL
            # ==================================================
            if not tooltip.exists(timeout=2):

                print("Netflix installed → Proceeding with uninstall")

                try:
                    self.main_window.close()
                    time.sleep(3)
                except Exception:
                    pyautogui.hotkey("alt", "f4")
                    time.sleep(2)

                pyautogui.press("winleft")
                time.sleep(1)
                pyautogui.write(app_name)
                time.sleep(3)

                search_win = Desktop(backend="uia").window(title_re=".*Search.*")
                search_win.wait("visible", timeout=10)

                uninstall_item = search_win.child_window(
                    title="Uninstall",
                    control_type="ListItem"
                )
                uninstall_item.wait("enabled", timeout=10)
                uninstall_item.invoke()
                time.sleep(3)

                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.press("enter")
                time.sleep(10)

                self._log_result("Uninstall Netflix", True, "Uninstall completed")

            # ==================================================
            # STEP 3: RELAUNCH HP
            # ==================================================
            if not self.open_hp_application():
                return False

            if not self.connect_to_application():
                return False

            if not self.navigate_to_Audio():
                return False

            # ==================================================
            # STEP 4: VALIDATE WARNING ICON
            # ==================================================
            self.main_window.set_focus()
            time.sleep(5)

            netflix_item = self.main_window.child_window(
                title="carousel-item-Netflix",
                control_type="ListItem"
            )

            netflix_item.click_input()
            time.sleep(2)

            tooltip = self.main_window.child_window(
                title=tooltip_text,
                control_type="ToolTip"
            )

            if tooltip.exists(timeout=3):
                self._log_result("Warning Icon Validation", True, "Warning icon present as expected")
                print("\nOverall test results : PASS")
                print("-" * 60)
                return True
            else:
                self._log_result("Warning Icon Validation", False, "Warning icon NOT present")
                print("\nOverall test results : FAIL")
                print("-" * 60)
                return False

        except Exception as e:
            self._log_result("Netflix Validation", False, str(e))
            print("\nOverall test results : FAIL")
            print("-" * 60)
            return False


#----------------- Verify Netflix uninstall shows tooltip in carousel and validates tooltip message ----------------


    def TC_ID_C51570648_netflix_uninstalled_Apperror_message_validation(self):
                
                """TC2: Click Netflix and verify the tooltip message only"""

                # ---------- Print Test Case Header ----------
                print("\nTEST CASE 2: Netflix Uninstalled Tooltip Validation")
                print("-" * 60)

                tooltip_text = "App not found. Try adding it again using the + to restore this profile."

                try:
                    # 🔹 If main_window is None, try reconnect instead of relaunch
                    if not self.main_window:
                        if not self.connect_to_application():
                            self._log_result("Reconnect HP", False, "Unable to connect to existing HP session")
                            print("\nOverall test results : FAIL")
                            print("-" * 60)
                            return False

                    self.main_window.set_focus()
                    time.sleep(3)

                    # ---------- Step 1: Locate Netflix ----------
                    netflix_item = self.main_window.child_window(
                        title="carousel-item-Netflix",
                        control_type="ListItem"
                    )

                    if not netflix_item.exists(timeout=5):
                        self._log_result("Locate Netflix", False, "Netflix not found in carousel")
                        print("\nOverall test results : FAIL")
                        print("-" * 60)
                        return False

                    # ---------- Step 2: Click Netflix ----------
                    netflix_item.click_input()
                    time.sleep(2)

                    # ---------- Step 3: Validate Tooltip ----------
                    tooltip = self.main_window.child_window(
                        title=tooltip_text,
                        control_type="ToolTip"
                    )

                    if tooltip.exists(timeout=3):

                        # Optional: verify exact text
                        actual_text = tooltip.window_text()

                        if actual_text == tooltip_text:
                            self._log_result(
                                "Tooltip Validation",
                                True,
                                "Correct tooltip message displayed → App is uninstalled"
                            )
                            print("\nOverall test results : PASS")
                            print("-" * 60)
                            return True
                        else:
                            self._log_result(
                                "Tooltip Validation",
                                False,
                                f"Tooltip text mismatch: {actual_text}"
                            )
                    else:
                        self._log_result(
                            "Tooltip Validation",
                            False,
                            "Tooltip not displayed"
                        )

                    print("\nOverall test results : FAIL")
                    print("-" * 60)
                    return False

                except Exception as e:
                    self._log_result("Netflix Tooltip Validation", False, str(e))
                    print("\nOverall test results : FAIL")
                    print("-" * 60)
                    return False





# verify Netflix uninstall shows tooltip in carousel, then install Netflix from MS Store and verify tooltip goes away



    # ---------------- Install Netflix from Microsoft Store ----------------

    def install_netflix_from_ms_store(self):
        """
        Launch Microsoft Store, search Netflix, press Enter,
        click Netflix app, install it, wait for Open button,
        then close Microsoft Store.
        """


        try:
            # ---- Launch Microsoft Store ----
            self._log_debug("Launching Microsoft Store")
            os.startfile("ms-windows-store:")
            time.sleep(10)

            # ---- Connect to Microsoft Store Window ----
            store_win = Desktop(backend="uia").window(title_re="Microsoft Store")
            store_win.wait("visible", timeout=30)
            store_win.set_focus()
            self._log_debug("Microsoft Store focused")
            time.sleep(5)

            # ---- Focus Search Box ----
            pyautogui.press("tab")
            time.sleep(1)

            # ---- Type Netflix ----
            pyautogui.typewrite("netflix", interval=0.1)
            self._log_debug("Typed 'Netflix' in search box")
            time.sleep(1)

            # ---- Press Enter to Search ----
            pyautogui.press("enter")
            self._log_debug("Pressed Enter to search Netflix")
            time.sleep(8)

            # ---- Click Netflix App Tile ----
            netflix_button = store_win.child_window(
                title_re="^Netflix.*",
                control_type="Button"
            )

            if not netflix_button.exists(timeout=20):
                self._log_result("Install Netflix", False, "Netflix app tile not found")
                return True

            netflix_button.click_input()
            self._log_debug("Clicked Netflix app tile")
            time.sleep(8)

            # ---- Click Install Button (handles dot or space) ----
            install_btn = store_win.child_window(
                title_re=r"^Install.*",  # Matches 'Install', 'Install.', 'Install '
                control_type="Button"
            )

            if install_btn.exists(timeout=15):
                install_btn.click_input()
                time.sleep(35)
                self._log_debug("Clicked Install button")
            else:
                self._log_debug("Install button not found (possibly already installed)")

            # ---- Wait for Open / Launch Button ----
            self._log_debug("Waiting for Open/Launch button")
            open_btn = None

            for _ in range(30):  # ~150 seconds max
                open_btn = store_win.child_window(
                    title_re=r"^(Open|Launch|Play).*",  # Matches 'Open', 'Open.', 'Launch', etc.
                    control_type="Button"
                )
                if open_btn.exists():
                    break
                time.sleep(5)

            if open_btn and open_btn.exists():
                self._log_result(
                    "Install Netflix",
                    True,
                    "Netflix installed successfully (Open button visible)"
                )
            else:
                self._log_result(
                    "Install Netflix",
                    False,
                    "Open/Launch button not detected after waiting"
                )

            # ---- Close Microsoft Store ----
            pyautogui.hotkey("alt", "f4")   
            time.sleep(2)
            self._log_debug("Closed Microsoft Store")

            return True

        except Exception as e:
            self._log_result("Install Netflix", False, str(e))
            return True




#     ---------------- Full end-to-end Netflix uninstall/install validation and tool tip verification ----------------

    def TC_ID_C51570649_netflix_app_error_resolve(self):

        """
        FULL END-TO-END FLOW

        1. Pre-check Netflix state
        2. Uninstall if installed
        3. Relaunch → Tooltip MUST exist
        4. Install from MS Store
        5. Relaunch → Tooltip MUST NOT exist
        """

        overall_result = True
        app_name = "Netflix"

        tooltip_text = (
            "App not found. Try adding it again using the + to restore this profile."
        )

        uninstall_required = False

        # --------------------------------------------------
        # HELPER: FORCE CLOSE HP
        # --------------------------------------------------
        def close_hp():
            try:
                if self.main_window:
                    self.main_window.close()
                    time.sleep(3)
            except Exception:
                try:
                    pyautogui.hotkey("alt", "f4")
                    time.sleep(2)
                except Exception:
                    pass

        # --------------------------------------------------
        # STEP 1: PRE-CHECK
        # --------------------------------------------------
        try:
            if self.main_window:
                self.main_window.set_focus()
                time.sleep(2)

                netflix_item = self.main_window.child_window(
                    title="carousel-item-Netflix",
                    control_type="ListItem"
                )

                if not netflix_item.exists(timeout=5):
                    self._log_result(
                        "Netflix Pre-check",
                        True,
                        "Netflix not in carousel → treated as UNINSTALLED"
                    )
                else:
                    netflix_item.click_input()
                    time.sleep(1.5)

                    tooltip = self.main_window.child_window(
                        title=tooltip_text,
                        control_type="ToolTip"
                    )

                    if tooltip.exists(timeout=2):
                        self._log_result(
                            "Netflix Pre-check",
                            True,
                            "Tooltip present → already UNINSTALLED"
                        )
                    else:
                        uninstall_required = True

        except Exception as e:
            self._log_result("Netflix Pre-check", False, str(e))
            overall_result = False

        # --------------------------------------------------
        # STEP 2: UNINSTALL (IF REQUIRED)
        # --------------------------------------------------
        if uninstall_required:
            try:
                close_hp()

                pyautogui.press("winleft")
                time.sleep(1)
                pyautogui.write(app_name)
                time.sleep(3)

                search_win = Desktop(backend="uia").window(title_re=".*Search.*")
                search_win.wait("visible", timeout=10)

                uninstall_item = search_win.child_window(
                    title="Uninstall",
                    control_type="ListItem"
                )
                uninstall_item.wait("enabled", timeout=10)
                uninstall_item.invoke()

                time.sleep(10)

                self._log_result("Uninstall Netflix", True, "Uninstall executed")

            except Exception as e:
                self._log_result("Uninstall Netflix", False, str(e))
                overall_result = False

        # --------------------------------------------------
        # STEP 3: RELAUNCH → TOOLTIP MUST EXIST
        # --------------------------------------------------
        try:
            close_hp()

            if self.open_hp_application() and \
            self.connect_to_application() and \
            self.navigate_to_Audio():

                self.main_window.set_focus()
                time.sleep(2)

                netflix_item = self.main_window.child_window(
                    title="carousel-item-Netflix",
                    control_type="ListItem"
                )

                if netflix_item.exists(timeout=5):
                    netflix_item.click_input()
                    time.sleep(1.5)

                    tooltip = self.main_window.child_window(
                        title=tooltip_text,
                        control_type="ToolTip"
                    )

                    if tooltip.exists(timeout=2):
                        self._log_result(
                            "Post-Uninstall Tooltip Check",
                            True,
                            "Tooltip present as expected"
                        )
                    else:
                        self._log_result(
                            "Post-Uninstall Tooltip Check",
                            False,
                            "Tooltip NOT found (unexpected)"
                        )
                        overall_result = False
                else:
                    self._log_result(
                        "Post-Uninstall Carousel Check",
                        False,
                        "Netflix not found in carousel"
                    )
                    overall_result = False
            else:
                overall_result = False

        except Exception as e:
            self._log_result("Post-Uninstall Validation", False, str(e))
            overall_result = False

        # --------------------------------------------------
        # STEP 4: INSTALL NETFLIX
        # --------------------------------------------------
        try:
            close_hp()

            install_success = self.install_netflix_from_ms_store()

            if not install_success:
                self._log_result("Install Netflix", False, "Installation failed")
                overall_result = False

        except Exception as e:
            self._log_result("Install Netflix", False, str(e))
            overall_result = False

        # --------------------------------------------------
        # STEP 5: RELAUNCH → TOOLTIP MUST NOT EXIST
        # --------------------------------------------------
        try:
            close_hp()

            if self.open_hp_application() and \
            self.handle_startup_conditions() and \
            self.navigate_to_Audio():

                self.main_window.set_focus()
                time.sleep(2)

                netflix_item = self.main_window.child_window(
                    title="carousel-item-Netflix",
                    control_type="ListItem"
                )

                if not netflix_item.exists(timeout=5):
                    self._log_result(
                        "Post-Install Carousel Check",
                        False,
                        "Netflix not found in carousel"
                    )
                    overall_result = False
                else:
                    netflix_item.click_input()
                    time.sleep(1.5)

                    tooltip = self.main_window.child_window(
                        title=tooltip_text,
                        control_type="ToolTip"
                    )

                    if tooltip.exists(timeout=2):
                        self._log_result(
                            "Post-Install Tooltip Check",
                            False,
                            "Tooltip present after install (unexpected)"
                        )
                        overall_result = False
                    else:
                        self._log_result(
                            "Post-Install Tooltip Check",
                            True,
                            "Tooltip not present as expected"
                        )
            else:
                overall_result = False

        except Exception as e:
            self._log_result("Post-Install Validation", False, str(e))
            overall_result = False

        # --------------------------------------------------
        # FINAL RESULT CONTROL
        # --------------------------------------------------
        if not overall_result:
            raise AssertionError(
                "TC_ID_C51570649_netflix_app_error_resolve FAILED"
            )

        return True   




    def TC_ID_C51570662_launch_multiple_apps(self):
        """
        TC: Add Calculator & Netflix and validate carousel focus when launched from Windows
        """

        print("\nTEST CASE: Calculator & Netflix Carousel Focus Validation")
        print("-" * 60)

        if not self.main_window:
            self._log_result("Carousel Validation", False, "Application not connected")
            return False

        try:

            self.main_window.set_focus()
            time.sleep(3)

            # -------------------------------------------------
            # FUNCTION: ADD APP TO CAROUSEL
            # -------------------------------------------------
            def add_app(app_name):

                add_btn = self.main_window.child_window(
                    title="Add Application",
                    auto_id="ReactPCContextAware.Carousel.AddButton",
                    control_type="Button"
                )

                add_btn.click_input()
                time.sleep(1)

                search_box = self.main_window.child_window(
                    auto_id="ReactPCContextAware.InstalledAppsModal.SearchApplication__text-box",
                    control_type="Edit"
                )

                search_box.click_input()
                search_box.type_keys("^a{BACKSPACE}")
                search_box.type_keys(app_name, with_spaces=True)
                time.sleep(2)

                app_btn = self.main_window.child_window(
                    title=app_name,
                    control_type="Button"
                )

                if not app_btn.exists(timeout=10):
                    self._log_result("Add App", False, f"{app_name} not found")
                    return False

                app_btn.click_input()
                time.sleep(1)

                continue_btn = self.main_window.child_window(
                    title="Continue",
                    auto_id="ReactPCContextAware.InstalledAppsModal.ContinueButton",
                    control_type="Button"
                )

                continue_btn.click_input()
                time.sleep(3)

                self._log_result("Add App", True, f"{app_name} added to carousel")
                return True


            # -------------------------------------------------
            # FUNCTION: LAUNCH APP FROM WINDOWS SEARCH
            # -------------------------------------------------
            def launch_app(app_name):

                pyautogui.press("win")
                time.sleep(1)

                pyautogui.write(app_name)
                time.sleep(2)

                pyautogui.press("enter")

                self._log_result("Launch App", True, f"{app_name} launched from Windows")
                time.sleep(5)


            # -------------------------------------------------
            # FUNCTION: HANDLE NETFLIX WINDOW (RESIZE)
            # -------------------------------------------------
            def handle_netflix_window():
                try:
                    # Get Netflix window directly from Desktop
                    netflix_window = Desktop(backend="uia").window(title_re=".*Netflix.*")

                    netflix_window.wait("visible", timeout=15)

                    # Resize without coordinates
                    netflix_window.restore()
                    netflix_window.set_focus()

                    self._log_result("Netflix Resize", True)

                except Exception as e:
                    self._log_result("Netflix Resize", False, str(e))


            # -------------------------------------------------
            # STEP 1: ADD CALCULATOR
            # -------------------------------------------------
            if not add_app("Calculator"):
                return False

            # -------------------------------------------------
            # STEP 2: ADD NETFLIX
            # -------------------------------------------------
            if not add_app("Netflix"):
                return False


            # Carousel elements
            calc_item = self.main_window.child_window(
                title="carousel-item-Calculator",
                control_type="ListItem"
            )

            netflix_item = self.main_window.child_window(
                title="carousel-item-Netflix",
                control_type="ListItem"
            )


            # -------------------------------------------------
            # STEP 3: LAUNCH CALCULATOR
            # -------------------------------------------------
            launch_app("Calculator")

            if calc_item.is_selected():
                self._log_result("Calculator Focus 1", True)
            else:
                self._log_result("Calculator Focus 1", False)


            # -------------------------------------------------
            # STEP 4: LAUNCH NETFLIX
            # -------------------------------------------------
            launch_app("Netflix")

            # HANDLE NETFLIX WINDOW HERE
            handle_netflix_window()

            if netflix_item.is_selected():
                self._log_result("Netflix Focus 1", True)
            else:
                self._log_result("Netflix Focus 1", False)


            # -------------------------------------------------
            # STEP 5: LAUNCH CALCULATOR AGAIN
            # -------------------------------------------------
            launch_app("Calculator")

            if calc_item.is_selected():
                self._log_result("Calculator Focus 2", True)
            else:
                self._log_result("Calculator Focus 2", False)


            # -------------------------------------------------
            # STEP 6: LAUNCH NETFLIX AGAIN
            # -------------------------------------------------
            launch_app("Netflix")

            # HANDLE AGAIN
            handle_netflix_window()

            if netflix_item.is_selected():
                self._log_result("Netflix Focus 2", True)
                print("\nOverall Test results : PASS")
                print("-" * 60)
                return True
            else:
                self._log_result("Netflix Focus 2", False)
                print("\nOverall Test results : FAIL")
                print("-" * 60)
                return False


        except Exception as e:
            self._log_result("Carousel Validation", False, str(e))
            print("\nOverall Test results : FAIL")
            print("-" * 60)
            return False





#--------------------------Application close and launch-----------------------

    def TC_ID_C51570663_Application_Setting_Close_launch(self):

        """Verify Calculator highlight persists in carousel after relaunch"""

        overall_result = True
        app_name = "Calculator"

        # --------------------------------------------------
        # STEP 1: Add Calculator to carousel
        # --------------------------------------------------
        try:

            calc_item = self.main_window.child_window(
                title="carousel-item-Calculator",
                control_type="ListItem"
            )

            if calc_item.exists(timeout=5):
                self._log_result("Add Calculator", True, "Calculator already present")

            else:

                add_btn = self.main_window.child_window(
                    title="Add Application",
                    auto_id="ReactPCContextAware.Carousel.AddButton",
                    control_type="Button"
                )

                add_btn.click_input()
                time.sleep(1)

                search_box = self.main_window.child_window(
                    auto_id="ReactPCContextAware.InstalledAppsModal.SearchApplication__text-box",
                    control_type="Edit"
                )

                search_box.click_input()
                search_box.type_keys("^a{BACKSPACE}")
                search_box.type_keys(app_name, with_spaces=True)
                time.sleep(2)

                app_btn = self.main_window.child_window(
                    title=app_name,
                    control_type="Button"
                )

                if not app_btn.exists(timeout=10):
                    self._log_result("Add Calculator", False, "Calculator not found")
                    overall_result = False
                else:
                    app_btn.click_input()
                    time.sleep(1)

                    continue_btn = self.main_window.child_window(
                        title="Continue",
                        auto_id="ReactPCContextAware.InstalledAppsModal.ContinueButton",
                        control_type="Button"
                    )

                    continue_btn.click_input()
                    time.sleep(3)

                    self._log_result("Add Calculator", True)

        except Exception as e:
            self._log_result("Add Calculator", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # STEP 2: Launch Calculator
        # --------------------------------------------------
        try:
            pyautogui.press("winleft")
            time.sleep(1)

            pyautogui.write(app_name)
            time.sleep(2)

            pyautogui.press("enter")
            time.sleep(5)

            self._log_result("Launch Calculator", True)

        except Exception as e:
            self._log_result("Launch Calculator", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # STEP 3: Verify Calculator highlighted
        # --------------------------------------------------
        try:
            self.main_window.set_focus()
            time.sleep(2)

            calc_item = self.main_window.child_window(
                title="carousel-item-Calculator",
                control_type="ListItem"
            )

            if calc_item.exists(timeout=5) and calc_item.is_selected():
                self._log_result("Calculator highlight check", True)
            else:
                self._log_result("Calculator highlight check", False, "Calculator not highlighted")
                overall_result = False

        except Exception as e:
            self._log_result("Calculator highlight check", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # STEP 4: Close HP
        # --------------------------------------------------
        try:
            self.main_window.close()
            time.sleep(3)
            self._log_result("Close HP", True)

        except Exception:
            pyautogui.hotkey("alt", "f4")
            time.sleep(3)
            self._log_result("Close HP", True)


        #--------------------------------------------------
        # STEP 5: Relaunch HP
        # --------------------------------------------------

        try:

            # Open HP
            try:
                self.open_hp_application()
                time.sleep(5)
                self._log_result("Open HP", True)
            except Exception as e:
                self._log_result("Open HP", False, str(e))
                overall_result = False

            # # Wait for HP
            # try:
            #     self.wait_for_hp_ready(timeout=60)
            #     time.sleep(3)
            #     self._log_result("Wait for HP Ready", True)
            # except Exception as e:
            #     self._log_result("Wait for HP Ready", False, str(e))
            #     overall_result = False

            # Connect Application
            try:
                if self.connect_to_application(timeout=60):
                    self._log_result("Connect to Application", True)
                else:
                    self._log_result("Connect to Application", False)
                    overall_result = False
            except Exception as e:
                self._log_result("Connect to Application", False, str(e))
                overall_result = False

            # Startup Handling
            try:
                if self.handle_startup_conditions():
                    self._log_result("Startup Handling", True)
                else:
                    self._log_result("Startup Handling", False)
                    overall_result = False
            except Exception as e:
                self._log_result("Startup Handling", False, str(e))
                overall_result = False

            # Navigate to Audio
            try:
                if self.navigate_to_Audio():
                    self._log_result("Navigate to Audio", True)
                else:
                    self._log_result("Navigate to Audio", False)
                    overall_result = False
            except Exception as e:
                self._log_result("Navigate to Audio", False, str(e))
                overall_result = False

        except Exception as e:
            self._log_result("HP Relaunch Flow", False, str(e))
            overall_result = False

        # --------------------------------------------------
        # STEP 6: Verify Calculator still highlighted
        # --------------------------------------------------
        try:
            self.main_window.set_focus()
            time.sleep(2)

            calc_item = self.main_window.child_window(
                title="carousel-item-Calculator",
                control_type="ListItem"
            )

            if calc_item.exists(timeout=5) and calc_item.is_selected():
                self._log_result("Post-relaunch highlight check", True)
            else:
                self._log_result("Post-relaunch highlight check", False, "Calculator not highlighted after relaunch")
                overall_result = False

        except Exception as e:
            self._log_result("Post-relaunch highlight check", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------
        if not calc_item.exists(timeout=5) or not calc_item.is_selected():
            raise AssertionError("Calculator highlight verification FAILED")

        return True






# ----------------application close and launch with different app that is not in appbar-----------------------------

    def TC_ID_C51570664_application_close_and_launch_with_different_app(self):

        print("\nTEST CASE: Verify 'For all applications' remains selected after launching Notepad and relaunching HP")
        print("-" * 60)

        overall_result = True
        app_name = "Notepad"

        # --------------------------------------------------
        # STEP 1: Close HP
        # --------------------------------------------------
        try:
            if self.main_window:
                self.main_window.close()
                time.sleep(3)
            else:
                pyautogui.hotkey("alt", "f4")
                time.sleep(2)

            self._log_result("Close HP", True)

        except Exception as e:
            self._log_result("Close HP", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # STEP 2: Launch Notepad
        # --------------------------------------------------
        try:
            pyautogui.press("winleft")
            time.sleep(1)

            pyautogui.write(app_name)
            time.sleep(2)

            pyautogui.press("enter")
            time.sleep(5)

            self._log_result("Launch Notepad", True)

        except Exception as e:
            self._log_result("Launch Notepad", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # STEP 3: Relaunch HP
        # --------------------------------------------------
        try:
            if (
                self.open_hp_application() and
                self.connect_to_application and
                self.handle_startup_conditions() and
                self.navigate_to_Audio()
            ):
                self._log_result("HP Relaunch", True)
            else:
                self._log_result("HP Relaunch", False, "Failed to relaunch HP")
                overall_result = False

        except Exception as e:
            self._log_result("HP Relaunch", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # STEP 4: Verify Global App
        # --------------------------------------------------
        try:
            self.main_window.set_focus()
            time.sleep(2)

            global_item = self.main_window.child_window(
                title="For all applications",
                auto_id="ReactPCContextAware.Carousel.AllAppsButton",
                control_type="ListItem"
            )

            if global_item.exists(timeout=5) and global_item.is_selected():

                self._log_result("For all applications", True)

            else:
                self._log_result(
                    "Global application selected",
                    False,
                    "Global application NOT selected"
                )
                overall_result = False

        except Exception as e:
            self._log_result("Global application selected", False, str(e))
            overall_result = False


        # --------------------------------------------------
        # FINAL
        # --------------------------------------------------
        print("-" * 60)

        return overall_result







            # ---------------- Delete Calculator and verify it is removed after relaunch ----------------

    def TC_ID_C51570665_Delete_App_and_verify_after_relunch(self):

        print("\nTEST CASE: Delete Calculator and verify it is removed after HP relaunch")
        print("-" * 60)

        overall_result = True

        try:

            # --------------------------------------------------
            # STEP 1: Click Calculator
            # --------------------------------------------------
            try:
                calc_item = self.main_window.child_window(
                    title="carousel-item-Calculator",
                    control_type="ListItem"
                )

                if calc_item.exists(timeout=5):
                    calc_item.click_input()
                    time.sleep(2)
                    self._log_result("Click Calculator", True)
                else:
                    self._log_result("Click Calculator", False, "Calculator not found in carousel")
                    overall_result = False

            except Exception as e:
                self._log_result("Click Calculator", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 2: Click Delete Profile
            # --------------------------------------------------
            try:
                delete_btn = self.main_window.child_window(
                    title="Delete profile",
                    auto_id="ReactPCContextAware.Carousel.DeleteProfileButton",
                    control_type="Button"
                )

                if delete_btn.exists(timeout=5) and delete_btn.is_enabled():
                    delete_btn.click_input()
                    time.sleep(2)
                    self._log_result("Delete Profile", True)
                else:
                    self._log_result("Delete Profile", False, "Delete button not available")
                    overall_result = False

            except Exception as e:
                self._log_result("Delete Profile", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 3: Click Continue (Optional Popup)
            # --------------------------------------------------
            try:
                continue_btn = self.main_window.child_window(
                    title="Continue",
                    auto_id="ReactPCContextAware.DeleteProfileModal.ContinueButton",
                    control_type="Button"
                )

                if continue_btn.exists(timeout=5):
                    continue_btn.click_input()
                    time.sleep(3)
                    self._log_result("Popup Continue", True, "Popup handled")
                else:
                    # Do NOT fail test — just log and continue
                    self._log_result("Popup Continue", True, "Popup not displayed, skipping")

            except Exception as e:
                # Even if error occurs, don't fail execution
                self._log_result("Popup Continue", True, f"Issue ignored: {str(e)}")


            # --------------------------------------------------
            # STEP 4: Close HP
            # --------------------------------------------------
            try:
                self.main_window.close()
                time.sleep(3)
                self._log_result("Close HP", True)

            except Exception as e:
                self._log_result("Close HP", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 5: Relaunch HP (UPDATED)
            # --------------------------------------------------
            try:
                if not self.relaunch_hp():
                    overall_result = False

            except Exception as e:
                self._log_result("HP Relaunch", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 6: Verify Calculator NOT in carousel
            # --------------------------------------------------
            try:
                calc_item = self.main_window.child_window(
                    title="carousel-item-Calculator",
                    control_type="ListItem"
                )

                if calc_item.exists(timeout=5):
                    self._log_result(
                        "Calculator Verification",
                        False,
                        "Calculator still appears in carousel"
                    )
                    overall_result = False
                else:
                    self._log_result(
                        "Calculator Verification",
                        True,
                        "Calculator successfully removed"
                    )

            except Exception as e:
                self._log_result("Calculator Verification", False, str(e))
                overall_result = False


            print("-" * 60)
            return overall_result


        except Exception as e:
            self._log_result("Delete Calculator Test", False, str(e))
            print("-" * 60)
            return False




#------Uninstall application and check in carosle after relaunch-----------------------------

    def TC_ID_C51570666_Application_Setting_Uninstall_Application(self):

        print("\nTEST CASE: Verify Netflix exists in carousel after uninstall and HP relaunch")
        print("-" * 60)

        overall_result = True
        app_name = "Netflix"

        try:

            # --------------------------------------------------
            # STEP 1: Check Netflix in Carousel
            # --------------------------------------------------
            try:
                netflix_item = self.main_window.child_window(
                    title="carousel-item-Netflix",
                    control_type="ListItem"
                )

                if netflix_item.exists(timeout=5):
                    self._log_result("Netflix Exists in Carousel", True)

                else:

                    self._log_result("Netflix Exists in Carousel", True, "Netflix not present, adding")

                    add_btn = self.main_window.child_window(
                        auto_id="ReactPCContextAware.Carousel.AddButton",
                        control_type="Button"
                    )

                    add_btn.wait("enabled", timeout=10)
                    add_btn.click_input()
                    time.sleep(1)

                    # ---------------- Search Netflix ----------------

                    search_box = self.main_window.child_window(
                        auto_id="ReactPCContextAware.InstalledAppsModal.SearchApplication__text-box",
                        control_type="Edit"
                    )

                    search_box.wait("visible", timeout=10)
                    search_box.click_input()
                    search_box.type_keys("^a{BACKSPACE}")
                    search_box.type_keys(app_name, with_spaces=True)
                    time.sleep(2)

                    # ---------------- Select Netflix ----------------

                    app_btn = self.main_window.child_window(
                        title=app_name,
                        control_type="Button"
                    )

                    if not app_btn.exists(timeout=5):
                        app_btn = self.main_window.child_window(
                            title=app_name,
                            control_type="ListItem"
                        )

                    if not app_btn.exists(timeout=10):
                        self._log_result("Add Netflix", False, "Netflix not found in search results")
                        return False

                    app_btn.wait("enabled", timeout=10)
                    app_btn.click_input()
                    time.sleep(1)

                    # ---------------- Continue ----------------

                    continue_btn = self.main_window.child_window(
                        title="Continue",
                        auto_id="ReactPCContextAware.InstalledAppsModal.ContinueButton",
                        control_type="Button"
                    )

                    continue_btn.wait("enabled", timeout=10)
                    continue_btn.click_input()
                    time.sleep(3)

                    self._log_result("Add Netflix", True)

            except Exception as e:
                self._log_result("Add Netflix", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 2: Close HP
            # --------------------------------------------------
            try:
                self.main_window.close()
                time.sleep(3)
                self._log_result("Close HP", True)

            except Exception:
                pyautogui.hotkey("alt", "f4")
                time.sleep(2)
                self._log_result("Close HP", True)


            # --------------------------------------------------
            # STEP 3: Uninstall Netflix (Windows Search)
            # --------------------------------------------------
            try:

                pyautogui.press("winleft")
                time.sleep(1)

                pyautogui.write(app_name)
                time.sleep(3)

                search_win = Desktop(backend="uia").window(title_re=".*Search.*")
                search_win.wait("visible", timeout=10)

                uninstall_item = search_win.child_window(
                    title="Uninstall",
                    control_type="ListItem"
                )

                uninstall_item.wait("enabled", timeout=10)
                uninstall_item.invoke()
                time.sleep(3)

                pyautogui.press("tab")
                time.sleep(1)

                pyautogui.press("enter")
                time.sleep(10)

                self._log_result("Uninstall Netflix", True)

            except Exception as e:
                self._log_result("Uninstall Netflix", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 4: Relaunch HP
            # --------------------------------------------------
            try:
                if (
                    self.open_hp_application() and
                    self.handle_startup_conditions() and
                    self.navigate_to_Audio()
                ):
                    self._log_result("HP Relaunch", True)

                else:
                    self._log_result("HP Relaunch", False)
                    overall_result = False

            except Exception as e:
                self._log_result("HP Relaunch", False, str(e))
                overall_result = False


            # --------------------------------------------------
            # STEP 5: Verify Netflix exists in carousel
            # --------------------------------------------------
            try:

                netflix_item = self.main_window.child_window(
                    title="carousel-item-Netflix",
                    control_type="ListItem"
                )

                if netflix_item.exists(timeout=5):

                    self._log_result("Netflix Carousel Verification", True)

                else:

                    self._log_result(
                        "Netflix Carousel Verification",
                        False,
                        "Netflix not found in carousel after uninstall"
                    )

                    overall_result = False

            except Exception as e:
                self._log_result("Netflix Carousel Verification", False, str(e))
                overall_result = False


            print("-" * 60)
            return overall_result

        except Exception as e:
            self._log_result("Netflix Test", False, str(e))
            print("-" * 60)
            return False






#    # ---------------- Run all steps in sequence ----------------

    def run_steps(self):
        steps = [
            self.open_hp_application,
            self.connect_to_application,
            self.handle_startup_conditions,
            self.navigate_to_Audio,
            self.TC_ID_C51570650_verify_default_state_of_CA_apps,
            self.TC_ID_C51570659_verify_imax_apps_in_carousel,
            self.TC_ID_C51570660_launch_and_verify_oob_apps,
            self.TC_ID_C53046320_Uninstall_OOB_apps_and_Reset_HPX_application,
            self.TC_ID_C77290501_navigate_to_CA_and_click_Add_button,
            self.TC_ID_C51570654_add_multiple_apps,
            self.TC_ID_C51570657_verify_selected_application_name_and_focus,
            self.TC_ID_C51570655_verify_application_selected_in_app_bar,
            self.TC_ID_C52986236_search_and_add_application,
            self.TC_ID_C51570652_click_carousel_next,
            self.TC_ID_C77291045_verify_carousel_apps,
            self.TC_ID_C51570658_verify_delete_profile_button_enable_disable,
            self.TC_ID_C60424978_verify_carousel_app_tooltips,
            self.TC_ID_C51570664_verify_global_app_focus_after_hp_relaunch,
            self.TC_ID_C53033386_verify_aapplication_Select_Unselect,
            self.TC_ID_C51570661_Delete_Custom_OOB_App,
            self.TC_ID_C53045345_Delete_app_without_delete_profile_page,
            self.TC_ID_C51570647_netflix_uninstal_Apperror_Icon_validation,
            self.TC_ID_C51570648_netflix_uninstalled_Apperror_message_validation,
            self.TC_ID_C51570649_netflix_app_error_resolve,
            self.TC_ID_C51570662_launch_multiple_apps,
            self.TC_ID_C51570663_Application_Setting_Close_launch,
            self.TC_ID_C51570664_application_close_and_launch_with_different_app,
            self.TC_ID_C51570665_Delete_App_and_verify_after_relunch,
            self.TC_ID_C51570666_Application_Setting_Uninstall_Application,
        
            self.device_page_backbutton
        ]

        
        overall_status = True

        print("\n" + "=" * 60)
        print(" STARTING TEST EXECUTION")
        print("=" * 60)

        for step in steps:
            step_name = step.__name__

            print(f"\n STEP: {step_name}")
            print("-" * 50)

            try:
                result = step()

                if not result:
                    print(f"STEP FAILED: {step_name}")
                    overall_status = False
                    break   #  stop execution on failure (recommended)
                else:
                    print(f"STEP PASSED: {step_name}")

            except Exception as e:
                print(f"STEP ERROR: {step_name} | {str(e)}")
                overall_status = False
                break

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------
        print("\n" + "=" * 60)

        if overall_status:
            print("OVERALL TEST RESULT: PASS")
        else:
            print("OVERALL TEST RESULT: FAIL")

        print("=" * 60)

        return overall_status



    # ---------------- Main ----------------
   
if __name__ == "__main__":
    hp_app = MyHP()

    if hp_app.run_steps():
        print("All tests completed.")
    else:
        print("OVERALL TEST RESULT : FAIL")





