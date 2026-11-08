import os

from terminal import create_bar
from monitor import get_status
from monitor import get_system_info, get_boot_date
from monitor import initialize_network
from monitor import initialize_gpu

from monitor import get_system_snapshot

from datetime import datetime

system, processor, cores = get_system_info()

boot_date = get_boot_date()

initialize_network()

gpu = initialize_gpu()

while True:
    snapshot = get_system_snapshot(gpu)
    uptime = datetime.now() - boot_date
    
    cpu_usage = snapshot["cpu"]["usage"]
    core_usage = snapshot["cpu"]["cores"]
    cpu_frequency = snapshot["cpu"]["frequency"]
    
    ram_usage = snapshot["ram"]["usage"]
    total_ram = snapshot["ram"]["total"]
    available_ram = snapshot["ram"]["available"]
    used_ram = snapshot["ram"]["used"]
    
    gpu_usage = snapshot["gpu"]["usage"]
    gpu_temp = snapshot["gpu"]["temperature"]
    total_vram = snapshot["gpu"]["vram_total"]

    used_vram = snapshot["gpu"]["vram_used"]
    free_vram = snapshot["gpu"]["vram_available"]

    disk_usage = snapshot["disk"]["usage"]
    total_disk = snapshot["disk"]["total"]
    free_disk = snapshot["disk"]["free"]
    used_disk = snapshot["disk"]["used"]

    downloaded = snapshot["network"]["downloaded"]
    uploaded = snapshot["network"]["uploaded"]
    download_speed = snapshot["network"]["download_speed"]
    upload_speed = snapshot["network"]["upload_speed"]

    connection_status = snapshot["network"]["connection_status"]

    ping_time = snapshot["network"]["latency"]
    packet_loss = snapshot["network"]["packet_loss"]
    total_pings = snapshot["network"]["total_pings"]

    internet_status = snapshot["network"]["internet_status"]

    os.system("cls")
    print("=" * 40)
    print("          sovva // system monitor")
    print("-" * 40)

    print(f"operating system: {system}")
    print(f"processor: {processor}")
    print(f"cores: {cores}")

    print("=" * 40)


    #uptime
    print(f"system uptime: {str(uptime).split(".")[0]}")

    print("-" * 40)
    
    
    #cpu
    print(f"cpu frequency: {cpu_frequency:.2f} GHz")
    print(f"cpu usage: {cpu_usage:.1f}%")
    
    cpu_bar = create_bar(cpu_usage)
    print(f"[{cpu_bar}]")

    for index in range(10):
        print(f"core {index + 1:02d}: {core_usage[index]:5.1f}%    core {index + 11:02d}: {core_usage[index + 10]:5.1f}%")
    
    cpu_status = get_status(cpu_usage)
    print(f"cpu status: {cpu_status}")

    print("-" * 40)
    
    #memory
    print(f"ram usage: {ram_usage:.1f}%")

    ram_bar = create_bar(ram_usage)
    print(f"[{ram_bar}]")
    
    print(f"total ram: {total_ram:.1f} GiB")
    print(f"available ram: {available_ram:.1f} GiB")
    print(f"used ram: {used_ram:.1f} GiB")

    memory_status = get_status(ram_usage)
    print(f"memory status: {memory_status}")

    print("-" * 40)

    #gpu
    print(f"gpu usage: {gpu_usage}%")
    
    gpu_bar = create_bar(gpu_usage)
    print(f"[{gpu_bar}]")
    
    print(f"gpu temperature: {gpu_temp}°C")
    print(f"total vram: {total_vram:.1f} GiB")
    print(f"available vram: {free_vram:.1f} GiB")
    print(f"used vram: {used_vram:.1f} GiB")

    gpu_status = get_status(gpu_usage)
    print(f"gpu status: {gpu_status}")

    print("-" * 40)

    #disk
    print(f"disk usage: {disk_usage:.1f}%")

    disk_bar = create_bar(disk_usage)
    print(f"[{disk_bar}]")

    print(f"total disk: {total_disk:.1f} GiB")
    print(f"available disk: {free_disk:.1f} GiB")
    print(f"used disk: {used_disk:.1f} GiB")
    
    disk_status = get_status(disk_usage)
    print(f"disk usage status: {disk_status}")

    print("-" * 40)

    #network
    print(f"downloaded: {downloaded:.2f} GiB")
    print(f"uploaded: {uploaded:.2f} GiB")

    print(f"download speed: {download_speed:.2f} Mbps")
    print(f"upload speed:   {upload_speed:.2f} Mbps")

    if ping_time == "unavailable":
        print("network latency: unavailable")
    else:
        print(f"network latency: {ping_time} ms")

    print(f"packet loss: {packet_loss}%")
    print(f"pings tested: {total_pings}")

    if connection_status:
        print("network status: connected")
    else:
        print("network status: disconnected")

    if internet_status:
        print("internet status: reachable")
    else:
        print("internet status: unreachable")