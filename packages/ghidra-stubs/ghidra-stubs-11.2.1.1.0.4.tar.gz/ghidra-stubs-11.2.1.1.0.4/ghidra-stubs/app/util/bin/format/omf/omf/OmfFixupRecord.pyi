from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.app.util.bin.format.omf.omf
import ghidra.app.util.bin.format.omf.omf.OmfFixupRecord
import ghidra.program.model.data
import java.lang


class OmfFixupRecord(ghidra.app.util.bin.format.omf.OmfRecord):





    class Subrecord(object):




        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def getDataRecordOffset(self) -> int: ...

        def getFixMethod(self) -> int: ...

        def getFixMethodWithSub(self, __a0: ghidra.app.util.bin.format.omf.omf.OmfFixupRecord.Subrecord) -> int: ...

        def getFixThreadNum(self) -> int: ...

        def getFrameMethod(self) -> int: ...

        def getIndex(self) -> int: ...

        def getLocationType(self) -> int: ...

        def getTargetDatum(self) -> int: ...

        def getTargetDisplacement(self) -> int: ...

        def getThreadMethod(self) -> int: ...

        def getThreadNum(self) -> int: ...

        def hashCode(self) -> int: ...

        def isFrameInSubThread(self) -> bool: ...

        def isFrameThread(self) -> bool: ...

        def isSegmentRelative(self) -> bool: ...

        def isTargetThread(self) -> bool: ...

        def isThreadSubrecord(self) -> bool: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @staticmethod
        def readSubrecord(__a0: ghidra.app.util.bin.BinaryReader, __a1: bool) -> ghidra.app.util.bin.format.omf.omf.OmfFixupRecord.Subrecord: ...

        def toString(self) -> unicode: ...

        @overload
        def wait(self) -> None: ...

        @overload
        def wait(self, __a0: long) -> None: ...

        @overload
        def wait(self, __a0: long, __a1: int) -> None: ...

        @property
        def dataRecordOffset(self) -> int: ...

        @property
        def fixMethod(self) -> int: ...

        @property
        def fixThreadNum(self) -> int: ...

        @property
        def frameInSubThread(self) -> bool: ...

        @property
        def frameMethod(self) -> int: ...

        @property
        def frameThread(self) -> bool: ...

        @property
        def index(self) -> int: ...

        @property
        def locationType(self) -> int: ...

        @property
        def segmentRelative(self) -> bool: ...

        @property
        def targetDatum(self) -> int: ...

        @property
        def targetDisplacement(self) -> int: ...

        @property
        def targetThread(self) -> bool: ...

        @property
        def threadMethod(self) -> int: ...

        @property
        def threadNum(self) -> int: ...

        @property
        def threadSubrecord(self) -> bool: ...

    def __init__(self, reader: ghidra.app.util.bin.BinaryReader):
        """
        Read a Fixup record from the input reader
        @param reader The actual reader
        @throws IOException if there was an IO-related error
        """
        ...



    def calcCheckSum(self) -> int:
        """
        Computes the record's checksum
        @return The record's checksum
        @throws IOException if an IO-related error occurred
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getData(self) -> List[int]: ...

    def getDataBlock(self) -> ghidra.app.util.bin.format.omf.omf.OmfData:
        """
        @return The datablock this fixup record is meant for
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

    def getSubrecords(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfFixupRecord.Subrecord]:
        """
        @return The array of subrecords
        """
        ...

    def hasBigFields(self) -> bool:
        """
        {@return true if this record has big fields; otherwise, false}
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseData(self) -> None: ...

    def setDataBlock(self, last: ghidra.app.util.bin.format.omf.omf.OmfData) -> None:
        """
        @param last The Datablock this fixup record is meant for
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
    def dataBlock(self) -> ghidra.app.util.bin.format.omf.omf.OmfData: ...

    @dataBlock.setter
    def dataBlock(self, value: ghidra.app.util.bin.format.omf.omf.OmfData) -> None: ...

    @property
    def subrecords(self) -> List[ghidra.app.util.bin.format.omf.omf.OmfFixupRecord.Subrecord]: ...