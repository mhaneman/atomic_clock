import pyvisa
import time
import sys

class Instr:
    def __init__(self, resource, baud_rate, setup_commands, term_commands, timeout=1000) -> None:
        self.name = resource
        self.setup_commands = setup_commands
        self.term_commands = term_commands

        try:
            rm = pyvisa.ResourceManager()
            self.instr = rm.open_resource(resource)
            self.instr.baud_rate = baud_rate
            self.instr.timeout = timeout
        except Exception:
            self.instr = None
            print(self.name + " cannot be initalized.")

    def setup_config(self):
        if self.instr is None:
            print(self.name + " cannot be setup. Exiting Program", file=sys.stderr)

        for command, value in self.setup_commands.items():
            self.write_and_verify(command, value)

    def term_config(self):
        if self.instr is not None:
            for command, value in self.term_commands.items():
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

        

