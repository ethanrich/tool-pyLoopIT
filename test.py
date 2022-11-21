from loopit import LoopIT

if __name__ == "__main__":

    # initialize the client
    loopit = LoopIT(host='127.0.0.1', port=1219)
    loopit.set_mode(module_name = "fes",
                    module_index= "0",
                    mode_name = "current_mode")
    
    # query the Loop IT
    loopit.query()
    # set some parameters
    loopit.set_parameters(parameter = "inter_pulse_interval", value = "4000000000")
    # start stimulation
    loopit.set_parameters(parameter = "state_mosi", value = "stimulate_once")
    # stop stimulation
    loopit.set_parameters(parameter = "state_mosi", value = "stop")
