from typing import List
from typing import overload
import ghidra.app.util.bin.format.elf
import ghidra.program.model.data
import java.lang


class ElfDynamicTable(object, ghidra.app.util.bin.format.elf.ElfFileSection):
    """
    If an object file participates in dynamic linking, its program header table 
     will have an element of type PT_DYNAMIC. This "segment" contains the ".dynamic" section. 
     A special symbol, _DYNAMIC, labels the section, which contains an array of the 
     Elf32_Dyn or Elf64_Dyn structures.
 
     All address entries contained within this table should adjusted for pre-linking 
     using ElfHeader#adjustAddressForPrelink(long).  If a pre-link adjustment is not applicable, 
     this adjustment will have no affect.
    """

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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, header: ghidra.app.util.bin.format.elf.ElfHeader, fileOffset: long, addrOffset: long):
        """
        Construct an ELF Dynamic data table
        @param reader byte provider reader (reader is not retained and position is unaffected)
        @param header elf header
        @param fileOffset file offset which will be used to temporarily position reader
        @param addrOffset memory address offset
        @throws IOException if IO error occurs during parse
        """
        ...



    def addDynamic(self, dyn: ghidra.app.util.bin.format.elf.ElfDynamic, index: int) -> None:
        """
        Adds the new dynamic at the specified index.
        @param dyn the new dynamic
        @param index the new index
        """
        ...

    @overload
    def containsDynamicValue(self, type: long) -> bool:
        """
        Returns true if the specified dynamic type has a value.
        @param type the dynamic type
        @return true if dynamic value exists
        """
        ...

    @overload
    def containsDynamicValue(self, type: ghidra.app.util.bin.format.elf.ElfDynamicType) -> bool:
        """
        Returns true if the specified dynamic (enum) type has a value.
        @param type the dynamic (enum) type
        @return true if dynamic value exists
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getAddressOffset(self) -> long: ...

    def getClass(self) -> java.lang.Class: ...

    @overload
    def getDynamicValue(self, type: long) -> long:
        """
        Returns the value of the specified dynamic type.
        @param type the dynamic type
        @return the dynamic value
        @throws NotFoundException if requested value type not found
        """
        ...

    @overload
    def getDynamicValue(self, type: ghidra.app.util.bin.format.elf.ElfDynamicType) -> long:
        """
        Returns the value of the specified dynamic (enum) type.
        @param type the dynamic (enum) type
        @return the dynamic value
        @throws NotFoundException if requested value type not found
        """
        ...

    @overload
    def getDynamics(self) -> List[ghidra.app.util.bin.format.elf.ElfDynamic]:
        """
        Returns an array of the dynamics defined this dynamic header.
        @return an array of the dynamics defined this dynamic header
        """
        ...

    @overload
    def getDynamics(self, type: long) -> List[ghidra.app.util.bin.format.elf.ElfDynamic]:
        """
        Returns an array of the dynamics defined this dynamic header
         with the specified type.
        @param type the desired dynamic type, e.g., DT_NEEDED
        @return an array of the dynamics defined this dynamic header
        """
        ...

    @overload
    def getDynamics(self, type: ghidra.app.util.bin.format.elf.ElfDynamicType) -> List[ghidra.app.util.bin.format.elf.ElfDynamic]:
        """
        Returns an array of the dynamics defined this dynamic header
         with the specified (enum) type.
        @param type the desired dynamic type, e.g., DT_NEEDED
        @return an array of the dynamics defined this dynamic header
        """
        ...

    def getEntrySize(self) -> int: ...

    def getFileOffset(self) -> long: ...

    def getLength(self) -> long: ...

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
    def addressOffset(self) -> long: ...

    @property
    def dynamics(self) -> List[ghidra.app.util.bin.format.elf.ElfDynamic]: ...

    @property
    def entrySize(self) -> int: ...

    @property
    def fileOffset(self) -> long: ...

    @property
    def length(self) -> long: ...