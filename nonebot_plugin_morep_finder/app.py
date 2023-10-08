from .config import Config


def no_op(name, color):
    return [
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "color": "#00ff00",
            "modules": [
                {
                    "type": "section",
                    "text": {
                        "type": "kmarkdown",
                        "content": f"查找完成，当前没有(font){name}(font)[{color}]！"
                    }
                }
            ]
        }
    ]


def op_unit(avatar, name, time):
    return {
        "type": "section",
        "text": {
            "type": "kmarkdown",
            "content": f"(font){name}(font)[danger] 当前时长: (font){time}(font)[danger] 分钟"
        },
        "mode": "left",
        "accessory": {
            "type": "image",
            "src": avatar,
            "size": "lg"
        }
    }


def op_template(name, color, users):
    return [
        {
            "type": "card",
            "theme": "secondary",
            "size": "lg",
            "color": "#ff0000",
            "modules": [
                           {
                               "type": "section",
                               "text": {
                                   "type": "kmarkdown",
                                   "content": f"查找完成，发现(font){name}(font)[{color}]！"
                               }
                           },
                           {
                               "type": "divider"
                           }
                       ] + [op_unit(i[0], i[1], i[2]) for i in users]
        }
    ]


def init(config: Config):
    from nonebot import on_command
    from nonebot.adapters.kaiheila import Bot as KookBot
    from nonebot.adapters.kaiheila import Event as KookEvent
    from nonebot.adapters.kaiheila import MessageSegment
    from nonebot.matcher import Matcher
    from nonebot.typing import T_State
    from nonebot import logger
    from .lib import get_users

    config = config.morep_config
    for item in config:
        user_finder = on_command(item["command"][0], aliases=set(item["command"]), state=item)

        @user_finder.handle()
        async def _(_bot: KookBot, event: KookEvent, matcher: Matcher, state: T_State):
            # logger.debug(f"channel_type: {event.channel_type}")
            if event.channel_type == "PERSON":
                matcher.finish()
            # channel_id = event.target_id
            guild_id = event.extra.guild_id
            # logger.debug(f"收到来自 guild_id|channel_id:{guild_id}|{channel_id} 的消息")
            users = await get_users(guild_id, state["game"])

            if len(users) == 0:
                # await bot.call_api("game/activity", id=1500242, data_type=1)
                await matcher.finish(MessageSegment.Card(no_op(state["name"], state["color"])))
            else:
                # await bot.call_api("game/delete-activity", data_type=1)
                await matcher.finish(
                    MessageSegment.Card(op_template(state["name"], state["color"], users)))
