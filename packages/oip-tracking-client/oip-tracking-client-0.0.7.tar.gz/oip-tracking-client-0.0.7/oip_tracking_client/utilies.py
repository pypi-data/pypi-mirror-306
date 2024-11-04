from oip_tracking_client.monitors.amd_monitor import AMDGPUMonitor


def amd_gpu_exists() -> bool:
    try:
        gpus = AMDGPUMonitor.get_gpus()
        return True if gpus else False
    except Exception:
        return False
