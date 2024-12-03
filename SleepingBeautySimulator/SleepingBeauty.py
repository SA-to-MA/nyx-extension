import math

class SleepingBeauty:
    def __init__(self, window_closed=True, magnet_operational=True, circuit=False, alarm_enabled=False, alarm_disabled=True, ringing=False, deeply_asleep=True, almost_awake=False,
                 awake=False, charge=0.0, resistance=1.0, ring_time=0.0, voltage=False):
        # Initial conditions based on provided initial state
        self.window_closed = window_closed
        self.magnet_operational = magnet_operational
        self.circuit = circuit
        self.alarm_enabled = alarm_enabled
        self.alarm_disabled = alarm_disabled
        self.ringing = ringing
        self.deeply_asleep = deeply_asleep
        self.almost_awake = almost_awake
        self.awake = awake
        self.charge = charge
        self.resistance = resistance
        self.ring_time = ring_time
        self.voltage = voltage
        self.kissed = False # initial state of kissed is false because no action was taken yet
        self.total_time = 0

    '''Actions'''
    def open_window(self):
        if self.window_closed and self.magnet_operational:
            self.window_closed = False
            self.magnet_operational = False
            print("Action: Window opened, fresh air enters.")

    def close_window(self):
        if not self.window_closed and not self.magnet_operational:
            self.window_closed = True
            self.magnet_operational = True
            print("Action: Window closed.")

    def kiss(self):
        if self.almost_awake:
            self.awake = True
            self.almost_awake = False
            self.kissed = True
            print("Action: Kiss. Sleeping Beauty is now fully awake.")

    '''Events'''
    ''' If event occured - returns true. otherwise, returns false'''
    def make_circuit(self):
        if not self.magnet_operational and not self.circuit:
            self.circuit = True
            print("Event: Circuit completed.")

    def break_circuit(self):
        if self.magnet_operational and self.circuit:
            self.circuit = False
            self.charge = 0
            print("Event: Circuit broken, charge reset.")

    def trigger_alarm(self):
        if self.circuit and self.alarm_disabled and self.voltage:
            self.alarm_enabled = True
            self.alarm_disabled = False
            self.ringing = True
            print("Event: Alarm triggered, ringing begins.")

    def voltage_available(self):
        if self.charge >= 5 and not self.voltage:
            self.voltage = True
            print("Event: Voltage available.")

    def rouse_princess(self):
        if self.ringing and self.ring_time >= 0.001 and self.deeply_asleep:
            self.deeply_asleep = False
            self.almost_awake = True
            print("Event: Rouse Princess. Sleeping Beauty is almost awake.")

    def disable_alarm(self):
        if not self.circuit and self.alarm_enabled and self.ringing:
            self.alarm_enabled = False
            self.ringing = False
            self.alarm_disabled = True
            self.ring_time = 0
            print("Event: Alarm disabled.")

    '''Process'''
    ''' If process occured - returns true. otherwise, returns false'''
    def ring(self, time_step=1):
        if self.ringing:
            self.ring_time += time_step
            print(f"Process: Ringing... Ring time: {self.ring_time:.3f}")
            self.rouse_princess()

    def charge_capacitor(self, time_step=1):
        if self.circuit and not self.voltage:
            self.charge += time_step * (1 / self.resistance)
            print(f"Process: Charging... Charge level: {self.charge:.2f}")
            self.voltage_available()
