
from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
import requests
llm = ChatOpanAI(model="gpt-4o-mini",temperature=0)
class TravelState(TypedDict):
        destination: str
        days: int
        budget: int
        travel_style: str
        interests: str
        destination_plan: str
        itinerary_plan: str   #
        budget_plan: str
        final_plan: str
        weather: str

def get_weather(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search"
    geo_response = requests.get(geo_url,params={"name":city, "count":1})
    geo_data = geo_response.json()
    if "results" not in geo_data:
        return "Weather information not found."
    latitude = float  (geo_data["results"] [0]["latitude"])
    longitude =float (geo_data["results"][0]["longitude"])

    weather_url ="https://api.open-meteo.com/v1/forecast"

    print("LAT:", latitude,type(latitude))
    print("LON:", longitude,type(longitude))

    weather_response = requests.get(weather_url,params={"latitude":latitude,"longitude":longitude,"current":"temperature_2m,relative_humidity_2m"})





    print("STATUS:" ,weather_response.status_code)
    print( weather_response.text)

    weather_data = weather_response.json()
    if "current" not in weather_data:
        return f"Weather API error: {weather_data}"

    current = weather_data['current']
    return (
        f"Temperature: {current['temperature_2m']}C, "
        f"Humidity: {current['relative_humidity_2m']}%"
    )
def get_location_info(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    response = requests.get(url)
    data = response.json()
    if "results" in data and data["results"]:
        location= data["results"][0]
        return {
            "city": location.get("name"),"country":
        location.get("country"),"latitude":
            location.get("latitude"),"longitude":
            location.get("longitude"),"timezone":
            location.get("timezone")

        }
    return {"error": "Location not found"
            }

def weather_agent(state: TravelState):
    location = get_location_info(state["destination"])
    weather = get_weather(state["destination"])
    return {"location_info": location,
            ""
            "weather": weather}

def destination_agent(state: TravelState):
    response = llm.invoke(f"""Suggedt tourist places and attractions in {state['destination']} based on
    the travelers preferences.
    Travel style: {state['travel_style']}
    Interests: {state['interests']}
    Recommended places that match these preferences.""")
    return  {"destination_plan": response.content}

def itinerary_agent(state: TravelState):
    response = llm.invoke(f"""Create a {state['days']}-day travel itinerary for {state['destination']}.
    Travel style: {state['travel_style']}
    Interests:{state['interests']}
    Budget:{state['budget']}
    Make the itinerary personalized to the travellers interests and travel style.
    include a balanced schedule for each day.""")
    return {"itinerary_plan": response.content}

def budget_agent(state: TravelState):
    budget = state["budget"]
    days = state["days"]
    accomodation = int(budget * 0.40)
    food = int(budget * 0.20)
    transportation = int(budget * 0.20)
    activities = int(budget * 0.20)
    total_estimated= (
        accomodation
       + food
       +transportation
       + activities
    )
    remaining = budget - total_estimated
    return {
        "budget_plan":( f" SMART BUDGET PLAN\n"
       f" Total Budget: {budget}\n"
        f"Accomodation: {accomodation}\n"
        f"Food: {food}\n"
        f"Transportation: {transportation}\n"
       f" Activities: {activities}\n" 
       f" Estimated Trip Cost: {total_estimated}\n"
        f"Remaining Budget: {remaining}")
    }




def review_agent(state: TravelState):
        return {
            "final_plan": f""" final TRAVEL PLAN Review:
            
Destination: {state.get('destination','')}
Duration: {state.get('days','')} 
Budget:{state.get('budget', '')}
Destination Plan:{state.get('destination_plan', '')}
Itinerary:{state.get('itinerary_plan', state.get('itinerary', ''))}
Budget Plan:{state.get('budget_plan', '')}
"""
        }
graph = StateGraph (TravelState)

graph.add_node("weather_agent", weather_agent)
graph.add_node( "destination_agent",  destination_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("budget_agent", budget_agent)
graph.add_node("review_agent", review_agent)

print("FINAL NODES:",list(graph.nodes.keys()))



graph.set_entry_point("weather_agent")
graph.add_edge("weather_agent" , "destination_agent")
graph.add_edge("destination_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "budget_agent")
graph.add_edge("budget_agent", "review_agent")

graph.set_finish_point("review_agent")

app = graph.compile()

result = app.invoke({
        "destination": "Goa",
            "days": 4,
"budget": 100000,
"travel_style": "Budget",
"interests": "Beaches,History, Nature",
"weather": "",
"destination_plan": "",
"itinerary_plan": "",    #
"budget_plan": "",
"final_plan": ""
})

print("\n===== FINAL TRAVEL PLAN =====")
print("destination",result["destination"])
print("Days:",result["days"])
print("Budget:",result["budget"])
print("\nDestination Plan:\n",result["destination_plan"])
print("\nItinerary:\n",result["itinerary_plan"])
print("\nBudget Plan:\n",result["budget_plan"])
print("\nFinal Plan:\n",result["final_plan"])
#print(get_weather("Jaipur"))



