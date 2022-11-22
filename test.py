from loopit import LoopIT
import time

if __name__ == "__main__":

    # initialize the client
    loopit = LoopIT(host='127.0.0.1', port=1219)
    loopit.set_mode(module_name = "fes",
                    module_index = "0",
                    mode_name = "current_mode")
    
    # query the Loop IT
    loopit.query()
    # set some parameters
    loopit.send_message(parameter = "inter_pulse_interval", value = "20000000") # 50 hz == 20000000 nanosecond period
    # loopit.send_message(parameter = "amplitude_A", value = "1000000") # one milliampere of current
    # loopit.send_message(parameter = "amplitude_A", value = "-1000000")
    # loopit.send_message(parameter = "pulsewidth_A", value = "200000") # 200 microsecond pulse width
    # loopit.send_message(parameter = "pulsewidth_B", value = "200000")
    # start stimulation
    # loopit.start_stimulation()
    # wait a few seconds
    # time.sleep(3)
    # stop stimulation
    # loopit.stop_stimulation()
