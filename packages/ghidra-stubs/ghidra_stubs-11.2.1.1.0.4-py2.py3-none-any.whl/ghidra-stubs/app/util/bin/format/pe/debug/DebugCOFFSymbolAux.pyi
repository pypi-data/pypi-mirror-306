from typing import overload
import ghidra.app.util.bin
import ghidra.program.model.data
import java.lang


class DebugCOFFSymbolAux(object, ghidra.app.util.bin.StructConverter):
    """
    A class to represent the COFF Auxiliary Symbol data structure.
 
 
     typedef union _IMAGE_AUX_SYMBOL {
         struct {
             DWORD    TagIndex;                      // struct, union, or enum tag index
             union {
                 struct {
                     WORD    Linenumber;             // declaration line number
                     WORD    Size;                   // size of struct, union, or enum
                 } LnSz;
                DWORD    TotalSize;
             }Misc;
             union {
                 struct {                            // if ISFCN, tag, or .bb
                     DWORD    PointerToLinenumber;
                     DWORD    PointerToNextFunction;
                 } Function;
                 struct {                            // if ISARY, up to 4 dimen.
                     WORD     Dimension[4];
                 } Array;
             } FcnAry;
             WORD    TvIndex;                        // tv index
         } Sym;
         struct {
             BYTE    Name[IMAGE_SIZEOF_SYMBOL];
         } File;
         struct {
             DWORD   Length;                         // section length
             WORD    NumberOfRelocations;            // number of relocation entries
             WORD    NumberOfLinenumbers;            // number of line numbers
             DWORD   CheckSum;                       // checksum for communal
             SHORT   Number;                         // section number to associate with
             BYTE    Selection;                      // communal selection type
         } Section;
     } IMAGE_AUX_SYMBOL;
 
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    IMAGE_SIZEOF_AUX_SYMBOL: int = 18
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType




    class AuxSection(object, ghidra.app.util.bin.StructConverter):
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






    class AuxSym(object, ghidra.app.util.bin.StructConverter):
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






    class AuxFile(object, ghidra.app.util.bin.StructConverter):
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







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode:
        """
        @see java.lang.Object#toString()
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

