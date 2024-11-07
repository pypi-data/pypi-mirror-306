from typing import List
from typing import overload
import ghidra.features.base.memsearch.bytesequence
import ghidra.program.model.address
import java.lang


class AddressableByteSequence(object, ghidra.features.base.memsearch.bytesequence.ByteSequence):
    """
    This class provides a ByteSequence view into an AddressableByteSource. By 
     specifying an address and length, this class provides a view into the byte source
     as a indexable sequence of bytes. It is mutable and can be reused by setting a new
     address range for this sequence. This was to avoid constantly allocating large byte arrays.
    """





    def __init__(self, byteSource: ghidra.features.base.memsearch.bytesource.AddressableByteSource, capacity: int):
        """
        Constructor
        @param byteSource the source of the underlying bytes that is a buffer into
        @param capacity the maximum size range that this object will buffer
        """
        ...



    def clear(self) -> None:
        """
        Sets this view to an empty byte sequence
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getAddress(self, index: int) -> ghidra.program.model.address.Address:
        """
        Returns the address of the byte represented by the given index into this buffer.
        @param index the index into the buffer to get its associated address
        @return the Address for the given index
        """
        ...

    def getByte(self, index: int) -> int: ...

    def getBytes(self, index: int, size: int) -> List[int]: ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int: ...

    def hasAvailableBytes(self, index: int, length: int) -> bool: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setRange(self, range: ghidra.program.model.address.AddressRange) -> None:
        """
        Sets the range of bytes that this object will buffer. This immediately will read the bytes
         from the byte source into it's internal byte array buffer.
        @param range the range of bytes to buffer
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
    def length(self) -> int: ...

    @property
    def range(self) -> None: ...  # No getter available.

    @range.setter
    def range(self, value: ghidra.program.model.address.AddressRange) -> None: ...