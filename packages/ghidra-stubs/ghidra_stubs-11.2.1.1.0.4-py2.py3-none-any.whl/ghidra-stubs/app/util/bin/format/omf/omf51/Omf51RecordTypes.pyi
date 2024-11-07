from typing import overload
import java.lang


class Omf51RecordTypes(object):
    """
    OMF-51 record types
    """

    Content: int = 6
    DebugItem: int = 18
    ExternalDEF: int = 24
    Fixup: int = 8
    LibDictionary: int = 42
    LibHeader: int = 44
    LibModLocs: int = 38
    LibModName: int = 40
    ModuleEND: int = 4
    ModuleHDR: int = 2
    PublicDEF: int = 22
    ScopeDEF: int = 16
    SegmentDEF: int = 14



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

