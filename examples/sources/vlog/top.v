`include "header.vh"

module Top #(
  parameter FREQ = 0
)(
  input  clk_i,
  output led_o
);

  initial begin
    if (FREQ==0) begin
      $stop("FREQ must be greater than 0");
      $error("FREQ must be greater than 0");
      $fatal("FREQ must be greater than 0");
    end
  end

`ifdef INCLUDE
`ifdef DEFINE
  Blink #(.FREQ (FREQ)) dut (.clk_i (clk_i), .led_o (led_o));
`endif
`endif

endmodule
