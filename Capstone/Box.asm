// Box.asm  -  K = 84
// Box starts at row 84, is 20 rows tall, 16 pixels (1 word) wide.
// Row 84 address = SCREEN + 32*84 = 16384 + 2688 = 19072
// Key pressed -> black box (-1). Key released -> box disappears (0).

(MAIN)
    @KBD
    D=M
    @PRESSED
    D;JNE           // any key? go set color black
    @color
    M=0             // no key: white
    @PAINT
    0;JMP
(PRESSED)
    @color
    M=-1            // key: black
(PAINT)
    @19072
    D=A
    @addr
    M=D             // addr = first word of row 84
    @20
    D=A
    @count
    M=D             // count = 20 rows
(ROW)
    @color
    D=M
    @addr
    A=M
    M=D             // paint one word (16 pixels)
    @32
    D=A
    @addr
    M=D+M           // next row = +32 words
    @count
    M=M-1
    D=M
    @ROW
    D;JGT           // repeat until 20 rows done
    @MAIN
    0;JMP
