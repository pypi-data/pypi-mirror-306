from typing import List
from typing import overload
import ghidra.app.util.bin.format.omf
import ghidra.program.model.data
import java.lang


class OmfCommentRecord(ghidra.app.util.bin.format.omf.OmfRecord):
    COMMENT_CLASS_DEFAULT_LIBRARY: int = -97
    COMMENT_CLASS_LIBMOD: int = -93
    COMMENT_CLASS_MICROSOFT_SETTINGS: int = -99
    COMMENT_CLASS_TRANSLATOR: int = 0
    COMMENT_CLASS_WATCOM_SETTINGS: int = -101



    def __init__(self, reader: ghidra.app.util.bin.BinaryReader): ...



    def calcCheckSum(self) -> int:
        """
        Computes the record's checksum
        @return The record's checksum
        @throws IOException if an IO-related error occurred
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCommentClass(self) -> int: ...

    def getCommentType(self) -> int: ...

    def getData(self) -> List[int]: ...

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

    def getValue(self) -> unicode: ...

    def hasBigFields(self) -> bool:
        """
        {@return true if this record has big fields; otherwise, false}
        """
        ...

    def hashCode(self) -> int: ...

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
    def commentClass(self) -> int: ...

    @property
    def commentType(self) -> int: ...

    @property
    def value(self) -> unicode: ...