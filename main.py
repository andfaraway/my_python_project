from src.http_request import http_request, api_push

if __name__ == "__main__":
    # api_push.push_alias(['biubiubiu'], 'Server Start！', '🎉🎉🎉')

    api_push.push_all('全新版本更新了！', '🎉🎉🎉')

    # api_push.push_alias(['Ivy'], 'Good Morning！', '记得蒸蛋哦🥚 ')
    # http_request.happy_morning()
    http_request.start()
