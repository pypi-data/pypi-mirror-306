from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.app.util.bin.format.omf.omf
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import java.lang


class OmfGroupRecord(ghidra.app.util.bin.format.omf.OmfRecord):





    class GroupSubrecord(object):




        def __init__(self): ...



        def equals(self, __a0: object) -> bool: ...

        def getClass(self) -> java.lang.Class: ...

        def hashCode(self) -> int: ...

        def notify(self) -> None: ...

        def notifyAll(self) -> None: ...

        @staticmethod
        def read(__a0: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.omf.omf.OmfGroupRecord.GroupSubrecord: ...

        def toString(self) -> unicode: ...

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

    def getAddress(self, language: ghidra.program.model.lang.Language) -> ghidra.program.model.address.Address: ...

    def getClass(self) -> java.lang.Class: ...

    def getData(self) -> List[int]: ...

    def getFrameDatum(self) -> int:
        """
        This is the segment selector needed for this object
        @return The segment selector
        """
        ...

    def getName(self) -> unicode: ...

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

    def getSegmentComponentType(self, i: int) -> int: ...

    def getSegmentIndex(self, i: int) -> int: ...

    def getStartAddress(self) -> long: ...

    def hasBigFields(self) -> bool:
        """
        {@return true if this record has big fields; otherwise, false}
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def numSegments(self) -> int: ...

    def parseData(self) -> None: ...

    def resolveNames(self, __a0: List[object]) -> None: ...

    def setStartAddress(self, val: long) -> None: ...

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
    def frameDatum(self) -> int: ...

    @property
    def name(self) -> unicode: ...

    @property
    def startAddress(self) -> long: ...

    @startAddress.setter
    def startAddress(self, value: long) -> None: ...