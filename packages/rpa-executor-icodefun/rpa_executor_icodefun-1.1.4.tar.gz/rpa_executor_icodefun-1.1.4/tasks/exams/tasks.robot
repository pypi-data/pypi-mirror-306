*** Settings ***
Documentation       Fetch students exams scores.

Library    RPA.Excel.Files
Library    String
Library    Collections
Library    RPA.FileSystem
Library    Dialogs

Resource    resources/anth.robot
Resource    resources/fetch.robot
Resource    resources/record.robot

Suite Setup    Setup
# Task Setup    New Context    viewport={'width': 1920, 'height': 1080}
# Task Teardown    Close Context
Suite Teardown    Teardown


*** Tasks ***

Fetch Students Scores

    ${start_code}=    Get Last Interupted code
    Log    ${start_code}
    IF    ${start_code} == $None
        ${start_code}=    Set Variable    ${STDT_CODE_BEGIN}
    END
        
    FOR    ${std_code}    IN RANGE    ${start_code}    ${STDT_CODE_END}+1    ${1}
        Set Last Interupted code    ${std_code}
        Process One    ${std_code}
        Save Workbook
    END

    Clear Last Interupted code
    Save Workbook


Fetch One Student Scores
    ${std_code_str}=    Get Value From User    Please input the code    
    ${std_code}=    Convert To Integer    ${std_code_str}
    Process One    ${std_code}
    Save Workbook


Fetch The Scores 
    ${std_code}=    Convert To Integer    ${STUDENT_CODE}
    Process One    ${std_code}
    Save Workbook
*** Keywords ***


Setup
    New Browser    browser=${BROWSER}    headless=${HEADLESS}
    Set Browser Timeout    60000

    ${need_new_file}=    Does File Not Exist    ${RESULT_FILE}
    IF    ${need_new_file}
        Create Workbook    ${RESULT_FILE}
        Save Workbook
    ELSE
        Open Workbook    ${RESULT_FILE}
    END
     

Teardown
    # Disconnect From Database
    Close Browser
    Save Workbook
    Close Workbook
        
Process One
    [Arguments]    ${std_code}
    
    ${suc}=    Login    ${std_code}
    IF    ${suc}
        ${student_info}=    Fetch Student Info
        IF    ${student_info} != $None
            ${exams}=    Fetch exams    ${FETCH_COUNT}
            IF    ${exams} != $None
                Record Scores    ${student_info}    ${exams}
                Log To Console    ${student_info}[code] is fetched!  
            END
            
        END
        
    END
    Logout


