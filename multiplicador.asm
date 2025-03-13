.code
VerificarMaior: lda x
                not
                add #01h
                add y
                jn XMax

YMax:           lda y
                sta max
                lda x
                sta min
                jmp Multiplicacao

XMax:           lda x
                sta max
                lda y
                sta min

Multiplicacao:  lda min
                jz Fim
                lda result
                add max
                sta result
                lda numDeSomas
                add #01h
                sta numDeSomas
                lda min
                add #0ffh
                sta min
                jmp Multiplicacao

Fim:            hlt
.endcode

.data
x:              db #00h
y:              db #00h
min:            db #00h
max:            db #00h
numDeSomas:     db #00h
result:         db #00h
.enddata
