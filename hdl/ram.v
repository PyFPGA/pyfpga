// A RAM initialized with an external file

module ram (
    input             clk_i,
    input             we_i,
    input       [5:0] addr_i,
    input      [31:0] data_i,
    output reg [31:0] data_o
);

reg [31:0] ram [0:63];

initial $readmemb("data/memory.dat",ram);

always @(posedge clk_i) begin
    if (we_i)
        ram[addr_i] <= data_i;
    data_o <= ram[addr_i];
end

endmodule
