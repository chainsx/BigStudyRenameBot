from collections import Counter

# 用于处理任何情况下都需要进行判断的函数
# 主要用于对一些违禁用户进行禁言处理
async def get_response_for_all_time(bot, chat, msg, user_id, group_id, default_ban_time, last_response,
                              words, cool_down, random_response):
    msg = msg.replace('阿', '啊')
    words = Counter(msg)

    # 针对恶臭发言用户
    if "哼" in words and "啊" in words:
        if words["哼"] >= 2 and words["啊"] >= 3:
            # 尝试禁言
            try:
                await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=default_ban_time)
            # 如果对方是管理员，那就假装无事发生
            except:
                pass
            return "恶臭，死吧！"

    # 针对发病用户
    if "嘿" in words:
        if words["嘿"] >= 5:
            # 尝试禁言
#            try:
#                await bot.set_group_ban(group_id=group_id, user_id=user_id, duration=default_ban_time)
            # 如果对方是管理员，那就假装无事发生
#            except:
#                pass
            return "禁止发病！"
