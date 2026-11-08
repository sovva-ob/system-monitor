import platform
import os
import psutil
import subprocess
import pynvml
import time
from datetime import datetime


#// SYSTEM INFO-------------------------------------------------------------
def get_system_info():
    system = platform.system()
    processor = platform.processor()
    cores = os.cpu_count()

    return system, processor, cores

def get_boot_date():
    return datetime.fromtimestamp(psutil.boot_time())


#// CPU INFO----------------------------------------------------------------------------
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_cpu_frequency():
    return psutil.cpu_freq()

def get_core_usage():
    return psutil.cpu_percent(percpu=True)


#// MEMORY INFO------------------------------------------
def get_memory_usage():
    return psutil.virtual_memory()


#// GPU INFO------------------------------------------------------------
def initialize_gpu():
    pynvml.nvmlInit()
    return pynvml.nvmlDeviceGetHandleByIndex(0)

def get_gpu_usage(gpu):
    return pynvml.nvmlDeviceGetUtilizationRates(gpu)

def get_gpu_temperature(gpu):
    return pynvml.nvmlDeviceGetTemperature(
        gpu,
        pynvml.NVML_TEMPERATURE_GPU
    )

def get_gpu_memory(gpu):
    return pynvml.nvmlDeviceGetMemoryInfo(gpu)


#// DISK INFO---------------------------------------------------------------------
def get_disk_usage():
    return psutil.disk_usage("C:\\")


#// NETWORK INFO-------------------------------------------------------------------------------------------------------------
previous_network = None
previous_time = None

total_pings = 0
failed_pings = 0

def initialize_network():
    global previous_network, previous_time

    previous_network = get_network_usage()
    previous_time = time.monotonic()

def get_network_speeds():
    global previous_network, previous_time

    current_network = get_network_usage()
    current_time = time.monotonic()

    elapsed_time = current_time - previous_time

    download_difference = current_network.bytes_recv - previous_network.bytes_recv
    upload_difference = current_network.bytes_sent - previous_network.bytes_sent

    download_speed = calc_net_speed(download_difference, elapsed_time)
    upload_speed = calc_net_speed(upload_difference, elapsed_time)

    previous_network = current_network
    previous_time = current_time

    return download_speed, upload_speed

def get_network_usage():
    return psutil.net_io_counters()

def get_network_interfaces():
    return psutil.net_if_stats()

def get_connection_status():
    interfaces = get_network_interfaces()
    return any(interface.isup for interface in interfaces.values())

def get_ping_result():
    return subprocess.run(
        ["ping", "-n", "1", "1.1.1.1"],
        capture_output=True,
        text=True
    )

def get_ping_latency(ping_output):
    if "time=" in ping_output:
        return ping_output.split("time=")[1].split("ms")[0]
    else:
        return "unavailable"

def get_packet_loss(result):
    global total_pings, failed_pings

    total_pings += 1

    if result.returncode != 0:
        failed_pings += 1

    return (failed_pings / total_pings) * 100, total_pings


#// UTILITIES--------------------------------------------------------------------------
def bytes_to_gib(value):
    return value / (1024 ** 3)

def calc_net_speed(byte_difference, elapsed_time):
    return byte_difference * 8 / 1_000_000 / elapsed_time


#// SYSTEM SNAPSHOT--------------------------------------
def get_status(percentage):
    if percentage > 90:
        return "CRITICAL"
    elif percentage > 75:
        return "ELEVATED"
    else:
        return "normal"

def get_system_snapshot(gpu):
    cpu = get_cpu_usage()
    frequency = get_cpu_frequency()
    cores = get_core_usage()
    memory = get_memory_usage()
    gpu_usage = get_gpu_usage(gpu)
    gpu_temp = get_gpu_temperature(gpu)
    gpu_memory = get_gpu_memory(gpu)
    disk = get_disk_usage()
    network = get_network_usage()
    download_speed, upload_speed = get_network_speeds()
    connection_status = get_connection_status()
    result = get_ping_result()
    ping_time = get_ping_latency(result.stdout)
    packet_loss, total_pings = get_packet_loss(result)

    return {
        "cpu": {
            "usage": cpu,
            "frequency": frequency.current / 1000,
            "cores": cores,
            "status": get_status(cpu)
        },
        "ram": {
            "usage": memory.percent,
            "total": bytes_to_gib(memory.total),
            "available": bytes_to_gib(memory.available),
            "used": bytes_to_gib(memory.used)
        },
        "gpu": {
            "usage": gpu_usage.gpu,
            "temperature": gpu_temp,
            "vram_total": bytes_to_gib(gpu_memory.total),
            "vram_available": bytes_to_gib(gpu_memory.free),
            "vram_used": bytes_to_gib(gpu_memory.used)
        },
        "disk": {
            "usage": disk.percent,
            "total": bytes_to_gib(disk.total),
            "free": bytes_to_gib(disk.free),
            "used": bytes_to_gib(disk.used)
        },
        "network": {
            "downloaded": bytes_to_gib(network.bytes_recv),
            "uploaded": bytes_to_gib(network.bytes_sent),
            "download_speed": download_speed,
            "upload_speed": upload_speed,
            "latency": ping_time,
            "packet_loss": packet_loss,
            "total_pings": total_pings,
            "connection_status": connection_status,
            "internet_status": result.returncode == 0
        }
    }