from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_crypto_keywords():
    try:
        response = requests.get(
            "https://cryptopanic.com/api/v1/posts/",
            params={
                "auth_token": "YOUR_CRYPTOPANIC_KEY",
                "filter": "hot"
            }
        )
        posts = response.json()['results']
        keywords = [post['title'].split()[0] for post in posts[:10]]
        return list(set(keywords))
    except:
        return ["Bitcoin", "Ethereum", "NFT", "DeFi"]

@app.route('/api/lark-webhook', methods=['POST'])
def handle_webhook():
    event = request.json
    if event.get('message', {}).get('content', '').startswith('/crypto'):
        keywords = get_crypto_keywords()
        return jsonify({
            "msg_type": "text",
            "content": f"🔑 Keywords: {', '.join(keywords[:15])}"
        })
    return jsonify({})

if __name__ == '__main__':
    app.run()
