from loopit import LoopIT
import time

if __name__ == "__main__":

    # initialize the client
    loopit = LoopIT(host='127.0.0.1', port=1219)
    loopit.set_mode(module_name = "fes",
                    module_index = "0",
                    mode_name = "current_mode")
    
    # query the Loop IT to test connection
    loopit.query()
    # get device configuration to view valid parameters and values
    loopit.get_device_config()
    # set some parameters
    loopit.inter_pulse_interval = "20000000" # 50 hz == 20000000 nanosecond period
    loopit.amplitude_A = "1000000" # one milliampere of current
    loopit.amplitude_A = "-1000000"
    loopit.pulsewidth_A = "200000" # 200 microsecond pulse width
    loopit.pulsewidth_B = "200000"
    # start stimulation
    loopit.start_stimulation()
    # wait a few seconds
    time.sleep(3)
    # stop stimulation
    loopit.stop_stimulation()
