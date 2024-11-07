from typing import List
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.mem
import java.io
import java.lang


class MemoryBlock(java.io.Serializable, java.lang.Comparable, object):
    """
    Interface that defines a block in memory.
    """

    ARTIFICIAL: int = 16
    EXECUTE: int = 1
    EXTERNAL_BLOCK_NAME: unicode = u'EXTERNAL'
    READ: int = 4
    VOLATILE: int = 8
    WRITE: int = 2







    def compareTo(self, __a0: object) -> int: ...

    def contains(self, addr: ghidra.program.model.address.Address) -> bool:
        """
        Return whether addr is contained in this block.
        @param addr address
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getAddressRange(self) -> ghidra.program.model.address.AddressRange:
        """
        Get the address range that corresponds to this block.
        @return block address range
        """
        ...

    def getByte(self, addr: ghidra.program.model.address.Address) -> int:
        """
        Returns the byte at the given address in this block.
        @param addr the address.
        @return byte value from this block and specified address
        @throws MemoryAccessException if any of the requested bytes are uninitialized.
        @throws IllegalArgumentException if the Address is not in this block.
        """
        ...

    @overload
    def getBytes(self, addr: ghidra.program.model.address.Address, b: List[int]) -> int:
        """
        Tries to get b.length bytes from this block at the given address. May return fewer bytes if
         the requested length is beyond the end of the block.
        @param addr the address from which to get the bytes.
        @param b the byte array to populate.
        @return the number of bytes actually populated.
        @throws MemoryAccessException if any of the requested bytes are uninitialized.
        @throws IllegalArgumentException if the Address is not in this block.
        """
        ...

    @overload
    def getBytes(self, addr: ghidra.program.model.address.Address, b: List[int], off: int, len: int) -> int:
        """
        Tries to get len bytes from this block at the given address and put them into the given byte
         array at the specified offet. May return fewer bytes if the requested length is beyond the
         end of the block.
        @param addr the address from which to get the bytes.
        @param b the byte array to populate.
        @param off the offset into the byte array.
        @param len the number of bytes to get.
        @return the number of bytes actually populated.
        @throws IndexOutOfBoundsException if invalid offset is specified
        @throws MemoryAccessException if any of the requested bytes are uninitialized.
        @throws IllegalArgumentException if the Address is not in this block.
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getComment(self) -> unicode:
        """
        Get the comment associated with this block.
        @return block comment string
        """
        ...

    def getData(self) -> java.io.InputStream:
        """
        Get memory data in the form of an InputStream. Null is returned for thos memory blocks which
         have no data.
        """
        ...

    def getEnd(self) -> ghidra.program.model.address.Address:
        """
        Return the end address of this block.
        @return end address of the block
        """
        ...

    def getFlags(self) -> int:
        """
        Returns block flags (i.e., permissions and attributes) as a bit mask. 
         These bits defined as {@link #READ}, {@link #WRITE}, {@link #EXECUTE}, {@link #VOLATILE},
         {@link #ARTIFICIAL}.
        @return block flag bits
        """
        ...

    def getName(self) -> unicode:
        """
        Get the name of this block
        @return block name
        """
        ...

    def getSize(self) -> long:
        """
        Get the number of bytes in this block.
        @return number of bytes in the block
        """
        ...

    def getSizeAsBigInteger(self) -> long:
        """
        Get the number of bytes in this block.
        @return the number of bytes in this block as a BigInteger
        """
        ...

    def getSourceInfos(self) -> List[ghidra.program.model.mem.MemoryBlockSourceInfo]:
        """
        Returns a list of {@link MemoryBlockSourceInfo} objects for this block. A block may consist
         of multiple sequences of bytes from different sources. Each such source of bytes is described
         by its respective SourceInfo object. Blocks may have multiple sources after two or more
         memory blocks have been joined together and the underlying byte sources can't be joined.
        @return a list of SourceInfo objects, one for each different source of bytes in this block.
        """
        ...

    def getSourceName(self) -> unicode:
        """
        Get the name of the source of this memory block.
        @return source name
        """
        ...

    def getStart(self) -> ghidra.program.model.address.Address:
        """
        Return the starting address for this block.
        @return block's start address
        """
        ...

    def getType(self) -> ghidra.program.model.mem.MemoryBlockType:
        """
        Get the type for this block: DEFAULT, BIT_MAPPED, or BYTE_MAPPED
         (see {@link MemoryBlockType}).
        @return memory block type
        """
        ...

    def hashCode(self) -> int: ...

    def isArtificial(self) -> bool:
        """
        Returns the artificial attribute state of this block. This attribute is
         generally associated with blocks which have been fabricated to facilitate 
         analysis but do not exist in the same form within a running/loaded process
         state.
        @return true if enabled else false
        """
        ...

    def isExecute(self) -> bool:
        """
        Returns the value of the execute property associated with this block
        @return true if enabled else false
        """
        ...

    def isExternalBlock(self) -> bool:
        """
        Returns true if this is a reserved EXTERNAL memory block based upon its name
         (see {@link MemoryBlock#EXTERNAL_BLOCK_NAME}).  Checks for individual addresses may be done
         using {@link Memory#isExternalBlockAddress(Address)}.
         <p>
         Note that EXTERNAL blocks always resides within a memory space and never within the artifial
         {@link AddressSpace#EXTERNAL_SPACE} which is not a memory space.  This can be a source of confusion.
         An EXTERNAL memory block exists to facilitate relocation processing for some external
         symbols which require a real memory address.
        @return true if this is a reserved EXTERNAL memory block
        """
        ...

    def isInitialized(self) -> bool:
        """
        Return whether this block has been initialized.
         <p>
         WARNING: A mapped memory block may have a mix of intialized, uninitialized, and undefined 
         regions.  The value returned by this method for a mapped memory block is always false 
         even if some regions are initialized.
        @return true if block is fully initialized and not a memory-mapped-block, else false
        """
        ...

    def isLoaded(self) -> bool:
        """
        Returns true if this memory block is a real loaded block (i.e. RAM) and not a special block
         containing file header data such as debug sections.
        @return true if this is a loaded block and not a "special" block such as a file header.
        """
        ...

    def isMapped(self) -> bool:
        """
        Returns true if this is either a bit-mapped or byte-mapped block
        @return true if this is either a bit-mapped or byte-mapped block
        """
        ...

    def isOverlay(self) -> bool:
        """
        Returns true if this is an overlay block (i.e., contained within overlay space).
        @return true if this is an overlay block
        """
        ...

    def isRead(self) -> bool:
        """
        Returns the value of the read property associated with this block
        @return true if enabled else false
        """
        ...

    def isVolatile(self) -> bool:
        """
        Returns the volatile attribute state of this block. This attribute is
         generally associated with block of I/O regions of memory.
        @return true if enabled else false
        """
        ...

    def isWrite(self) -> bool:
        """
        Returns the value of the write property associated with this block
        @return true if enabled else false
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def putByte(self, addr: ghidra.program.model.address.Address, b: int) -> None:
        """
        Puts the given byte at the given address in this block.
        @param addr the address.
        @param b byte value
        @throws MemoryAccessException if the block is uninitialized
        @throws IllegalArgumentException if the Address is not in this block.
        """
        ...

    @overload
    def putBytes(self, addr: ghidra.program.model.address.Address, b: List[int]) -> int:
        """
        Tries to put b.length bytes from the specified byte array to this block. All the bytes may
         not be put if the requested length is beyond the end of the block.
        @param addr the address of where to put the bytes.
        @param b the byte array containing the bytes to write.
        @return the number of bytes actually written.
        @throws MemoryAccessException if the block is uninitialized
        @throws IllegalArgumentException if the Address is not in this block.
        """
        ...

    @overload
    def putBytes(self, addr: ghidra.program.model.address.Address, b: List[int], off: int, len: int) -> int:
        """
        Tries to put len bytes from the specified byte array to this block. All the bytes may not be
         written if the requested length is beyond the end of the block.
        @param addr the address of where to put the bytes.
        @param b the byte array containing the bytes to write.
        @param off the offset into the byte array.
        @param len the number of bytes to write.
        @return the number of bytes actually written.
        @throws IndexOutOfBoundsException if invalid offset is specified
        @throws MemoryAccessException if the block is uninitialized
        @throws IllegalArgumentException if the Address is not in this block.
        """
        ...

    def setArtificial(self, a: bool) -> None:
        """
        Sets the artificial attribute state associated with this block. This attribute is
         generally associated with blocks which have been fabricated to facilitate 
         analysis but do not exist in the same form within a running/loaded process
         state.
        @param a the artificial attribute state.
        """
        ...

    def setComment(self, comment: unicode) -> None:
        """
        Set the comment associated with this block.
        @param comment the comment to associate with this block.
        """
        ...

    def setExecute(self, e: bool) -> None:
        """
        Sets the execute property associated with this block.
        @param e the value to set the execute property to.
        """
        ...

    def setName(self, name: unicode) -> None:
        """
        Set the name for this block (See {@link NamingUtilities#isValidName(String)} for naming
         rules). Specified name must not conflict with an address space name.
        @param name the new name for this block.
        @throws IllegalArgumentException if invalid name specified
        @throws LockException renaming an Overlay block without exclusive access
        """
        ...

    def setPermissions(self, read: bool, write: bool, execute: bool) -> None:
        """
        Sets the read, write, execute permissions on this block
        @param read the read permission
        @param write the write permission
        @param execute the execute permission
        """
        ...

    def setRead(self, r: bool) -> None:
        """
        Sets the read property associated with this block.
        @param r the value to set the read property to.
        """
        ...

    def setSourceName(self, sourceName: unicode) -> None:
        """
        Sets the name of the source file that provided the data.
        @param sourceName the name of the source file.
        """
        ...

    def setVolatile(self, v: bool) -> None:
        """
        Sets the volatile attribute state associated of this block.  This attribute is
         generally associated with block of I/O regions of memory.
        @param v the volatile attribute state.
        """
        ...

    def setWrite(self, w: bool) -> None:
        """
        Sets the write property associated with this block.
        @param w the value to set the write property to.
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
    def addressRange(self) -> ghidra.program.model.address.AddressRange: ...

    @property
    def artificial(self) -> bool: ...

    @artificial.setter
    def artificial(self, value: bool) -> None: ...

    @property
    def comment(self) -> unicode: ...

    @comment.setter
    def comment(self, value: unicode) -> None: ...

    @property
    def data(self) -> java.io.InputStream: ...

    @property
    def end(self) -> ghidra.program.model.address.Address: ...

    @property
    def execute(self) -> bool: ...

    @execute.setter
    def execute(self, value: bool) -> None: ...

    @property
    def externalBlock(self) -> bool: ...

    @property
    def flags(self) -> int: ...

    @property
    def initialized(self) -> bool: ...

    @property
    def loaded(self) -> bool: ...

    @property
    def mapped(self) -> bool: ...

    @property
    def name(self) -> unicode: ...

    @name.setter
    def name(self, value: unicode) -> None: ...

    @property
    def overlay(self) -> bool: ...

    @property
    def read(self) -> bool: ...

    @read.setter
    def read(self, value: bool) -> None: ...

    @property
    def size(self) -> long: ...

    @property
    def sizeAsBigInteger(self) -> long: ...

    @property
    def sourceInfos(self) -> List[object]: ...

    @property
    def sourceName(self) -> unicode: ...

    @sourceName.setter
    def sourceName(self, value: unicode) -> None: ...

    @property
    def start(self) -> ghidra.program.model.address.Address: ...

    @property
    def type(self) -> ghidra.program.model.mem.MemoryBlockType: ...

    @property
    def volatile(self) -> bool: ...

    @volatile.setter
    def volatile(self, value: bool) -> None: ...

    @property
    def write(self) -> bool: ...

    @write.setter
    def write(self, value: bool) -> None: ...