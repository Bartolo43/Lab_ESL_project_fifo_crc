from myhdl import block, delay, always, now, Signal, instances,always_seq, intbv, enum
from CRC import crc
from fifo import fifo_module

@block
def top(clk, reset, in_data, in_rvalid, in_wready, out_data, out_wvalid,
         data_size, polynomial, crc_size, frame_num):

    fifo_out = Signal(intbv(0)[data_size:])
    fifo_valid = Signal(0)
    fifo_ready = Signal(0)

    fifo0 = fifo_module(clk, reset, in_data, fifo_out, fifo_valid, fifo_ready, in_rvalid, frame_num, data_size)

    crc0 = crc(clk, reset, fifo_out, fifo_valid, in_wready, out_data,
                  out_wvalid, fifo_ready, data_size, polynomial, crc_size)


    return fifo0, crc0
