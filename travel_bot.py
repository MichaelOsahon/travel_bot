from openai import AzureOpenAI
import os
import requests
import json

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	azure_endpoint = os.getenv("AZURE_ENDPOINT"),
	api_version = "2023-10-01-preview"
)

messages = [
	# "role": "system", "content": "Respond to everything as a short poem"},
	{"role": "user", "content": "tell me the number of planes in the sky above Belgium?"}
]

def flights(country_name):
	url=f"https://opensky-network.org/api/states/all"
	response = requests.get(url)
	data = response.json()
	states = data.get('states', [])	
	country_list = [state[2] for state in states if len(state) > 0]
	country_count = country_list.count(country_name)
	return f"there are currently {country_count} planes in the sky above {country_name}" 

functions = [
	{
		"type": "function",
		"function": {
			"name": "get_flights",
			"description": "finds the number of planes above a country",
			"parameters": {
				# lettings chat-gpt know that it's getting
				# key-value pairs
				"type": "object",
				"properties": {
					"country_name": {
						"type": "string",
						"description": "The name of the country"
					},
					
			
				},
				"required": ["country_name"]
			}
		}
	}
]

response = client.chat.completions.create(
	model = "GPT-4",
	messages = messages,
	tools = functions,
	# auto means chat-gpt decides when it needs to use external functions
	tool_choice = "auto"
)
response_message = response.choices[0].message
# if chat-gpt doesn't need help, this will be None, otherwise there will be stuff
gpt_tools = response.choices[0].message.tool_calls

# if gpt_tools is not None
# gpt_tools is a list!
if gpt_tools:

	# set up a 'phonebook', if we see a function name, we need to tell our code 
	# which function to call
	available_functions = {
		"get_flights": flights
	}

	messages.append(response_message)
	for gpt_tool in gpt_tools:
		# figure out which friend to call
		function_name = gpt_tool.function.name
		# looking up my function name in my 'phonebook'
		function_to_call = available_functions[function_name]
		# need the parameters for the function
		function_parameters = json.loads(gpt_tool.function.arguments)
		function_response = function_to_call(function_parameters.get('country_name'))
		messages.append(
			{
				"tool_call_id": gpt_tool.id,
				"role": "tool",
				"name": function_name,
				"content": function_response
			}
		)
		second_response = client.chat.completions.create(
			model = "GPT-4",
			messages=messages
		)
		print(second_response.choices[0].message.content)

else:
	print(response.choices[0].message.content)