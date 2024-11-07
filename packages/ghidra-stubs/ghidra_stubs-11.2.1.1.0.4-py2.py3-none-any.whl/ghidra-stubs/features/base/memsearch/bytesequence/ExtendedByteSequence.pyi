from typing import List
from typing import overload
import ghidra.features.base.memsearch.bytesequence
import java.lang


class ExtendedByteSequence(object, ghidra.features.base.memsearch.bytesequence.ByteSequence):
    """
    A class for accessing a contiguous sequence of bytes from some underlying byte source to 
     be used for searching for a byte pattern within the byte source. This sequence of bytes 
     consists of two parts; the primary sequence and an extended sequence. Search matches
     must begin in the primary sequence, but may extend into the extended sequence.
 
     Searching large ranges of memory can be partitioned into searching smaller chunks. But
     to handle search sequences that span chunks, two chunks are presented at a time, with the second
     chunk being the extended bytes. On the next iteration of the search loop, the extended chunk
     will become the primary chunk, with the next chunk after that becoming the extended sequence
     and so on.
    """





    def __init__(self, main: ghidra.features.base.memsearch.bytesequence.ByteSequence, extended: ghidra.features.base.memsearch.bytesequence.ByteSequence, extendedLimit: int):
        """
        Constructs an extended byte sequence from two {@link ByteSequence}s.
        @param main the byte sequence where search matches may start
        @param extended the byte sequence where search matches may extend into
        @param extendedLimit specifies how much of the extended byte sequence to allow search
         matches to extend into. (The extended buffer will be the primary buffer next time, so
         it is a full size buffer, but we only need to use a portion of it to support overlap.
        """
        ...



    def equals(self, __a0: object) -> bool: ...

    def getByte(self, i: int) -> int: ...

    def getBytes(self, index: int, size: int) -> List[int]: ...

    def getClass(self) -> java.lang.Class: ...

    def getExtendedLength(self) -> int:
        """
        Returns the overall length of sequence of available bytes. This will be the length of
         the primary sequence as returned by {@link #getLength()} plus the length of the available
         extended bytes, if any.
        @return the
        """
        ...

    def getLength(self) -> int: ...

    def hasAvailableBytes(self, index: int, length: int) -> bool: ...

    def hashCode(self) -> int: ...

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
    def extendedLength(self) -> int: ...

    @property
    def length(self) -> int: ...