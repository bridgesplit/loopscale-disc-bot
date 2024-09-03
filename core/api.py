import asyncio
import os
import aiohttp
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter

api_endpoint = "https://tars.loopscale.com/ruby/discord"

# Load the .env file
load_dotenv()
LOOPSCALE_API_KEY = os.getenv('LOOPSCALE_API_KEY')

# Create a rate limiter: 5 requests per 10 seconds.
rate_limiter = AsyncLimiter(2, 10)

#Attempted to use aiolimiter library since dictionary/timer was throwing errors
async def rate_limited_request(url, headers, params):
    try:
        async with rate_limiter:
            async with aiohttp.ClientSession() as session:
                async with asyncio.timeout(2.5):
                    async with session.get(url, headers=headers, params=params) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            return False
    except asyncio.TimeoutError:
        # This will be raised if the request takes longer than 2.5 seconds, to make sure we are below discords 3 second rule
        return 'RATE_LIMITED'
    except Exception as e:
        print(f"Unexpected error in rate_limited_request: {str(e)}")
        return False

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
    return await rate_limited_request(url, headers, params)

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
    return await rate_limited_request(url, headers, params)

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
    return await rate_limited_request(url, headers, params)