from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.BinaryReader
import ghidra.util
import java.io
import java.lang


class BinaryReader(object):
    """
    A class for reading data from a
     generic byte provider in either big-endian or little-endian.
    """

    SIZEOF_BYTE: int = 1
    SIZEOF_INT: int = 4
    SIZEOF_LONG: int = 8
    SIZEOF_SHORT: int = 2




    class ReaderFunction(object):








        def equals(self, __a0: object) -> bool: ...

        def get(self, __a0: ghidra.app.util.bin.BinaryReader) -> object: ...

        def getClass(self) -> java.lang.Class: ...

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






    class InputStreamReaderFunction(object):








        def equals(self, __a0: object) -> bool: ...

        def get(self, __a0: java.io.InputStream) -> object: ...

        def getClass(self) -> java.lang.Class: ...

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



    @overload
    def __init__(self, provider: ghidra.app.util.bin.ByteProvider, isLittleEndian: bool):
        """
        Constructs a reader using the given ByteProvider and endian-order.

         If isLittleEndian is true, then all values read
         from the file will be done so assuming
         little-endian order.

         Otherwise, if isLittleEndian
         is false, then all values will be read
         assuming big-endian order.
        @param provider the byte provider
        @param isLittleEndian the endian-order
        """
        ...

    @overload
    def __init__(self, provider: ghidra.app.util.bin.ByteProvider, converter: ghidra.util.DataConverter, initialIndex: long):
        """
        Creates a BinaryReader instance.
        @param provider the ByteProvider to use
        @param converter the {@link DataConverter} to use
        @param initialIndex the initial offset
        """
        ...



    def align(self, alignValue: int) -> int:
        """
        Advances the current index so that it aligns to the specified value (if not already
         aligned).
         <p>
         For example, if current index was 123 and align value was 16, then current index would
         be advanced to 128.
        @param alignValue position index alignment
        @return the number of bytes required to align (0..alignValue-1)
        """
        ...

    def asBigEndian(self) -> ghidra.app.util.bin.BinaryReader:
        """
        Returns a BinaryReader that is in BigEndian mode.
        @return a new independent BinaryReader, at the same position, in BigEndian mode
        """
        ...

    def asLittleEndian(self) -> ghidra.app.util.bin.BinaryReader:
        """
        Returns a BinaryReader that is in LittleEndian mode.
        @return a new independent instance, at the same position, in LittleEndian mode
        """
        ...

    @overload
    def clone(self) -> ghidra.app.util.bin.BinaryReader:
        """
        Returns an independent clone of this reader positioned at the same index.
        @return a independent clone of this reader positioned at the same index
        """
        ...

    @overload
    def clone(self, newIndex: long) -> ghidra.app.util.bin.BinaryReader:
        """
        Returns a clone of this reader, with its own independent current position,
         positioned at the new index.
        @param newIndex the new index
        @return an independent clone of this reader positioned at the new index
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getByteProvider(self) -> ghidra.app.util.bin.ByteProvider:
        """
        Returns the underlying byte provider.
        @return the underlying byte provider
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getInputStream(self) -> java.io.InputStream:
        """
        Returns an InputStream that is a live view of the BinaryReader's position.
         <p>
         Any bytes read with the stream will affect the current position of the BinaryReader, and
         any change to the BinaryReader's position will affect the next value the inputstream returns.
        @return {@link InputStream}
        """
        ...

    def getPointerIndex(self) -> long:
        """
        Returns the current index value.
        @return the current index value
        """
        ...

    @overload
    def hasNext(self) -> bool:
        """
        Returns true if this stream has data that could be read at the current position.
        @return true if there are more bytes that could be read at the 
         {@link #getPointerIndex() current index}.
        """
        ...

    @overload
    def hasNext(self, count: int) -> bool:
        """
        Returns true if this stream has data that could be read at the current position.
        @param count number of bytes to verify
        @return true if there are at least count more bytes that could be read at the 
         {@link #getPointerIndex() current index}.
        """
        ...

    def hashCode(self) -> int: ...

    def isBigEndian(self) -> bool:
        """
        Returns true if this reader will extract values in big endian.
        @return true is big endian, false is little endian
        """
        ...

    def isLittleEndian(self) -> bool:
        """
        Returns true if this reader will extract values in little endian,
         otherwise in big endian.
        @return true is little endian, false is big endian
        """
        ...

    @overload
    def isValidIndex(self, index: long) -> bool:
        """
        Returns true if the specified index into the underlying byte provider is valid.
        @param index the index in the byte provider
        @return returns true if the specified index is valid
        """
        ...

    @overload
    def isValidIndex(self, index: int) -> bool:
        """
        Returns true if the specified unsigned int32 index into the underlying byte provider is
         valid.
        @param index an integer that is treated as an unsigned int32 index into the byte provider
        @return returns true if the specified index is valid
        """
        ...

    def isValidRange(self, startIndex: long, count: int) -> bool:
        """
        Returns true if the specified range is valid and does not wrap around the end of the 
         index space.
        @param startIndex the starting index to check, treated as an unsigned int64
        @param count the number of bytes to check
        @return boolean true if all bytes between startIndex to startIndex+count (exclusive) are 
         valid (according to the underlying byte provider)
        """
        ...

    def length(self) -> long:
        """
        Returns the length of the underlying file.
        @return returns the length of the underlying file
        @exception IOException if an I/O error occurs
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def peekNextByte(self) -> int:
        """
        Peeks at the next byte without incrementing
         the current index.
        @return the next byte
        @exception IOException if an I/O error occurs
        """
        ...

    def peekNextInt(self) -> int:
        """
        Peeks at the next integer without incrementing
         the current index.
        @return the next int
        @exception IOException if an I/O error occurs
        """
        ...

    def peekNextLong(self) -> long:
        """
        Peeks at the next long without incrementing
         the current index.
        @return the next long
        @exception IOException if an I/O error occurs
        """
        ...

    def peekNextShort(self) -> int:
        """
        Peeks at the next short without incrementing
         the current index.
        @return the next short
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readAsciiString(self, index: long) -> unicode:
        """
        Reads a null terminated US-ASCII string, starting at specified index, stopping at
         the first null character.
         <p>
         Note: this method no longer trims() the returned String.
         <p>
        @param index starting position of the string
        @return US-ASCII string, excluding the trailing null terminator character
        @throws IOException if error reading bytes
        """
        ...

    @overload
    def readAsciiString(self, index: long, length: int) -> unicode:
        """
        Reads an fixed length US-ASCII string starting at <code>index</code>.
         <p>
         Trailing null terminator characters will be removed.  (suitable for reading
         a string from a fixed length field that is padded with trailing null chars)
         <p>
         Note: this method no longer trims() the returned String.
         <p>
        @param index where the string begins
        @param length number of bytes to read
        @return the US-ASCII string
        @exception IOException if an I/O error occurs
        """
        ...

    def readByte(self, index: long) -> int:
        """
        Returns the signed BYTE at <code>index</code>.
        @param index the index where the BYTE begins
        @return the signed BYTE
        @exception IOException if an I/O error occurs
        """
        ...

    def readByteArray(self, index: long, nElements: int) -> List[int]:
        """
        Returns the BYTE array of <code>nElements</code>
         starting at <code>index</code>.
        @param index the index where the BYTE begins
        @param nElements the number of array elements
        @return the BYTE array
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readInt(self, index: long) -> int:
        """
        Returns the signed INTEGER at <code>index</code>.
        @param index the index where the INTEGER begins
        @return the signed INTEGER
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readInt(self, dc: ghidra.util.DataConverter, index: long) -> int:
        """
        Returns the signed INTEGER at <code>index</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index the index where the INTEGER begins
        @return the signed INTEGER
        @exception IOException if an I/O error occurs
        """
        ...

    def readIntArray(self, index: long, nElements: int) -> List[int]:
        """
        Returns the INTEGER array of <code>nElements</code>
         starting at <code>index</code>.
        @param index the index where the INTEGER begins
        @param nElements the number of array elements
        @return the INTEGER array
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readLong(self, index: long) -> long:
        """
        Returns the signed LONG at <code>index</code>.
        @param index the index where the LONG begins
        @return the LONG
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readLong(self, dc: ghidra.util.DataConverter, index: long) -> long:
        """
        Returns the signed LONG at <code>index</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index the index where the LONG begins
        @return the LONG
        @exception IOException if an I/O error occurs
        """
        ...

    def readLongArray(self, index: long, nElements: int) -> List[long]:
        """
        Returns the LONG array of <code>nElements</code>
         starting at <code>index</code>.
        @param index the index where the LONG begins
        @param nElements the number of array elements
        @return the LONG array
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNext(self, func: ghidra.app.util.bin.BinaryReader.InputStreamReaderFunction) -> object:
        """
        Reads an object from the current position, using the supplied reader function.
        @param <T> type of the object that will be returned
        @param func {@link InputStreamReaderFunction} that will read and return an object
        @return new object of type T
        @throws IOException if error reading
        """
        ...

    @overload
    def readNext(self, func: ghidra.app.util.bin.BinaryReader.ReaderFunction) -> object:
        """
        Reads an object from the current position, using the supplied reader function.
        @param <T> type of the object that will be returned
        @param func {@link ReaderFunction} that will read and return an object
        @return new object of type T
        @throws IOException if error reading
        """
        ...

    @overload
    def readNextAsciiString(self) -> unicode:
        """
        Reads a null terminated US-ASCII string starting at the current index,
         advancing the current index by the length of the string that was found.
         <p>
         Note: this method no longer trims() the returned String.
         <p>
        @return the US-ASCII string at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextAsciiString(self, length: int) -> unicode:
        """
        Reads a fixed length US-ASCII string starting at the current index,
         advancing the current index by the specified fixed length.
         <p>
         Trailing null terminator characters will be removed.  (suitable for reading
         a string from a fixed length field that is padded with trailing null chars)
         <p>
         Note: this method no longer trims() the returned String.
         <p>
        @param length number of bytes to read
        @return the US-ASCII string at the current index
        """
        ...

    def readNextByte(self) -> int:
        """
        Reads the byte at the current index and then increments the current
         index by <code>SIZEOF_BYTE</code>.
        @return the byte at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    def readNextByteArray(self, nElements: int) -> List[int]:
        """
        Reads a byte array of <code>nElements</code>
         starting at the current index and then increments the current
         index by <code>SIZEOF_BYTE * nElements</code>.
        @return the byte array starting at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextInt(self) -> int:
        """
        Reads the integer at the current index and then increments the current
         index by <code>SIZEOF_INT</code>.
        @return the integer at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextInt(self, dc: ghidra.util.DataConverter) -> int:
        """
        Reads the integer at the current index and then increments the current
         index by <code>SIZEOF_INT</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @return the integer at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    def readNextIntArray(self, nElements: int) -> List[int]:
        """
        Reads an integer array of <code>nElements</code>
         starting at the current index and then increments the current
         index by <code>SIZEOF_INT * nElements</code>.
        @param nElements number of elements to read
        @return the integer array starting at the current index
        @throws IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextLong(self) -> long:
        """
        Reads the long at the current index and then increments the current
         index by <code>SIZEOF_LONG</code>.
        @return the long at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextLong(self, dc: ghidra.util.DataConverter) -> long:
        """
        Reads the long at the current index and then increments the current
         index by <code>SIZEOF_LONG</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @return the long at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    def readNextLongArray(self, nElements: int) -> List[long]:
        """
        Reads a long array of <code>nElements</code>
         starting at the current index and then increments the current
         index by <code>SIZEOF_LONG * nElements</code>.
        @param nElements number of elements to read
        @return the long array starting at the current index
        @throws IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextShort(self) -> int:
        """
        Reads the short at the current index and then increments the current
         index by <code>SIZEOF_SHORT</code>.
        @return the short at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextShort(self, dc: ghidra.util.DataConverter) -> int:
        """
        Reads the short at the current index and then increments the current
         index by <code>SIZEOF_SHORT</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @return the short at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    def readNextShortArray(self, nElements: int) -> List[int]:
        """
        Reads a short array of <code>nElements</code>
         starting at the current index and then increments the current
         index by <code>SIZEOF_SHORT * nElements</code>.
        @return the short array starting at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnicodeString(self) -> unicode:
        """
        Reads a null-terminated UTF-16 Unicode string at the current index, 
         advancing the current index by the length of the string that was found.
         <p>
        @return UTF-16 string at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnicodeString(self, charCount: int) -> unicode:
        """
        Reads a fixed length UTF-16 Unicode string at the current index,
         advancing the current index by the length of the string that was found.
         <p>
        @param charCount number of UTF-16 characters to read (not bytes)
        @return the UTF-16 Unicode string at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    def readNextUnsignedByte(self) -> int:
        """
        Reads the unsigned byte at the current index and then increments the current
         index by <code>SIZEOF_BYTE</code>.
        @return the unsigned byte at the current index, as an int
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedInt(self) -> long:
        """
        Reads the unsigned integer at the current index and then increments the current
         index by <code>SIZEOF_INT</code>.
        @return the unsigned integer at the current index, as a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedInt(self, dc: ghidra.util.DataConverter) -> long:
        """
        Reads the unsigned integer at the current index and then increments the current
         index by <code>SIZEOF_INT</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @return the unsigned integer at the current index, as a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedIntExact(self) -> int:
        """
        Reads an unsigned int32 value, and returns it as a java int (instead of a java long).
         <p>
         If the value is outside the range of 0..Integer.MAX_VALUE, an InvalidDataException is thrown.
         <p>
         Useful for reading uint32 values that are going to be used in java to allocate arrays or
         other similar cases where the value must be a java integer.
        @return the uint32 value read from the stream, if it fits into the range [0..MAX_VALUE] 
         of a java integer
        @throws IOException if there was an error reading
        @throws InvalidDataException if value can not be held in a java integer
        """
        ...

    @overload
    def readNextUnsignedIntExact(self, dc: ghidra.util.DataConverter) -> int:
        """
        Reads an unsigned int32 value, and returns it as a java int (instead of a java long).
         <p>
         If the value is outside the range of 0..Integer.MAX_VALUE, an InvalidDataException is thrown.
         <p>
         Useful for reading uint32 values that are going to be used in java to allocate arrays or
         other similar cases where the value must be a java integer.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @return the uint32 value read from the stream, if it fits into the range [0..MAX_VALUE] 
         of a java integer
        @throws IOException if there was an error reading
        @throws InvalidDataException if value can not be held in a java integer
        """
        ...

    @overload
    def readNextUnsignedShort(self) -> int:
        """
        Reads the unsigned short at the current index and then increments the current
         index by <code>SIZEOF_SHORT</code>.
        @return the unsigned short at the current index, as an int
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedShort(self, dc: ghidra.util.DataConverter) -> int:
        """
        Reads the unsigned short at the current index and then increments the current
         index by <code>SIZEOF_SHORT</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @return the unsigned short at the current index, as an int
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedValue(self, len: int) -> long:
        """
        Returns the unsigned value of the integer (of the specified length) at the current index.
        @param len the number of bytes that the integer occupies, 1 to 8
        @return unsigned value of requested length, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedValue(self, dc: ghidra.util.DataConverter, len: int) -> long:
        """
        Returns the unsigned value of the integer (of the specified length) at the current index.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param len the number of bytes that the integer occupies, 1 to 8
        @return unsigned value of requested length, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUnsignedVarIntExact(self, func: ghidra.app.util.bin.BinaryReader.InputStreamReaderFunction) -> int:
        """
        Reads a variable length / unknown format unsigned integer from the current position, using
         the supplied reader function, returning it (if it fits) as a 32 bit java integer.
        @param func {@link InputStreamReaderFunction}
        @return unsigned int32
        @throws IOException if error reading data
        @throws InvalidDataException if value can not be held in a java integer
        """
        ...

    @overload
    def readNextUnsignedVarIntExact(self, func: ghidra.app.util.bin.BinaryReader.ReaderFunction) -> int:
        """
        Reads a variable length / unknown format unsigned integer from the current position, using
         the supplied reader function, returning it (if it fits) as a 32 bit java integer.
        @param func {@link ReaderFunction}
        @return unsigned int32
        @throws IOException if error reading data
        @throws InvalidDataException if value can not be held in a java integer
        """
        ...

    @overload
    def readNextUtf8String(self) -> unicode:
        """
        Reads a null-terminated UTF-8 string at the current index, 
         advancing the current index by the length of the string that was found.
         <p>
        @return UTF-8 string at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextUtf8String(self, length: int) -> unicode:
        """
        Reads a fixed length UTF-8 string the current index,
         advancing the current index by the length of the string that was found.
         <p>
        @param length number of bytes to read
        @return the UTF-8 string at the current index
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextValue(self, len: int) -> long:
        """
        Returns the signed value of the integer (of the specified length) at the current index.
        @param len the number of bytes that the integer occupies, 1 to 8
        @return value of requested length, with sign bit extended, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextValue(self, dc: ghidra.util.DataConverter, len: int) -> long:
        """
        Returns the signed value of the integer (of the specified length) at the current index.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param len the number of bytes that the integer occupies, 1 to 8
        @return value of requested length, with sign bit extended, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readNextVarInt(self, func: ghidra.app.util.bin.BinaryReader.InputStreamReaderFunction) -> int:
        """
        Reads a variable length / unknown format integer from the current position, using the
         supplied reader function, returning it (if it fits) as a 32 bit java integer.
        @param func {@link InputStreamReaderFunction}
        @return signed int32
        @throws IOException if error reading or if the value does not fit into a 32 bit java int
        @throws InvalidDataException if value can not be held in a java integer
        """
        ...

    @overload
    def readNextVarInt(self, func: ghidra.app.util.bin.BinaryReader.ReaderFunction) -> int:
        """
        Reads a variable length / unknown format integer from the current position, using the
         supplied reader function, returning it (if it fits) as a 32 bit java integer.
        @param func {@link ReaderFunction}
        @return signed int32
        @throws IOException if error reading or if the value does not fit into a 32 bit java int
        @throws InvalidDataException if value can not be held in a java integer
        """
        ...

    @overload
    def readShort(self, index: long) -> int:
        """
        Returns the signed SHORT at <code>index</code>.
        @param index the index where the SHORT begins
        @return the signed SHORT
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readShort(self, dc: ghidra.util.DataConverter, index: long) -> int:
        """
        Returns the signed SHORT at <code>index</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index the index where the SHORT begins
        @return the signed SHORT
        @exception IOException if an I/O error occurs
        """
        ...

    def readShortArray(self, index: long, nElements: int) -> List[int]:
        """
        Returns the SHORT array of <code>nElements</code>
         starting at <code>index</code>.
        @param index the index where the SHORT begins
        @param nElements the number of array elements
        @return the SHORT array
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnicodeString(self, index: long) -> unicode:
        """
        Reads a null-terminated UTF-16 Unicode string starting at <code>index</code> and using 
         the pre-specified {@link #setLittleEndian(boolean) endianness}.
         <p>
         The end of the string is denoted by a two-byte (ie. short) <code>null</code> character.
         <p>
        @param index where the UTF-16 Unicode string begins
        @return the UTF-16 Unicode string
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnicodeString(self, index: long, charCount: int) -> unicode:
        """
        Reads a fixed length UTF-16 Unicode string of <code>length</code> characters
         starting at <code>index</code>, using the pre-specified
         {@link #setLittleEndian(boolean) endianness}.
         <p>
         Trailing null terminator characters will be removed.  (suitable for reading
         a string from a fixed length field that is padded with trailing null chars)
         <p>
        @param index the index where the UTF-16 Unicode string begins
        @param charCount the number of UTF-16 character elements to read.
        @return the UTF-16 Unicode string
        @exception IOException if an I/O error occurs
        """
        ...

    def readUnsignedByte(self, index: long) -> int:
        """
        Returns the unsigned BYTE at <code>index</code>.
        @param index the index where the BYTE begins
        @return the unsigned BYTE as an int
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnsignedInt(self, index: long) -> long:
        """
        Returns the unsigned INTEGER at <code>index</code>.
        @param index the index where the INTEGER begins
        @return the unsigned INTEGER as a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnsignedInt(self, dc: ghidra.util.DataConverter, index: long) -> long:
        """
        Returns the unsigned INTEGER at <code>index</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index the index where the INTEGER begins
        @return the unsigned INTEGER as a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnsignedShort(self, index: long) -> int:
        """
        Returns the unsigned SHORT at <code>index</code>.
        @param index the index where the SHORT begins
        @return the unsigned SHORT as an int
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnsignedShort(self, dc: ghidra.util.DataConverter, index: long) -> int:
        """
        Returns the unsigned SHORT at <code>index</code>.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index the index where the SHORT begins
        @return the unsigned SHORT as an int
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnsignedValue(self, index: long, len: int) -> long:
        """
        Returns the unsigned value of the integer (of the specified length) at the specified offset.
        @param index where the value begins
        @param len the number of bytes that the integer occupies, 1 to 8
        @return unsigned value of requested length, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUnsignedValue(self, dc: ghidra.util.DataConverter, index: long, len: int) -> long:
        """
        Returns the unsigned value of the integer (of the specified length) at the specified offset.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index where the value begins
        @param len the number of bytes that the integer occupies, 1 to 8
        @return unsigned value of requested length, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUtf8String(self, index: long) -> unicode:
        """
        Reads a null-terminated UTF-8 string starting at <code>index</code>.
         <p>
        @param index where the UTF-8 string begins
        @return the string
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readUtf8String(self, index: long, length: int) -> unicode:
        """
        Reads a fixed length UTF-8 string of <code>length</code> bytes
         starting at <code>index</code>.
         <p>
         Trailing null terminator characters will be removed.  (suitable for reading
         a string from a fixed length field that is padded with trailing null chars)
         <p>
        @param index the index where the UTF-8 string begins
        @param length the number of bytes to read
        @return the string
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readValue(self, index: long, len: int) -> long:
        """
        Returns the signed value of the integer (of the specified length) at the specified offset.
        @param index where the value begins
        @param len the number of bytes that the integer occupies, 1 to 8
        @return value of requested length, with sign bit extended, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    @overload
    def readValue(self, dc: ghidra.util.DataConverter, index: long, len: int) -> long:
        """
        Returns the signed value of the integer (of the specified length) at the specified offset.
        @param dc {@link BigEndianDataConverter BE} or {@link LittleEndianDataConverter LE}
        @param index where the value begins
        @param len the number of bytes that the integer occupies, 1 to 8
        @return value of requested length, with sign bit extended, in a long
        @exception IOException if an I/O error occurs
        """
        ...

    def setLittleEndian(self, isLittleEndian: bool) -> None:
        """
        Sets the endian of this binary reader.
        @param isLittleEndian true for little-endian and false for big-endian
        """
        ...

    @overload
    def setPointerIndex(self, index: long) -> long:
        """
        Sets the current index to the specified value.
         The pointer index will allow the reader
         to operate as a pseudo-iterator.
        @param index the byte provider index value
        @return previous reader offset for use with this method to restore previous position.
        """
        ...

    @overload
    def setPointerIndex(self, index: int) -> long:
        """
        A convenience method for setting the index using a 32 bit integer.
        @param index new index, treated as a 32 bit unsigned integer
        @return previous reader offset for use with {@link #setPointerIndex(long)} to restore 
         previous position.
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
    def bigEndian(self) -> bool: ...

    @property
    def byteProvider(self) -> ghidra.app.util.bin.ByteProvider: ...

    @property
    def inputStream(self) -> java.io.InputStream: ...

    @property
    def littleEndian(self) -> bool: ...

    @littleEndian.setter
    def littleEndian(self, value: bool) -> None: ...

    @property
    def pointerIndex(self) -> long: ...

    @pointerIndex.setter
    def pointerIndex(self, value: long) -> None: ...