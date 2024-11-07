from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format
import ghidra.app.util.bin.format.elf
import ghidra.program.model.address
import ghidra.program.model.data
import java.io
import java.lang
import java.util.function


class ElfProgramHeader(object, ghidra.app.util.bin.StructConverter, java.lang.Comparable, ghidra.app.util.bin.format.MemoryLoadable):
    """
    An executable or shared object file's program header table is an 
     array of structures, each describing a segment
     or other information the system needs to prepare the program for execution. 
     An object file segment contains one or more sections. 
     Program headers are meaningful only for executable 
     and shared object files. A file specifies its 
     own program header size with the ELF
     header's e_phentsize and e_phnum members.
     Some entries describe process segments; others give supplementary information and do not contribute to
     the process image. Segment entries may appear in any order. Except for PT_LOAD segment 
     entries which must appear in ascending order, sorted on the p_vaddr member.
 
 
     typedef struct {
         Elf32_Word   p_type;
         Elf32_Off    p_offset;
         Elf32_Addr   p_vaddr;
         Elf32_Addr   p_paddr;
         Elf32_Word   p_filesz;
         Elf32_Word   p_memsz;
         Elf32_Word   p_flags;
         Elf32_Word   p_align;
     } Elf32_Phdr;
 
     typedef struct {
         Elf64_Word   p_type;         //Segment type
         Elf64_Word   p_flags;        //Segment flags
         Elf64_Off    p_offset;       //Segment file offset
         Elf64_Addr   p_vaddr;        //Segment virtual address
         Elf64_Addr   p_paddr;        //Segment physical address
         Elf64_Xword  p_filesz;       //Segment size in file
         Elf64_Xword  p_memsz;        //Segment size in memory
         Elf64_Xword  p_align;        //Segment alignment
     } Elf64_Phdr;
 
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



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader, header: ghidra.app.util.bin.format.elf.ElfHeader):
        """
        Construct {@link ElfProgramHeader}
        @param reader dedicated reader instance positioned to the start of the program header data.
         (the reader supplied will be retained and altered).
        @param header ELF header
        @throws IOException if an IO error occurs during parse
        """
        ...



    @overload
    def compareTo(self, that: ghidra.app.util.bin.format.elf.ElfProgramHeader) -> int: ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, obj: object) -> bool: ...

    def getAdjustedLoadSize(self) -> long:
        """
        Get the adjusted file load size (i.e., filtered load size) to be loaded into memory block which relates to 
         this program header; it may be zero if no block should be created.  The returned value reflects any adjustment 
         the ElfExtension may require based upon the specific processor/language implementation which may 
         require filtering of file bytes as loaded into memory.
        @return the number of bytes to be loaded into the resulting memory block
        """
        ...

    def getAdjustedMemorySize(self) -> long:
        """
        Get the adjusted memory size in bytes of the memory block which relates to this program header; it may be zero
         if no block should be created.  The returned value reflects any adjustment the ElfExtension may require
         based upon the specific processor/language implementation which may require filtering of file bytes
         as loaded into memory.
        @return the number of bytes in the resulting memory block
        """
        ...

    def getAlign(self) -> long:
        """
        As ''Program Loading'' later in this part describes, loadable process segments must have
         congruent values for p_vaddr and p_offset, modulo the page size. This member
         gives the value to which the segments are aligned in memory and in the file. Values 0
         and 1 mean no alignment is required. Otherwise, p_align should be a positive, integral
         power of 2, and p_vaddr should equal p_offset, modulo p_align.
        @return the segment alignment value
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getComment(self) -> unicode:
        """
        Get descriptive comment which includes type and description
        @return descriptive comment
        """
        ...

    def getDescription(self) -> unicode:
        """
        Get header description
        @return header description
        """
        ...

    def getElfHeader(self) -> ghidra.app.util.bin.format.elf.ElfHeader:
        """
        Return ElfHeader associated with this program header
        @return ElfHeader
        """
        ...

    def getFileSize(self) -> long:
        """
        This member gives the number of bytes in the file image of the segment; it may be zero.
        @return the number of bytes in the file image
        """
        ...

    def getFilteredLoadInputStream(self, elfLoadHelper: ghidra.app.util.bin.format.elf.ElfLoadHelper, start: ghidra.program.model.address.Address, dataLength: long, errorConsumer: java.util.function.BiConsumer) -> java.io.InputStream: ...

    def getFlags(self) -> int:
        """
        This member gives flags relevant to the segment. Defined flag values appear below.
        @return the segment flags
        """
        ...

    def getMemorySize(self) -> long:
        """
        Get the unadjusted memory size in bytes specified by this program header; it may be zero.
        @return the unadjusted memory size in bytes specified by this program header
        """
        ...

    @overload
    def getOffset(self) -> long:
        """
        This member gives the offset from the beginning of the file at which 
         the first byte of the segment resides.
        @return the offset from the beginning of the file
        """
        ...

    @overload
    def getOffset(self, virtualAddress: long) -> long:
        """
        Compute the file offset associated with the specified loaded virtual address 
         defined by this PT_LOAD program header.  This can be useful when attempting to locate
         addresses defined by the PT_DYNAMIC section.
        @param virtualAddress a memory address which has already had the PRElink adjustment applied
        @return computed file offset or -1 if virtual address not contained within this header
        @see ElfHeader#getProgramLoadHeaderContaining(long) for obtaining PT_LOAD segment which contains
         virtualAddress
        """
        ...

    def getPhysicalAddress(self) -> long:
        """
        On systems for which physical addressing is relevant, this member is reserved for the
         segment's physical address. Because System V ignores physical addressing for application
         programs, this member has unspecified contents for executable files and shared objects.
        @return the segment's physical address
        """
        ...

    def getRawInputStream(self) -> java.io.InputStream: ...

    def getReader(self) -> ghidra.app.util.bin.BinaryReader:
        """
        Returns the binary reader.
        @return the binary reader
        """
        ...

    def getType(self) -> int:
        """
        This member tells what kind of segment this array element describes or how to interpret
         the array element's information. Type values and their meanings appear below.
        @return the program header type
        """
        ...

    def getTypeAsString(self) -> unicode:
        """
        Get header type as string.  ElfProgramHeaderType name will be returned
         if know, otherwise a numeric name of the form "PT_0x12345678" will be returned.
        @return header type as string
        """
        ...

    def getVirtualAddress(self) -> long:
        """
        This member gives the virtual address at which the first 
         byte of the segment resides in memory.
        @return the virtual address
        """
        ...

    def hasFilteredLoadInputStream(self, elfLoadHelper: ghidra.app.util.bin.format.elf.ElfLoadHelper, start: ghidra.program.model.address.Address) -> bool: ...

    def hashCode(self) -> int: ...

    def isExecute(self) -> bool:
        """
        Returns true if this segment is executable when loaded
        @return true if this segment is executable when loaded
        """
        ...

    def isInvalidOffset(self) -> bool:
        """
        Return true if this program header's offset is invalid.
        @return true if this program header's offset is invalid
        """
        ...

    def isRead(self) -> bool:
        """
        Returns true if this segment is readable when loaded
        @return true if this segment is readable when loaded
        """
        ...

    def isWrite(self) -> bool:
        """
        Returns true if this segment is writable when loaded
        @return true if this segment is writable when loaded
        """
        ...

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
    def adjustedLoadSize(self) -> long: ...

    @property
    def adjustedMemorySize(self) -> long: ...

    @property
    def align(self) -> long: ...

    @property
    def comment(self) -> unicode: ...

    @property
    def description(self) -> unicode: ...

    @property
    def elfHeader(self) -> ghidra.app.util.bin.format.elf.ElfHeader: ...

    @property
    def execute(self) -> bool: ...

    @property
    def fileSize(self) -> long: ...

    @property
    def flags(self) -> int: ...

    @property
    def invalidOffset(self) -> bool: ...

    @property
    def memorySize(self) -> long: ...

    @property
    def offset(self) -> long: ...

    @property
    def physicalAddress(self) -> long: ...

    @property
    def rawInputStream(self) -> java.io.InputStream: ...

    @property
    def read(self) -> bool: ...

    @property
    def reader(self) -> ghidra.app.util.bin.BinaryReader: ...

    @property
    def type(self) -> int: ...

    @property
    def typeAsString(self) -> unicode: ...

    @property
    def virtualAddress(self) -> long: ...

    @property
    def write(self) -> bool: ...