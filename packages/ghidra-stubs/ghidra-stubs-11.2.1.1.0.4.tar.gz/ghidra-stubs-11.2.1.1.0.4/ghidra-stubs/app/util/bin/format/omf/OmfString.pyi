from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class OmfString(object, ghidra.app.util.bin.StructConverter):
    """
    An variable length OMF string
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



    def __init__(self, length: int, str: unicode):
        """
        Creates a new {@link OmfString}
        @param length The length of the string
        @param str The string
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def length(self) -> int:
        """
        {@return the length of the string}
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def str(self) -> unicode:
        """
        {@return the string}
        """
        ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

