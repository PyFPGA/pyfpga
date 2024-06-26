`include "header1.vh"
`include "header2.vh"

module Top #(
  parameter FREQ = 0,
  parameter SECS = 0
)(
  input  clk_i,
  output led_o
);

  initial begin
    if (!FREQ) begin
      $stop("FREQ not set");
      $error("FREQ not set");
      $fatal("FREQ not set");
    end
    if (!SECS) begin
      $stop("SECS not set");
      $error("SECS not set");
      $fatal("SECS not set");
    end
    `ifndef INCLUDE1
      $stop("INCLUDE1 not defined");
      $error("INCLUDE1 not defined");
      $fatal("INCLUDE1 not defined");
    `endif
    `ifndef INCLUDE2
      $stop("INCLUDE2 not defined");
      $error("INCLUDE2 not defined");
      $fatal("INCLUDE2 not defined");
    `endif
    `ifndef DEFINE1
      $stop("DEFINE1 not defined");
      $error("DEFINE1 not defined");
      $fatal("DEFINE1 not defined");
    `endif
    `ifndef DEFINE2
      $stop("DEFINE2 not defined");
      $error("DEFINE2 not defined");
      $fatal("DEFINE2 not defined");
    `endif
  end

`ifdef INCLUDE1
`ifdef INCLUDE2
`ifdef DEFINE1
`ifdef DEFINE2
  Blink #(.FREQ (FREQ), .SECS (SECS)) dut (.clk_i (clk_i), .led_o (led_o));
`endif
`endif
`endif
`endif

endmodule
