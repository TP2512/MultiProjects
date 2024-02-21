# import aiml
# import requests
#
# # Create a Kernel object
# kernel = aiml.Kernel()
#
# # Load AIML files
# kernel.learn("hello.aiml")  # Load AIML files
#
# def get_weather(city):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8a57ebe7c8311e5b3fa4b407aea78c23"
#     response = requests.get(url)
#     # print(response)
#     data = response.json()
#     weather = data["weather"][0]["description"]
#     return weather
import aiml
import requests

# Initialize AIML Kernel
kernel = aiml.Kernel()

# Load AIML files
kernel.learn("data_retrieval.aiml")

# Function to get weather data from API
def get_weather(city):
    api_key = "8a57ebe7c8311e5b3fa4b407aea78c23"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8a57ebe7c8311e5b3fa4b407aea78c23"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return "Sorry, unable to fetch weather data."
    else:
        return data["current"]["condition"]["text"]

# Function to handle AIML GET_WEATHER pattern
def handle_weather(city):
    return get_weather(city)

# Main loop for chatbot interaction
while True:
    user_input = input("You: ")
    response = kernel.respond(user_input)
    if response.startswith("GET_WEATHER"):
        city = response.split()[-1]
        weather_response = handle_weather(city)
        print("Chatbot:", weather_response)
    else:
        print("Chatbot:", response)
