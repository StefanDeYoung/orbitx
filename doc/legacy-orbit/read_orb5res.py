"""
This duplicates the functionality of GOSUB 800 from orbit5v.bas.

I want to know what is inside orb5res.rnd because that's where Dr. Magwood
is keeping a lot of information about the setup of engineering. This script
opens the file and creates the same variables that he does, then logs them
to console
"""
import sys
import numpy as np

SOURCEs = np.empty([6-1, 3-1])
source = np.empty((10-1, 5-1))
DEVICEs = []
SWITCHs = []
SHORTc = []
coolant = np.array((10, 4))
Zvar = [None]*30

f = open('ORB5res.RND', 'rb')
inpSTR = f.read()
f.close()

assert len(inpSTR) == 412
assert inpSTR[0] == inpSTR[-1]

k = 2
for i in range(5):
    SOURCEs[i, 0] = float(int.from_bytes(inpSTR[k:k+8],
                                         byteorder=sys.byteorder, signed=True))
    k += 8
    SOURCEs[i, 1] = float(int.from_bytes(inpSTR[k:k+8],
                                         byteorder=sys.byteorder, signed=True))
    k += 8
    z = int.from_bytes(inpSTR[k:k+8],
                       byteorder=sys.byteorder, signed=True)
    k += 8
    if z == 1:
        source[i, 2] = 0
for i in range(47):
    DEVICEs.append(int.from_bytes(inpSTR[k:k+2],
                                  byteorder=sys.byteorder, signed=True)
                   )
    k += 2
for i in range(64):
    SWITCHs.append(int.from_bytes(inpSTR[k:k+2],
                                  byteorder=sys.byteorder, signed=True)
                   )
    k += 2
# Reecom = (28 and SWITCHs%(21))/4
# Reecom = 1/((Reecom/10)+ (1/10000))
# SWITCHs%(21) = (3 and SWITCHs%(21))
# SWITCHs%(15) = SWITCHs%(15) + (4 * SWITCHs%(24))
# SWITCHs%(52) = SWITCHs%(52) + (4096 * SWITCHs%(53))
for i in range(4):
    z = int.from_bytes(inpSTR[k:k+4],
                       byteorder=sys.byteorder, signed=True)
    k += 4
    # I find that usually z=4311040, and print can't handle str(10**z)
    # Even computing it and appending causes a biiiig slow down
    # SHORTc.append(10**z)
#  IF (i AND DEVICEs(43)) = i THEN coolant(i, 3) = 0
# NEXT i

HABfuelleak= int.from_bytes(inpSTR[k:k+4],
                       byteorder=sys.byteorder, signed=True)
k += 4
AYSEfuelleak= int.from_bytes(inpSTR[k:k+4],
                       byteorder=sys.byteorder, signed=True)
k += 4
for i in range(13, 26):
    Zvar[i] = int.from_bytes(inpSTR[k:k+4],
                             byteorder=sys.byteorder, signed=True)
    k += 4

# IF SWITCHs%(63) = 2 THEN SRBused = 1
# IF SWITCHs%(63) = 1 THEN SRBused = 0
# SWITCHs%(40)=0

print(k)
print(SOURCEs)
print(DEVICEs)
print(SWITCHs)
#print(SHORTc)
print(HABfuelleak, AYSEfuelleak)
print(Zvar)

# DIM switch(65, 16), switchlist(255), switchlabel$(30), source(10, 5), BattAH(10), EL(15)
# DIM SOURCEs(6, 3), DEVICEs(70), SWITCHs%(70), SHORTc(10), engineOP(4), coolant(10, 4), RAD(12, 3), coolantPUMP(10), Zvar#(30)
# 800     OPEN "R", #1, "orb5rEs.RND", 412
# 801     inpSTR$=space$(412)
#         GET #1, 1, inpSTR$
#         close #1
#         if len(inpSTR$) <> 412 then return
#         chkCHAR1$=left$(inpSTR$,1)
#         chkCHAR2$=right$(inpSTR$,1)
#         if chkCHAR1$<>chkCHAR2$ then return
#         k = 2
#         FOR i = 1 TO 5
#          SOURCEs(i, 1)=cvd(mid$(inpSTR$,k,8)):k=k+8
#          SOURCEs(i, 2)=cvd(mid$(inpSTR$,k,8)):k=k+8
#          z=cvd(mid$(inpSTR$,k,8)):k=k+8
#          IF z = 1 THEN source(i, 2) = 0
#         NEXT i
#         FOR i = 1 TO 47
#          DEVICEs(i)=cvi(mid$(inpSTR$,k,2)):k=k+2
#         NEXT i
#         FOR i = 1 TO 64
#          SWITCHs%(i)=cvi(mid$(inpSTR$,k,2)):k=k+2
#         NEXT i
#         Reecom = (28 and SWITCHs%(21))/4
#         Reecom = 1/((Reecom/10)+ (1/10000))
#         SWITCHs%(21) = (3 and SWITCHs%(21))
#         SWITCHs%(15) = SWITCHs%(15) + (4 * SWITCHs%(24))
#         SWITCHs%(52) = SWITCHs%(52) + (4096 * SWITCHs%(53))
#         FOR i = 1 TO 4
#          z=cvs(mid$(inpSTR$,k,4)):k=k+4
#          SHORTc(i) = 10 ^ z
#          IF (i AND DEVICEs(43)) = i THEN coolant(i, 3) = 0
#         NEXT i
#         HABfuelleak=cvs(mid$(inpSTR$,k,4)):k=k+4
#         AYSEfuelleak=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(14)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(15)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(16)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(17)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(18)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(19)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(20)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(21)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(22)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(23)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         Zvar#(26)=cvs(mid$(inpSTR$,k,4)):k=k+4
#         IF SWITCHs%(63) = 2 THEN SRBused = 1
#         IF SWITCHs%(63) = 1 THEN SRBused = 0
#         SWITCHs%(40)=0
#         RETURN