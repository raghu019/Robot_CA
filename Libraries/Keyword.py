# myhp_robot.py
from PS import MyHP       # Main HP app functions
from robot.api import logger

# Instantiate general HP app object
hp_app = MyHP()  

# ---------------- Robot Framework Keywords ----------------

def open_hp_application():
    """Open the HP application."""
    result = hp_app.open_hp_application()
    logger.info(f"Open HP Application result: {result}")
    return result


def connect_to_application():
    """Open the HP application."""
    result = hp_app.connect_to_application()
    logger.info(f"Connect to HP Application result: {result}")
    return result


def handle_startup_conditions():
    """Handle all startup screens in order"""
    result = hp_app.handle_startup_conditions()
    logger.info(f"Handle all startup screen in order: {result}")
    return result


def navigate_to_audio():
    """Navigate to Audio section."""
    result = hp_app.navigate_to_Audio()
    logger.info(f"Navigate to Audio result: {result}")
    return result



def TC_ID_C51570650_verify_default_state_of_CA_apps():
    """Verify default state of Context Aware applications."""
    result = hp_app.TC_ID_C51570650_verify_default_state_of_CA_apps()
    logger.info(f"Verify default state of CA apps result: {result}")
    return result



def TC_ID_C51570659_verify_imax_apps_in_carousel():
    """Verify IMAX apps in carousel."""
    result = hp_app.TC_ID_C51570659_verify_imax_apps_in_carousel()
    logger.info(f"Verify IMAX apps in carousel result: {result}")
    return result



def TC_ID_C51570660_launch_and_verify_oob_apps():
    """Launch and verify OOB apps."""
    result = hp_app.TC_ID_C51570660_launch_and_verify_oob_apps()
    logger.info(f"Launch and verify OOB apps result: {result}")
    return result




def TC_ID_C53046320_Uninstall_OOB_apps_and_Reset_HPX_application():
    """Uninstall OOB apps and reset the HPX application."""
    result = hp_app.TC_ID_C53046320_Uninstall_OOB_apps_and_Reset_HPX_application()
    logger.info(f"Uninstall OOB apps and reset HPX application result: {result}")
    return result




def TC_ID_C77290501_navigate_to_CA_and_click_Add_button():
    """Navigate to Context Aware section and click Add button."""
    result = hp_app.TC_ID_C77290501_navigate_to_CA_and_click_Add_button()
    logger.info(f"Navigate to CA and click Add button result: {result}")
    return result



def TC_ID_C51570654_add_multiple_apps():
    """Add multiple apps and verify they are added successfully."""
    result = hp_app.TC_ID_C51570654_add_multiple_apps()
    logger.info(f"Add multiple apps result: {result}")
    return result



def TC_ID_C51570657_verify_selected_application_name_and_focus():
    """Verify selected application name and focus."""
    result = hp_app.TC_ID_C51570657_verify_selected_application_name_and_focus()
    logger.info(f"Verify selected application name and focus result: {result}")
    return result



def TC_ID_C51570655_verify_application_selected_in_app_bar():
    """Verify application is selected in app bar."""
    result = hp_app.TC_ID_C51570655_verify_application_selected_in_app_bar()
    logger.info(f"Verify application selected in app bar result: {result}")
    return result



def TC_ID_C52986236_search_and_add_application():
    """Search for an application and add it."""
    result = hp_app.TC_ID_C52986236_search_and_add_application()
    logger.info(f"Search and add application result: {result}")
    return result



def TC_ID_C51570652_click_carousel_next():
    """Click the next button in the carousel."""
    result = hp_app.TC_ID_C51570652_click_carousel_next()
    logger.info(f"Click carousel next result: {result}")
    return result



def TC_ID_C77291045_verify_carousel_apps():
    """Verify the apps displayed in the carousel."""
    result = hp_app.TC_ID_C77291045_verify_carousel_apps()
    logger.info(f"Verify carousel apps result: {result}")
    return result



def TC_ID_C51570658_verify_delete_profile_button_enable_disable():
    """Verify the enable/disable state of the delete profile button."""
    result = hp_app.TC_ID_C51570658_verify_delete_profile_button_enable_disable()
    logger.info(f"Verify delete profile button enable/disable result: {result}")
    return result   



def TC_ID_C60424978_verify_carousel_app_tooltips():
    """Verify the tooltips of the apps in the carousel."""
    result = hp_app.TC_ID_C60424978_verify_carousel_app_tooltips()
    logger.info(f"Verify carousel app tooltips result: {result}")
    return result



def TC_ID_C51570664_verify_global_app_focus_after_hp_relaunch():
    """Verify global app focus after HP application relaunch."""
    result = hp_app.TC_ID_C51570664_verify_global_app_focus_after_hp_relaunch()
    logger.info(f"Verify global app focus after HP relaunch result: {result}")
    return result



def TC_ID_C53033386_verify_aapplication_Select_Unselect():
    """Verify that selecting and unselecting an application enables and disables the Continue button."""
    result = hp_app.TC_ID_C53033386_verify_aapplication_Select_Unselect()
    logger.info(f"Verify application select/unselect result: {result}")
    return result



def TC_ID_C51570661_Delete_Custom_OOB_App():
    """Delete a custom OOB app and verify it is deleted successfully."""
    result = hp_app.TC_ID_C51570661_Delete_Custom_OOB_App()
    logger.info(f"Delete custom OOB app result: {result}")
    return result


def TC_ID_C53045345_Delete_app_without_delete_profile_page():
    """Delete an app without going through the delete profile page."""
    result = hp_app.TC_ID_C53045345_Delete_app_without_delete_profile_page()
    logger.info(f"Delete app without delete profile page result: {result}")
    return result



def Tc_Id_C51570647_netflix_uninstal_Apperror_Icon_validation():
    """Verify that the Netflix app shows an error icon after uninstallation."""
    result = hp_app.TC_ID_C51570647_netflix_uninstal_Apperror_Icon_validation()
    logger.info(f"Netflix uninstall app error icon validation result: {result}")
    return result




def TC_ID_C51570648_netflix_uninstalled_Apperror_message_validation():
    """Verify that the correct error message is displayed when clicking the uninstalled Netflix app."""
    result = hp_app.TC_ID_C51570648_netflix_uninstalled_Apperror_message_validation()
    logger.info(f"Netflix uninstall app error message validation result: {result}")
    return result



def TC_ID_C51570649_netflix_app_error_resolve():
    """Perform end-to-end validation of Netflix uninstall and reinstall, including error resolution."""
    result = hp_app.TC_ID_C51570649_netflix_app_error_resolve()
    logger.info(f"Netflix app error resolve result: {result}")
    return result


def TC_ID_C51570662_launch_multiple_apps():
    """Launch multiple apps and verify they launch successfully."""
    result = hp_app.TC_ID_C51570662_launch_multiple_apps()
    logger.info(f"Launch multiple apps result: {result}")
    return result



def TC_ID_C51570663_Application_Setting_Close_launch():
    """Verify application settings and close launch."""
    result = hp_app.TC_ID_C51570663_Application_Setting_Close_launch()
    logger.info(f"Application setting close launch result: {result}")
    return result



def TC_ID_C51570664_application_close_and_launch_with_different_app():
    """Close an application and launch a different one, verifying the behavior."""
    result = hp_app.TC_ID_C51570664_application_close_and_launch_with_different_app()
    logger.info(f"Application close and launch with different app result: {result}")
    return result


def TC_ID_C51570665_Delete_App_and_verify_after_relunch():
    """Delete an app and verify it is removed after relaunching the HP application."""
    result = hp_app.TC_ID_C51570665_Delete_App_and_verify_after_relunch()
    logger.info(f"Delete app and verify after relaunch result: {result}")
    return result 



def TC_ID_C51570666_Application_Setting_Uninstall_Application():
    """Uninstall an application from the application settings and verify it is uninstalled."""
    result = hp_app.TC_ID_C51570666_Application_Setting_Uninstall_Application()
    logger.info(f"Application setting uninstall application result: {result}")
    return result



def device_page_backbutton():
    """Click the back button on the device page."""
    result = hp_app.device_page_backbutton()
    logger.info(f"Device page back button result: {result}")
    return result


