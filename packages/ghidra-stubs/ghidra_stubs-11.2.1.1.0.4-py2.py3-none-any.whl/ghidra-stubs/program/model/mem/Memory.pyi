from typing import Iterator
from typing import List
from typing import overload
import ghidra.program.database.mem
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.mem
import ghidra.util.task
import java.io
import java.lang
import java.util
import java.util.function


class Memory(ghidra.program.model.address.AddressSetView, object):
    """
    Memory provides the ability to inspect and manage the memory model for a Program.
     In addition to conventional MemoryBlocks defined within physical memory 
     AddressSpaces other special purpose memory block types may be defined (e.g.,
     byte-mapped, bit-mapped, overlays, etc.).  
 
     All memory block manipulations require excusive access (see Program#hasExclusiveAccess())
     and all memory changes should generally be completed prior to analysis.  In particular, adding 
     additional overlay blocks to an existing overlay space that has already been analyzed should be 
     avoided.  Code references discovered during analysis from an overlay block will give preference 
     to remaining within the corresponding overlay address space provided a block exists at the 
     referenced offset.
 
     Block Types
 
     Initialized - a memory block which defines a memory region with specific data.  
     Data may be initialized from defined FileBytes, an InputStream, or set to all 
     zeros.
     Uninitialized - a memory block which defines a memory region whose data is unknown.
     Byte-Mapped - a memory block whose bytes are mapped to another memory region using 
     either a 1:1 byte-mapping or other specified mapping scheme  (see ByteMappingScheme).
     Byte read/write operations are passed-through the mapped region.
 
     Bit-Mapped - a memory block whose bytes are mapped to a corresponding bit in another
     memory region where a mapped byte has a value of 0 or 1 only.  Byte read/write operations are 
     passed-through to the corresponding bit within the mapped region.
 
 
 
     Overlay Blocks
     An overlay memory block provides the ability to define alternate content for a physical memory
     region.  Any of the Block Types above may be created as an overlay block. The use of an overlay 
     block and its corresponding overlay address space can be used to reflect a different execution 
     context.  Use of overlays during analysis has limitations that must be considered.
 
     Loaded vs. Non-Loaded
     A special purpose AddressSpace#OTHER_SPACE has been established for storing adhoc
     non-loaded data as a memory block.  This is frequently used for storing portions of a file
     that never actually get loaded into memory.  All blocks created using the
     AddressSpace#OTHER_SPACE must be created as an overlay memory block.  All other
     blocks based upon a memory address space, including overlays, are treated as Loaded and
     use offsets into a physical memory space.
 
     Sub-Blocks
     When a memory block is first created it corresponds to a single sub-block.  When
     a block join operation is performed the resulting block will consist of multiple sub-blocks.
     However, the join operation is restricted to default block types only and does not support
     byte/bit-mapped types.
 
    """

    GBYTE: long = 0x40000000L
    GBYTE_SHIFT_FACTOR: int = 30
    MAX_BINARY_SIZE: long = 0x400000000L
    MAX_BINARY_SIZE_GB: int = 16
    MAX_BLOCK_SIZE: long = 0x400000000L
    MAX_BLOCK_SIZE_GB: int = 16





    def __iter__(self): ...

    @overload
    def contains(self, __a0: ghidra.program.model.address.Address) -> bool: ...

    @overload
    def contains(self, __a0: ghidra.program.model.address.AddressSetView) -> bool: ...

    @overload
    def contains(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address) -> bool: ...

    def convertToInitialized(self, uninitializedBlock: ghidra.program.model.mem.MemoryBlock, initialValue: int) -> ghidra.program.model.mem.MemoryBlock:
        """
        Convert an existing uninitialized block with an
         initialized block.
        @param uninitializedBlock uninitialized block to convert
        @param initialValue initial value for the bytes
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryBlockException if there is no block in memory
         at the same address as block or if the block lengths are not
         the same.
        """
        ...

    def convertToUninitialized(self, itializedBlock: ghidra.program.model.mem.MemoryBlock) -> ghidra.program.model.mem.MemoryBlock: ...

    def createBitMappedBlock(self, name: unicode, start: ghidra.program.model.address.Address, mappedAddress: ghidra.program.model.address.Address, length: long, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create a bit-mapped overlay memory block and add it to this Memory.  Each byte address
         within the resulting memory block will correspond to a single bit location within the mapped
         region specified by {@code mappedAddress}.
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start start of the block
        @param mappedAddress start address in the source block for the
         beginning of this block
        @param length block length
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Bit Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a
         previous block
        @throws MemoryConflictException if the new block overlaps with a
         previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IllegalArgumentException if invalid block name specified
        """
        ...

    def createBlock(self, block: ghidra.program.model.mem.MemoryBlock, name: unicode, start: ghidra.program.model.address.Address, length: long) -> ghidra.program.model.mem.MemoryBlock:
        """
        Creates a MemoryBlock at the given address with the same properties
         as block, and adds it to this Memory.  Initialized Default blocks will
         have block filled with 0's.  Method will only create physical space blocks
         and will not create an overlay block.
        @param block source block
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules).
        @param start start of the block
        @param length the size of the new block.
        @return new block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if block specification conflicts with an existing block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IllegalArgumentException if invalid block name specifiede
        """
        ...

    @overload
    def createByteMappedBlock(self, name: unicode, start: ghidra.program.model.address.Address, mappedAddress: ghidra.program.model.address.Address, length: long, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create a byte-mapped memory block and add it to this memory.  Each byte address
         within the resulting memory block will correspond to a byte within the mapped
         region specified by {@code mappedAddress} using a 1:1 byte-mapping.
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start start of the block
        @param mappedAddress start address in the source block for the
         beginning of this block
        @param length block length
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Bit Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IllegalArgumentException if invalid block name
        """
        ...

    @overload
    def createByteMappedBlock(self, name: unicode, start: ghidra.program.model.address.Address, mappedAddress: ghidra.program.model.address.Address, length: long, byteMappingScheme: ghidra.program.database.mem.ByteMappingScheme, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create a byte-mapped memory block and add it to this memory.  Each byte address
         within the resulting memory block will correspond to a byte within the mapped
         region specified by {@code mappedAddress}.  While a 1:1 byte-mapping is the default,
         a specific byte-mapping ratio may be specified.
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start start of the block
        @param mappedAddress start address in the source block for the
         beginning of this block
        @param length block length
        @param byteMappingScheme byte mapping scheme (may be null for 1:1 mapping)
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Bit Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IllegalArgumentException if invalid block name
        """
        ...

    def createFileBytes(self, filename: unicode, offset: long, size: long, is_: java.io.InputStream, monitor: ghidra.util.task.TaskMonitor) -> ghidra.program.database.mem.FileBytes:
        """
        Stores a sequence of bytes into the program.  Typically, this method is used by importers
         to store the original raw program bytes.
        @param filename the name of the file from where the bytes originated
        @param offset the offset into the file for the first byte in the input stream.
        @param size the number of bytes to store from the input stream.
        @param is the input stream that will supply the bytes to store in the program.
         Caller is responsible for closing input stream upon return.
        @param monitor task monitor
        @return a FileBytes that was created to access the bytes.
        @throws IOException if there was an IOException saving the bytes to the program database.
        @throws CancelledException if the user cancelled this operation. Note: the database will
         be stable, but the buffers may contain 0s instead of the actual bytes.
        """
        ...

    @overload
    def createInitializedBlock(self, name: unicode, start: ghidra.program.model.address.Address, fileBytes: ghidra.program.database.mem.FileBytes, offset: long, size: long, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create an initialized memory block using bytes from a {@link FileBytes} object.
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start starting address of the block
        @param fileBytes the {@link FileBytes} object to use as the underlying source of bytes.
        @param offset the offset into the FileBytes for the first byte of this memory block.
        @param size block length (positive non-zero value required)
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Initialized Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a
         previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IndexOutOfBoundsException if file bytes range specified by offset and size 
         is out of bounds for the specified fileBytes.
        @throws IllegalArgumentException if invalid block name specified
        """
        ...

    @overload
    def createInitializedBlock(self, name: unicode, start: ghidra.program.model.address.Address, is_: java.io.InputStream, length: long, monitor: ghidra.util.task.TaskMonitor, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create an initialized memory block based upon a data {@link InputStream} and add it to 
         this Memory.
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start start address of the block
        @param is source of the data used to fill the block or null for zero initialization.
        @param length the size of the block
        @param monitor task monitor
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Initialized Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a
         previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws CancelledException user cancelled operation
        @throws IllegalArgumentException if invalid block name specified
        """
        ...

    @overload
    def createInitializedBlock(self, name: unicode, start: ghidra.program.model.address.Address, size: long, initialValue: int, monitor: ghidra.util.task.TaskMonitor, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create an initialized memory block initialized and add it to this Memory.  All bytes
         will be initialized to the specified value (NOTE: use of zero as the initial value
         is encouraged for reduced storage).
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start start of the block
        @param size block length (positive non-zero value required)
        @param initialValue initialization value for every byte in the block.
        @param monitor progress monitor, may be null.
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Initialized Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a
         previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IllegalArgumentException if invalid block name specified
        @throws CancelledException user cancelled operation
        """
        ...

    def createUninitializedBlock(self, name: unicode, start: ghidra.program.model.address.Address, size: long, overlay: bool) -> ghidra.program.model.mem.MemoryBlock:
        """
        Create an uninitialized memory block and add it to this Memory.
         <p>
         Overlay Blocks: An overlay memory block may be created in two ways:
         <ul>
         <li>Specifying a {@code start} address within an existing overlay address space 
         ({@code overlay} parameter is ignored), or</li>
         <li>Specifying a {@code start} address within a physical memory address space and passing
         {@code overlay=true}.  This use case will force the creation of a new unique overlay 
         address space.</li>
         </ul>
        @param name block name (See {@link Memory#isValidMemoryBlockName(String)} for
         naming rules)
        @param start start of the block
        @param size block length
        @param overlay if true, the block will be created as an OVERLAY block.  If the {@code start}
         address is a non-overlay memory address a new overlay address space will be created and the 
         block will have a starting address at the same offset within the new overlay space.  If the
         specified {@code start} address is an overlay address an overlay block will be created at
         that overlay address.
        @return new Uninitialized Memory Block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if the new block overlaps with a
         previous block
        @throws AddressOverflowException if block specification exceeds bounds of address space
        @throws IllegalArgumentException if invalid block name specified
        """
        ...

    def deleteFileBytes(self, fileBytes: ghidra.program.database.mem.FileBytes) -> bool:
        """
        Deletes a stored sequence of file bytes.  The file bytes can only be deleted if there
         are no memory block references to the file bytes.
        @param fileBytes the FileBytes for the file bytes to be deleted.
        @return true if the FileBytes was deleted.  If any memory blocks are referenced by this 
         FileBytes or it is invalid then it will not be deleted and false will be returned.
        @throws IOException if there was an error updating the database.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    @overload
    def findBytes(self, addr: ghidra.program.model.address.Address, bytes: List[int], masks: List[int], forward: bool, monitor: ghidra.util.task.TaskMonitor) -> ghidra.program.model.address.Address:
        """
        Finds a sequence of contiguous bytes that match the
         given byte array at all bit positions where the mask contains an "on" bit.
         Search is performed over loaded memory only.
        @param addr The beginning address in memory to search.
        @param bytes the array of bytes to search for.
        @param masks the array of masks. (One for each byte in the byte array)
                      if all bits of each byte is to be checked (ie: all mask bytes are 0xff),
                      then pass a null for masks.
        @param forward if true, search in the forward direction.
        @return The address of where the first match is found. Null is returned
         if there is no match.
        """
        ...

    @overload
    def findBytes(self, startAddr: ghidra.program.model.address.Address, endAddr: ghidra.program.model.address.Address, bytes: List[int], masks: List[int], forward: bool, monitor: ghidra.util.task.TaskMonitor) -> ghidra.program.model.address.Address:
        """
        Finds a sequence of contiguous bytes that match the
         given byte array at all bit positions where the mask contains an "on" bit.
         Starts at startAddr and ends at endAddr.
         If forward is true, search starts at startAddr and will end if startAddr "&gt;" endAddr.
         If forward is false, search starts at start addr and will end if startAddr "&lt;" endAddr.
        @param startAddr The beginning address in memory to search.
        @param endAddr The ending address in memory to search (inclusive).
        @param bytes the array of bytes to search for.
        @param masks the array of masks. (One for each byte in the byte array)
                      if all bits of each byte is to be checked (ie: all mask bytes are 0xff),
                      then pass a null for masks.
        @param forward if true, search in the forward direction.
        @return The address of where the first match is found. Null is returned
         if there is no match.
        """
        ...

    def findFirstAddressInCommon(self, __a0: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.Address: ...

    def forEach(self, __a0: java.util.function.Consumer) -> None: ...

    def getAddressCountBefore(self, __a0: ghidra.program.model.address.Address) -> long: ...

    @overload
    def getAddressRanges(self) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddressRanges(self, __a0: bool) -> ghidra.program.model.address.AddressRangeIterator: ...

    @overload
    def getAddressRanges(self, __a0: ghidra.program.model.address.Address, __a1: bool) -> ghidra.program.model.address.AddressRangeIterator: ...

    def getAddressSourceInfo(self, address: ghidra.program.model.address.Address) -> ghidra.program.database.mem.AddressSourceInfo:
        """
        Returns information ({@link AddressSourceInfo}) about the byte source at the given address.
        @param address the address to query. Returns null if the address is not in memory.
        @return information ({@link AddressSourceInfo}) about the byte source at the given address or
         null if the address is not in memory.
        """
        ...

    @overload
    def getAddresses(self, __a0: bool) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getAddresses(self, __a0: ghidra.program.model.address.Address, __a1: bool) -> ghidra.program.model.address.AddressIterator: ...

    def getAllFileBytes(self) -> List[ghidra.program.database.mem.FileBytes]:
        """
        Returns a list of all the stored original file bytes objects
        @return a list of all the stored original file bytes objects
        """
        ...

    def getAllInitializedAddressSet(self) -> ghidra.program.model.address.AddressSetView:
        """
        Returns the set of addresses which correspond to all memory blocks that have
         initialized data.  This includes initialized memory blocks that contain data from
         the program's file header that are not actually in the running in memory image,
         such as debug sections.  Use {@link #getLoadedAndInitializedAddressSet} if you only want
         the addressed of the loaded in memory blocks.
        """
        ...

    @overload
    def getBlock(self, blockName: unicode) -> ghidra.program.model.mem.MemoryBlock:
        """
        Returns the Block with the specified blockName
        @param blockName the name of the requested block
        @return the Block with the specified blockName
        """
        ...

    @overload
    def getBlock(self, addr: ghidra.program.model.address.Address) -> ghidra.program.model.mem.MemoryBlock:
        """
        Returns the Block which contains addr.
        @param addr a valid data Address.
        @return the block containing addr; null if addr is not a valid location.
        """
        ...

    def getBlocks(self) -> List[ghidra.program.model.mem.MemoryBlock]:
        """
        Returns an array containing all the memory blocks.
        """
        ...

    def getByte(self, addr: ghidra.program.model.address.Address) -> int:
        """
        Get byte at addr.
        @param addr the Address of the byte.
        @return the byte.
        @throws MemoryAccessException if the address is
         not contained in any memory block.
        """
        ...

    @overload
    def getBytes(self, addr: ghidra.program.model.address.Address, dest: List[int]) -> int:
        """
        Get dest.length number of bytes starting at the given address.
        @param addr the starting Address.
        @param dest the byte array to populate.
        @return the number of bytes put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
        @throws MemoryAccessException if the starting address is
         not contained in any memory block.
        """
        ...

    @overload
    def getBytes(self, addr: ghidra.program.model.address.Address, dest: List[int], destIndex: int, size: int) -> int:
        """
        Get size number of bytes starting at the given address and populates
         dest starting at dIndex.
        @param addr the starting Address.
        @param dest the byte array to populate.
        @param destIndex the offset into dest to place the bytes.
        @param size the number of bytes to get.
        @return the number of bytes put into dest.  May be less than
         size if the requested number extends beyond initialized / available memory.
        @throws IndexOutOfBoundsException if an invalid index is specified
        @throws MemoryAccessException if the starting address is
         not contained in any memory block or is an uninitialized location.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getExecuteSet(self) -> ghidra.program.model.address.AddressSetView:
        """
        Returns the set of addresses which correspond to the executable memory.
        """
        ...

    def getFirstRange(self) -> ghidra.program.model.address.AddressRange: ...

    def getInitializedAddressSet(self) -> ghidra.program.model.address.AddressSetView:
        """
        Use {@link #getLoadedAndInitializedAddressSet} instead.
        @deprecated
        """
        ...

    @overload
    def getInt(self, addr: ghidra.program.model.address.Address) -> int:
        """
        Get the int at addr.
        @param addr the Address where the int starts.
        @return the int.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getInt(self, addr: ghidra.program.model.address.Address, bigEndian: bool) -> int:
        """
        Get the int at addr using the specified endian order.
        @param addr the Address where the int starts.
        @param bigEndian true means to get the int in
         big endian order
        @return the int.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getInts(self, addr: ghidra.program.model.address.Address, dest: List[int]) -> int:
        """
        Get dest.length number of ints starting at the given address.
        @param addr the starting Address.
        @param dest the int array to populate.
        @return the number of ints put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is not 0 mod 4, the final byte(s) will be discarded.
        @throws MemoryAccessException if the starting address is
         not contained in any memory block.
        """
        ...

    @overload
    def getInts(self, addr: ghidra.program.model.address.Address, dest: List[int], dIndex: int, nElem: int) -> int:
        """
        Get dest.length number of ints starting at the given address.
        @param addr the starting Address.
        @param dest the int array to populate.
        @param dIndex the offset into dest to place the ints.
        @param nElem the number of ints to get.
        @return the number of ints put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is not 0 mod 4, the final byte(s) will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getInts(self, addr: ghidra.program.model.address.Address, dest: List[int], dIndex: int, nElem: int, isBigEndian: bool) -> int:
        """
        Get dest.length number of ints starting at the given address.
        @param addr the starting Address.
        @param dest the int array to populate.
        @param dIndex the offset into dest to place the ints.
        @param nElem the number of ints to get.
        @param isBigEndian true means to get the ints in
         bigEndian order
        @return the number of ints put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is not 0 mod 4, the final byte(s) will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    def getLastRange(self) -> ghidra.program.model.address.AddressRange: ...

    def getLiveMemoryHandler(self) -> ghidra.program.model.mem.LiveMemoryHandler:
        """
        Returns the live memory handler instance used by this memory.
        @return the live memory handler
        """
        ...

    def getLoadedAndInitializedAddressSet(self) -> ghidra.program.model.address.AddressSetView:
        """
        Returns the set of addresses which correspond to all the "loaded" memory blocks that have
         initialized data.  This does not include initialized memory blocks that contain data from
         the program's file header such as debug sections.
        """
        ...

    @overload
    def getLong(self, addr: ghidra.program.model.address.Address) -> long:
        """
        Get the long at addr.
        @param addr the Address where the long starts.
        @return the long.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getLong(self, addr: ghidra.program.model.address.Address, bigEndian: bool) -> long:
        """
        Get the long at addr in the specified endian order.
        @param addr the Address where the long starts.
        @param bigEndian true means to get the long in
         big endian order
        @return the long.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getLongs(self, addr: ghidra.program.model.address.Address, dest: List[long]) -> int:
        """
        Get dest.length number of longs starting at the given address.
        @param addr the starting Address.
        @param dest the long array to populate.
        @return the number of longs put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is not 0 mod 8, the final byte(s) will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getLongs(self, addr: ghidra.program.model.address.Address, dest: List[long], dIndex: int, nElem: int) -> int:
        """
        Get dest.length number of longs starting at the given address.
        @param addr the starting Address.
        @param dest the long array to populate.
        @param dIndex the offset into dest to place the longs.
        @param nElem the number of longs to get.
        @return the number of longs put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is not 0 mod 8, the final byte(s) will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getLongs(self, addr: ghidra.program.model.address.Address, dest: List[long], dIndex: int, nElem: int, isBigEndian: bool) -> int:
        """
        Get dest.length number of longs starting at the given address.
        @param addr the starting Address.
        @param dest the long array to populate.
        @param dIndex the offset into dest to place the longs.
        @param nElem the number of longs to get.
        @param isBigEndian true means to get the longs in
         bigEndian order
        @return the number of longs put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is not 0 mod 8, the final byte(s) will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getNumAddressRanges(self) -> int: ...

    def getNumAddresses(self) -> long: ...

    def getProgram(self) -> ghidra.program.model.listing.Program:
        """
        Returns the program that this memory belongs to.
        """
        ...

    def getRangeContaining(self, __a0: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressRange: ...

    @overload
    def getShort(self, addr: ghidra.program.model.address.Address) -> int:
        """
        Get the short at addr.
        @param addr the Address where the short starts.
        @return the short.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getShort(self, addr: ghidra.program.model.address.Address, bigEndian: bool) -> int:
        """
        Get the short at addr using the specified endian order.
        @param addr the Address where the short starts.
        @param bigEndian true means to get the short in
         bigEndian order
        @return the short.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getShorts(self, addr: ghidra.program.model.address.Address, dest: List[int]) -> int:
        """
        Get dest.length number of shorts starting at the given address.
        @param addr the starting Address.
        @param dest the short array to populate.
        @return the number of shorts put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is odd, the final byte will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getShorts(self, addr: ghidra.program.model.address.Address, dest: List[int], dIndex: int, nElem: int) -> int:
        """
        Get dest.length number of shorts starting at the given address.
        @param addr the starting Address.
        @param dest the short array to populate.
        @param dIndex the offset into dest to place the shorts.
        @param nElem the number of shorts to get.
        @return the number of shorts put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is odd, the final byte will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    @overload
    def getShorts(self, addr: ghidra.program.model.address.Address, dest: List[int], dIndex: int, nElem: int, isBigEndian: bool) -> int:
        """
        Get dest.length number of shorts starting at the given address.
        @param addr the starting Address.
        @param dest the short array to populate.
        @param dIndex the offset into dest to place the shorts.
        @param nElem the number of shorts to get.
        @param isBigEndian true means to get the shorts in
         bigEndian order
        @return the number of shorts put into dest.  May be less than
         dest.length if the requested number extends beyond available memory.
         If the number of retrievable bytes is odd, the final byte will be discarded.
        @throws MemoryAccessException if not all needed bytes are contained in initialized memory.
        """
        ...

    def getSize(self) -> long:
        """
        Get the memory size in bytes.
        """
        ...

    def hasSameAddresses(self, __a0: ghidra.program.model.address.AddressSetView) -> bool: ...

    def hashCode(self) -> int: ...

    def intersect(self, __a0: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    def intersectRange(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSet: ...

    @overload
    def intersects(self, __a0: ghidra.program.model.address.AddressSetView) -> bool: ...

    @overload
    def intersects(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address) -> bool: ...

    def isBigEndian(self) -> bool:
        """
        Returns true if the memory is bigEndian, false otherwise.
        """
        ...

    def isEmpty(self) -> bool: ...

    def isExternalBlockAddress(self, addr: ghidra.program.model.address.Address) -> bool:
        """
        Determine if the specified address is contained within the reserved EXTERNAL block
         (see {@link MemoryBlock#EXTERNAL_BLOCK_NAME}).  This artificial memory block has certain
         limitations that may require associated addresses to be properly identified.  All
         data access/referencing has the biggest exposure since the importers generally
         allocate a fixed and possibly insufficient amount of memory to corresponding data
         symbols.  Any pointer math performed based upon an EXTERNAL block symbol address
         is likely to produce an unuseable address that may collide with unrelated symbols
         stored within the memory block (e.g., {@link OffsetReference} is one such example).
        @param addr address
        @return true if address is contained within EXTERNAL memory block, else false.
        """
        ...

    @staticmethod
    def isValidMemoryBlockName(name: unicode) -> bool:
        """
        Validate the given block name: cannot be null, cannot be an empty string, 
         cannot contain control characters (ASCII 0..0x19).
         <BR>
         NOTE: When producing an overlay memory space which corresponds to a block, the space
         name will be modified to be consistent with address space name restrictions
         and to ensure uniqueness.
        @param name memory block name
        @return true if name is valid else false
        """
        ...

    @overload
    def iterator(self) -> java.util.Iterator: ...

    @overload
    def iterator(self, __a0: bool) -> java.util.Iterator: ...

    @overload
    def iterator(self, __a0: ghidra.program.model.address.Address, __a1: bool) -> java.util.Iterator: ...

    def join(self, blockOne: ghidra.program.model.mem.MemoryBlock, blockTwo: ghidra.program.model.mem.MemoryBlock) -> ghidra.program.model.mem.MemoryBlock:
        """
        Join the two blocks to create a single memory block.
         IMPORTANT! When done, both blockOne and blockTwo should no longer be used.
        @param blockOne block to be combined with blockTwo
        @param blockTwo block to be combined with blockOne
        @return new block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryBlockException thrown if the blocks are
         not contiguous in the address space,
        """
        ...

    def locateAddressesForFileBytesOffset(self, fileBytes: ghidra.program.database.mem.FileBytes, offset: long) -> List[ghidra.program.model.address.Address]:
        """
        Gets a list of addresses where the byte at the given offset
         from the given FileBytes was loaded into memory.
        @param offset the file offset in the given FileBytes of the byte that is to be 
         located in memory
        @param fileBytes the FileBytesobject whose byte is to be located in memory
        @return a list of addresses that are associated with the given
         FileBytes and offset
        """
        ...

    def locateAddressesForFileOffset(self, fileOffset: long) -> List[ghidra.program.model.address.Address]:
        """
        Gets a {@link List} of {@link Address addresses} that correspond to the given file offset.
        @param fileOffset the file offset that will be used to locate the corresponding memory 
           addresses
        @return a {@link List} of {@link Address}es that are associated with the provided file offset
        """
        ...

    def moveBlock(self, block: ghidra.program.model.mem.MemoryBlock, newStartAddr: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Move the memory block containing source address to the destination
         address.
        @param block block to be moved
        @param newStartAddr new start address for block
        @param monitor task monitor so the move block can be canceled
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws MemoryConflictException if move would cause
         blocks to overlap.
        @throws MemoryBlockException if block movement is not permitted
        @throws AddressOverflowException if block movement would violate bounds of address space
        @throws NotFoundException if memoryBlock does not exist in
           this memory.
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def removeBlock(self, block: ghidra.program.model.mem.MemoryBlock, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Remove the memory block.
        @param block the block to be removed.
        @param monitor monitor that is used to cancel the remove operation
        @throws LockException if exclusive lock not in place (see haveLock())
        """
        ...

    def setByte(self, addr: ghidra.program.model.address.Address, value: int) -> None:
        """
        Write byte at addr.
        @param addr the Address of the byte.
        @param value the data to write.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setBytes(self, addr: ghidra.program.model.address.Address, source: List[int]) -> None:
        """
        Write size bytes from values at addr.
        @param addr the starting Address.
        @param source the bytes to write.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setBytes(self, addr: ghidra.program.model.address.Address, source: List[int], sIndex: int, size: int) -> None:
        """
        Write an array of bytes.  This should copy size bytes or fail!
        @param addr the starting Address of the bytes.
        @param source an array to get bytes from.
        @param sIndex the starting source index.
        @param size the number of bytes to fill.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setInt(self, addr: ghidra.program.model.address.Address, value: int) -> None:
        """
        Write int at addr in the default endian order.
        @param addr the Address of the int.
        @param value the data to write.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setInt(self, addr: ghidra.program.model.address.Address, value: int, bigEndian: bool) -> None:
        """
        Write int at addr in the specified endian order.
        @param addr the Address of the int.
        @param bigEndian true means to write the short in
         bigEndian order
        @param value the data to write.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    def setLiveMemoryHandler(self, handler: ghidra.program.model.mem.LiveMemoryHandler) -> None:
        """
        Sets the live memory handler
        @param handler the live memory handler
        """
        ...

    @overload
    def setLong(self, addr: ghidra.program.model.address.Address, value: long) -> None:
        """
        Write long at addr in the default endian order.
        @param addr the Address of the long.
        @param value the data to write.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setLong(self, addr: ghidra.program.model.address.Address, value: long, bigEndian: bool) -> None:
        """
        Write long at addr in the specified endian order.
        @param addr the Address of the long.
        @param value the data to write.
        @param bigEndian true means to write the long in
         bigEndian order
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setShort(self, addr: ghidra.program.model.address.Address, value: int) -> None:
        """
        Write short at addr in default endian order.
        @param addr the Address of the short.
        @param value the data to write.
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    @overload
    def setShort(self, addr: ghidra.program.model.address.Address, value: int, bigEndian: bool) -> None:
        """
        Write short at addr in the specified endian order.
        @param addr the Address of the short.
        @param value the data to write.
        @param bigEndian true means to write short in
         big endian order
        @throws MemoryAccessException if writing is not allowed.
        """
        ...

    def split(self, block: ghidra.program.model.mem.MemoryBlock, addr: ghidra.program.model.address.Address) -> None:
        """
        Split a block at the given addr and create a new block
         starting at addr.
        @param block block to be split into two
        @param addr address (within block) that will be the
         start of new block
        @throws LockException if exclusive lock not in place (see haveLock())
        @throws NotFoundException thrown if block does not exist
         in memory
        @throws MemoryBlockException memory split not permitted
        @throws AddressOutOfBoundsException thrown if address is not in the block
        """
        ...

    def spliterator(self) -> java.util.Spliterator: ...

    def subtract(self, __a0: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    def toString(self) -> unicode: ...

    @staticmethod
    def trimEnd(__a0: ghidra.program.model.address.AddressSetView, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSetView: ...

    @staticmethod
    def trimStart(__a0: ghidra.program.model.address.AddressSetView, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressSetView: ...

    def union(self, __a0: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def xor(self, __a0: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressSet: ...

    @property
    def addressRanges(self) -> ghidra.program.model.address.AddressRangeIterator: ...

    @property
    def allFileBytes(self) -> List[object]: ...

    @property
    def allInitializedAddressSet(self) -> ghidra.program.model.address.AddressSetView: ...

    @property
    def bigEndian(self) -> bool: ...

    @property
    def blocks(self) -> List[ghidra.program.model.mem.MemoryBlock]: ...

    @property
    def empty(self) -> bool: ...

    @property
    def executeSet(self) -> ghidra.program.model.address.AddressSetView: ...

    @property
    def firstRange(self) -> ghidra.program.model.address.AddressRange: ...

    @property
    def initializedAddressSet(self) -> ghidra.program.model.address.AddressSetView: ...

    @property
    def lastRange(self) -> ghidra.program.model.address.AddressRange: ...

    @property
    def liveMemoryHandler(self) -> ghidra.program.model.mem.LiveMemoryHandler: ...

    @liveMemoryHandler.setter
    def liveMemoryHandler(self, value: ghidra.program.model.mem.LiveMemoryHandler) -> None: ...

    @property
    def loadedAndInitializedAddressSet(self) -> ghidra.program.model.address.AddressSetView: ...

    @property
    def maxAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def numAddressRanges(self) -> int: ...

    @property
    def numAddresses(self) -> long: ...

    @property
    def program(self) -> ghidra.program.model.listing.Program: ...

    @property
    def size(self) -> long: ...