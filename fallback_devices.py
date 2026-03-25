"""
Minimal device control - for testing without PyP100/greeclimate
استخدام بديل بسيط للتحكم بالأجهزة - للاختبار بدون المكتبات الأصلية
"""

import logging
import datetime
import time

logger = logging.getLogger(__name__)

class Tapo:
    """Mock Tapo P100 controller for testing"""
    def __init__(self):
        self.ok = False
        self._ip = ""
        self.power_state = False
        
    def connect(self, ip, email, password):
        logger.info(f"📡 [MOCK] Tapo connecting to {ip}")
        self._ip = ip
        self.ok = True
        logger.info("✅ [MOCK] Tapo connected (mock mode)")
        return True
    
    def on(self):
        if self.ok:
            self.power_state = True
            logger.info("🔌 [MOCK] Tapo turned ON")
        else:
            logger.error("❌ [MOCK] Tapo not connected")
    
    def off(self):
        if self.ok:
            self.power_state = False
            logger.info("🔌 [MOCK] Tapo turned OFF")
        else:
            logger.error("❌ [MOCK] Tapo not connected")
    
    def toggle(self):
        if self.ok:
            self.power_state = not self.power_state
            state = "ON" if self.power_state else "OFF"
            logger.info(f"🔌 [MOCK] Tapo toggled to {state}")


class Gree:
    """Mock Gree AC controller for testing"""
    def __init__(self):
        self.ok = False
        self._ip = ""
        self.temperature = 24
        self.power_state = False
        self.mode = "cool"
        
    async def _connect_async(self, ip, mac):
        logger.info(f"❄️ [MOCK] Gree connecting to {ip}")
        self._ip = ip
        self.ok = True
        logger.info("✅ [MOCK] Gree connected (mock mode)")
        return True
    
    async def _on_async(self):
        if self.ok:
            self.power_state = True
            logger.info("❄️ [MOCK] Gree turned ON")
        else:
            logger.error("❌ [MOCK] Gree not connected")
    
    async def _off_async(self):
        if self.ok:
            self.power_state = False
            logger.info("❄️ [MOCK] Gree turned OFF")
        else:
            logger.error("❌ [MOCK] Gree not connected")
    
    async def _set_temp_async(self, temp):
        if self.ok:
            self.temperature = temp
            logger.info(f"❄️ [MOCK] Gree temperature set to {temp}°C")
        else:
            logger.error("❌ [MOCK] Gree not connected")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test Tapo
    tapo = Tapo()
    tapo.connect("192.168.1.100", "test@example.com", "password")
    tapo.on()
    tapo.off()
    
    # Test Gree
    gree = Gree()
    import asyncio
    asyncio.run(gree._connect_async("192.168.1.101", "aa:bb:cc:dd:ee:ff"))
    asyncio.run(gree._on_async())
    asyncio.run(gree._set_temp_async(20))
    asyncio.run(gree._off_async())
