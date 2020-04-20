module Params #(
   parameter BOO = 0,
   parameter INT = 0,
   parameter LOG = 1'b0,
   parameter VEC = 8'd0,
   parameter STR = "ABCD",
   parameter REA = 0.0
)(
   output wire boo_o,
   output wire [7:0] int_o,
   output wire log_o,
   output wire [7:0] vec_o,
   output wire str_o,
   output wire rea_o
);

   initial begin
      if (BOO != 1) begin
         $display("The boolean is not True");
         $finish;
      end
      if (INT != 255) begin
         $display("The integer is not 255");
         $finish;
      end
      if (LOG != 1) begin
         $display("The std_logic is not '1'");
         $finish;
      end
      if (VEC != 8'b11111111) begin
         $display("The std_logic_vector is not 11111111");
         $finish;
      end
      if (STR != "WXYZ") begin
         $display("The string is not WXYZ");
         $finish;
      end
      if (REA != 1.1) begin
         $display("The real is not 1.1");
         $finish;
      end
   end

   assign boo_o = BOO;
   assign int_o = INT;
   assign log_o = LOG;
   assign vec_o = VEC;
   assign str_o = (STR=="WXYZ") ? 1'b1 : 1'b0;
   assign rea_o = (REA==1.1) ? 1'b1 : 1'b0;

endmodule
