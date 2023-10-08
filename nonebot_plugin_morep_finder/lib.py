import asyncio
import time
import aiohttp
from .config import Config

cookies = {
    'auth': '',
}

headers = {
    'authority': 'www.kookapp.cn',
    'accept': '*/*',
    'accept-language': 'zh',
    'content-type': 'application/json; charset=utf-8',
    'referer': 'https://www.kookapp.cn/app/channels/2127841922601861/3735309828842826',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'x-client-sessionid': 'c13d75c7-ed00-45cf-947e-deedf0bf11e6',
    'x-client-utm': 'official.site....pc',
}


def init(config: Config):
    cookies['auth'] = config.kook_auth_key


async def get_user_game_and_music(user_id):
    async with aiohttp.ClientSession() as session:
        response = await session.request("GET", f'https://www.kookapp.cn/api/v2/users/{user_id}', cookies=cookies,
                                         headers=headers)
        result = await response.json()
        return [result.get("game", None), result.get("music", None)]


async def get_users(guild_id, game: list):
    users_list = []
    left_count = 600
    offset = 0
    while left_count > 500:
        params = {
            'offset': f'{offset}',
            'perPage': '500',
        }
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f'https://www.kookapp.cn/api/v2/guilds/users-v2/{guild_id}',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            result = await response.json()
            left_count = result['count']
            offset += 500
            for i in result['data']:
                if i['online'] and i.get("game", False) and i['game']['name'] in game:
                    users_list.append([i['vip_avatar'], i['nickname'], (time.time() - int(i['game']['start_time'])) // 60])
    return users_list

if __name__ == '__main__':
    async def main():
        print(await get_user_game_and_music(239017136))


    asyncio.run(main())
