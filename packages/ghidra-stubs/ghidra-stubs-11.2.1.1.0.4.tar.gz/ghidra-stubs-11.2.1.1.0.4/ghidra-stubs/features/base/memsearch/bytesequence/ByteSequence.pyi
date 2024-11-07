from typing import List
from typing import overload
import java.lang


class ByteSequence(object):
    """
    An interface for accessing bytes from a byte source.
    """









    def equals(self, __a0: object) -> bool: ...

    def getByte(self, index: int) -> int:
        """
        Returns the byte at the given index. The index must between 0 and the extended length.
        @param index the index in the byte sequence to retrieve a byte value
        @return the byte at the given index
        """
        ...

    def getBytes(self, start: int, length: int) -> List[int]:
        """
        Returns a byte array containing the bytes from the given range.
        @param start the start index of the range to get bytes
        @param length the number of bytes to get
        @return a byte array containing the bytes from the given range
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getLength(self) -> int:
        """
        Returns the length of available bytes.
        @return the length of the sequence of bytes
        """
        ...

    def hasAvailableBytes(self, index: int, length: int) -> bool:
        """
        A convenience method for checking if this sequence can provide a range of bytes from some
         offset.
        @param index the index of the start of the range to check for available bytes
        @param length the length of the range to check for available bytes
        @return true if bytes are available for the given range
        """
        ...

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
    def length(self) -> int: ...