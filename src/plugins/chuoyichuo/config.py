from pydantic import BaseSettings

class Config:
    # 记录在哪些群组中使用
    used_in_group = ["965126988", "704428994", "951526238"]
    # 插件执行优先级
    priority = 10
    # 接话冷却时间（秒），在这段时间内不会连续两次接话
    chat_cd = 15
    # 戳一戳冷却时间（秒）
    notice_cd = 900
    # 机器人QQ号
    bot_id = "1417898966"
    # 管理员QQ号，管理员无视冷却cd和触发概率
    super_uid = ["1396219808"]
    # 聊天回复概率，用百分比表示，0-100%
    p_chat_response = 100
    # 戳一戳回复概率，用百分比表示，0-100%
    p_poke_response = 100
    # 默认禁言时间，每多戳一次会在默认禁言时间上翻倍
    default_ban_time = 60
