# 用于处理超级用户信息的函数
async def get_response_for_surper_user(bot, chat, msg, user_id, group_id, default_ban_time, last_response,
                                 words, cool_down, random_response):

    if "贴贴" in msg or "贴一贴" in msg:
        return "贴贴~♡"

    if "抱抱" in msg or "抱一抱" in msg:
        return "好耶~抱住你蹭蹭~"

    if "我只离开了几分钟" in msg:
        return "你们就搞出这种大新闻！这像话吗？！"
