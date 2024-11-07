module circuit_b(A,B,C,Y,Z);
input A,B,C;
output Y,Z;
wire d,e,f,k;

NAND2X1 NAND_1(.Y(d), .A(A), .B(B));
NAND2X1 NAND_2(.Y(e), .A(B), .B(C));
XOR2X1 XOR_1(.Y(f), .A(C), .B(B));
NOR2X1 NOR_1(.Y(Y), .A(d), .B(e));
NAND2X1 NAND_3(.Y(k), .A(Y), .B(f));
XOR2X1 XOR_2(.Y(Z), .A(k), .B(B));

endmodule