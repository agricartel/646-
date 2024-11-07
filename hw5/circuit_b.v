module circuit_b(A,B,C,Y,Z);
input A,B,C;
output Y,Z;
wire B1,B2,B3,B4,B5,C1,C2,d,e,f,g,h,k;

assign B1 <= B;
assign B2 <= B;
assign B3 <= B;
assign B4 <= B3;
assign B5 <= B3;
assign C1 <= C;
assign C2 <= C;
assign h <= g;

NAND2X1 NAND_1(.Y(d), .A(A), .B(B1));
NAND2X1 NAND_2(.Y(e), .A(B2), .B(C1));
XOR2X1 XOR_1(.Y(f), .A(C2), .B(B4));
NOR2X1 NOR_1(.Y(g), .A(d), .B(e));
NAND2X1 NAND_3(.Y(k), .A(h), .B(f));
XOR2X1 XOR_2(.Y(Z), .A(k), .B(B5));

endmodule