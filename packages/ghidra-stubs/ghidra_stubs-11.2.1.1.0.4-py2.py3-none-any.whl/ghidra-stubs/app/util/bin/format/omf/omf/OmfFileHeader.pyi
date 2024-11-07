from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.app.util.bin.format.omf.omf
import ghidra.app.util.importer
import ghidra.program.model.data
import ghidra.util.task
import java.lang


class OmfFileHeader(ghidra.app.util.bin.format.omf.OmfRecord):




    def __init__(self, reader: ghidra.app.util.bin.BinaryReader): ...



    def calcCheckSum(self) -> int:
        """
        Computes the record's checksum
        @return The record's checksum
        @throws IOException if an IO-related error occurred
        """
        ...

    @staticmethod
    def checkMagicNumber(reader: ghidra.app.util.bin.BinaryReader) -> bool:
        """
        Check that the file has the specific OMF magic number
        @param reader accesses the bytes of the file
        @return true if the magic number matches
        @throws IOException for problems reading bytes
        """
        ...

    @staticmethod
    def doLinking(__a0: long, __a1: List[object], __a2: List[object]) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getData(self) -> List[int]: ...

    def getExternalSymbols(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfExternalSymbol]:
        """
        @return the list of symbols that are external to this file
        """
        ...

    def getExtraSegments(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfSegmentHeader]:
        """
        @return the list of segments which are Borland extensions
        """
        ...

    def getFixups(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfFixupRecord]:
        """
        @return the list of relocation records for this file
        """
        ...

    def getGroups(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfGroupRecord]:
        """
        @return the list of group records for this file
        """
        ...

    def getLibraryModuleName(self) -> unicode:
        """
        The name of the object module (within a library)
        @return the name
        """
        ...

    def getLocalSymbols(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfSymbolRecord]:
        """
        @return the list of local symbols in this file
        """
        ...

    def getMachineName(self) -> unicode:
        """
        @return the string identifying the architecture this object was compiled for
        """
        ...

    def getName(self) -> unicode:
        """
        This is usually the original source filename
        @return the name
        """
        ...

    def getPublicSymbols(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfSymbolRecord]:
        """
        @return the list of public symbols exported by this file
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

    def getRecords(self) -> List[ghidra.app.util.bin.format.omf.OmfRecord]:
        """
        {@return the list of records}
        """
        ...

    def getSegments(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfSegmentHeader]:
        """
        @return the list of segments in this file
        """
        ...

    def getTranslator(self) -> unicode:
        """
        If the OMF file contains a "translator" record, this is usually a string
         indicating the compiler which produced the file.
        @return the translator for this file
        """
        ...

    def hasBigFields(self) -> bool:
        """
        {@return true if this record has big fields; otherwise, false}
        """
        ...

    def hashCode(self) -> int: ...

    def isLittleEndian(self) -> bool:
        """
        @return true if the file describes the load image for a little endian architecture
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def parse(factory: ghidra.app.util.bin.format.omf.AbstractOmfRecordFactory, monitor: ghidra.util.task.TaskMonitor, log: ghidra.app.util.importer.MessageLog) -> ghidra.app.util.bin.format.omf.omf.OmfFileHeader:
        """
        Parse the entire object file
        @param factory the {@link AbstractOmfRecordFactory}
        @param monitor is checked for cancel button
        @param log the log
        @return the header record as root of object
        @throws IOException for problems reading data
        @throws OmfException for malformed records
        """
        ...

    def parseData(self) -> None: ...

    def resolveNames(self) -> None:
        """
        Resolve special names associated with each segment: segment, class, overlay names
         and group: group name
         For each segment, the read/write/execute permissions are also determined
        @throws OmfException if any name indices are malformed
        """
        ...

    def resolveSegment(self, index: int) -> ghidra.app.util.bin.format.omf.omf.OmfSegmentHeader:
        """
        Given an index, retrieve the specific segment it refers to. This
         incorporates the special Borland segments, where the index has 
         the bit 0x4000 set.
        @param index identifies the segment
        @return the corresponding OmfSegmentHeader
        @throws OmfException if the index is malformed
        """
        ...

    @staticmethod
    def scan(factory: ghidra.app.util.bin.format.omf.AbstractOmfRecordFactory, monitor: ghidra.util.task.TaskMonitor, fastscan: bool) -> ghidra.app.util.bin.format.omf.omf.OmfFileHeader:
        """
        Scan the object file, for the main header and comment records. Other records are parsed but not saved
        @param factory the {@link AbstractOmfRecordFactory}
        @param monitor is checked for cancellation
        @param fastscan is true if we only want to scan the header until first seghead,
        @return the header record
        @throws IOException for problems reading program data
        @throws OmfException for malformed records
        """
        ...

    def sortSegmentDataBlocks(self) -> None:
        """
        Sort the explicit data-blocks for each segment into address order.
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
    def externalSymbols(self) -> List[object]: ...

    @property
    def extraSegments(self) -> List[object]: ...

    @property
    def fixups(self) -> List[object]: ...

    @property
    def groups(self) -> List[object]: ...

    @property
    def libraryModuleName(self) -> unicode: ...

    @property
    def littleEndian(self) -> bool: ...

    @property
    def localSymbols(self) -> List[object]: ...

    @property
    def machineName(self) -> unicode: ...

    @property
    def name(self) -> unicode: ...

    @property
    def publicSymbols(self) -> List[object]: ...

    @property
    def records(self) -> List[object]: ...

    @property
    def segments(self) -> List[object]: ...

    @property
    def translator(self) -> unicode: ...