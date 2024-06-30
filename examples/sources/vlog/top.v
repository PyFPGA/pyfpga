`include "header1.vh"
`include "header2.vh"

module Top #(
  parameter FREQ = 0,
  parameter SECS = 0
)(
  input  clk_i,
  output led_o
);

  Blink #(.FREQ (FREQ), .SECS (SECS)) dut (.clk_i (clk_i), .led_o (led_o));

`ifndef INCLUDE1
  Top Top (.clk_i (clk_i), .led_o (led_o));
`endif

`ifndef INCLUDE2
  Top Top (.clk_i (clk_i), .led_o (led_o));
`endif

`ifndef DEFINE1
  Top Top (.clk_i (clk_i), .led_o (led_o));
`endif

`ifndef DEFINE2
  Top Top (.clk_i (clk_i), .led_o (led_o));
`endif

  generate
    if (!FREQ || !SECS) begin: gen_error
      Top Top (.clk_i (clk_i), .led_o (led_o));
    end
  endgenerate

endmodule
