*** Settings ***
Documentation       KT11 — Automated Testing with Robot Framework (exactly 10 cases).
Resource            ../resources/common.resource
Resource            ../resources/pages.resource
Suite Setup         Suite Bootstrap
Suite Teardown      Suite Teardown Steps
Test Setup          No Operation
Test Teardown       Close Test Application
Test Tags           KT11

*** Test Cases ***
TC-11-01 Page Opens And Title Is Correct
    [Documentation]    Home page loads with the expected document title and heading.
    [Tags]    KT11    smoke    title
    Open Home Page
    Element Text Should Be    id:home-heading    KT11 Robot Framework Demo
    Element Should Be Visible    id:home-intro
    Capture Scenario Screenshot    01_home_title

TC-11-02 Navigation Link Opens Expected Page
    [Documentation]    Clicking the registration nav link opens register.html.
    [Tags]    KT11    navigation
    Open Home Page
    Navigate To Registration Via Link
    Element Text Should Be    id:register-heading    Регистрация KT11
    Capture Scenario Screenshot    02_navigation_register

TC-11-03 Valid Form Submission Succeeds
    [Documentation]    Valid name and email produce an accepted form status.
    [Tags]    KT11    form    positive
    Open Registration Page
    Submit Registration Form    Анна Тестова    anna.kt11@example.com
    Verify Form Accepted    Анна Тестова    anna.kt11@example.com
    Capture Scenario Screenshot    03_form_valid

TC-11-04 Invalid Form Data Is Rejected
    [Documentation]    Missing/invalid fields show the validation error status.
    [Tags]    KT11    form    negative
    Open Registration Page
    Submit Registration Form    ${EMPTY}    not-an-email
    Verify Form Validation
    Capture Scenario Screenshot    04_form_invalid

TC-11-05 Checkbox Can Be Selected And Deselected
    [Documentation]    Newsletter checkbox toggles between selected and not selected.
    [Tags]    KT11    checkbox
    Open Controls Page
    Toggle Newsletter Checkbox    ${True}
    Element Should Contain    id:controls-summary    Чекбокс: on
    Toggle Newsletter Checkbox    ${False}
    Element Should Contain    id:controls-summary    Чекбокс: off
    Capture Scenario Screenshot    05_checkbox

TC-11-06 Radio Button Selection Changes Active Option
    [Documentation]    Selecting plan radios updates the active option and summary.
    [Tags]    KT11    radio
    Open Controls Page
    Select Plan Radio    basic
    Element Should Contain    id:controls-summary    План: basic
    Select Plan Radio    pro
    Element Should Contain    id:controls-summary    План: pro
    Capture Scenario Screenshot    06_radio

TC-11-07 Dropdown Selection Produces Correct Value
    [Documentation]    Selecting a country by value updates list selection and summary.
    [Tags]    KT11    dropdown
    Open Controls Page
    Select Country From Dropdown    kz    Казахстан
    Element Should Contain    id:controls-summary    Страна: kz
    Capture Scenario Screenshot    07_dropdown

TC-11-08 Iframe Interaction And Return To Main Document
    [Documentation]    Switch into iframe, submit text, then return to default content.
    [Tags]    KT11    iframe
    Open Frames Page
    Interact Inside Demo Iframe    KT11 iframe OK
    Element Text Should Be    id:host-status    Контекст: основной документ
    Capture Scenario Screenshot    08_iframe

TC-11-09 Open New Tab Switch Verify And Return
    [Documentation]    Open secondary tab, verify content, return to the main window.
    [Tags]    KT11    windows
    Open Home Page
    ${main}=    Get Window Handles
    ${main_handle}=    Set Variable    ${main}[0]
    Open Secondary Tab
    Capture Scenario Screenshot    09_secondary_tab
    Return To Main Page    ${main_handle}
    Capture Scenario Screenshot    09_back_main

TC-11-10 Dynamic UI Update Is Verified
    [Documentation]    Clicking the dynamic button changes the status text on the page.
    [Tags]    KT11    dynamic
    Open Home Page
    Trigger Dynamic Status Update
    Capture Scenario Screenshot    10_dynamic_update
