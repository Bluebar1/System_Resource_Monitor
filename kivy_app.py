from kivymd.app import MDApp
from kivy.lang import Builder
from time import sleep
from threading import Thread
import utils as u
import psutil
from kivymd.uix.list import *



"""
Python driver code for kivy app using MDApp

Sets title and color theme before loading and running kv file
"""



class MyTaskManager(MDApp):

    loaded = False

    def updatePageIndex(self, index) :
        self.index = index

    def updateDisks(self, data) :
        disks = list(data)
        print(disks)
        if not self.loaded :
            for disk in disks :
                self.root.ids.disks_id.add_widget(OneLineListItem(text=str(disk)))
            
            self.loaded = True
        
        try:
            for disk in self.root.ids.disks_id.children :
                disk.text = disk
        except:
            pass

    def updateCPU(self, data) :
        try:
            
            self.root.ids.cpu_cores.text = "Cores: " + str(data['CPU']['cores'])
            self.root.ids.cpu_threads.text = "Threads: " + str(data['CPU']['threads'])
            self.root.ids.cpu_usage.text = "Usage: " + str(data['CPU']['usage'])
            self.root.ids.cpu_maxfreq.text = "Max Freq: " + str(data['CPU']['freq']['max'])
        except:
            pass

    def updateRam(self, data) :
        print(data)
        try:
            self.root.ids.ram_total.text = "Total: " + str(data['total']) + "gb"
            self.root.ids.ram_available.text = "Available: " + str(data['available']) + "gb"
            self.root.ids.ram_percent.text = "Percent Used: " + str(data['percent']) + "%"
            self.root.ids.ram_used.text = "Used: " + str(data['used']) + "gb"
            self.root.ids.ram_free.text = "Free: " + str(data['free']) + "gb"
        except:
            pass

    def updateProcesses(self, data) :
        
        try: 
            # Clear processes page and append new ones
            self.root.ids.proc.clear_widgets()
            for process in data :
                self.root.ids.proc.add_widget(TwoLineListItem(text=str(process), 
                secondary_text= 
                "Status: " + str(data[process]['status']) + "   |   " + 
                "Username: " + str(data[process]['username']) + "   |   " + 
                "Name: " + str(data[process]['name'])
                ))
        except:
            pass
 
    
    def build(self):
        self.title = "MyTaskManager"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Blue"
        self.index = "PROCESSES"
        self.statsThread = Thread(target=threadedProc, args=(self,))
        self.statsThread.start()
        return Builder.load_file('kivy_app.kv')

        

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
    


# Flag to terminate thread when app terminates
running = True 
app = MyTaskManager().run()
running = False







