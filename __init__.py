from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.typing import T_State
import time
import httpx
import re
import os

youth_study_asst_upload = on_command("大学习上传", permission=GROUP, priority=3)

@youth_study_asst_upload.handle()
async def hw_dept_test_handle(bot: Bot, event: Event, state: T_State):
    global files, ocr, user_real_name, member_name, response
    path = os.getcwd()
    uid = event.get_user_id()
    msg = Message(MessageSegment.at(uid))
    # 提取url
    url = str(event.get_message())
    event_id = event.get_session_id()
    pattern_event = re.compile('group_.+_')
    group_id_dist = pattern_event.findall(event_id)
    group_id = group_id_dist[0][6:-1]
    try:
        pattern = re.compile('file=.+.image')
        result = pattern.findall(url)
        ocr_img_id = result[0][5:]
    except Exception as e:
        print(e)
        msg.append('指令错误，请在消息内包含图片')
        await youth_study_asst_upload.finish(msg)
    member_id = event.get_user_id()
    try:
        member_name = await bot.call_api("get_group_member_info", group_id=group_id, user_id=member_id)
    except Exception as e:
        print(e)
        msg.append('获取成员信息错误')
        await youth_study_asst_upload.finish(msg)
    match = re.search(r'https(.*)]', str(url))
    try:
        url = match.group(0)[:-1]
    except Exception as e:
        print(e)
        msg.append('错误: 未检测到图片')
        await youth_study_asst_upload.finish(msg)
    # 下载图片并重命名
    headers = {
        'Host': 'gchat.qpic.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38'
    }
    try:
        response = httpx.get(url=url, headers=headers)
    except Exception as e:
        print(e)
    imgfile = path + '/' + 'target-' + str(int(time.time())) + '.jpg'

    try:
        ocr = await bot.call_api("ocr_image", image=str(ocr_img_id).lower())
    except Exception as e:
        print(e)
        msg.append('OCR发生错误! 可能为网络问题, 或者所上传文件无文字')
        await youth_study_asst_upload.finish(msg)
    isbigstudy = 1
    match = re.search(r'青年大学习', str(ocr))
    if (match is None) or (str(match.group(0)) != '青年大学习'):
        isbigstudy = 0
        msg.append('检测到图片不是青年大学习截图, 请检查所上传图片')
        await youth_study_asst_upload.finish(msg)
#    match = re.findall('第.+季.+第.+期)', str(ocr))
#    print('!!!' +  str(match))
    ocr_data = ocr['texts']
    season_index = 0
    for x in range(len(ocr_data)):
        if len(re.findall('第.+季.+第.+期',ocr_data[x]['text'])) != 0:
            user_real_name = ocr_data[x+1]['text']
            season_index = x
            break
    season = ocr_data[season_index]['text']
    msg.append(f'\r\n检测到{user_real_name}的{season}的截图, ')

    open(imgfile, 'wb').write(response.content)
    if isbigstudy != 1:
        os.remove(imgfile)
    if isbigstudy == 1:
        season = '青年大学习' + season
        name = member_name['card']
        try:
            files = await bot.call_api("get_group_root_files", group_id=group_id)
        except Exception as e:
            print(e)
            msg.append('获取群文件信息失败')
            await youth_study_asst_upload.finish(msg)
        group_folders = files['folders']
        create_floder_flag = True
        upload_folder_id = ''
        for x in range(len(group_folders)):
            if group_folders[x]['folder_name'] == season:
                create_floder_flag = False
                upload_folder_id = group_folders[x]['folder_id']
        if create_floder_flag:
            try:
                await bot.call_api("create_group_file_folder", group_id=group_id, name=season)
            except Exception as e:
                print(e)
                msg.append('创建群文件夹失败')
                await youth_study_asst_upload.finish(msg)
            try:
                files = await bot.call_api("get_group_root_files", group_id=group_id)
            except Exception as e:
                print(e)
                msg.append('获取群文件信息失败')
                await youth_study_asst_upload.finish(msg)
            group_folders = files['folders']
            for x in range(len(group_folders)):
                if group_folders[x]['folder_name'] == season:
                    upload_folder_id = group_folders[x]['folder_id']
        upload_img_name = name + '.jpg'
        if not os.path.exists(upload_img_name):
            os.rename(imgfile, upload_img_name)
        if upload_folder_id != '':
            try:
                await bot.call_api("upload_group_file", group_id=group_id, file=path + '/' + upload_img_name, name=upload_img_name, folder=upload_folder_id)
            except Exception as e:
                print(e)
                msg.append('大学习截图上传失败')
                await youth_study_asst_upload.finish(msg)
            os.remove(upload_img_name)
        msg.append('大学习截图上传成功')
        await youth_study_asst_upload.finish(msg)


youth_study_asst_index = on_command("大学习查询", permission=GROUP, priority=3)

@youth_study_asst_index.handle()
async def youth_study_asst_index_handle(bot: Bot, event: Event, state: T_State):
    uid = event.get_user_id()
    msg = Message(MessageSegment.at(uid))
    msg.append('因为我不是团支书，暂时不想开发催交截图的功能')
    await youth_study_asst_index.finish(msg)


youth_study_asst_help = on_command("help", permission=GROUP, priority=3)

@youth_study_asst_help.handle()
async def youth_study_asst_help_handle(bot: Bot, event: Event, state: T_State):
    uid = event.get_user_id()
    msg = Message(MessageSegment.at(uid))
    msg.append('我才不会告诉你我能干什么')
    await youth_study_asst_help.finish(msg)