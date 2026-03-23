*** Settings ***
Library    ../Libraries/Keyword.py
Library    Collections

*** Test Cases ***
1.Open HP Application       
    [Documentation]    Open the HP application
    ${result}=   Open Hp Application
    Should Be True    ${result}    Failed to open HP application

2.connect to Application
    [Documentation]    Connect application
    ${result}=    Connect To Application
    Should Be True    ${result}    Failed to connect 


2.Handle startup condition
    [Documentation]    Connect to the HP application
    ${result}=    Handle Startup Conditions
    Should Be True    ${result}    Failed to connect to HP application


3.Navigate To Audio Section
    [Documentation]    Navigate to Audio section
    ${result}=    Navigate To Audio
    Should Be True    ${result}    Failed to navigate to Audio



4.TC_ID_C51570650_verify_default_state_of_CA_apps
    [Documentation]    Verify the default state of CA apps in the carousel
    ${result}=    TC_ID_C51570650_verify_default_state_of_CA_apps
    Should Be True    ${result}    Default state of CA apps in the carousel is not as expected



5.TC_ID_C51570659_verify_imax_apps_in_carousel
    [Documentation]    Verify IMAX apps are displayed in the carousel
    ${result}=    TC_ID_C51570659_verify_imax_apps_in_carousel
    Should Be True    ${result}    IMAX apps are not displayed in the carousel



6.TC_ID_C51570660_launch_and_verify_oob_apps
    [Documentation]    Launch and verify OOB apps from the carousel
    ${result}=    TC_ID_C51570660_launch_and_verify_oob_apps
    Should Be True    ${result}    Failed to launch and verify OOB apps from the carousel




7.TC_ID_C53046320_Uninstall_OOB_apps_and_Reset_HPX_application
    [Documentation]    Uninstall OOB apps and reset the HPX application
    ${result}=    TC_ID_C53046320_Uninstall_OOB_apps_and_Reset_HPX_application
    Should Be True    ${result}    Failed to uninstall OOB apps and reset the HPX application




8.TC_ID_C77290501_navigate_to_CA_and_click_Add_button
    [Documentation]    Navigate to CA section and click the Add button
    ${result}=    TC_ID_C77290501_navigate_to_CA_and_click_Add_button
    Should Be True    ${result}    Failed to navigate to CA section and click the Add button



9.TC_ID_C51570654_add_multiple_apps
    [Documentation]    Add multiple apps to the carousel
    ${result}=    TC_ID_C51570654_add_multiple_apps
    Should Be True    ${result}    Failed to add multiple apps to the carousel



10.TC_ID_C51570657_verify_selected_application_name_and_focus
    [Documentation]    Verify the selected application name and focus in the carousel
    ${result}=    TC_ID_C51570657_verify_selected_application_name_and_focus
    Should Be True    ${result}    Selected application name and focus in the carousel are not as expected



11.TC_ID_C51570655_verify_application_selected_in_app_bar
    [Documentation]    Verify the selected application is displayed in the app bar
    ${result}=    TC_ID_C51570655_verify_application_selected_in_app_bar
    Should Be True    ${result}    Selected application is not displayed in the app bar




12.TC_ID_C52986236_search_and_add_application
    [Documentation]    Search and add an application to the carousel
    ${result}=    TC_ID_C52986236_search_and_add_application
    Should Be True    ${result}    Failed to search and add an application to the carousel



13.TC_ID_C51570652_click_carousel_next
    [Documentation]    Click the carousel next button and verify the carousel scrolls
    ${result}=    TC_ID_C51570652_click_carousel_next
    Should Be True    ${result}    Failed to click the carousel next button and verify the carousel scrolls



14.TC_ID_C77291045_verify_carousel_apps
    [Documentation]    Verify the apps displayed in the carousel
    ${result}=    TC_ID_C77291045_verify_carousel_apps
    Should Be True    ${result}    Apps displayed in the carousel are not as expected




15.TC_ID_C51570658_verify_delete_profile_button_enable_disable
    [Documentation]    Verify the delete profile button is enabled/disabled
    ${result}=    TC_ID_C51570658_verify_delete_profile_button_enable_disable
    Should Be True    ${result}    Delete profile button enable/disable state is not as expected



16.TC_ID_C60424978_verify_carousel_app_tooltips
    [Documentation]    Verify the tooltips of apps in the carousel
    ${result}=    TC_ID_C60424978_verify_carousel_app_tooltips
    Should Be True    ${result}    Tooltips of apps in the carousel are not as expected




17.TC_ID_C51570664_verify_global_app_focus_after_hp_relaunch
    [Documentation]    Verify global app focus is retained after HP application relaunch
    ${result}=    TC_ID_C51570664_verify_global_app_focus_after_hp_relaunch
    Should Be True    ${result}    Global app focus is not retained after HP application relaunch




18.TC_ID_C53033386_verify_aapplication_Select_Unselect
    [Documentation]    Verify selecting and unselecting an application enables/disables the Continue button
    ${result}=    TC_ID_C53033386_verify_aapplication_Select_Unselect
    Should Be True    ${result}    Selecting and unselecting an application does not enable/disable the Continue button as expected

    


19.TC_ID_C51570661_Delete_Custom_OOB_App
    [Documentation]    Delete a custom  app and verify it is deleted successfully
    ${result}=    TC_ID_C51570661_Delete_Custom_OOB_App
    Should Be True    ${result}    Failed to delete a custom OOB App 
    



20.TC_ID_C53045345_Delete_app_without_delete_profile_page
    [Documentation]    Delete an app without going through the delete profile page and verify it is deleted successfully
    ${result}=    TC_ID_C53045345_Delete_app_without_delete_profile_page
    Should Be True    ${result}    Failed to delete an app without going through the delete profile page and verify it is deleted successfully




21.Tc_Id_C51570647_netflix_uninstal_Apperror_Icon_validation():
    [Documentation]    Uninstall Netflix and verify the app error icon is displayed in the carousel
    ${result}=    TC_ID_C51570647_netflix_uninstal_Apperror_Icon_validation
    Should Be True    ${result}    Failed to uninstall Netflix and verify the app error icon is displayed in the carousel



22.TC_ID_C51570648_netflix_uninstalled_Apperror_message_validation
    [Documentation]    Click the Netflix app error icon and verify the tooltip message is displayed correctly
    ${result}=    TC_ID_C51570648_netflix_uninstalled_Apperror_message_validation
    Should Be True    ${result}    Failed to click the Netflix app error icon and verify the tooltip message is displayed correctly



23.TC_ID_C51570649_netflix_app_error_resolve
    [Documentation]    Resolve the Netflix app error and verify Netflix is reinstalled successfully
    ${result}=    TC_ID_C51570649_netflix_app_error_resolve
    Should Be True    ${result}    Failed to resolve the Netflix app error and verify Netflix is reinstalled successfully



24.TC_ID_C51570662_launch_multiple_apps
    [Documentation]    Launch multiple apps and verify they launch successfully
    ${result}=    TC_ID_C51570662_launch_multiple_apps
    Should Be True    ${result}    Failed to launch multiple apps and verify they launch successfully




25.TC_ID_C51570663_Application_Setting_Close_launch
    [Documentation]    Verify application settings and close launch
    ${result}=    TC_ID_C51570663_Application_Setting_Close_launch
    Should Be True    ${result}    Failed to verify application settings and close launch




26.TC_ID_C51570664_application_close_and_launch_with_different_app
    [Documentation]    Close an application and launch a different one, verifying the behavior
    ${result}=    TC_ID_C51570664_application_close_and_launch_with_different_app
    Should Be True    ${result}    Failed to close an application and launch a different one, verifying the behavior



27.TC_ID_C51570665_Delete_App_and_verify_after_relunch
    [Documentation]    Delete an app and verify it is removed after relaunching the HP application
    ${result}=    TC_ID_C51570665_Delete_App_and_verify_after_relunch
    Should Be True    ${result}    Failed to delete an app and verify it is removed after relaunching the HP application        



28.TC_ID_C51570666_Application_Setting_Uninstall_Application
    [Documentation]    Uninstall an application from the application settings and verify it is uninstalled
    ${result}=    TC_ID_C51570666_Application_Setting_Uninstall_Application
    Should Be True    ${result}    Failed to uninstall an application from the application settings and verify it is uninstalled



29.Device Page Back Button
    [Documentation]    Click the back button on the device page and verify navigation
    ${result}=    Device Page Back Button
    Should Be True    ${result}    Failed to click the back button on the device page and verify navigation




    

