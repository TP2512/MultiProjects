*** Settings ***
Documentation    This is sample test execution for package
Resource    keywords.resource
Suite Setup       Connect to MongoDB
Test Teardown   Close DB
Suite Teardown  Close Mongodb Connection


*** Variables ***
${database1}     my_graph_database
${database2}     test1

*** Test Cases ***
Access All Collections From DB
    [Documentation]    Tests able to get collections from db.
    Use DB      ${database1}
    ${collections}=   Get All Collections In Database
    log    ${collections}
    Use DB      ${database2}
    ${collections}=   Get All Collections In Database
    log    ${collections}


