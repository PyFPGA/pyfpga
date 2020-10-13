module Top (
   input  wire clk_i,
   output wire led_o
);

localparam FREQ = 50000000;

Blinking
   // #(.FREQ (FREQ), .SECS (1)) // see https://github.com/ghdl/ghdl-yosys-plugin/issues/136
   dut (.clk_i (clk_i), .led_o (led_o));

endmodule
