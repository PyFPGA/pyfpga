`include "blinking.vh"

module Blinking #(
   parameter FREQ = `DEFAULT_FREQ,
   parameter SECS = `DEFAULT_SECS
)(
   input  wire clk_i,
   output wire led_o
);

localparam DIV = FREQ*SECS;

reg                 led;
reg [$clog2(DIV)-1:0] cnt = 0;

always @(posedge clk_i) begin
   if (cnt == DIV-1) begin
      cnt = 0;
      led <= ~led;
   end else begin
      cnt = cnt + 1;
   end
end

assign led_o = led;

endmodule
