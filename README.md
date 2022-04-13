# System Resource Monitor
Monitors a computer's resources such as CPU, RAM, hard drives, and what processes are using the most.

## Kivy App
Kivy is an opensource multi-platform GUI development library for Python and can run on iOS, Android, Windows, OS X, and GNU/Linux.  
The app has 4 different pages: Processes, Disks, CPU, and RAM. Each is accessible by the bottom navigator bar.  
When a page is selected, it will display constantly updated data provided by seperate threaded process.

## Threaded Process
Before the kivy_app.kv file is loaded, an asynchronous threaded process is started.
```python
    def build(self):
        self.title = "MyTaskManager"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        self.index = "PROCESSES"
        self.statsThread = Thread(target=threadedProc, args=(self,))
        self.statsThread.start()
        return Builder.load_file('kivy_app.kv')
```
The threaded process will cycle once a second, updating the information for the page the user has selected.
```python
def threadedProc(app) :
    
    global running

    
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count()
    disks = psutil.disk_partitions()

    
    while running :
        # Only load data of current index
        if app.index == "DISKS" :
            app.updateDisks(u.currentDiskStats(disks))
        elif app.index == "CPU" :
            app.updateCPU(u.cpuStats(cores, threads))
        elif app.index == "RAM" :
            app.updateRam(u.ramStats())
        else :
            app.updateProcesses(u.processes())

        
        sleep(1)
```

