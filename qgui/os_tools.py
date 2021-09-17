# Author: Acer Zhang
# Datetime: 2021/9/17 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import io


class StdOutWrapper(io.TextIOWrapper):
    def __init__(self, stdout, callback=None, do_print=True):
        super().__init__(io.BytesIO(), encoding="utf-8")
        self.buff = ''
        self.ori_stout = stdout
        self.callback = callback
        self.do_print = do_print

    def write(self, output_stream):
        if self.do_print:
            self.buff += output_stream
        if self.callback:
            self.callback(output_stream)

    def flush(self):
        self.buff = ''
