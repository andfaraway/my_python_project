import socket

from src.http_request import http_request, api_push

if __name__ == "__main__":
    # api_push.push_alias(['biubiubiu'], 'Server Start！', '🎉🎉🎉')
    # api_push.push_all('版本更新了！', '🎉🎉🎉')
    http_request.steam_egg()
    http_request.start()



