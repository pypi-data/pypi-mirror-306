from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format
import ghidra.app.util.bin.format.pe.rich
import ghidra.program.model.data
import ghidra.util
import java.io
import java.lang


class RichHeader(object, ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.Writeable):
    """
    The "Rich" header contains encoded metadata about the tool chain used to generate the binary.
     This class decodes and writes the Rich header (if it exists).
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    IMAGE_DANS_SIGNATURE: int = 1399742788
    IMAGE_RICH_SIGNATURE: int = 1751345490
    NAME: unicode = u'IMAGE_RICH_HEADER'
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Creates the Rich header found from the given reader.  The reader should be
         positioned directly after the DOS header.
        @param reader The reader to read the PE with.
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getMask(self) -> int:
        """
        Gets the Rich header mask.
        @return the Rich header mask, or -1 if a Rich header was not found.
        """
        ...

    def getOffset(self) -> int:
        """
        Gets the offset of the Rich header.
        @return the offset of the Rich header, or -1 if a Rich header was not found.
        """
        ...

    def getRecords(self) -> List[ghidra.app.util.bin.format.pe.rich.RichHeaderRecord]:
        """
        Gets the Rich header records.
        @return the Rich header records.  Could be empty if a Rich header was not found.
        """
        ...

    def getSize(self) -> int:
        """
        Gets the size of the Rich header.
        @return the size of the Rich header.  Will be 0 if a Rich header was not found.
        """
        ...

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

    def write(self, raf: java.io.RandomAccessFile, dc: ghidra.util.DataConverter) -> None: ...

    @property
    def mask(self) -> int: ...

    @property
    def offset(self) -> int: ...

    @property
    def records(self) -> List[ghidra.app.util.bin.format.pe.rich.RichHeaderRecord]: ...

    @property
    def size(self) -> int: ...