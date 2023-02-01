import pyvisa
import time

class Instr:
    def __init__(self, resource, baud_rate, setup_config, term_config, timeout=1000) -> None:
        self.name = resource
        self.setup_config = setup_config
        self.term_config = term_config

        try:
            rm = pyvisa.ResourceManager()
            self.instr = rm.open_resource(resource)
            self.instr.baud_rate = baud_rate
            self.instr.timeout = timeout
        except Exception:
            print(self.name + " cannot be initalized.")
            self.instr = None

    def setup_config(self):
        for command, value in self.setup_config:
            self.write_and_verify(command, value)

    def term_config(self):
        for command, value in self.term_config:
            self.write_and_verify(command, value)


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

        

