import json
import os
import urllib.request

# Lambdaの環境変数からSlackトークンを取得します
SLACK_TOKEN = os.environ['SLACK_TOKEN']

def lambda_handler(event, context):
    # Slackからのリクエストボディを解析
    body = json.loads(event['body'])

    # Slackのイベントサブスクリプションの最初の確認用
    if 'challenge' in body:
        return {
            'statusCode': 200,
            'body': body['challenge']
        }

    # メンションされた場合の処理
    if 'event' in body and body['event']['type'] == 'app_mention':
        user_id = body['event']['user']
        text = body['event']['text']
        channel_id = body['event']['channel']
        send_message(channel_id, text)

    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }

def send_message(channel_id, text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_TOKEN}"
    }
    data = {
        "channel": channel_id,
        "text": text
    }
    req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
    with urllib.request.urlopen(req) as res:
        res_body = res.read()
        print(res_body)
