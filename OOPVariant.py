import os
import subprocess
import re

class HDD:
    def __init__(self):
        subprocess.call("sudo hdparm -I /dev/sda > " + os.getcwd() + "/temp.txt", shell=True)

        self.keys = ["Model Number", "Firmware Revision", "Serial Number", "Transport", "DMA", "PIO"]
        self.dictianary = {key: None for key in self.keys}

    def OpenFile(self):
        self.log = open(os.getcwd() + "/temp.txt")

    def Parse(self):
        for i in self.log:
            for j in self.keys:
                if ((j + ":") in i):
                    temp = i.split(j)[1]
                    d = {
                         ":": lambda x: x.split(":")[1],
                         "\t": lambda x: x.split("\t")[1],
                         "\n": lambda x: x.split("\n")[0]
                    }
                    for i in d.keys():
                        if i in temp:
                            temp = d[i](temp)
                    while (temp[0] == ' '):
                        temp = temp[1:]
                    while (temp[-1] == ' '):
                        temp = temp[:-2]
                    self.dictianary[j] = temp

    def CloseFile(self):
        self.log.close()

    def ShowResult(self):
        for k in self.dictianary.keys():
            print(k + " : ")
            print(self.dictianary[k])

    def ShowMemoryStatus(self):
        subprocess.call("df -hm | grep /dev/sda > " + os.getcwd() + "/temp.txt", shell=True)
        log = open(os.getcwd() + "/temp.txt")
        result = re.split(r" +", log.read())
        memoryDict = dict(all=None, free=None, used=None)
        memoryDict["all"] = result[1]
        memoryDict["used"] = result[2]
        memoryDict["free"] = result[3]
        tempDict = dict(Memory=memoryDict)
        self.dictianary.update(tempDict)
        for k in self.dictianary.keys():
            print(k + " : ")
            print(self.dictianary[k])


    def RemoveFile(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.getcwd() + "/temp.txt")
        os.remove(path)



if __name__== "__main__":
    hdd = HDD()
    hdd.OpenFile()
    hdd.Parse()
    hdd.ShowResult()
    hdd.ShowMemoryStatus()
    hdd.CloseFile() 
    hdd.RemoveFile()
