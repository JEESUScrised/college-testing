*** Settings ***
Documentation       Shared browser setup/teardown and fixture HTTP server for KT11.
Library             SeleniumLibrary    timeout=10    run_on_failure=Capture Page Screenshot
Library             ../lib/FixtureServer.py
Library             OperatingSystem

*** Variables ***
${BROWSER}          chrome
${WINDOW_WIDTH}     1400
${WINDOW_HEIGHT}    1000
${SHOT_DIR}         ${CURDIR}${/}..${/}..${/}screenshots${/}kt11
${BASE_URL}         ${EMPTY}

*** Keywords ***
Suite Bootstrap
    [Documentation]    Start local fixture server and prepare screenshot directory.
    ${url}=    Start Fixture Server
    Set Suite Variable    ${BASE_URL}    ${url}
    Create Directory    ${SHOT_DIR}
    Set Screenshot Directory    ${SHOT_DIR}

Suite Teardown Steps
    [Documentation]    Close browsers and stop fixture server.
    Close All Browsers
    Stop Fixture Server

Open Test Application
    [Documentation]    Open Chrome session on a local KT11 page.
    [Arguments]    ${path}=index.html
    Open Browser    ${BASE_URL}/${path}    ${BROWSER}
    Set Window Size    ${WINDOW_WIDTH}    ${WINDOW_HEIGHT}
    Set Selenium Implicit Wait    0
    Set Selenium Timeout    10 seconds

Close Test Application
    Run Keyword And Ignore Error    Close Browser

Capture Scenario Screenshot
    [Arguments]    ${name}
    ${path}=    Capture Page Screenshot    ${name}.png
    RETURN    ${path}
