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
import json


class LoopIT(Client):
### Further simplified methods for use in research setting
    module_attributes = [] # initialize the module attributes as a property to check in __getattr__

    def set_mode(self, module_name, module_index, mode_name):
        self.module_name, self.module_index, self.mode_name = module_name, module_index, mode_name

    def query(self):
        # test the connection
        self.request()

    def get_device_config(self):
        # query the LoopIT for module parameters for the user to later update
        response = self.request(msg='{"?": null}')
        self.get_module_parameters(response)
        
    def get_module_parameters(self, response):
        # grab module parameters
        if self.module_name == 'fes' and 'fes' in response.keys():
            module_parameters = response['mosi']['fes']['current_mode']['encoding']['biphasic']['fields']
            del module_parameters['reserved_2'] # not relevant to user

            # format
            formatted_parameters = {}
            for k in module_parameters.keys():
                formatted_parameters[k] =  {'valid': module_parameters[k]['encoding']['valid'][0],
                                            'unit': module_parameters[k]['encoding']['unit']}
            
            # debugging
            # formatted_parameters = {'amplitude_A': {'valid': [-30000, 30000], 'unit': '0.0000010 A'},
            #                                'amplitude_B': {'valid': [-30000, 30000], 'unit': '0.0000010 A'},
            #                                'pulsewidth_A': {'valid': [0, 4294967296], 'unit': '1.0E-9 s'},
            #                                'pulsewidth_B': {'valid': [0, 4294967296], 'unit': '1.0E-9 s'},
            #                                'inter_pulse_interval': {'valid': [0, 4294967296], 'unit': '1.0E-9 s'},
            #                                'inter_burst_interval': {'valid': [0, 4294967296], 'unit': '0.0000010 s'},
            #                                'pulses_per_burst': {'valid': [0, 65536], 'unit': '1.0 count'},
            #                                'burst_repeats': {'valid': [0, 65536], 'unit': '1.0 count'}}
            
            # show a pretty message
            print('###########')
            print('FES module found. Valid parameters and values are: ')
            for p, v in formatted_parameters.items():
                print(p + ":")
                print("    valid value: " + str(v['valid']) + " in units: " + v['unit'])
            print('###########')
            
            self.module_attributes = list(formatted_parameters.keys()) # get a list of the parameters to check in __setattr__

            self.add_parameter_attributes(formatted_parameters)
        else:
            # tell user that the fes module was not found in the response
            print('No modules found. Device not connected or device servers are mocked')
            
    def add_parameter_attributes(self, formatted_parameters):
        # set the parameters as class attributes
        for k in formatted_parameters:
            setattr(self, k, "0") # initialize the values of each parameter as 0 for now #NOTE might only work for FES module
            
    def __setattr__(self, name, value):
        # override __setsttr__ to also trigger updating LoopIT
        self.__dict__[name] = value
        if name in self.module_attributes:
            self.send_message(name, value)
                    
    def build_message(self, parameter, value):
        # build the message content here
        msg = '{' + self.module_name + ': {' + self.module_index + ': {' + self.mode_name +  \
        ': {' + parameter + ': ' + value + '}}}}'
        return msg
        
    def check_response(self, response):
        # check for null values in LoopIT response
        if None in response.values():
            print("Warning: LoopIT returned null due to an invalid parameter.")

    def send_message(self, parameter, value):
        # update parameters and their values
        msg = self.build_message(parameter, value)
        # send the message
        response = self.request(msg=msg)
        self.check_response(response)
        
    def start_stimulation(self):
        # trigger start of stimulation with the current parameters
        msg = self.build_message("state_mosi", "stimulate_continuous")
        # send the message
        self.request(msg=msg)
    
    def stop_stimulation(self):
        # stop stimulation 
        msg = self.build_message("state_mosi", "stop")
        # send the message
        self.request(msg=msg)
    
    
