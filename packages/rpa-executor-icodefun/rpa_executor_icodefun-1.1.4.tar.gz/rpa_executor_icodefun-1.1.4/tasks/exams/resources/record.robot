*** Settings ***
Library    RPA.Excel.Files
Library    Collections

Resource    var.robot

*** Keywords ***

Get Last Interupted code
    ${code}=    Get Cell Value    1    1    Sheet
    RETURN    ${code}
Set Last Interupted code
    [Arguments]    ${code}
    Set Cell Value    1    1    ${code}    Sheet

Clear Last Interupted code
    Set Active Worksheet    Sheet
    Clear Cell Range    A1  
Prepare Worksheet
    [Arguments]    ${catalog}
    ${is_exist}=    Worksheet Exists    ${catalog}
    IF    ${is_exist}
        Set Active Worksheet    ${catalog}
    ELSE
        Create Worksheet    ${catalog}
        Set Active Worksheet    ${catalog}
        Set Cell Value    1    1    catalog
        Set Cell Value    1    2    exam
        Set Cell Value    1    3    name
        Set Cell Value    1    4    dynamic
        Set Cell Value    1    5    score
        Set Cell Value    1    6    total
        Set Cell Value    1    7    level
        Set Cell Value    1    8    code
        Set Cell Value    1    9    school
        Set Cell Value    1    10    grade
        Set Cell Value    1    11    class
    END

Prepare Empty Row
    ${next_row}=    Find Empty Row 
    RETURN    ${next_row}

Record Scores
    [Arguments]
    ...    ${student_info}
    ...    ${exams}
    ${c}=    Get Length    ${exams}
    FOR    ${i}    IN RANGE    0    ${c}    1
        Prepare Worksheet    ${exams}[${i}][catalog]
        ${next_row}=    Prepare Empty Row
        Set Cell Value    ${next_row}    1    ${exams}[${i}][catalog]
        Set Cell Value    ${next_row}    2    ${exams}[${i}][name]
        Set Cell Value    ${next_row}    3    ${student_info}[name]
        Set Cell Value    ${next_row}    4    ${exams}[${i}][dynamic]
        Set Cell Value    ${next_row}    5    ${exams}[${i}][score]
        Set Cell Value    ${next_row}    6    ${exams}[${i}][total]
        Set Cell Value    ${next_row}    7    ${exams}[${i}][level]
        Set Cell Value    ${next_row}    8    ${student_info}[code]
        Set Cell Value    ${next_row}    9    ${student_info}[school]
        Set Cell Value    ${next_row}    10    ${student_info}[grade]
        Set Cell Value    ${next_row}    11    ${student_info}[class]
    END