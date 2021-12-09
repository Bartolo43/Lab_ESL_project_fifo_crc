from myhdl import block, delay, always, now, Signal, instances,always_seq, intbv, enum


@block
def crc(clk, reset, in_rdata, in_rvalid, in_wready, out_wdata, out_wvalid,
        out_rready, data_size, polynomial, crc_size):

    """ CRC block

    inputs:
        clk -- global interface clock signal
        reset -- global synchronous reset
        in_rdata -- input data
        in_rvalid -- previous block is ready to send data
        in_wready -- next block is ready to accept data
    outputs:
        out_wdata -- output data
        out_wvalid -- this block is ready to send data
        out_rready -- this block is ready to accept data
    parameters:
        data_size -- size (in bits) of input data
        polynomial -- polynomial for crc calculations
        crc_size -- number of crc bits

    polynomial divisor = 100011101
    """

    data_crc = intbv(0)[crc_size:]
    temp_data = intbv(0)[data_size:]

    t_state = enum('READY_TO_READ', 'READY_TO_SEND')
    fsm_state = Signal(t_state.READY_TO_READ)


    def crc_process(data, crc_polynomial, d_size, c_size):

        crc_divisor = intbv(crc_polynomial)[c_size+1:]
        input_with_padding = intbv(0)[d_size + len(crc_divisor) - 1:]
        crc_input = intbv(int(data))[d_size:]
        input_with_padding[len(input_with_padding):len(crc_divisor) - 1] = crc_input
        remainder = intbv(0)[len(crc_divisor):]
        remainder = input_with_padding[len(input_with_padding):len(input_with_padding) - len(crc_divisor)]

        for i in range(d_size):
            if int(remainder[c_size]) == 1:
                remainder = remainder ^ crc_divisor
            if i != d_size - 1:
                remainder = intbv((remainder << 1), _nrbits=9)
                remainder[0] = input_with_padding[len(input_with_padding) - len(crc_divisor) - i-1]

        crc_checksum = remainder[len(crc_divisor)-2:0]
        return crc_checksum

    @always_seq(clk.posedge, reset=reset)
    def access_process():
        if reset == 1:
            out_wdata.next = 0
            out_wvalid.next = 0
            out_rready.next = 1
        if reset == 0:
            if fsm_state == t_state.READY_TO_READ:
                out_wdata.next = 0
                out_rready.next = 1
                if in_rvalid == 1:
                    out_rready.next = 0
                    out_wvalid.next = 1
                    data_crc.next = crc_process(in_rdata, polynomial, data_size, crc_size)
                    temp_data.next = in_rdata
                    fsm_state.next = t_state.READY_TO_SEND

            if fsm_state == t_state.READY_TO_SEND:
                if in_wready == 1:
                    out_rready.next = 1
                    out_wvalid.next = 0
                    out_wdata.next = (temp_data.next << 8) + int(data_crc.next)
                    fsm_state.next = t_state.READY_TO_READ

    return instances()
