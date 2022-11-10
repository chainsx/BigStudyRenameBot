from random import choice
import asyncio

# 用于处理普通用户信息的函数
async def get_response_for_common_user(bot, chat, msg, user_id, group_id, default_ban_time, last_response,
                                 words, cool_down, random_response, is_super_user):
    # 使用默认冷却cd与默认概率的响应
    if (cool_down(group_id) and random_response()) or is_super_user:
        # 随机返回响应
        if "抱一抱" in msg or "抱抱" in msg:
            responses = ["这就送你一发恒星核心温度的抱抱~",
                         "倒也不是不行，但是你真的能承受住吗？",
                         "为什么会有人想要拥抱真空呢？"]
            return choice(responses)

        # 发送多条信息并且在过程中休眠
        if "自爆" in msg:
            await chat.send("自爆程序即将启动，倒计时：")
            await asyncio.sleep(1)
            await chat.send("3")
            await asyncio.sleep(1)
            await chat.send("2")
            await asyncio.sleep(1)
            await chat.send("1")
            await asyncio.sleep(1)
            return r'开始执行rm -rf /*'

    # 添加响应概率不同的事件
    if (cool_down(group_id) and random_response(p=20)) or is_super_user:
        if "？" == msg or "?" == msg:
            responses = ['？',
                         '¿',
                         '？？',
                         '？？？',
                         '当我打出问号的时候，不是我有问题，而是我觉得你有问题']
            return choice(responses)
