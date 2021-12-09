from myhdl import *
from ram import *
FRAME_NUM = 10
FRAME_SIZE = 32


@block
def fifo_module(clk, rst, data_in, data_out, data_valid, data_ready, valid_in, frame_num, frame_size):


    write_addr = Signal(intbv(0, max=FRAME_NUM)[4:])
    read_addr = Signal(intbv(0, max=FRAME_NUM)[4:])
    fifo_full = Signal(intbv(0))
    fifo_empty = Signal(intbv(1))
    data_counter = Signal(intbv(0, max=FRAME_NUM)[4:])
    memory = RAM(data_in, write_addr, read_addr, clk, rst, data_out, valid_in, frame_num, frame_size)

    @always_seq(clk.posedge, reset=rst)
    def fifo():
        if rst == 1:
            data_valid.next = 0
            write_addr.next = 0
            read_addr.next = 0
            fifo_empty.next = 1
        else:
            if valid_in == 1:
                if write_addr < frame_num:
                    write_addr.next = (write_addr + 1)
                    #data_counter.next = data_counter + 1
                    fifo_empty.next = 0
                elif write_addr == frame_num and read_addr != 0:
                    write_addr.next = 0
                
                if write_addr == read_addr and write_addr != 0:
                    fifo_full.next = 1

            if ((write_addr != read_addr) or write_addr == 0):
                if data_ready:
                    data_valid.next = 1
                else:
                    data_valid.next = 1
            
            if data_ready == 1 and fifo_empty == 0:
                if write_addr - read_addr == 0:
                    fifo_empty.next = 1
                if read_addr < frame_num:
                    read_addr.next = read_addr + 1
                    #if valid_in != 1 and write_addr < frame_num:
                        #data_counter.next = data_counter - 1
                elif read_addr == frame_num and write_addr != 0:
                    read_addr.next = 0



    return fifo, memory