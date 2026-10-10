*** Settings ***
Documentation       Page-level keywords for KT11 fixtures (keyword-driven layer).
Resource            common.resource

*** Keywords ***
Open Home Page
    Open Test Application    index.html
    Wait Until Element Is Visible    id:home-heading
    Title Should Be    KT11 Robot Home

Open Registration Page
    Open Test Application    register.html
    Wait Until Element Is Visible    id:register-heading
    Title Should Be    KT11 Registration

Open Controls Page
    Open Test Application    controls.html
    Wait Until Element Is Visible    id:controls-heading
    Title Should Be    KT11 Controls

Open Frames Page
    Open Test Application    frames.html
    Wait Until Element Is Visible    id:frames-heading
    Title Should Be    KT11 IFrame Host

Navigate To Registration Via Link
    Wait Until Element Is Visible    id:nav-register
    Click Element    id:nav-register
    Wait Until Element Is Visible    id:register-heading
    Title Should Be    KT11 Registration

Submit Registration Form
    [Arguments]    ${name}    ${email}
    Wait Until Element Is Visible    id:reg-name
    Clear Element Text    id:reg-name
    Input Text    id:reg-name    ${name}
    Clear Element Text    id:reg-email
    Input Text    id:reg-email    ${email}
    Click Element    id:reg-submit

Verify Form Accepted
    [Arguments]    ${name}    ${email}
    Wait Until Element Contains    id:form-status    принято
    Element Should Contain    id:form-status    ${name}
    Element Should Contain    id:form-status    ${email}

Verify Form Validation
    Wait Until Element Contains    id:form-status    ошибка валидации
    Element Text Should Be    id:form-status    Статус: ошибка валидации

Toggle Newsletter Checkbox
    [Arguments]    ${should_be_selected}
    IF    ${should_be_selected}
        Select Checkbox    id:newsletter
        Checkbox Should Be Selected    id:newsletter
    ELSE
        Unselect Checkbox    id:newsletter
        Checkbox Should Not Be Selected    id:newsletter
    END

Select Plan Radio
    [Arguments]    ${value}
    Select Radio Button    plan    ${value}
    Radio Button Should Be Set To    plan    ${value}

Select Country From Dropdown
    [Arguments]    ${value}    ${label}
    Select From List By Value    id:country    ${value}
    ${selected}=    Get Selected List Value    id:country
    Should Be Equal    ${selected}    ${value}
    List Selection Should Be    id:country    ${label}

Interact Inside Demo Iframe
    [Arguments]    ${text}
    Wait Until Element Is Visible    id:demo-frame
    Select Frame    id:demo-frame
    Wait Until Element Is Visible    id:frame-input
    Clear Element Text    id:frame-input
    Input Text    id:frame-input    ${text}
    Click Element    id:frame-submit
    Wait Until Element Contains    id:frame-result    ${text}
    Element Text Should Be    id:frame-result    Результат: ${text}
    Unselect Frame
    Wait Until Element Is Visible    id:frames-heading
    Element Should Be Visible    id:host-status

Open Secondary Tab
    ${before}=    Get Window Handles
    ${count_before}=    Get Length    ${before}
    ${expected}=    Evaluate    ${count_before} + 1
    Wait Until Element Is Visible    id:nav-secondary
    Click Element    id:nav-secondary
    Wait Until Keyword Succeeds    10 seconds    0.2 seconds
    ...    Window Handle Count Should Be    ${expected}
    Switch Window    NEW
    Wait Until Element Is Visible    id:secondary-heading
    Title Should Be    KT11 Secondary Tab
    Element Text Should Be    id:secondary-heading    Вторичная вкладка KT11

Window Handle Count Should Be
    [Arguments]    ${expected}
    ${handles}=    Get Window Handles
    ${n}=    Get Length    ${handles}
    Should Be Equal As Integers    ${n}    ${expected}

Return To Main Page
    [Arguments]    ${main_handle}
    Switch Window    ${main_handle}
    Wait Until Element Is Visible    id:home-heading
    Title Should Be    KT11 Robot Home

Trigger Dynamic Status Update
    Wait Until Element Is Visible    id:dynamic-status
    ${before}=    Get Text    id:dynamic-status
    Should Be Equal    ${before}    Статус: исходный
    Click Element    id:dynamic-btn
    Wait Until Element Contains    id:dynamic-status    обновлено
    ${after}=    Get Text    id:dynamic-status
    Should Not Be Equal    ${before}    ${after}
    Element Text Should Be    id:dynamic-status    Статус: обновлено (1)
