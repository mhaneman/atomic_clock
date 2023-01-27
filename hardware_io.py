import pyvisa
import time
rm = pyvisa.ResourceManager()

class Instr:
    def __init__(self, resource, baud_rate, timeout=1000) -> None:
        self.name = resource
        self.instr = rm.open_resource(resource)
        self.instr.baud_rate = baud_rate
        self.instr.timeout = timeout

    # returns value read from hardware
    def query(self, command):
        if self.instr is None:
            print("instrument is not defined or cannot extablish communication")
            return
        
        if type(command) is not str:
            print("command must be of type string")
            return

        return self.instr.query(command)

    # prints and returns value read from hardware
    def query_and_print(self, command):
        response = self.query(command)
        print(response)
        return response

    # writes to hardware
    def write(self, command, value):
        self.instr.write(command + str(value))

    # writes to hardware and checks if hardware agrees
    def write_and_verify(self, command, value):
        self.write(command, value)

        response = self.instr.query(command + "?")
        print(self.name, "response ->", command, ": ", response)
        return response

        

