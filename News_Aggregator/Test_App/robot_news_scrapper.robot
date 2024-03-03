*** Settings ***
Library         SeleniumLibrary
Library         RequestsLibrary
Library         Collections
Library         String
Library         OperatingSystem

*** Test Cases ***
Check Broken Link On Page
    Open Browser    https://timesofindia.indiatimes.com/briefs    chrome    executable_path=C:/drivers/chromedriver.exe
    Set Selenium Implicit Wait    20
    Set Selenium Timeout    10
    Maximize Browser Window
    Wait Until Element Is Enabled    xpath:(//div[@data-section_name='/briefs'])[1]
    ${available_data} =   Article Data

    Log To Console    *****************************************************    no_newline=true
    Log  Valid links are :${available_data}
    Log To Console    *****************************************************


*** Keywords ***
Article Data
    ${links}    Get WebElements    //div[@data-section_name='/briefs']
    ${all_links}    Create List
    FOR    ${link}      IN    @{links}
        ${link_data}=    Get text    ${link}
#        Append To File    C:/drivers    ${link_data}
        Append To List    ${all_links}    ${link_data}
    END
    [Return]    ${all_links}