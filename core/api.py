import os
import aiohttp
from dotenv import load_dotenv

api_endpoint = "https://tars.loopscale.com/ruby/discord"

# Load the .env file
load_dotenv()
LOOPSCALE_API_KEY = os.getenv('LOOPSCALE_API_KEY')

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