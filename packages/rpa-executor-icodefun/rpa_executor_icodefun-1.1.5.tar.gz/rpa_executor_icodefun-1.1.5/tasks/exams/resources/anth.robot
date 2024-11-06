*** Settings ***
Library    RPA.Browser.Playwright
Library    Collections

Resource    var.robot

*** Keywords ***

Login
    [Arguments]    ${std_code}

    New Context
    New Page    ${HOST}/student/index/login
    Fill Text   //*[@id="id_userlogin_dlg"]/input[1]    ${std_code}
    ${std_password}=    Get Password    ${std_code}
    Fill Text   //*[@id="id_userlogin_dlg"]/input[2]  ${std_password}
    
    ${pro}=    Promise To    Wait For Response    response => response.url().endsWith("/student/index/login") && response.status() === 200
    Click       xpath=/html/body/div/div[3]/button
    ${response}=    Wait For    ${pro}
    IF    ${response}[body] == $None
        Sleep   1s
        ${mobilecheck}=    Get Element Count   css=#main >>> css=#checkmobilesubmit
        IF    ${mobilecheck} == ${0}
            RETURN  ${True}
        END
    END
    RETURN  ${False}
    

Logout
    Close Page
    Close Context


Get Password
    [Arguments]    ${code}
    ${pswd}=    Get From Dictionary    ${PSW}    ${code}    default=${code}
    RETURN    ${pswd}