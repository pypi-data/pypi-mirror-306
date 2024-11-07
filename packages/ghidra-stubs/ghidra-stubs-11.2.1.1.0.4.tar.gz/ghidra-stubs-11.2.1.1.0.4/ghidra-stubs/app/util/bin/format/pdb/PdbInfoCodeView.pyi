from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.pdb
import ghidra.framework.options
import ghidra.program.model.data
import java.lang


class PdbInfoCodeView(object, ghidra.app.util.bin.StructConverter, ghidra.app.util.bin.format.pdb.PdbInfo):
    """
    Older style pdb information, using a simple 32bit hash to link the pdb to its binary.
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

    def hashCode(self) -> int: ...

    @staticmethod
    def isMatch(reader: ghidra.app.util.bin.BinaryReader, offset: long) -> bool:
        """
        Returns true if the pdb information at the specified offset is a {@link PdbInfoCodeView}
         type (based on the signature at that offset).
        @param reader {@link BinaryReader}
        @param offset offset of the Pdb information
        @return boolean true if it is a {@link PdbInfoCodeView} type
        @throws IOException if error reading data
        """
        ...

    def isValid(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def read(reader: ghidra.app.util.bin.BinaryReader, offset: long) -> ghidra.app.util.bin.format.pdb.PdbInfoCodeView:
        """
        Reads the pdb information from a PE binary.
        @param reader {@link BinaryReader}
        @param offset offset of the Pdb information
        @return new {@link PdbInfoCodeView} instance, never null
        @throws IOException if error reading data
        """
        ...

    def serializeToOptions(self, options: ghidra.framework.options.Options) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def valid(self) -> bool: ...