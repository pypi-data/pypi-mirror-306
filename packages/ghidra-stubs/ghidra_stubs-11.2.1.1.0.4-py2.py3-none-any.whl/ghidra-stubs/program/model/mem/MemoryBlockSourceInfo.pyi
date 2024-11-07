from typing import overload
import ghidra.program.model.address
import ghidra.program.model.mem
import java.lang
import java.util


class MemoryBlockSourceInfo(object):
    """
    Describes the source of bytes for a memory block.
    """









    def contains(self, address: ghidra.program.model.address.Address) -> bool:
        """
        Returns true if this SourceInfo object applies to the given address;
        @param address the address to test if this is its SourceInfo
        @return true if this SourceInfo object applies to the given address;
        """
        ...

    def containsFileOffset(self, fileOffset: long) -> bool:
        """
        Determine if this block source contains the specified file offset.
        @param fileOffset file offset within underlying FileBytes (if applicable) within the loaded 
           range associated with this source info.
        @return true if file offset is within the loaded range of the corresponding FileBytes, else 
           false if method is not supported by the sub-block type (e.g., bit/byte-mapped sub-block).
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getByteMappingScheme(self) -> java.util.Optional:
        """
        Returns an {@link Optional} {@link ByteMappingScheme} employed if this is a byte-mapped 
         memory block.  Otherwise, the Optional is empty.
        @return an {@link Optional} {@link ByteMappingScheme} employed if this is a byte-mapped memory block.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode:
        """
        Returns a description of this SourceInfo object.
        @return a description of this SourceInfo object.
        """
        ...

    def getFileBytes(self) -> java.util.Optional:
        """
        Returns an {@link Optional} {@link FileBytes} object if a FileBytes object is the byte
         source for this SourceInfo.  Otherwise, the Optional will be empty.
        @return the {@link FileBytes} object if it is the byte source for this section
        """
        ...

    @overload
    def getFileBytesOffset(self) -> long:
        """
        Returns the offset into the underlying {@link FileBytes} object where this sub-block 
         starts getting its bytes from or -1 if this sub-block does not have an associated {@link FileBytes}
         or a complex bit/byte-mapping is used.
        @return the offset into the {@link FileBytes} object where this section starts getting its bytes.
        """
        ...

    @overload
    def getFileBytesOffset(self, address: ghidra.program.model.address.Address) -> long:
        """
        Returns the offset into the {@link FileBytes} object for the given address or
         -1 if this sub-block if address is out of range or this sub-block does not have 
         an associated {@link FileBytes}, or a complex bit/byte-mapping is used.
        @param address the address for which to get an offset into the {@link FileBytes} object.
        @return the offset into the {@link FileBytes} object for the given address.
        """
        ...

    def getLength(self) -> long:
        """
        Returns the length of this block byte source.
        @return the length of this block byte source.
        """
        ...

    def getMappedRange(self) -> java.util.Optional:
        """
        Returns an {@link Optional} {@link AddressRange} for the mapped addresses if this is a mapped
         memory block (bit mapped or byte mapped). Otherwise, the Optional is empty.
        @return an {@link Optional} {@link AddressRange} for the mapped addresses if this is a mapped
         memory block
        """
        ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns the end address where this byte source is mapped.
        @return the end address where this byte source is mapped.
        """
        ...

    def getMemoryBlock(self) -> ghidra.program.model.mem.MemoryBlock:
        """
        Returns the containing Memory Block
        @return the containing Memory Block
        """
        ...

    def getMinAddress(self) -> ghidra.program.model.address.Address:
        """
        Returns the start address where this byte source is mapped.
        @return the start address where this byte source is mapped.
        """
        ...

    def hashCode(self) -> int: ...

    def locateAddressForFileOffset(self, fileOffset: long) -> ghidra.program.model.address.Address:
        """
        Get the Address within this sub-block which corresponds to the specified file offset.
        @param fileOffset file offset
        @return {@link Address} within this sub-block or null if file offset is out of range
         or method is not supported by the sub-block type (e.g., bit/byte-mapped sub-block).
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def byteMappingScheme(self) -> java.util.Optional: ...

    @property
    def description(self) -> unicode: ...

    @property
    def fileBytes(self) -> java.util.Optional: ...

    @property
    def fileBytesOffset(self) -> long: ...

    @property
    def length(self) -> long: ...

    @property
    def mappedRange(self) -> java.util.Optional: ...

    @property
    def maxAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def memoryBlock(self) -> ghidra.program.model.mem.MemoryBlock: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...