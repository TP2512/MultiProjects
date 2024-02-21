import aiml
import requests

# Create a Kernel (AIML interpreter) instance
kernel = aiml.Kernel()

# Load AIML files
kernel.learn("basic.aiml")
kernel.learn("data-retrieval.aiml")

# Function to fetch weather data from an external API
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8a57ebe7c8311e5b3fa4b407aea78c23"
    response = requests.get(url)
    # print(response)
    data = response.json()
    weather = data["weather"][0]["description"]
    return weather

# Main loop to interact with users
while True:
    user_input = input("You: ").upper()  # Get user input
    response = kernel.respond(user_input)  # Get response from AIML
    print("chatbot: ",response)
    # Check if the response is a data retrieval command
    # if response.startswith("GET_WEATHER"):
    #     city = response.split()[-1]
    #     weather = get_weather(city)
    #     print(f"Chatbot: The weather in {city} is {weather}.")
    # else:
    #     print("Chatbot:", response)  # Print response
