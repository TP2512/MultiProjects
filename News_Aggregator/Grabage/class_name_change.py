from pydantic import BaseModel

class UserMeta(type):
    def __new__(cls, name, bases, dct):
        dct['__name__'] = 'User'
        return super().__new__(cls, name, bases, dct)

class UserBase(BaseModel, metaclass=UserMeta):
    username: str
    email: str
    password: str



# Test
user_data = {"username": "john_doe", "email": "john@example.com", "password": "secret"}
user = UserBase(**user_data)
print(user)
print(UserBase.__name__)  # Output: User
