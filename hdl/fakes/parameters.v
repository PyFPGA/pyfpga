module Params #(
   parameter INT = 0,
   parameter REA = 0.0,
   parameter LOG = 1'd0,
   parameter VEC = 8'd0,
   parameter STR = "ABCD"
)(
   input  wire d_i,
   output wire d_o
);

assign d_o = d_i;

endmodule
