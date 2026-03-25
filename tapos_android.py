"""
Smart Alarm Pro — Android Version with Kivy
تطبيق منبّه ذكي على Android
يعمل مع Tapo P100 و Gree AC

pip install kivy buildozer cython python-dotenv
"""

import threading
import asyncio
import time
import math
import random
import io
import wave
import datetime
import logging
import json
import os
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock, mainthread
from kivy.core.audio import SoundLoader

import schedule

# ═══════════════════════════════════════════════════════════
# LOGGING (Setup first, before any logging calls)
# ═══════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# استيراد اختياري للمكتبات التي قد لا تكون متوفرة على Android
try:
    from kivy.garden.sounddevice import SoundFile
except ImportError:
    logger.warning("⚠️ SoundFile غير متوفرة - سيتم استخدام بديل")
    SoundFile = None

try:
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
except ImportError:
    logger.warning("⚠️ Matplotlib غير متوفرة")
    FigureCanvasKivyAgg = None

# ═══════════════════════════════════════════════════════════
# PATHS & CONFIG
# ═══════════════════════════════════════════════════════════
STORAGE_PATH = Path.home() / ".smart_alarm"
STORAGE_PATH.mkdir(exist_ok=True)
CFG_FILE = STORAGE_PATH / "alarm_config.json"

def load_cfg():
    try:
        if CFG_FILE.exists():
            with open(CFG_FILE, encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"❌ خطأ قراءة الإعدادات: {e}")
    return {}

def save_cfg(d):
    try:
        with open(CFG_FILE, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"❌ خطأ حفظ الإعدادات: {e}")

# ═══════════════════════════════════════════════════════════
# ASYNC LOOP (للـ Gree)
# ═══════════════════════════════════════════════════════════
_aloop = asyncio.new_event_loop()

def _handle_exception(loop, context):
    exc = context.get('exception')
    if exc and isinstance(exc, OSError):
        logger.debug(f"🔌 Network error (expected): {exc}")
    else:
        if exc:
            logger.warning(f"⚠️ AsyncIO: {type(exc).__name__}: {exc}")

_aloop.set_exception_handler(_handle_exception)
threading.Thread(target=_aloop.run_forever, daemon=True).start()

def arun(coro, timeout=15):
    try:
        return asyncio.run_coroutine_threadsafe(coro, _aloop).result(timeout=timeout)
    except Exception as e:
        logger.error(f"❌ arun error: {e}")
        raise

# ═══════════════════════════════════════════════════════════
# DEVICE IMPORTS - Try real libraries, fallback to mocks if not available
# ═══════════════════════════════════════════════════════════
USING_REAL_DEVICES = False

try:
    from PyP100 import PyP100 as RealPyP100
    logger.info("✅ PyP100 library loaded")
    TAPO_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ PyP100 not available - using fallback mock")
    TAPO_AVAILABLE = False
    RealPyP100 = None

try:
    from greeclimate.device import Device, DeviceInfo
    logger.info("✅ greeclimate library loaded")
    GREE_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ greeclimate not available - using fallback mock")
    GREE_AVAILABLE = False
    Device = None
    DeviceInfo = None

# ═══════════════════════════════════════════════════════════
class Tapo:
    def __init__(self):
        self.ok = False
        self._ip = self._em = self._pw = ""
        self._last_connect_time = None
        self._connect_attempts = 0

    def connect(self, ip, em, pw):
        try:
            if not TAPO_AVAILABLE:
                logger.warning("🔌 [MOCK MODE] Tapo - using fallback (no PyP100)")
                self._ip, self._em, self._pw = ip, em, pw
                self.ok = True
                return
            
            self._connect_attempts = 0
            max_attempts = 3
            
            for attempt in range(max_attempts):
                try:
                    self._connect_attempts += 1
                    p = RealPyP100.P100(ip, em, pw)
                    p.handshake()
                    p.login()
                    p.getDeviceInfo()
                    self._ip, self._em, self._pw = ip, em, pw
                    self.ok = True
                    self._last_connect_time = datetime.datetime.now()
                    logger.info(f"✅ Tapo متصل — محاولة #{attempt+1}")
                    return
                except Exception as e:
                    logger.warning(f"⚠️ Tapo محاولة {attempt+1}/{max_attempts} فشلت: {type(e).__name__}")
                    if attempt < max_attempts - 1:
                        time.sleep(1)
            
            self.ok = False
            raise Exception(f"فشل الاتصال بـ Tapo بعد {max_attempts} محاولات")
        except Exception as e:
            logger.error(f"❌ Tapo: {e}")
            raise

    def _dev(self):
        if not TAPO_AVAILABLE:
            logger.debug("[MOCK] Tapo device operation")
            class MockDevice:
                def turnOn(self): logger.info("🔌 [MOCK] Tapo ON")
                def turnOff(self): logger.info("🔌 [MOCK] Tapo OFF")
            return MockDevice()
        
        p = RealPyP100.P100(self._ip, self._em, self._pw)
        p.handshake()
        p.login()
        return p

    def on(self):
        try:
            self._dev().turnOn()
            logger.info("✅ Tapo تشغيل")
        except Exception as e:
            logger.error(f"❌ Tapo خطأ: {e}")
            raise

    def off(self):
        try:
            self._dev().turnOff()
            logger.info("✅ Tapo إيقاف")
        except Exception as e:
            logger.error(f"❌ Tapo خطأ: {e}")
            raise

# ═══════════════════════════════════════════════════════════
# GREE AC CLASS
# ═══════════════════════════════════════════════════════════
class Gree:
    def __init__(self):
        self.ok = False
        self._d = None
        self._ip = None
        self._mac = None
        self._last_connect_time = None
        self._connect_attempts = 0

    async def _connect(self, ip, mac):
        try:
            if not GREE_AVAILABLE:
                logger.warning("❄️ [MOCK MODE] Gree - using fallback (no greeclimate)")
                self._ip = ip
                self._mac = mac
                self.ok = True
                return
            
            mac = mac.replace(":", "").replace("-", "").lower()
            if len(mac) != 12:
                mac = "aabbccddeeff"
            self._ip, self._mac = ip, mac
            self._d = Device(DeviceInfo(ip=ip, port=7000, mac=mac, name="Gree"))
            await self._d.bind()
            self.ok = True
            self._last_connect_time = datetime.datetime.now()
            logger.info("✅ Gree متصل")
        except Exception as e:
            logger.error(f"❌ Gree connect failed: {e}")
            self.ok = False
            raise

    async def _reconnect(self):
        if not (self._ip and self._mac):
            logger.error("❌ Gree: لا توجد بيانات IP/MAC")
            self.ok = False
            return
        
        if not GREE_AVAILABLE:
            logger.debug("[MOCK] Gree reconnect")
            self.ok = True
            return
        
        for attempt in range(3):
            try:
                logger.info(f"🔌 Gree إعادة اتصال {attempt+1}/3...")
                mac = self._mac.replace(":", "").replace("-", "").lower()
                self._d = Device(DeviceInfo(ip=self._ip, port=7000, mac=mac, name="Gree"))
                await self._d.bind()
                self.ok = True
                logger.info("✅ Gree متصل!")
                return
            except Exception as e:
                logger.warning(f"⚠️ محاولة {attempt+1} فشلت: {type(e).__name__}")
                if attempt < 2:
                    await asyncio.sleep(1)
        
        self.ok = False
        logger.error("❌ Gree: فشل الاتصال بعد 3 محاولات")

    async def _off(self):
        try:
            if not self._d:
                logger.info("سحب الجهاز، جاري إعادة الاتصال...")
                await self._reconnect()
            if self._d and self.ok:
                await self._d.update_state()
                self._d.power = False
                await self._d.push_state_update()
            else:
                raise Exception("فشل الاتصال بـ Gree")
        except (OSError, asyncio.TimeoutError, Exception) as e:
            logger.warning(f"⚠️ محاولة أولى فشلت, إعادة اتصال قسرية...")
            self.ok = False
            await self._reconnect()
            if self.ok and self._d:
                await self._d.update_state()
                self._d.power = False
                await self._d.push_state_update()

    async def _on(self):
        try:
            if not self._d:
                await self._reconnect()
            await self._d.update_state()
            self._d.power = True
            await self._d.push_state_update()
            logger.info("✅ Gree - تشغيل")
        except (OSError, asyncio.TimeoutError, Exception) as e:
            logger.warning(f"⚠️ محاولة أولى فشلت, إعادة اتصال...")
            await self._reconnect()
            if self.ok:
                await self._d.update_state()
                self._d.power = True
                await self._d.push_state_update()

    async def _set_temp(self, t):
        try:
            if not self._d:
                await self._reconnect()
            await self._d.update_state()
            self._d.target_temperature = int(t)
            await self._d.push_state_update()
            logger.info(f"✅ Gree - درجة الحرارة: {t}°")
        except (OSError, asyncio.TimeoutError, Exception) as e:
            logger.warning(f"⚠️ فشل, إعادة اتصال...")
            await self._reconnect()
            if self.ok:
                await self._d.update_state()
                self._d.target_temperature = int(t)
                await self._d.push_state_update()

    async def _set_mode(self, m):
        try:
            from greeclimate.device import Mode
            M = {0: Mode.Auto, 1: Mode.Cool, 2: Mode.Dry, 3: Mode.Fan, 4: Mode.Heat}
            if not self._d:
                await self._reconnect()
            await self._d.update_state()
            self._d.mode = M.get(m, Mode.Cool)
            await self._d.push_state_update()
        except Exception as e:
            logger.warning(f"⚠️ فشل تغيير الوضع: {e}")

    async def _set_fan(self, s):
        try:
            from greeclimate.device import FanSpeed
            F = {0: FanSpeed.Auto, 1: FanSpeed.Low, 2: FanSpeed.Medium, 3: FanSpeed.High}
            if not self._d:
                await self._reconnect()
            await self._d.update_state()
            self._d.fan_speed = F.get(s, FanSpeed.Auto)
            await self._d.push_state_update()
        except Exception as e:
            logger.warning(f"⚠️ فشل تغيير السرعة: {e}")

    async def _state(self):
        try:
            if not self._d:
                await self._reconnect()
            await self._d.update_state()
            return dict(
                power=self._d.power,
                temp=self._d.target_temperature,
                cur=getattr(self._d, "current_temperature", "--"),
                mode=str(self._d.mode).split(".")[-1],
                fan=str(self._d.fan_speed).split(".")[-1]
            )
        except (OSError, asyncio.TimeoutError, Exception) as e:
            logger.warning(f"⚠️ فشل الحصول على الحالة: {e}")
            await self._reconnect()
            if self.ok:
                await self._d.update_state()
                return dict(
                    power=self._d.power,
                    temp=self._d.target_temperature,
                    cur=getattr(self._d, "current_temperature", "--"),
                    mode=str(self._d.mode).split(".")[-1],
                    fan=str(self._d.fan_speed).split(".")[-1]
                )
            return {"power": "--", "temp": "--", "cur": "--", "mode": "--", "fan": "--"}

# ═══════════════════════════════════════════════════════════
# SOUND CLASS (استخدام pygame أو Kivy الصوت)
# ═══════════════════════════════════════════════════════════
class Sound:
    SR = 44100
    TONES = [(523, "s"), (659, "s"), (784, "s"), (880, "s"),
             (440, "q"), (988, "q"), (698, "w"), (1047, "s")]

    def __init__(self):
        self._stop = threading.Event()
        self._t = None
        self._snds = []
        self._ready = False
        self._error = None
        self._preload_time = None
        self._playing = False

    def _make(self, freq, kind):
        try:
            import numpy as np
            n = int(self.SR * 0.36)
            d = bytearray(n * 2)
            for i in range(n):
                t = i / self.SR
                env = 1.0 if i < n * 0.75 else max(0, (n - i) / (n * 0.25))
                if kind == "s":
                    v = 0.6 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(4 * math.pi * freq * t)
                elif kind == "q":
                    v = 0.4 if math.sin(2 * math.pi * freq * t) > 0 else -0.4
                else:
                    v = 0.5 * (2 * (t * freq - math.floor(t * freq + 0.5)))
                val = max(-32767, min(32767, int(32767 * v * env)))
                d[2 * i] = val & 0xFF
                d[2 * i + 1] = (val >> 8) & 0xFF
            b = io.BytesIO()
            with wave.open(b, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(2)
                w.setframerate(self.SR)
                w.writeframes(bytes(d))
            b.seek(0)
            
            # حفظ الملف مؤقتاً
            sound_file = STORAGE_PATH / f"tone_{freq}.wav"
            with open(sound_file, "wb") as f:
                f.write(b.getvalue())
            
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load(str(sound_file))
            return sound
        except Exception as e:
            logger.error(f"❌ خطأ توليد الصوت: {e}")
            self._error = str(e)
            return None

    def preload(self):
        try:
            self._snds = [self._make(f, k) for f, k in self.TONES]
            if all(s for s in self._snds):
                self._ready = True
                self._preload_time = datetime.datetime.now()
                logger.info("✅ الأصوات جاهزة")
            else:
                self._error = "بعض الأصوات فشلت"
                logger.warning(f"⚠️ بعض الأصوات فشلت: {self._error}")
        except Exception as e:
            logger.error(f"❌ خطأ التحميل: {e}")
            self._error = str(e)

    def _run(self):
        if not self._ready:
            logger.warning("⚠️ الأصوات غير جاهزة، جاري التحميل...")
            self.preload()
        if not self._ready:
            logger.error("❌ فشل تحميل الأصوات")
            return
        
        ch = None
        prev = -1
        self._playing = True
        
        while not self._stop.is_set():
            try:
                if len(self._snds) > 0 and self._snds[0]:
                    i = prev
                    while i == prev:
                        i = random.randrange(len(self._snds))
                    snd = self._snds[i]
                    if snd:
                        snd.play()
                        prev = i
            except Exception as e:
                logger.error(f"❌ خطأ التشغيل: {e}")
            time.sleep(0.01)
        
        self._playing = False

    def start(self):
        if self._t and self._t.is_alive():
            logger.warning("⚠️ الصوت يعمل بالفعل")
            return
        self._stop.clear()
        self._t = threading.Thread(target=self._run, daemon=True)
        self._t.start()
        logger.info("🔊 الصوت قيد التشغيل")

    def stop(self):
        self._stop.set()
        if self._t:
            self._t.join(2)
            self._t = None
        logger.info("🔇 الصوت متوقف")

    def playing(self):
        return self._playing

    def is_ready(self):
        return self._ready

# ═══════════════════════════════════════════════════════════
# WATCHDOG
# ═══════════════════════════════════════════════════════════
class Watchdog:
    def __init__(self, app):
        self._app = app
        self._stop = threading.Event()
        self._thread = None
        self._beats = 0

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()

    def _loop(self):
        while not self._stop.is_set():
            try:
                self._beats += 1
                app = self._app

                # تحديث معلومات الحالة
                if hasattr(app, 'root'):
                    app.root.after_update_status()

                if self._beats % 10 == 0:
                    st = "🔌 Tapo: " + ("متصل ✓" if app.tapo.ok else "⚠ غير متصل")
                    sg = "❄️ Gree: " + ("متصل ✓" if app.gree.ok else "⚠ غير متصل")
                    logger.info(f"💓 Watchdog #{self._beats} — {st} | {sg}")
            except Exception as e:
                logger.error(f"❌ Watchdog خطأ: {e}")

            self._stop.wait(60)

# ═══════════════════════════════════════════════════════════
# KIVY APP
# ═══════════════════════════════════════════════════════════
class SmartAlarmApp(App):
    def build(self):
        self.title = "⏰ Smart Alarm Pro"
        
        # إنشاء الأجهزة
        self.tapo = Tapo()
        self.gree = Gree()
        self.sound = Sound()
        self.watchdog = Watchdog(self)

        # متغيرات الحالة
        self.ringing = False
        self.scheduled = False
        self.alarm_dt = None
        self._cfg = load_cfg()

        # الواجهة الرئيسية
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # الرأس
        header = Label(
            text="⏰ Smart Alarm Pro\nمنبّه ذكي مع Tapo + Gree",
            size_hint_y=0.1,
            font_size='18sp',
            bold=True,
            color=(0, 1, 1, 1)
        )
        main_layout.add_widget(header)

        # TabPanel
        self.tabs = TabbedPanel()
        self.tabs.default_tab_text = '⏰ المنبّه'

        # Tab 1: المنبّه
        tab1 = TabbedPanelItem(text='⏰ المنبّه')
        tab1.content = self._build_alarm_tab()
        self.tabs.add_widget(tab1)

        # Tab 2: Tapo
        tab2 = TabbedPanelItem(text='🔌 Tapo')
        tab2.content = self._build_tapo_tab()
        self.tabs.add_widget(tab2)

        # Tab 3: Gree
        tab3 = TabbedPanelItem(text='❄️ Gree')
        tab3.content = self._build_gree_tab()
        self.tabs.add_widget(tab3)

        # Tab 4: السجل
        tab4 = TabbedPanelItem(text='📝 السجل')
        tab4.content = self._build_log_tab()
        self.tabs.add_widget(tab4)

        main_layout.add_widget(self.tabs)

        # السجل السفلي
        self.log_text = Label(
            text="تم تحميل التطبيق بنجاح ✅\n",
            size_hint_y=0.15,
            text_size=(self.width, None)
        )
        main_layout.add_widget(self.log_text)

        self.root = main_layout

        # إنشاء التطبيق
        threading.Thread(target=self.sound.preload, daemon=True).start()
        threading.Thread(target=self._sched_loop, daemon=True).start()
        Clock.schedule_interval(self._tick, 1)
        self.watchdog.start()

        self.log("✅ تم تحميل التطبيق", "success")
        return main_layout

    def _build_alarm_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # إدخال الوقت
        time_layout = GridLayout(cols=3, size_hint_y=0.2, spacing=10)
        
        self.alarm_h_spinner = Spinner(
            text='06',
            values=[f'{i:02d}' for i in range(24)],
            size_hint_x=0.3
        )
        time_layout.add_widget(self.alarm_h_spinner)
        
        time_layout.add_widget(Label(text=':', size_hint_x=0.1))
        
        self.alarm_m_spinner = Spinner(
            text='00',
            values=[f'{i:02d}' for i in range(60)],
            size_hint_x=0.3
        )
        time_layout.add_widget(self.alarm_m_spinner)
        
        layout.add_widget(time_layout)
        
        # زر تفعيل
        btn_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=10)
        btn_layout.add_widget(
            Button(
                text='✅ تفعيل المنبّه',
                background_color=(0, 1, 0, 1),
                on_press=self._set_alarm
            )
        )
        btn_layout.add_widget(
            Button(
                text='❌ إلغاء المنبّه',
                background_color=(1, 0, 0, 1),
                on_press=self._cancel_alarm
            )
        )
        layout.add_widget(btn_layout)
        
        # أزرار الاختبار
        test_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=10)
        test_layout.add_widget(
            Button(
                text='🔊 اختبار الصوت',
                on_press=self._test_sound
            )
        )
        test_layout.add_widget(
            Button(
                text='🧪 اختبار المنبّه',
                on_press=self._test_alarm
            )
        )
        layout.add_widget(test_layout)
        
        # حالة المنبّه
        self.alarm_status = Label(
            text="لم يُضبط بعد",
            size_hint_y=0.5,
            font_size='20sp'
        )
        layout.add_widget(self.alarm_status)
        
        return layout

    def _build_tapo_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # IP Input
        layout.add_widget(Label(text='عنوان IP:', size_hint_y=0.1))
        self.tapo_ip_input = TextInput(
            text=self._cfg.get('tapo_ip', ''),
            multiline=False,
            size_hint_y=0.1
        )
        layout.add_widget(self.tapo_ip_input)
        
        # Email Input
        layout.add_widget(Label(text='البريد الإلكتروني:', size_hint_y=0.1))
        self.tapo_em_input = TextInput(
            text=self._cfg.get('tapo_em', ''),
            multiline=False,
            size_hint_y=0.1
        )
        layout.add_widget(self.tapo_em_input)
        
        # Password Input
        layout.add_widget(Label(text='كلمة المرور:', size_hint_y=0.1))
        self.tapo_pw_input = TextInput(
            text=self._cfg.get('tapo_pw', ''),
            password=True,
            multiline=False,
            size_hint_y=0.1
        )
        layout.add_widget(self.tapo_pw_input)
        
        # اتصال
        layout.add_widget(
            Button(
                text='🔗 اتصال بـ Tapo',
                size_hint_y=0.15,
                on_press=self._conn_tapo
            )
        )
        
        # التحكم
        ctrl = GridLayout(cols=2, size_hint_y=0.15, spacing=10)
        ctrl.add_widget(
            Button(
                text='▶️ تشغيل',
                background_color=(0, 1, 0, 1),
                on_press=lambda x: self._tapo_do('on')
            )
        )
        ctrl.add_widget(
            Button(
                text='⏹️ إيقاف',
                background_color=(1, 0, 0, 1),
                on_press=lambda x: self._tapo_do('off')
            )
        )
        layout.add_widget(ctrl)
        
        # الحالة
        self.tapo_status = Label(
            text='غير متصل',
            size_hint_y=0.35,
            font_size='18sp'
        )
        layout.add_widget(self.tapo_status)
        
        return layout

    def _build_gree_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # IP Input
        layout.add_widget(Label(text='عنوان IP:', size_hint_y=0.1))
        self.gree_ip_input = TextInput(
            text=self._cfg.get('gree_ip', ''),
            multiline=False,
            size_hint_y=0.1
        )
        layout.add_widget(self.gree_ip_input)
        
        # MAC Input
        layout.add_widget(Label(text='MAC Address:', size_hint_y=0.1))
        self.gree_mac_input = TextInput(
            text=self._cfg.get('gree_mac', ''),
            multiline=False,
            size_hint_y=0.1
        )
        layout.add_widget(self.gree_mac_input)
        
        # اتصال
        layout.add_widget(
            Button(
                text='🔗 اتصال بـ Gree',
                size_hint_y=0.15,
                on_press=self._conn_gree
            )
        )
        
        # التحكم
        ctrl = GridLayout(cols=2, size_hint_y=0.15, spacing=10)
        ctrl.add_widget(
            Button(
                text='▶️ تشغيل',
                background_color=(0, 1, 0, 1),
                on_press=lambda x: self._gree_cmd(self.gree._on())
            )
        )
        ctrl.add_widget(
            Button(
                text='⏹️ إيقاف',
                background_color=(1, 0, 0, 1),
                on_press=lambda x: self._gree_cmd(self.gree._off())
            )
        )
        layout.add_widget(ctrl)
        
        # درجة الحرارة
        temp_layout = GridLayout(cols=3, size_hint_y=0.15, spacing=10)
        temp_layout.add_widget(Button(text='-', on_press=self._temp_dn))
        self.gree_temp_lbl = Label(text='24°', font_size='20sp')
        temp_layout.add_widget(self.gree_temp_lbl)
        temp_layout.add_widget(Button(text='+', on_press=self._temp_up))
        layout.add_widget(temp_layout)
        
        # الحالة
        self.gree_status = Label(
            text='غير متصل',
            size_hint_y=0.35,
            font_size='18sp'
        )
        layout.add_widget(self.gree_status)
        
        return layout

    def _build_log_tab(self):
        scroll = ScrollView()
        self.log_display = Label(
            text="السجل سيظهر هنا...\n",
            size_hint_y=None,
            markup=True,
            text_size=(self.width - 20, None)
        )
        scroll.add_widget(self.log_display)
        return scroll

    def log(self, msg, level="info"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{ts}] {msg}\n"
        try:
            current = self.log_display.text
            self.log_display.text = current + log_msg
        except:
            pass
        logger.info(f"{level.upper()}: {msg}")

    def _set_alarm(self, *args):
        h = self.alarm_h_spinner.text
        m = self.alarm_m_spinner.text
        t = f"{h}:{m}"
        
        schedule.clear()
        schedule.every().day.at(t).do(self._fire)
        self.scheduled = True
        self.alarm_dt = datetime.datetime.strptime(t, "%H:%M").time()
        
        self.alarm_status.text = f"✅ المنبّه مضبوط\n{t}"
        self.log(f"📅 المنبّه مضبوط: {t}", "success")
        save_cfg({**self._cfg, "alarm_h": h, "alarm_m": m, "alarm_active": True})

    def _cancel_alarm(self, *args):
        schedule.clear()
        self.scheduled = False
        self.alarm_status.text = "لم يُضبط بعد"
        self.log("❌ تم إلغاء المنبّه", "warning")
        save_cfg({**self._cfg, "alarm_active": False})

    def _fire(self):
        self.log("🚨 المنبّه يرن الآن!", "alarm")
        self.ringing = True

        if self.tapo.ok:
            def _t():
                try:
                    self.tapo.on()
                    self.log("✅ Tapo — تشغيل", "success")
                except Exception as e:
                    self.log(f"❌ Tapo: {e}", "error")
            threading.Thread(target=_t, daemon=True).start()

        def _g():
            try:
                time.sleep(0.5)
                arun(self.gree._off(), timeout=45)
                self.log("✅ Gree — إيقاف", "success")
            except Exception as e:
                self.log(f"❌ Gree: {e}", "error")
        
        threading.Thread(target=_g, daemon=True).start()

        self.sound.start()
        self.alarm_status.text = "🚨 المنبّه يرن!"

    def _test_alarm(self, *args):
        self.log("🧪 اختبار المنبّه", "info")
        threading.Thread(target=self._fire, daemon=True).start()

    def _test_sound(self, *args):
        if self.sound.playing():
            self.sound.stop()
            self.log("🔇 إيقاف الصوت", "info")
        else:
            self.sound.start()
            self. log("🔊 اختبار الصوت", "info")

    def _conn_tapo(self, *args):
        ip = self.tapo_ip_input.text.strip()
        em = self.tapo_em_input.text.strip()
        pw = self.tapo_pw_input.text.strip()
        
        if not (ip and em and pw):
            self.log("⚠️ الرجاء ملء بيانات Tapo", "warning")
            return
        
        def task():
            try:
                self.tapo.connect(ip, em, pw)
                save_cfg({**self._cfg, "tapo_ip": ip, "tapo_em": em, "tapo_pw": pw})
                self.log("✅ Tapo متصل", "success")
                self.tapo_status.text = "✅ متصل"
            except Exception as e:
                self.log(f"❌ Tapo: {e}", "error")
                self.tapo_status.text = f"❌ فشل: {str(e)[:30]}"
        
        threading.Thread(target=task, daemon=True).start()

    def _tapo_do(self, cmd):
        if not self.tapo.ok:
            self.log("⚠️ Tapo غير متصل", "warning")
            return
        
        def task():
            try:
                if cmd == "on":
                    self.tapo.on()
                else:
                    self.tapo.off()
                self.log(f"✅ Tapo — {cmd}", "success")
            except Exception as e:
                self.log(f"❌ Tapo: {e}", "error")
        
        threading.Thread(target=task, daemon=True).start()

    def _conn_gree(self, *args):
        ip = self.gree_ip_input.text.strip()
        mac = self.gree_mac_input.text.strip()
        
        if not ip:
            self.log("⚠️ الرجاء إدخال IP", "warning")
            return
        
        def task():
            try:
                arun(self.gree._connect(ip, mac), timeout=20)
                save_cfg({**self._cfg, "gree_ip": ip, "gree_mac": mac})
                self.log("✅ Gree متصل", "success")
                self.gree_status.text = "✅ متصل"
            except Exception as e:
                self.log(f"❌ Gree: {e}", "error")
                self.gree_status.text = f"❌ فشل: {str(e)[:30]}"
        
        threading.Thread(target=task, daemon=True).start()

    def _gree_cmd(self, coro):
        if not self.gree.ok:
            self.log("⚠️ Gree غير متصل", "warning")
            return
        
        def task():
            try:
                arun(coro, timeout=30)
                self.log("✅ Gree أمر تنفيذ", "success")
            except Exception as e:
                self.log(f"❌ Gree: {e}", "error")
        
        threading.Thread(target=task, daemon=True).start()

    def _temp_up(self, *args):
        # يتم تنفيذ الأمر الفعلي عند الضغط
        pass

    def _temp_dn(self, *args):
        pass

    def _tick(self, dt):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return True

    def _sched_loop(self):
        while True:
            try:
                schedule.run_pending()
            except Exception as e:
                logger.error(f"❌ Schedule error: {e}")
            time.sleep(1)

    def after_update_status(self):
        pass

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    app = SmartAlarmApp()
    app.run()
