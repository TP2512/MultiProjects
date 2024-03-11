# Contains tests for endpoints related to fetching user details.
from fastapi.testclient import TestClient
from main import app
import pytest
from fastapi import status
from bson import ObjectId
from unittest.mock import AsyncMock
from endpoints.users import router
# from database.database_connection import get_database
# from utils import oauth2


# Define fixtures for mocking database and current user
@pytest.fixture
async def test_db():
    return AsyncMock()


@pytest.fixture
async def test_current_user():
    return {"_id": ObjectId("606769f6bc93c98da8b5e450")}  # Example user ID


# Test successful retrieval of user data
@pytest.mark.asyncio
async def test_get_user_success(test_db, test_current_user):
    expected_user_data = {
        "_id": ObjectId("606769f6bc93c98da8b5e450"),
        "username": "test_user",
        "email": "test@example.com"
    }
    test_db["UserBase"].find_one.return_value = expected_user_data

    response = await router.get("/users/606769f6bc93c98da8b5e450",
                                db=test_db,
                                current_user=test_current_user)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": "606769f6bc93c98da8b5e450",
        "username": "test_user",
        "email": "test@example.com"
    }

#
# # Test unauthorized access
# @pytest.mark.asyncio
# async def test_get_user_unauthorized(test_db, test_current_user):
#     # Provide a different user ID than the one in the current user fixture
#     response = await router.get("/users/606769f6bc93c98da8b5e451",
#                                 db=test_db,
#                                 current_user=test_current_user)
#
#     assert response.status_code == status.HTTP_403_FORBIDDEN
#
#
# # Test user not found
# @pytest.mark.asyncio
# async def test_get_user_not_found(test_db, test_current_user):
#     test_db["UserBase"].find_one.return_value = None
#
#     response = await router.get("/users/606769f6bc93c98da8b5e450",
#                                 db=test_db,
#                                 current_user=test_current_user)
#
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#
