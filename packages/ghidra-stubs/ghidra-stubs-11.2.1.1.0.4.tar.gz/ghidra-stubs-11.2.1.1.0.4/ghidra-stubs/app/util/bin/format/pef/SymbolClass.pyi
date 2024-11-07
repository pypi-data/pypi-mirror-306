from typing import List
from typing import overload
import ghidra.app.util.bin.format.pef
import java.lang
import java.util


class SymbolClass(java.lang.Enum):
    kPEFCodeSymbol: ghidra.app.util.bin.format.pef.SymbolClass
    kPEFDataSymbol: ghidra.app.util.bin.format.pef.SymbolClass
    kPEFGlueSymbol: ghidra.app.util.bin.format.pef.SymbolClass
    kPEFTOCSymbol: ghidra.app.util.bin.format.pef.SymbolClass
    kPEFTVectSymbol: ghidra.app.util.bin.format.pef.SymbolClass
    kPEFUndefinedSymbol: ghidra.app.util.bin.format.pef.SymbolClass







    @overload
    def compareTo(self, __a0: java.lang.Enum) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def describeConstable(self) -> java.util.Optional: ...

    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def get(__a0: int) -> ghidra.app.util.bin.format.pef.SymbolClass: ...

    def getClass(self) -> java.lang.Class: ...

    def getDeclaringClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def name(self) -> unicode: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def ordinal(self) -> int: ...

    def toString(self) -> unicode: ...

    def value(self) -> int: ...

    @overload
    @staticmethod
    def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.pef.SymbolClass: ...

    @overload
    @staticmethod
    def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

    @staticmethod
    def values() -> List[ghidra.app.util.bin.format.pef.SymbolClass]: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

