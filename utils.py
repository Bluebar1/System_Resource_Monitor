import psutil


def toGB(d, fields = []) :
    """
    Converts specified fields of dictionary from bytes to gigabytes
    Params:
    *d* JSON data that contains 1 or more byte values
    *fields* List of key values to be converted
    Returns:

    """
    for field in fields :
        d[field] =  d[field] / 1000000000

    return d
        

def processes(filters=[]) :
    """
    Converts generator type object of all processes into a list 
    and removes them given filters
    """
    # Create generator object
    _gen = psutil.process_iter(['name', 'username', 'status'])
    # Convert to list
    _list = list(_gen)
    
    # Trim List
    # TODO: use filters to trim list
    del _list[10:]
    
    # return dictionary objects
    return {p.pid: p.info for p in _list}


def currentDiskStats(disks) :
    """
    Returns system disk drive statistics
    as a list of dictionaries
    """
    disksJson = []
    for disk in disks :
        usage = psutil.disk_usage(disk.device)
        disksJson.append( 
            {
                str(disk.device) : toGB(usage._asdict(), ['total', 'used', 'free'])
            }
        )
    return disksJson


def cpuStats(cores, threads) :
    return {
                'CPU' :
                {
                    'cores': cores,
                    'threads': threads,
                    'usage': psutil.cpu_percent(interval=1),
                    'freq': psutil.cpu_freq()._asdict(),
                    'stats': psutil.cpu_stats()._asdict(),
                    'loadAVG': psutil.getloadavg()
                }
            }

def ramStats() :
    return toGB(psutil.virtual_memory()._asdict(), ['total', 'available', 'used', 'free'])
