from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta

class PoolController:
    def __init__(self, hass, update_callback, scan_interval, handler):
        self._hass = hass
        self._update_callback = update_callback
        self._scan_interval = scan_interval
        self._remove_listener = None
        self._handler = handler
        self.modbus_ok = False
        self._modbus_fail_count = 0
        self._modbus_fail_threshold = 5

    @property
    def scan_interval(self):
        return self._scan_interval

    @property
    def handler(self):
        return self._handler

    async def start(self):
        self._start_polling()

    def _start_polling(self):
        if self._remove_listener:
            self._remove_listener()
        self._remove_listener = async_track_time_interval(
            self._hass, self._update_callback, timedelta(seconds=self._scan_interval)
        )

    async def update_interval(self, new_interval):
        self._scan_interval = new_interval
        self._start_polling()

    def notify_modbus_success(self):
        self._modbus_fail_count = 0
        self.modbus_ok = True

    def notify_modbus_failure(self):
        self._modbus_fail_count += 1
        if self._modbus_fail_count >= self._modbus_fail_threshold:
            self.modbus_ok = False
