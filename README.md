# system-monitor

python-based command-line system monitoring application.

monitors real-time hardware performance, system resources, and network activity.

## FEATURES
- cpu usage, frequency, individual core utilization
- ram usage and availability
- nvidia gpu utilization, temperature, and memory
- disk usage and available storage
- network activity, latency, and packet loss
- system info and uptime

## REQUIREMENTS
- windows os
- python 3
- nvidia gpu (for gpu monitoring)

## LIMITATIONS
- gpu monitoring currently supports nvidia hardware only
- amd and intel gpu monitoring are not implemented
- application currently uses a command-line interface

## FUTURE DEVELOPMENT (potential)
- graphical user interface
- multi-vendor gpu support
- standalone executable

## INSTALLATION
    prerequisites: python 3 and git installed

enter terminal commands in as follows...

1. clone repository:
    ```bash
    git clone https://github.com/sovva-ob/system-monitor 

    cd system-monitor
    ```
2. install dependancies:
    ```bash
    python -m pip install -r requirements.txt
    ```
3. run system-monitor:
    ```bash
    python main.py
    ```