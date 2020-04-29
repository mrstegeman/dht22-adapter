import threading
from gateway_addon import Device,Adapter,Property,Database,Event
import time


_POLL_INTERVAL = 5


class DHT22Adapter(Adapter):
    """ Adapter for a DHT22 Sensor connected to Raspberry Pi GPIO"""

    def __init__(self, verbose=False):

        """

        Initialize the object.



        verbose -- whether or not to enable verbose logging

        """

        self.name = self.__class__.__name__

        Adapter.__init__(self,

                         'dht22-adapter',

                         'dht22-adapter',

                         verbose=verbose)
        database = Database('dht22-adapter')

        if not database.open():

            return


        config = database.load_config()

        database.close()

        if not config:

            return

        for pinConfig in config['DHT22']:

            device = DHT22Device(self, pinConfig['pin'], pinConfig)
            self.handle_device_added(device)


    

class DHT22Device(Device):
    """ One DHT22 Sensor """
    def __init__(self, adapter, _pin, config):
        Device.__init__(self, adapter, _pin)
        self.pin = _pin
        self.i = 0
        
        self.properties['temp'] = DHT22Property( self,
                                            'temperature',
                                            {
                                                'title': 'Temperature',
                                                'type': 'number',
                                                'unit': '°C'
                                            },
                                            self.pin,
                                            )        

        t = threading.Thread(target=self.poll)
        t.daemon = True
        t.start()

    def poll(self):
        # Polling Thread
        while True:
            time.sleep(_POLL_INTERVAL)
            self.properties['temp'].update(self.i+1)


class DHT22Property(Property):
    def __init__(self, device, name, description, pin, value):
        Property.__init__(self, device, name, description)
        self.pin = pin
        self.set_cached_value(value)

    def update(self, value):
        print(time.ctime(),'Value of', self.name, 'sensor on pin', self.pin, 'has changed from', self.value,'to', value, flush=True)
        self.set_cached_value(value)
        self.device.notify_property_changed(self)


 
        
        


