from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.app.util.importer
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import java.io
import java.lang


class OmfSegmentHeader(ghidra.app.util.bin.format.omf.OmfRecord):





    class SectionStream(java.io.InputStream):




        def __init__(self, __a0: ghidra.app.util.bin.format.omf.omf.OmfSegmentHeader, __a1: ghidra.app.util.bin.BinaryReader, __a2: ghidra.app.util.importer.MessageLog): ...



        def available(self) -> int: ...

        def close(self) -> None: ...

        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def mark(self, __a0: int) -> None: ...

        def markSupported(self) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @staticmethod
        def nullInputStream() -> java.io.InputStream: ...

        @overload
        def read(self) -> int: ...

        @overload
        def read(self, __a0: List[int]) -> int: ...

        @overload
        def read(self, __a0: List[int], __a1: int, __a2: int) -> int: ...

        def readAllBytes(self) -> List[int]: ...

        @overload
        def readNBytes(self, __a0: int) -> List[int]: ...

        @overload
        def readNBytes(self, __a0: List[int], __a1: int, __a2: int) -> int: ...

        def reset(self) -> None: ...

        def skip(self, __a0: long) -> long: ...

        def skipNBytes(self, __a0: long) -> None: ...

        def toString(self) -> unicode: ...

        def transferTo(self, __a0: java.io.OutputStream) -> long: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader): ...



    def calcCheckSum(self) -> int:
        """
        Computes the record's checksum
        @return The record's checksum
        @throws IOException if an IO-related error occurred
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getAddress(self, language: ghidra.program.model.lang.Language) -> ghidra.program.model.address.Address:
        """
        @param language is the Program language for this binary
        @return the starting Address for this segment
        """
        ...

    def getAlignment(self) -> int:
        """
        @return the alignment required for this segment
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getClassName(self) -> unicode:
        """
        @return the class name of this segment
        """
        ...

    def getCombine(self) -> int:
        """
        @return special combining rules for this segment
        """
        ...

    def getData(self) -> List[int]: ...

    def getFrameDatum(self) -> int:
        """
        @return the segment selector needed for this object
        """
        ...

    def getName(self) -> unicode:
        """
        @return the name of this segment
        """
        ...

    def getOverlayName(self) -> unicode:
        """
        @return the name of the overlay, or the empty string
        """
        ...

    def getRawDataStream(self, reader: ghidra.app.util.bin.BinaryReader, log: ghidra.app.util.importer.MessageLog) -> java.io.InputStream:
        """
        Get an InputStream that reads in the raw data for this segment
        @param reader is the image file reader
        @param log the log
        @return the InputStream
        @throws IOException for problems reading from the image file
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

    def getSegmentLength(self) -> long:
        """
        @return the length of the segment in bytes
        """
        ...

    def getStartAddress(self) -> long:
        """
        @return the load image address for this segment
        """
        ...

    def hasBigFields(self) -> bool:
        """
        {@return true if this record has big fields; otherwise, false}
        """
        ...

    def hasNonZeroData(self) -> bool:
        """
        @return true if this block uses filler other than zero bytes
        """
        ...

    def hashCode(self) -> int: ...

    def is16Bit(self) -> bool:
        """
        @return if 16 or 32 bit segments are used
        """
        ...

    def isCode(self) -> bool:
        """
        @return true if this is a code segment
        """
        ...

    def isExecutable(self) -> bool:
        """
        @return true if this segment is executable
        """
        ...

    def isReadable(self) -> bool:
        """
        @return true if this segment is readable
        """
        ...

    def isWritable(self) -> bool:
        """
        @return true if this segment is writable
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseData(self) -> None: ...

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
    def 16Bit(self) -> bool: ...

    @property
    def alignment(self) -> int: ...

    @property
    def className(self) -> unicode: ...

    @property
    def code(self) -> bool: ...

    @property
    def combine(self) -> int: ...

    @property
    def executable(self) -> bool: ...

    @property
    def frameDatum(self) -> int: ...

    @property
    def name(self) -> unicode: ...

    @property
    def overlayName(self) -> unicode: ...

    @property
    def readable(self) -> bool: ...

    @property
    def segmentLength(self) -> long: ...

    @property
    def startAddress(self) -> long: ...

    @property
    def writable(self) -> bool: ...