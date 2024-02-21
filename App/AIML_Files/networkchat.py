import aiml
import requests

# Create a Kernel object
kernel = aiml.Kernel()
# # Load AIML files
kernel.learn("api_req.aiml")
#GIVE ME THE STATUS OF NODE RESTID
# Function to query node status from NMS API
def get_node_status():
    kernel.setPredicate("number")
    node_id = kernel.getPredicate("number")
    print(node_id)
    # Make HTTP request to NMS API to retrieve node status
    # Replace 'api_endpoint' and 'api_key' with actual values
    api_endpoint = 'https://10.34.0.32/api/20.5/enbStatusRf'
    api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJhdXRobWV0aG9kIjoiUmVzdEFwaUtleSIsIm5hbWVpZCI6IjYxMzU2MjdjZmYwZTRiNzg5YmY5NjBjODYyYTVmOTcxIiwibmJmIjoxNzAzMDU2NDEwLCJleHAiOjIwMTg2NzU2MTAsImlhdCI6MTcwMzA1NjQxMH0.cqokIACzP9BlYn77oT_7KBaKL69YWH1KsIKmWdqKGpg'
    response = requests.get(f'{api_endpoint}/{node_id}', headers={'Authorization': f'Bearer {api_key}'},verify=False)

    node_status = response.json() .get('rfStatus')[0].get('operationalStatus')

    if node_status:
        return f"The status of node RESTID {node_id} is {node_status}."
    else:
        return f"Failed to retrieve status for node RESTID {node_id}."

# Set current time (for demonstration purposes)
kernel.setPredicate("current_time", "12:00 PM")
kernel.setPredicate("number",)
clients_dogs_name = kernel.getPredicate("number")
# Accept user input and get bot response
while True:
    user_input = input("You: ")  # Get user input
    bot_response = kernel.respond(user_input)  # Get bot response
    print("Bot:", bot_response)  # Print bot response
