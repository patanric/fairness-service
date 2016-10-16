import subprocess


def _get_disk_speeds():
    """ Returns the sum of all disk speeds in bytes/s

    :return: Combined disk speeds in bytes/s
    :rtype: int
    """
    speeds = 0
    try:
        disks = list()
        output = execute('lsblk', '-io', 'KNAME,TYPE', run_as_root=True)
        # print output
        if output is not None:
            for line in output.splitlines():
                line_segments = line.split(' ')
                if line_segments[len(line_segments)-1] == 'disk':
                    disks.append(line_segments[0])
        for disk in disks:
            output = subprocess.check_output(['sudo', 'hdparm', '-t', '/dev/'+disk])
            # print output
            if output is not None:
                lines = output.splitlines()
                line_segments = lines[2].split(' ')
                speed_in_mbs = line_segments[len(line_segments)-2]
                speed_in_bytes = float(speed_in_mbs) * 1000000
                speeds += int(speed_in_bytes)
    except subprocess.CalledProcessError:
        print "An error in _get_disk_speeds() has ocured: Command 'exit 1' returned non-zero exit status 1"
    print "speeds: ", speeds


def execute(*cmd, **kwargs):
    """Convenience wrapper around oslo's execute() method."""
    if 'run_as_root' in kwargs and 'root_helper' not in kwargs:
        kwargs['root_helper'] = _get_root_helper()
    return processutils.execute(*cmd, **kwargs)

if __name__ == '__main__':
    _get_disk_speeds()
