from pymodbus.client.sync import ModbusTcpClient

class ModbusHandler:
    def __init__(self, host="192.168.1.100", port=502, unit_id=1):
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client = ModbusTcpClient(host=self.host, port=self.port)

    def read_register(self, address, count=1):
        if not self.client.connect():
            return None
        result = self.client.read_holding_registers(address, count, unit=self.unit_id)
        self.client.close()
        if not result.isError():
            return result.registers
        return None

    def write_register(self, address, value):
        if not self.client.connect():
            return False
        result = self.client.write_register(address, value, unit=self.unit_id)
        self.client.close()
        return not result.isError()
