from flask import Flask, request
import requests
import json

app = Flask(__name__)

FACEBOOK_PAGE_ID = '102400995610569'
VERIFY_TOKEN = "ashbcvasbifurvabsjvbasbviabvjasbkcj"
PAGE_ACCESS_TOKEN = "EAAZAbInuj2bUBOzMoiUnu9IQJXXOaK3Fg2HmureZBiMazpDraFN8AwZB7F7ZAcrxkUnZAzBsRxycqBqKQn3IBrARZBUikl9JszFYI31DmrMUVIoZC1ZB8UYnUdQgMcUVKNg3ETTELZCZCFAJU3HZA6PxURDzFpz3tZBSAYv4FNASm7WsmXTGCGlIdF9XHCROiPzjYmSrvvQZBYZAZCG1CngJrc5"

def callSendAPI(senderPsid, response):
    payload = {
        'recipient': {'id': senderPsid},
        'message': response,
        'messaging_type': 'RESPONSE',
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v19.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)

def handleMessage(senderPsid, receivedMessage):
    if 'text' in receivedMessage:
        response = {"text": 'You just sent: {}'.format(receivedMessage['text'])}
    else:
        response = {"text": 'This chatbot only accepts text messages'}
    callSendAPI(senderPsid, response)

@app.route("/")
def hello_world():
    return "Hello from Flask!"

@app.route('/webhook', methods=["GET", "POST"])
def fbwebhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print('WEBHOOK VERIFIED')
            return challenge, 200
        else:
            return 'ERROR', 403

    elif request.method == 'POST':
        body = json.loads(request.data.decode('utf-8'))
        if body.get('object') == 'page':
            for entry in body['entry']:
                webhookEvent = entry.get('messaging', [])[0]
                senderPsid = webhookEvent.get('sender', {}).get('id')
                
                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])

            return 'MSG_RECEIVED', 200
        else:
            return 'ERROR', 404

if __name__ == "__main__":
    app.run(debug=True)
