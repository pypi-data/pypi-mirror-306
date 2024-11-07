from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class DynamicLibraryModule(object, ghidra.app.util.bin.StructConverter):
    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, header: ghidra.app.util.bin.format.macho.MachHeader): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getExtDefSymCount(self) -> int: ...

    def getExtDefSymIndex(self) -> int: ...

    def getExternalRelocationCount(self) -> int: ...

    def getExternalRelocationIndex(self) -> int: ...

    def getInitTermCount(self) -> int:
        """
        low 16 bits are the number of init section entries, 
         high 16 bits are the number of term section entries
        @return 
        """
        ...

    def getInitTermIndex(self) -> int:
        """
        low 16 bits are the index into the init section, 
         high 16 bits are the index into the term section
        """
        ...

    def getLocalSymbolCount(self) -> int: ...

    def getLocalSymbolIndex(self) -> int: ...

    def getModuleName(self) -> unicode: ...

    def getModuleNameIndex(self) -> int: ...

    def getObjcModuleInfoAddress(self) -> long: ...

    def getObjcModuleInfoSize(self) -> int: ...

    def getReferenceSymbolTableCount(self) -> int: ...

    def getReferenceSymbolTableIndex(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def extDefSymCount(self) -> int: ...

    @property
    def extDefSymIndex(self) -> int: ...

    @property
    def externalRelocationCount(self) -> int: ...

    @property
    def externalRelocationIndex(self) -> int: ...

    @property
    def initTermCount(self) -> int: ...

    @property
    def initTermIndex(self) -> int: ...

    @property
    def localSymbolCount(self) -> int: ...

    @property
    def localSymbolIndex(self) -> int: ...

    @property
    def moduleName(self) -> unicode: ...

    @property
    def moduleNameIndex(self) -> int: ...

    @property
    def objcModuleInfoAddress(self) -> long: ...

    @property
    def objcModuleInfoSize(self) -> int: ...

    @property
    def referenceSymbolTableCount(self) -> int: ...

    @property
    def referenceSymbolTableIndex(self) -> int: ...