import psutil
import time

def get_network_speed():
    net1 = psutil.net_io_counters()
    sent1 = net1.bytes_sent
    recv1 = net1.bytes_recv

    time.sleep(1)

    net2 = psutil.net_io_counters()
    sent2 = net2.bytes_sent
    recv2 = net2.bytes_recv

    upload_speed = (sent2 - sent1) / 1024  # KB/s
    download_speed = (recv2 - recv1) / 1024  # KB/s

    return upload_speed, download_speed