# 安装依赖 pip3 install requests html5lib bs4 schedule
import os
import requests
import json
import random
from bs4 import BeautifulSoup

# 从测试号信息获取
appID = os.environ.get("APP_ID")
appSecret = os.environ.get("APP_SECRET")
# 收信人ID即 用户列表中的微信号
openId = os.environ.get("OPEN_ID")
# 天气预报模板ID
weather_template_id = os.environ.get("TEMPLATE_ID")

def get_weather(my_city):
    urls = ["http://www.weather.com.cn/textFC/hb.shtml",
            "http://www.weather.com.cn/textFC/db.shtml",
            "http://www.weather.com.cn/textFC/hd.shtml",
            "http://www.weather.com.cn/textFC/hz.shtml",
            "http://www.weather.com.cn/textFC/hn.shtml",
            "http://www.weather.com.cn/textFC/xb.shtml",
            "http://www.weather.com.cn/textFC/xn.shtml"
            ]
    for url in urls:
        resp = requests.get(url)
        text = resp.content.decode("utf-8")
        soup = BeautifulSoup(text, 'html5lib')
        div_conMidtab = soup.find("div", class_="conMidtab")
        tables = div_conMidtab.find_all("table")
        for table in tables:
            trs = table.find_all("tr")[2:]
            for index, tr in enumerate(trs):
                tds = tr.find_all("td")
                # 这里倒着数，因为每个省会的td结构跟其他不一样
                city_td = tds[-8]
                this_city = list(city_td.stripped_strings)[0]
                if this_city == my_city:

                    high_temp_td = tds[-5]
                    low_temp_td = tds[-2]
                    weather_type_day_td = tds[-7]
                    weather_type_night_td = tds[-4]
                    wind_td_day = tds[-6]
                    wind_td_day_night = tds[-3]

                    high_temp = list(high_temp_td.stripped_strings)[0]
                    low_temp = list(low_temp_td.stripped_strings)[0]
                    weather_typ_day = list(weather_type_day_td.stripped_strings)[0]
                    weather_type_night = list(weather_type_night_td.stripped_strings)[0]

                    wind_day = list(wind_td_day.stripped_strings)[0] + list(wind_td_day.stripped_strings)[1]
                    wind_night = list(wind_td_day_night.stripped_strings)[0] + list(wind_td_day_night.stripped_strings)[1]

                    # 如果没有白天的数据就使用夜间的
                    temp = f"{low_temp}——{high_temp}摄氏度" if high_temp != "-" else f"{low_temp}摄氏度"
                    weather_typ = weather_typ_day if weather_typ_day != "-" else weather_type_night
                    wind = f"{wind_day}" if wind_day != "--" else f"{wind_night}"
                    return this_city, temp, weather_typ, wind


def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token

sentences = [
    "坚持下去，你的梦想就在前方。",
    "只要不放弃，一切皆有可能。",
    "考研是你对自己未来的投资，加油！",
    "每一步的努力，都会让你离成功更近。",
    "梦想并不遥远，迈开步子去追寻。",
    "今天的努力，是为了明天的更好。",
    "别让放弃成为你唯一的选择。",
    "你的坚持，终将创造奇迹。",
    "勇敢追梦，你值得更好的未来。",
    "不怕慢，只怕停，坚持就是胜利。",
    "考研路上，每一步都是积累。",
    "现在的努力，都是为了未来的自信。",
    "你越努力，机会就越多。",
    "不负自己，不负梦想，加油！",
    "成功的路上并不拥挤，因为坚持的人不多。",
    "路虽远，行则将至。",
    "没有到不了的明天，只有放弃的今天。",
    "勇敢去追，梦想从未离你而去。",
    "考研是一场马拉松，坚持就是胜利。",
    "每一天都是新的起点，继续前行。",
    "不积跬步，无以至千里。",
    "为了梦想，拼尽全力。",
    "现在流的汗，终将浇灌出明天的花。",
    "未来掌握在自己手中，加油！",
    "成功不是偶然，而是每天的努力。",
    "别忘了，你在为梦想而奋斗。",
    "每一次的努力，都是对未来的投资。",
    "你能做到的，远超你的想象。",
    "考研路上，你不是一个人。",
    "把握现在，成就未来。",
    "坚持就是胜利，努力才有收获。",
    "现在的苦，将来会变成甜。",
    "没有谁的梦想能轻易实现，加油！",
    "只要你不放弃，奇迹终会发生。",
    "不要让今天的努力，成为明天的遗憾。",
    "每一次的坚持，都是向成功迈进。",
    "放下焦虑，坚定前行。",
    "勇敢面对挑战，你一定行！",
    "考研路上的每一步，都是积累。",
    "不懈的努力，终会迎来胜利的曙光。",
    "不惧风雨，勇往直前。",
    "只要心中有梦，路就不会迷失。",
    "为了梦想，再苦再累也值得。",
    "你现在的努力，是未来的勋章。",
    "勇敢追梦，不负韶华。",
    "你所经历的一切，都是为了更好的明天。",
    "坚持到底，梦想终将实现。",
    "每一次的努力，都是为了未来的光辉。",
    "未来的你，会感谢现在拼搏的自己。",
    "不忘初心，方得始终。",
    "成功总是青睐那些不放弃的人。",
    "梦想不会自动实现，只有靠自己去争取。",
    "你现在的努力，会在未来成为你的资本。",
    "别让任何借口阻挡你前进的脚步。",
    "今天的坚持，是为了明天的灿烂。",
    "无论多难，勇敢去面对。",
    "一分耕耘，一分收获。",
    "每一次的努力，都是对自己的肯定。",
    "现在流的汗水，将会成为未来的荣耀。",
    "别让懒惰毁了你的梦想。",
    "勇敢面对每一天，相信自己能做到。",
    "为了明天的辉煌，今天要拼尽全力。",
    "每一次努力，都是对未来的一次投资。",
    "现在的你，正在为梦想铺路。",
    "未来的成就，来自于今天的努力。",
    "不怕失败，只怕放弃。",
    "只要坚持，梦想就会实现。",
    "每一天的努力，都是为明天积累力量。",
    "无论多难，别忘了你的初心。",
    "勇敢去追，成功在前方等着你。",
    "今天的付出，都会成为未来的礼物。",
    "你有无限的可能性，加油！",
    "每一次的坚持，都会让你离梦想更近。",
    "不惧风雨，勇敢前行。",
    "现在的每一分努力，都会在未来倍增。",
    "成功源于每一天的努力积累。",
    "无论多难，别让放弃成为选项。",
    "勇敢去面对每一个挑战，你可以的。",
    "每一次的坚持，都是对未来的承诺。",
    "只要心中有梦，未来就不会迷失。",
    "今天的每一步，都是为了更好的明天。",
    "梦想需要付出，行动才会有收获。",
    "勇敢去追，你的未来由你掌握。",
    "坚持到最后，你会发现梦想就在眼前。",
    "每一个努力的今天，都是成功的起点。",
    "别让懒惰阻挡你追梦的脚步。",
    "每一次的进步，都是向成功迈进。",
    "不怕辛苦，只怕不努力。",
    "未来的成就，源于今天的努力。",
    "只要坚持，梦想终会实现。",
    "别让任何借口阻挡你前进的步伐。",
    "每一次的拼搏，都会成为未来的财富。",
    "勇敢追梦，别让懒惰拖住脚步。",
    "无论多难，别忘了你的梦想。",
    "每一天的努力，都是为了更好的未来。",
    "勇敢去追，每一步都是新的起点。",
    "现在的你，正在为未来打下基础。",
    "梦想不会自动实现，需要努力去追求。",
    "勇敢面对每一个挑战，相信自己。",
    "坚持不懈，成功就在不远处。"
]

def get_daily_love():
    # 每日一句
  # 随机选择一个语句
  sentence = random.choice(sentences)
  daily_love = sentence
  return daily_love




def send_weather(access_token, weather):
    # touser 就是 openID
    # template_id 就是模板ID
    # url 就是点击模板跳转的url
    # data就按这种格式写，time和text就是之前{{time.DATA}}中的那个time，value就是你要替换DATA的值

    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    body = {
        "touser": openId.strip(),
        "template_id": weather_template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "date": {
                "value": today_str
            },
            "region": {
                "value": weather[0]
            },
            "weather": {
                "value": weather[2]
            },
            "temp": {
                "value": weather[1]
            },
            "wind_dir": {
                "value": weather[3]
            },
            "today_note": {
                "value": get_daily_love()
            }
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    print(requests.post(url, json.dumps(body)).text)



def weather_report(this_city):
    # 1.获取access_token
    access_token = get_access_token()
    # 2. 获取天气
    weather = get_weather(this_city)
    print(f"天气信息： {weather}")
    # 3. 发送消息
    send_weather(access_token, weather)



if __name__ == '__main__':
    weather_report("东港")
