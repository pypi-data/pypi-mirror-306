from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.listing
import ghidra.util.task
import java.lang


class LibObjcOptimization(object, ghidra.app.util.bin.StructConverter):
    """
    Represents a objc_opt_t structure, which resides in the libobjc DYLIB within a DYLD cache
    """

    ASCII: ghidra.program.model.data.DataType
    BYTE: ghidra.program.model.data.DataType
    DWORD: ghidra.program.model.data.DataType
    IBO32: ghidra.program.model.data.DataType
    IBO64: ghidra.program.model.data.DataType
    POINTER: ghidra.program.model.data.DataType
    QWORD: ghidra.program.model.data.DataType
    SECTION_NAME: unicode = u'__objc_opt_ro'
    SLEB128: ghidra.program.model.data.SignedLeb128DataType
    STRING: ghidra.program.model.data.DataType
    ULEB128: ghidra.program.model.data.UnsignedLeb128DataType
    UTF16: ghidra.program.model.data.DataType
    UTF8: ghidra.program.model.data.DataType
    VOID: ghidra.program.model.data.DataType
    WORD: ghidra.program.model.data.DataType



    def __init__(self, program: ghidra.program.model.listing.Program, objcOptRoSectionAddr: ghidra.program.model.address.Address):
        """
        Create a new {@link LibObjcOptimization}.
        @param program The {@link Program}
        @param objcOptRoSectionAddr The start address of the __objc_opt_ro section
        @throws IOException if there was an IO-related problem parsing the structure
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getAddr(self) -> long:
        """
        Gets the address of the objc_opt_t structure
        @return The address of the objc_opt_t structure
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getRelativeSelectorBaseAddressOffset(self) -> long:
        """
        Gets the relative method selector base address offset.  This will be 0 if the version is less
         than 16.
        @return The relative method selector base address offset
        """
        ...

    def hashCode(self) -> int: ...

    def markup(self, program: ghidra.program.model.listing.Program, space: ghidra.program.model.address.AddressSpace, log: ghidra.app.util.importer.MessageLog, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Marks up up this structure in memory
        @param program The {@link Program}
        @param space The {@link AddressSpace}
        @param log The log
        @param monitor A cancelable task monitor
        """
        ...

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
    def addr(self) -> long: ...

    @property
    def relativeSelectorBaseAddressOffset(self) -> long: ...