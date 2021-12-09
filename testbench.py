from myhdl import block, delay, always, now, Signal, instance,always_seq, intbv, enum, ResetSignal
from top import top
from CRC_check import crc_check

@block
def testbench():

    clk = Signal(0)
    reset = ResetSignal(0, active=1, isasync=0)

    data_size = 32
    data_size_after_crc = 40
    polynomial = 285
    crc_size = 8

    in_data = Signal(intbv(1000)[data_size:])
    out_top = Signal(intbv(0)[data_size+crc_size:])
    out_data = Signal(intbv(0)[data_size:])
    frame_num = 10

    in_valid = Signal(0)
    in_wready = Signal(1)
    out_wvalid = Signal(0)
    crc_ready = Signal(0)
    valid_top = Signal(0)

    top_uut = top(clk, reset, in_data, in_valid, crc_ready, out_top, valid_top,
            data_size, polynomial, crc_size, frame_num)

    crc_check_uut = crc_check(clk, reset, out_top, valid_top, in_wready, out_data, out_wvalid,
                        crc_ready, data_size_after_crc, polynomial, crc_size)

    HALF_PERIOD = delay(10)
    counter = 0

    @always(HALF_PERIOD)
    def clkGen():
        clk.next = not clk

    @instance
    def stimulus():
        reset = 1
        yield clk.posedge
        reset = 0
        yield clk.posedge
        while True:
            yield clk.posedge
            in_data.next = in_data + 1000
            in_valid.next = Signal(1)
            yield clk.posedge
            in_valid.next = Signal(0)
            in_wready.next = Signal(1)


    return top_uut, stimulus, clkGen, crc_check_uut

tb = testbench()
tb.config_sim(trace=True)
tb.run_sim(1000)

