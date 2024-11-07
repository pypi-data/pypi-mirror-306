from typing import overload
import java.lang


class OmfRecordTypes(object):
    """
    Relocatable OMF record types
    """

    ALIAS: int = 198
    BAKPAT: int = 178
    BLKDEF: int = 122
    BLKEND: int = 124
    CEXTDEF: int = 188
    COMDAT: int = 194
    COMDEF: int = 176
    COMENT: int = 136
    DEBSYM: int = 126
    END: int = 241
    ENDREC: int = 120
    EXTDEF: int = 140
    FIXUPP: int = 156
    GRPDEF: int = 154
    LCOMDEF: int = 184
    LEDATA: int = 160
    LEXTDEF: int = 180
    LHEADR: int = 130
    LIBDIC: int = 170
    LIBHED: int = 164
    LIBLOC: int = 168
    LIBNAM: int = 166
    LIDATA: int = 162
    LINNUM: int = 148
    LINSYM: int = 196
    LLNAMES: int = 202
    LNAMES: int = 150
    LOCSYM: int = 146
    LPUBDEF: int = 182
    MODEND: int = 138
    NBKPAT: int = 200
    OVLDEF: int = 118
    PEDATA: int = 132
    PIDATA: int = 134
    PUBDEF: int = 144
    REDATA: int = 114
    REGINT: int = 112
    RHEADR: int = 110
    RIDATA: int = 116
    SEGDEF: int = 152
    START: int = 240
    THEADR: int = 128
    TYPDEF: int = 142
    VENDEXT: int = 206
    VERNUM: int = 204



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

