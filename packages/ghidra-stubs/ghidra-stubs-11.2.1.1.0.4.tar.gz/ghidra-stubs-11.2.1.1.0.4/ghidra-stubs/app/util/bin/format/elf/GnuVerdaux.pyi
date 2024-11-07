from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class GnuVerdaux(object, ghidra.app.util.bin.StructConverter):
    """
    Auxiliary version information.
 
     typedef struct {
       Elf32_Word	vda_name;		//Version or dependency names
       Elf32_Word	vda_next;		//Offset in bytes to next verdaux entry
     } Elf32_Verdaux;
 
     typedef struct {
       Elf64_Word	vda_name;		//Version or dependency names
       Elf64_Word	vda_next;		//Offset in bytes to next verdaux entry
     } Elf32_Verdaux;
 
 
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







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getVda_name(self) -> int: ...

    def getVda_next(self) -> int: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType:
        """
        @see ghidra.app.util.bin.StructConverter#toDataType()
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def vda_name(self) -> int: ...

    @property
    def vda_next(self) -> int: ...