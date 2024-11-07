from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.macho
import ghidra.program.model.data
import java.io
import java.lang


class Section(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a section and section_64 structure.
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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, is32bit: bool): ...



    def contains(self, address: long) -> bool:
        """
        Returns true if the section contains the given address
        @param address The address to check
        @return True if the section contains the given address; otherwise, false
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getAddress(self) -> long: ...

    def getAlign(self) -> int: ...

    def getAttributes(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getDataStream(self, header: ghidra.app.util.bin.format.macho.MachHeader) -> java.io.InputStream:
        """
        Returns an input stream to underlying bytes of this section.
        @param header The Mach-O header
        @return an input stream to underlying bytes of this section
        @throws IOException if an i/o error occurs.
        """
        ...

    def getFlags(self) -> int: ...

    def getNumberOfRelocations(self) -> int: ...

    def getOffset(self) -> int: ...

    def getRelocationOffset(self) -> int: ...

    def getRelocations(self) -> List[ghidra.app.util.bin.format.macho.RelocationInfo]: ...

    def getReserved1(self) -> int: ...

    def getReserved2(self) -> int: ...

    def getReserved3(self) -> int: ...

    def getSectionName(self) -> unicode: ...

    def getSegmentName(self) -> unicode: ...

    def getSize(self) -> long: ...

    def getType(self) -> int: ...

    def hashCode(self) -> int: ...

    def isExecute(self) -> bool:
        """
        Returns true if this section has EXECUTE permission.
         <p>
         NOTE: On a real system, sections don't have their own permissions, only the segments they 
         live in do.  However, Ghidra needs finer-grained control for analysis to work correctly, so 
         we take control over section permissions to fit our needs.
        @return true if this section has EXECUTE permission
        """
        ...

    def isRead(self) -> bool:
        """
        Returns true if this section has READ permission.
         <p>
         NOTE: On a real system, sections don't have their own permissions, only the segments they 
         live in do.  However, Ghidra needs finer-grained control for analysis to work correctly, so 
         we take control over section permissions to fit our needs.
        @return true if this section has READ permission
        """
        ...

    def isWrite(self) -> bool:
        """
        Returns true if this section has WRITE permission.
         <p>
         NOTE: On a real system, sections don't have their own permissions, only the segments they 
         live in do.  However, Ghidra needs finer-grained control for analysis to work correctly, so 
         we take control over section permissions to fit our needs.
        @return true if this section has WRITE permission
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setSectionName(self, name: unicode) -> None: ...

    def setSegmentName(self, name: unicode) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def address(self) -> long: ...

    @property
    def align(self) -> int: ...

    @property
    def attributes(self) -> int: ...

    @property
    def execute(self) -> bool: ...

    @property
    def flags(self) -> int: ...

    @property
    def numberOfRelocations(self) -> int: ...

    @property
    def offset(self) -> int: ...

    @property
    def read(self) -> bool: ...

    @property
    def relocationOffset(self) -> int: ...

    @property
    def relocations(self) -> List[object]: ...

    @property
    def reserved1(self) -> int: ...

    @property
    def reserved2(self) -> int: ...

    @property
    def reserved3(self) -> int: ...

    @property
    def sectionName(self) -> unicode: ...

    @sectionName.setter
    def sectionName(self, value: unicode) -> None: ...

    @property
    def segmentName(self) -> unicode: ...

    @segmentName.setter
    def segmentName(self, value: unicode) -> None: ...

    @property
    def size(self) -> long: ...

    @property
    def type(self) -> int: ...

    @property
    def write(self) -> bool: ...