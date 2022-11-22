'''
order of the JSON message nesting is:
{"module_name": {"idx": {"mode_name": {"parameter_name": "parameter_value:<string, int, boolean>"}}}}

-> set the inter-pulse interval to 4 seconds
'{"fes": {"0": {"current_mode": {"inter_pulse_interval": "4000000000"}}}}'

-> trigger one stimulation
'{"fes": {"0": {"current_mode": {"state mosi": "stimulate_once"}}}}'

-> stop stimulation
'{"fes": {"0": {"current_mode": {"state mosi": "stop"}}}}'

'''

from loopit.rcc import Client

class LoopIT(Client):
### Further simplified methods for use in research setting
    
    def set_mode(self, module_name, module_index, mode_name):
        self.module_name, self.module_index, self.mode_name = module_name, module_index, mode_name
        
    def build_message(self, parameter, value):
        # build the message content here
        msg = '{' + self.module_name + ': {' + self.module_index + ': {' + self.mode_name +  \
        ': {' + parameter + ': ' + value + '}}}}'
        return msg

    def query(self):
        # test the connection
        self.request()

    def send_message(self, parameter, value):
        msg = self.build_message(parameter, value)
        # send the message
        self.request(msg=msg)
        
    def start_stimulation(self):
        msg = self.build_message("state_mosi", "stimulate_continuous")
        # send the message
        self.request(msg=msg)
    
    def stop_stimulation(self):
        msg = self.build_message("state_mosi", "stop")
        # send the message
        self.request(msg=msg)
    
    
