import os
import aiohttp
from dotenv import load_dotenv

api_endpoint = "https://tars.loopscale.com/ruby/discord"
api_points = "https://tars.bridgesplit.com/ruby/points"
# Load the .env file

# curl --location 'https://tars.bridgesplit.com/ruby/points/add_community?api_key=f64b442c-94da-485e-8185-c61c61f702d5' \
# --header 'Content-Type: application/json' \
# --data '{
#     "points":100,
#     "discordId":"452901254969163797"
# }'
load_dotenv()
LOOPSCALE_API_KEY = os.getenv('LOOPSCALE_API_KEY')
LOOPSCALE_POINTS_API_KEY = os.getenv('LOOPSCALE_POINTS_API_KEY')
async def _get_user_waitlist_position(discord_user_id: str, discord_user_name: str):
    resource = f"/user-waitlist-info"
    url = api_endpoint + resource   
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "user": discord_user_id,
        "username": discord_user_name,
        "api_key": LOOPSCALE_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return False

async def _get_user_points(discord_user_id: str,  discord_user_name: str):
    resource = f"/user-points-info"
    url = api_endpoint + resource   
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "user": discord_user_id,
        "username": discord_user_name,
        "api_key": LOOPSCALE_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return False
            
async def _mutate_user_points(discord_user_id: str, points: int):
    resource = f"/add_community"
    url = f"{api_points}{resource}?api_key={LOOPSCALE_POINTS_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "points": points,
        "discordId": str(discord_user_id),
    }
    
    print(url, headers, payload, "internal _mutate_user_points")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                return True
            else:
                print(response, "internal response")
                return False
            
async def _top_10_leaderboard(type: str):
    if type == 'points':
        resource = f"/top-users"
    else:
        resource = f"/top-waitlist"
        
    url = api_endpoint + resource   
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "limit": 10,
        "api_key": LOOPSCALE_API_KEY
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return False