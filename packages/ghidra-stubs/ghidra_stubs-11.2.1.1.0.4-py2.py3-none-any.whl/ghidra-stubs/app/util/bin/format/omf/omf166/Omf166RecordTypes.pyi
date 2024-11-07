from typing import overload
import java.lang


class Omf166RecordTypes(object):
    """
    OMF-166 record types
    """

    BLKDEF: int = 183
    BLKEND: int = 124
    COMMENT: int = 136
    DEBSYM: int = 182
    DEPLST: int = 112
    EXTDEF: int = 140
    FIXUPP: int = 180
    GLBDEF: int = 230
    GRPDEF: int = 177
    LEDATA: int = 184
    LHEADR: int = 130
    LIBDICT: int = 170
    LIBHDR: int = 186
    LIBLOC: int = 168
    LIBNAMES: int = 166
    LINNUM: int = 148
    LNAMES: int = 150
    LOCSYM: int = 181
    MODEND: int = 138
    MODINF: int = 231
    PECDEF: int = 228
    PEDATA: int = 185
    PHEADR: int = 224
    PUBDEF: int = 179
    REGDEF: int = 227
    REGMSK: int = 114
    RTXDEF: int = 48
    SEDEF: int = 176
    SSKDEF: int = 229
    THEADR: int = 128
    TSKDEF: int = 225
    TSKEND: int = 226
    TYPDEF: int = 178
    TYPNEW: int = 240
    VECTAB: int = 233
    XSECDEF: int = 197



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getName(type: int) -> unicode:
        """
        Gets the name of the given record type
        @param type The record type
        @return The name of the given record type
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

