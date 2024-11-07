from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.app.util.bin.format.omf.omf
import ghidra.program.model.data
import java.lang


class OmfData(ghidra.app.util.bin.format.omf.OmfRecord, java.lang.Comparable):
    """
    Object representing data loaded directly into the final image.
    """





    def __init__(self, reader: ghidra.app.util.bin.BinaryReader): ...



    def calcCheckSum(self) -> int:
        """
        Computes the record's checksum
        @return The record's checksum
        @throws IOException if an IO-related error occurred
        """
        ...

    @overload
    def compareTo(self, o: ghidra.app.util.bin.format.omf.omf.OmfData) -> int:
        """
        Compare datablocks by data offset
        @return a value less than 0 for lower address, 0 for same address, or greater than 0 for
           higher address
        """
        ...

    @overload
    def compareTo(self, __a0: object) -> int: ...

    def equals(self, __a0: object) -> bool: ...

    def getByteArray(self, reader: ghidra.app.util.bin.BinaryReader) -> List[int]:
        """
        Create a byte array holding the data represented by this object. The length
         of the byte array should exactly match the value returned by getLength()
        @param reader is for pulling bytes directly from the binary image
        @return allocated and filled byte array
        @throws IOException for problems accessing data through the reader
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getData(self) -> List[int]: ...

    def getDataOffset(self) -> long:
        """
        @return the starting offset, within the loaded image, of this data
        """
        ...

    def getLength(self) -> int:
        """
        @return the length of this data in bytes
        """
        ...

    def getRecordChecksum(self) -> int: ...

    def getRecordLength(self) -> int:
        """
        {@return the record length}
        """
        ...

    def getRecordOffset(self) -> long:
        """
        {@return the record offset}
        """
        ...

    def getRecordType(self) -> int:
        """
        {@return the record type}
        """
        ...

    def getSegmentIndex(self) -> int:
        """
        @return get the segments index for this datablock
        """
        ...

    def hasBigFields(self) -> bool:
        """
        {@return true if this record has big fields; otherwise, false}
        """
        ...

    def hashCode(self) -> int: ...

    def isAllZeroes(self) -> bool:
        """
        @return true if this is a block entirely of zeroes
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseData(self) -> None:
        """
        Parses this {@link OmfRecord}'s type-spefic data
        @throws IOException if there was an IO-related error
        @throws OmfException if there was a problem with the OMF specification
        """
        ...

    def toDataType(self) -> ghidra.program.model.data.DataType: ...

    def toString(self) -> unicode: ...

    def validCheckSum(self) -> bool:
        """
        Validates the record's checksum
        @return True if the checksum is valid; otherwise, false
        @throws IOException if an IO-related error occurred
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def allZeroes(self) -> bool: ...

    @property
    def dataOffset(self) -> long: ...

    @property
    def length(self) -> int: ...

    @property
    def segmentIndex(self) -> int: ...