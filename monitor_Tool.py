# #-- MonitorNetwork/monitor_1.py--
# #هذ الScript لمراقبة نوافذ المتصفح المفتوحة على النظام وارسال تنبيهات عبر التليجرام عند زيارة مواقع معينة

# import pygetwindow as gw #lمراقبة اي نافدة مفتوحة على النظام
# #pip install pywin3
# import win32con #مكتبة للتعامل مع نوافذ الويندوز
# import win32gui #مكتبة للتعامل مع نوافذ الويندوز
# import time # ,وقت للمراقبة
# import ctypes # select location inside 
# import requests # send and respons to bot in telegram
# # اضافه imports بسيطة لاستخدام UI Automation لقراءة شريط العنوان في Chrome
# from pywinauto import Application
# from pywinauto.findwindows import ElementNotFoundError

# windows= gw.getWindowsWithTitle('Google Chrom') #جلب جميع النوافذ المفتوحة التي تحتوي على هذا العنوان


# #استمرار البرنامج
# while (True):
#     for window in windows:
#         title=window.title.lower() 
#         page_url = None
#         try:
#             # الاتصال بالتطبيق باستخدام مقبض النافذة
#             app = Application(backend="uia").connect(handle=hwnd, timeout=1)
#             win = app.window(handle=hwnd)
#             # محاولة إيجاد أول عنصر تحرير (Edit) والذي غالبًا يحمل الـ URL في Chrome
#             edits = win.descendants(control_type="Edit")
#             if edits:
#                 try:
#                     page_url = edits[0].get_value().strip()
#                     if not page_url:
#                         page_url = None
#                 except Exception:
#                     page_url = None
#         except Exception:
#             page_url = None
#         if not page_url:
#             page_url = f"(no-url-read) title: {title}"
#         # مثال: إضافة page_url إلى المتغير message أو payload
#         massage_url = f" {page_url}"

        
#         print(f"window  Title: {title}")
#         sites=['facebook','youtube','twitter','instagram','Facebook','YouTube','فيسبوك','يوتيوب','ChatGPT']#قائمة المواقع التي اريد مراقبتها
#         for x in sites:
#             if x in title.lower(): #قم بمراقبة الروابط التي يتصفحها المستخدم لان الروابط تكتب بالاحرف الصغيرة
#                 hwnd=window._hWnd # معرف النافذه
#                 title= win32gui.GetWindowText(hwnd) # جلب عنوان النافذة
#                 massage = f"{title}"
#                 title = f"That from :{x}"
                
#                 bot_token = '8220484748:AAExld8jSSsbQ0-90D3d01cvTBJEbdsvCCI'
#                 chat_id = '5739511727'
#                 message = f'Window Title: {title}\nLocation: {massage}'
#                 # ارسال التنبيه عبر التليجرام
#                 url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=security:\n-------\n[-]- tiltle:\n{title}\n[-]- visited:\n{massage}\n [-]- url: {massage_url }"
#                 requests.get(url)
                
#             time.sleep(8) 
            
            
            
                
            
        
        

        
        
        
        
        
        
import time
import os
import requests
import pygetwindow as gw
from dotenv import load_dotenv
from datetime import datetime

# مكتبات التعامل مع النوافذ للحصول على الرابط (إن أمكن)
from pywinauto import Application

# تحميل البيانات السرية من ملف .env
load_dotenv()

class BrowserMonitor:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        self.targets = [
            'facebook', 'youtube', 'twitter', 'instagram', 
            'chatgpt', 'فيسبوك', 'يوتيوب', 'whatsapp'
        ]
        
        # لتخزين النوافذ التي تم التبليغ عنها مسبقاً لمنع الإزعاج
        # الهيكل: { "Window Title": timestamp }
        self.alerted_windows = {} 
        self.cleanup_interval = 60 # تنظيف الذاكرة كل دقيقة

    def send_telegram_alert(self, title, url_info):
        """ارسال التنبيه عبر التليجرام"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_text = (
            f"**Security Alert**\n"
            f"-------------------\n"
            f" Time: {timestamp}\n"
            f" Window: {title}\n"
            f" Detected in: {url_info}\n"
            f"-------------------"
        )
        
        api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        try:
            response = requests.post(api_url, data={'chat_id': self.chat_id, 'text': message_text, 'parse_mode': 'Markdown'})
            if response.status_code == 200:
                print(f"[+] Alert sent for: {title}")
            else:
                print(f"[-] Failed to send alert: {response.text}")
        except Exception as e:
            print(f"[-] Connection Error: {e}")

    def get_browser_url(self, window):
        """
        محاولة متقدمة لجلب الرابط من شريط العنوان.
        ملاحظة: هذه العملية قد تكون غير مستقرة لأن المتصفحات تغير هيكليتها باستمرار.
        """
        try:
            # الحصول على معرف النافذة
            hwnd = window._hWnd
            app = Application(backend="uia").connect(handle=hwnd, timeout=2)
            win = app.window(handle=hwnd)
            
            # البحث عن شريط العنوان (Address Bar)
            # هذه الطريقة تعمل مع Chrome/Edge غالباً
            address_bar = win.descendants(control_type="Edit")
            if address_bar:
                return address_bar[0].get_value()
        except Exception:
            return "URL Hidden/Protected"
        return "Unknown URL"

    def start_monitoring(self):
        print(" Monitor Tool Started... Press Ctrl+C to stop.")
        
        while True:
            try:
                # 1. جلب جميع النوافذ المفتوحة حالياً (داخل اللوب لتحديث القائمة)
                windows = gw.getAllWindows()

                for window in windows:
                    title = window.title.lower()
                    
                    # تخطي النوافذ الفارغة
                    if not title:
                        continue

                    # 2. فحص هل العنوان يحتوي على كلمات محظورة
                    for target in self.targets:
                        if target in title:
                            # التأكد من أننا لم نرسل تنبيهاً لهذه النافذة مؤخراً
                            if title not in self.alerted_windows:
                                print(f"[!] Detected: {title}")
                                
                                # محاولة جلب الرابط
                                url = self.get_browser_url(window)
                                
                                # إرسال التنبيه
                                self.send_telegram_alert(window.title, target.upper())
                                
                                # تسجيل النافذة لمنع التكرار
                                self.alerted_windows[title] = time.time()
                            
                # 3. آلية بسيطة لمسح التنبيهات القديمة لتمكين التنبيه مرة أخرى بعد فترة
                current_time = time.time()
                # نحذف التنبيهات التي مر عليها دقيقتين
                keys_to_delete = [k for k, v in self.alerted_windows.items() if current_time - v > 120]
                for k in keys_to_delete:
                    del self.alerted_windows[k]

                time.sleep(5) # فحص كل 5 ثواني لتخفيف الضغط على المعالج

            except KeyboardInterrupt:
                print("\n Monitoring Stopped.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)

if __name__ == "__main__":
    monitor = BrowserMonitor()
    monitor.start_monitoring()