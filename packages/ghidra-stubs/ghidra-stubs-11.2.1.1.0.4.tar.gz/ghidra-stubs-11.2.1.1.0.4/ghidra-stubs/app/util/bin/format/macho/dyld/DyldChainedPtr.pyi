from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho.dyld
import ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr
import java.lang
import java.util


class DyldChainedPtr(object):
    DYLD_CHAINED_PTR_START_LAST: int = 32768
    DYLD_CHAINED_PTR_START_MULTI: int = 32768
    DYLD_CHAINED_PTR_START_NONE: int = 65535




    class DyldChainType(java.lang.Enum):
        DYLD_CHAINED_PTR_32: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_32_CACHE: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_32_FIRMWARE: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_64: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_64_KERNEL_CACHE: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_64_OFFSET: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_ARM64E: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_ARM64E_FIRMWARE: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_ARM64E_KERNEL: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_ARM64E_SHARED_CACHE: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_ARM64E_USERLAND: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_ARM64E_USERLAND24: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_TYPE_UNKNOWN: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType
        DYLD_CHAINED_PTR_X86_64_KERNEL_CACHE: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType







        @overload
        def compareTo(self, __a0: java.lang.Enum) -> int: ...

        @overload
        def compareTo(self, __a0: object) -> int: ...

        def describeConstable(self) -> java.util.Optional: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDeclaringClass(self) -> java.lang.Class: ...

        def getName(self) -> unicode: ...

        def getValue(self) -> int: ...

        def hashCode(self) -> int: ...

        @staticmethod
        def lookupChainPtr(__a0: int) -> ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType: ...

        def name(self) -> unicode: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        def ordinal(self) -> int: ...

        def toString(self) -> unicode: ...

        @overload
        @staticmethod
        def valueOf(__a0: unicode) -> ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType: ...

        @overload
        @staticmethod
        def valueOf(__a0: java.lang.Class, __a1: unicode) -> java.lang.Enum: ...

        @staticmethod
        def values() -> List[ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType]: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...

        @property
        def value(self) -> int: ...

    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    @staticmethod
    def getAddend(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, chainValue: long) -> long: ...

    @staticmethod
    def getChainValue(reader: ghidra.app.util.bin.BinaryReader, chainLoc: long, ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getNext(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, chainValue: long) -> long: ...

    @staticmethod
    def getOrdinal(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, chainValue: long) -> long: ...

    @staticmethod
    def getSize(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType) -> int: ...

    @staticmethod
    def getStride(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType) -> long: ...

    @staticmethod
    def getTarget(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, chainValue: long) -> long: ...

    def hashCode(self) -> int: ...

    @staticmethod
    def isAuthenticated(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, chainValue: long) -> bool: ...

    @staticmethod
    def isBound(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType, chainValue: long) -> bool: ...

    @staticmethod
    def isRelative(ptrFormat: ghidra.app.util.bin.format.macho.dyld.DyldChainedPtr.DyldChainType) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

