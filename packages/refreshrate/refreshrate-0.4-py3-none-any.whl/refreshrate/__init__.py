import wmi

def get():
    wmi_client = wmi.WMI()
    try:
        for monitor in wmi_client.Win32_VideoController():
            refreshrate = monitor.MaxRefreshRate
            if refreshrate is not None:
                return refreshrate
        print("MaxRefreshRate not found for any video controller.")
    except Exception as e:
        print(f"Failed to retrieve monitor refresh rate: {e}")
    return None
