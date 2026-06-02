from flask import Flask, request, abort
import requests
import os

app = Flask(__name__)

# المعلومات تاعك — راح نحطوها كمتغيرات سرية فالمنصة لاحقاً
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
SECRET_KEY = os.environ.get("SECRET_KEY")


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=data)


@app.route("/", methods=["GET"])
def home():
    return "Bot is working ✅", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}

    # نتأكدو من المفتاح السري باش غير TradingView تاعك يقدر يبعث
    if data.get("secret") != SECRET_KEY:
        abort(403)

    signal = data.get("signal", "")
    symbol = data.get("symbol", "")
    price = data.get("price", "")

    message = (
        f"📢 <b>إشارة جديدة</b>\n\n"
        f"الزوج: <b>{symbol}</b>\n"
        f"النوع: <b>{signal}</b>\n"
        f"السعر: <b>{price}</b>"
    )

    send_to_telegram(message)
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)