from __future__ import print_function

from datetime import datetime

from fairness.libvirt_driver import LibvirtConnection


class RUI(object):
    """ This class represents the RUI data model (resource utilization information) """

    server_greediness = {}

    def __init__(self):
        self.cpu_time = 0
        self.memory_used = 0
        self.disk_bytes_read = 0
        self.disk_bytes_written = 0
        self.network_bytes_received = 0
        self.network_bytes_transmitted = 0
        self.time_stamp = 0

    def get_utilization(self, domain_id):
        conn = LibvirtConnection()
        print("cpu_time:", self.cpu_time)
        self.cpu_time = conn.get_vcpu_stats(domain_id)
        self.memory_used = conn.get_memory_stats(domain_id)
        self.disk_bytes_read = conn.get_disk_stats(domain_id)[0]  # 2 for IOPS
        self.disk_bytes_written = conn.get_disk_stats(domain_id)[1]  # 3 for IOPS
        self.network_bytes_received = conn.get_network_stats(domain_id)[0]
        self.network_bytes_transmitted = conn.get_network_stats(domain_id)[1]
        self.time_stamp = datetime.now().time()
