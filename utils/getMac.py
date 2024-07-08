import netifaces

interface_name = "wlp0s20f3"  # Replace with your desired interface name


print(netifaces.ifaddresses(interface_name)[netifaces.AF_LINK][0]['addr']
) 