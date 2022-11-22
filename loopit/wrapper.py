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

valid_parameters = ["amplitude_A",
                    "amplitude_B",
                    "pulsewidth_A",
                    "pulsewidth_B",
                    "inter_pulse_interval",
                    "inter_burst_interval",
                    "pulses_per_burst"
                    ]

class LoopIT(Client):
### Further simplified methods for use in research setting
    
    def set_mode(self, module_name, module_index, mode_name):
        self.module_name, self.module_index, self.mode_name = module_name, module_index, mode_name
        
    def build_message(self, parameter, value):
        # build the message content here
        msg = '{' + self.module_name + ': {' + self.module_index + ': {' + self.mode_name +  \
        ': {' + parameter + ': ' + value + '}}}}'
        return msg
    
    def check_parameter(self, parameter):
        if parameter in valid_parameters:
            pass
        else:
            raise Exception("Please use only valid parameters: " + ", ".join(valid_parameters))
        
    def check_response(self, response):
        if None in response.values():
            print("Warning: LoopIT returned null for an invalid parameter. Check parameters and values, or make sure your device is connected and turned on.")

    def query(self):
        # test the connection
        self.request()

    def send_message(self, parameter, value):
        self.check_parameter(parameter)
        msg = self.build_message(parameter, value)
        # send the message
        response = self.request(msg=msg)
        self.check_response(response)
        
    def start_stimulation(self):
        msg = self.build_message("state_mosi", "stimulate_continuous")
        # send the message
        self.request(msg=msg)
    
    def stop_stimulation(self):
        msg = self.build_message("state_mosi", "stop")
        # send the message
        self.request(msg=msg)
    
    
