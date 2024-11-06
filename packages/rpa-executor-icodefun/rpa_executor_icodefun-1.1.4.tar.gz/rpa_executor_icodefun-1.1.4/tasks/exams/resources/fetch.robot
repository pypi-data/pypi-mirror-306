*** Settings ***
Library    RPA.Browser.Playwright
Library    Collections
Library    RPA.RobotLogListener

Resource    var.robot

*** Keywords ***

Check If Mobile Check Active
    ${c}=    Get Element Count    selector   #checkmobilesubmit
    IF    ${c} == 0
        RETURN    ${False}
    ELSE
        RETURN    ${True}
    END

Validate Result
    [Arguments]    ${result} 
    IF    ${result} == $None
        RETURN    ${False}
    ELSE
        RETURN    ${True}
    END


Fetch Student Info
    
    Go To    ${HOST}/student/profile/index
    # ${c}=    Check If Mobile Check Active
    # IF    ${c}
    #     RETURN    ${None}
    # END
    
    Wait For Elements State    xpath=/html/body/p[3]

    &{student_info}=    Create Dictionary
    ${student_info}[name]=    Get Text   xpath=/html/body/table/tbody/tr[1]/td
    ${student_info}[school]=    Get Text   xpath=/html/body/table/tbody/tr[2]/td
    ${student_info}[grade]=    Get Text   xpath=/html/body/table/tbody/tr[3]/td
    ${student_info}[class]=    Get Text   xpath=/html/body/table/tbody/tr[4]/td     # TODO
    ${student_info}[code]=    Get Text   xpath=/html/body/table/tbody/tr[5]/td
    RETURN      ${student_info}

Fetch Exams
    [Arguments]     ${topN}
    
    Go To    ${HOST}/student/exam/studentexamlist
    # ${c}=    Check If Mobile Check Active
    # IF    ${c}
    #     RETURN    ${None}
    # END

    Wait For Elements State    xpath=/html/body/p[2]


    ${total_exams_count}=     Get Element Count    css=body > ul > li > a
    @{urls}=    Create List

    FOR    ${current_index}    IN RANGE    ${1}    ${total_exams_count}+1    ${1}
        IF    ${current_index} <= ${topN}
            ${url}=    Get Property    xpath=/html/body/ul/li[${current_index}]/a    href
            Append To List    ${urls}    ${url}
        END
    END

    ${exams}=    Create List
    FOR    ${e}    IN    @{urls}
        &{exam}=    Fatch Exam    ${e}
        ${v}=    Validate Result    ${exam}
        IF    &{exam} != ${None}
            Append To List    ${exams}    ${exam}
        END
        
    END
    
    RETURN  ${exams}

Fatch Exam
    [Arguments]    ${url}
    

    Go To    ${url}
    # ${c}=    Check If Mobile Check Active
    # IF    ${c}
    #     RETURN    ${None}
    # END
    
    &{exam}=    Create Dictionary
    ${exam}[catalog]=    Get Text   xpath=/html/body/div[2]/table/tbody/tr[2]/td[1]
    ${exam}[dynamic]=    Get Text   xpath=/html/body/div[2]/table/tbody/tr[2]/td[2]
    ${score_str}=    Get Text   xpath=/html/body/div[2]/table/tbody/tr[2]/td[3]
    ${exam}[score]=    Convert To Integer    ${score_str}
    ${total_str}=    Get Text   xpath=/html/body/div[2]/table/tbody/tr[2]/td[4]
    ${exam}[total]=    Convert To Integer    ${total_str}
    ${exam}[level]=    Get Text   xpath=/html/body/div[2]/table/tbody/tr[2]/td[5]
    ${exam}[name]=    Get Text   xpath=/html/body/p[1]
    
    RETURN    ${exam}