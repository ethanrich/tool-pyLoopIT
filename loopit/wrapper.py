# how to import Client from the loop it codebase?


'''
python ipc/tests/rcc.py --msg
                          
python __init__.py --msg '{"tft":{"0":{"ip_address": null}}}'                                  
python __init__.py --msg '{"fes": ("O": {"new parameters": "available"}}}'    
python __init__.py --msg '{"fes" : {"O" {"current mode": {"biphasic": {"amplitude A" :null}}}}}'
python __init__.py --msg '["fes" : ("O": ("state mosi": "stimulate once"]]]'
python __init__.py --msg '("fes": {"O": ("state mosi": "stop"})]'

order of the JSON message nesting is:
module name: "fes"
module identifier: "0"
mode name: "current_mode"
parameter name: "inter_pulse_interval"
parameter value: 4000000000

e.g. set the inter-pulse interval to 4 seconds
'{"fes": {"0": {"current_mode": {"inter_pulse_interval": "4000000000"}}}}'



'''

from loopit.rcc import Client

class LoopIT(Client):
### Further simplified methods for use in research setting

    def format_message_json(msg=r'{"ping":"pong"}'):
        # take a message from the user and format to JSON structure expected by the Loop IT
        pass

    def query(self):
        self.request()

    def set_parameters(self, msg=r'{"fes": {"0": {"current_mode": {"inter_pulse_interval": "4000000000"}}}}'):
        self.request(msg=msg)

    def start_stimulation():
        pass

    def stop_stimulation():
        pass