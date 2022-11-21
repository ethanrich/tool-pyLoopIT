from loopit import LoopIT

if __name__ == "__main__":

    # initialize the client
    loopit = LoopIT(host='127.0.0.1', port=1219)
    
    # query the Loop IT
    loopit.query()
    # set some parameters
    loopit.set_parameters()
    # start stimulation
    
    # stop stimulation
