# hardware.py
import psutil
import wmi
import pynvml
import threading
import time


def safe_call(func, name):
    try:
        return func()
    except Exception as e:
        print(f"[WARN] {name} konnte nicht geladen werden: {e}")
        return None


def get_physical_drives_with_partitions_and_labels():
    c = wmi.WMI()
    drive_map = {}

    for disk in c.Win32_DiskDrive():
        disk_id = disk.DeviceID.split("\\")[-1].upper()
        if disk_id not in drive_map:
            drive_map[disk_id] = []

        partitions = disk.associators("Win32_DiskDriveToDiskPartition")
        for partition in partitions:
            logical_disks = partition.associators("Win32_LogicalDiskToPartition")
            for logical_disk in logical_disks:
                letter = logical_disk.DeviceID.upper().strip()
                volume_name = logical_disk.VolumeName or "Kein Name"
                if not any(d["letter"] == letter for d in drive_map[disk_id]):
                    drive_map[disk_id].append({
                        "letter": letter,
                        "label": volume_name
                    })
    print("[DEBUG] Drive Info:", drive_map)
    return drive_map



def get_cpu_info():
    cpu_freq = psutil.cpu_freq()
    cpu_info = {
        "logical_cores": psutil.cpu_count(logical=True),
        "physical_cores": psutil.cpu_count(logical=False),
        "frequency": round(cpu_freq.max) if cpu_freq else None,
    }
    return cpu_info


def get_ram_info():
    mem = psutil.virtual_memory()
    ram_info = {
        "total_gb": round(mem.total / (1024 ** 3)),
        "available_gb": round(mem.available / (1024 ** 3)),
    }
    print("[DEBUG] RAM Info:", ram_info)
    return ram_info



def get_gpu_info():
    gpu_info = []
    pynvml.nvmlInit()
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name_raw = pynvml.nvmlDeviceGetName(handle)
            name = name_raw.decode() if isinstance(name_raw, bytes) else name_raw
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)

            try:
                max_temp = pynvml.nvmlDeviceGetTemperatureThreshold(
                    handle,
                    pynvml.NVML_TEMPERATURE_THRESHOLD_GPU_MAX
                )
            except Exception:
                max_temp = 90

            gpu_info.append({
                "name": name,
                "memory_total_mb": int(mem_info.total / 1024**2),
                "max_temp": max_temp
            })
    except Exception as e:
        print(f"[WARN] GPU-Info konnte nicht geladen werden: {e}")
    finally:
        pynvml.nvmlShutdown()
    print("[DEBUG] RAM Info:", gpu_info)        
    return gpu_info


def get_network_adapters():
    c = wmi.WMI()
    adapters = []
    for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if hasattr(nic, 'Description'):
            adapters.append(nic.Description)
    print("[DEBUG] RAM Info:", adapters)
    return adapters


def detect_hardware():
    drive_map = safe_call(get_physical_drives_with_partitions_and_labels, "Laufwerke") or {}
    cpu_info = safe_call(get_cpu_info, "CPU") or {}
    gpu_info = safe_call(get_gpu_info, "GPU") or []
    ram_info = safe_call(get_ram_info, "RAM") or {}
    network_adapters = safe_call(get_network_adapters, "Netzwerkadapter") or []
    '''
    device_partitions = [
        (dev, part)
        for dev, parts in drive_map.items()
        for part in parts
    ]
    '''
    return {
        'cpu_info': cpu_info,
        'ram_info': ram_info,
        'gpu_info': gpu_info,
        'network_adapters': network_adapters,
        'drive_map': drive_map
    }



def main():
    print("[INFO] Starte Hardware-Erkennung...\n")
    hardware_info = detect_hardware()

    # Optional: Ausgabe der erkannten Hardware (kann auskommentiert werden)
    #for key, value in hardware_info.items():
    #    print(f"[RESULT] {key}: {value}")

    print("\n[INFO] Warte 5 Sekunden...")
    time.sleep(5)
    print("[INFO] Hardware Erkennung beendet.")

if __name__ == "__main__":
    main()

