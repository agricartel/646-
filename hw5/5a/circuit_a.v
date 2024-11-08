module circuit_a(a,b,c,d,e,f,o1,o2,o3);
input a,b,c,d,e,f;
output o1,o2,o3;

wire g,hijk,l,m,n,p,rst,w;

NAND2X1 NAND_1(.Y(g), .A(a), .B(hijk));
NAND2X1 NAND_2(.Y(hijk), .A(b), .B(c));
XNOR2X1 XNOR_1(.Y(h), .A(d), .B(e));
XOR2X1 XOR_1(.Y(o3), .A(rst), .B(f));

NAND2X1 NAND_3(.Y(o1), .A(g), .B(w));
INVX1 INV_1(.Y(l), .A(hijk));
XNOR2X1 XNOR_2(.Y(o2), .A(hijk), .B(m));

NAND2X1 NAND_4(.Y(rst), .A(l), .B(o2));

INVX1 INV_2(.Y(w), .A(rst));

endmodule
