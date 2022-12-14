import subprocess
import threading
import signal
import os

""" Run system commands with timeout
"""
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.out = None

    def run_command(self, capture = False):
        if not capture:
            self.process = subprocess.Popen(self.cmd,shell=True)
            self.process.communicate()
            return
        # capturing the outputs of shell commands
        self.process = subprocess.Popen(self.cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        out,err = self.process.communicate()
        if len(out) > 0:
            self.out = out.splitlines()
        else:
            self.out = None

    # set default timeout to 2 minutes
    def run(self, capture = False, timeout = 10):
        thread = threading.Thread(target=self.run_command, args=(capture,))
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            print('Command timeout, kill it: ' + self.cmd)
            self.process.terminate()
            print("Kiiiillled")
            self.process.kill()
            print("Kiiiillled2")
            print(self.process.pid)
            os.kill(self.process.pid, signal.SIGINT)
            os.kill(self.process.pid+1, signal.SIGINT)

            thread.join()
            print("Kiiiillled3")
            return False
        return self.out