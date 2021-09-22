# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import sys


class StdOutWrapper:
    def __init__(self, stdout, callback=None, do_print=True):
        self.buff = ""
        self.stdout = stdout
        self.callback = callback
        self.do_print = do_print

    def write(self, output_stream):
        self.buff += output_stream
        if self.do_print:
            self.stdout.write(output_stream)
        if self.callback and "\n" in self.buff:
            self.callback(self.buff)
            self.buff = ""

    def flush(self):
        self.buff = ""

    def __del__(self):
        sys.stdout = self.stdout
