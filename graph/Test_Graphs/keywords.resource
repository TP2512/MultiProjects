*** Settings ***
Documentation    This is file where all keywords defination is there
Library    CustomLibrary.py


*** Variables ***
${mongostring}    mongodb://localhost:27017

*** Keywords ***
Connect To Mongodb
    Connect    ${mongostring}

Use DB
    [Arguments]    ${database}
    Dbconnect    ${database}

Close Mongodb Connection
    Disconnect

Get All Collections In Database
    ${Collections}=    run keyword and return    Get All Collections
    RETURN    ${Collections}

Close DB
    Dbdisconnect