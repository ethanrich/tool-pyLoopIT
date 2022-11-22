<p align="center">
  <img src="https://github.com/ethanrich/tool-pyLoopIT/blob/main/neuroConn.png?raw=true" alt="logo"/>
</p>

# tool-pyLoopIT

This is a Python wrapper that simplifies interfacing with a LoopIT device from within your Python experiment code. You can update parameters, start stimulation, and stop stimulation with simple class method calls.

# Installation
Git clone this repository and then pip install. 
```
git clone https://github.com/ethanrich/tool-pyLoopIT.git
```

# Prerequisites
Running this program assumes that you have a LoopIT device connected or you have mocked one for development.

# Usage
After you have connected your LoopIT device or booted the development servers, please run test.py.

```
python test.py
```

In this file, you will see how certain values must be given to connect to the LoopIT. Then, you can send any command you want as a "parameter" and "value". All parameters and values must be strings.

# Parameters

Please see your LoopIT device guide for a list of parameters and values. 

# Updates

* TODO:
    * Type and value checking for LoopIT class methods
    * Helpful error messages
    * Testing on actual LoopIT platform
