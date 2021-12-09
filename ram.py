from myhdl import *
FRAME_NUM = 10
FRAME_SIZE = 32

@block
def RAM(data_in, write_addr, read_addr, clk, rst, data_out, write_en, frame_num, frame_size):

    mem = [Signal(intbv(0)[frame_size:]) for i in range(frame_num)]

    @always(clk.posedge)
    def write():
        if write_en and write_addr < frame_num:
            mem[write_addr].next = data_in
    @always_comb
    def read():
        if read_addr < frame_num:
            data_out.next = mem[read_addr]

    @always(rst.posedge)
    def reset():
        mem = [Signal(intbv(0)[frame_size:]) for i in range(frame_num)]
  
    return write, read, reset