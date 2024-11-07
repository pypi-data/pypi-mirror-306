from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import ghidra.program.model.data
import java.lang


class OmfUtils(object):
    """
    Utility class for OMF-based file formats
    """

    CATEGORY_PATH: unicode = u'/OMF'



    def __init__(self): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getRecordName(type: int, recordTypesClass: java.lang.Class) -> unicode:
        """
        Gets the name of the given record type
        @param type The record type
        @param recordTypesClass The class that contains accessible OMF type fields
        @return The name of the given record type
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    @staticmethod
    def readIndex(reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.omf.OmfIndex: ...

    @staticmethod
    def readInt2Or4(reader: ghidra.app.util.bin.BinaryReader, isBig: bool) -> ghidra.app.util.bin.format.omf.Omf2or4: ...

    @staticmethod
    def readRecords(factory: ghidra.app.util.bin.format.omf.AbstractOmfRecordFactory) -> List[ghidra.app.util.bin.format.omf.OmfRecord]:
        """
        Reads all the {@link OmfRecord records} associated with the given 
         {@link AbstractOmfRecordFactory}
        @param factory The {@link AbstractOmfRecordFactory}
        @return A {@link List} of read {@link OmfRecord records}
        @throws IOException if there was an IO-related error
        @throws OmfException if there was a problem with the OMF specification
        """
        ...

    @staticmethod
    def readString(reader: ghidra.app.util.bin.BinaryReader) -> ghidra.app.util.bin.format.omf.OmfString:
        """
        Read the OMF string format: 1-byte length, followed by that many ascii characters
        @param reader A {@link BinaryReader} positioned at the start of the string
        @return the read OMF string
        @throws IOException if an IO-related error occurred
        """
        ...

    @staticmethod
    def toOmfRecordDataType(record: ghidra.app.util.bin.format.omf.OmfRecord, name: unicode) -> ghidra.program.model.data.DataType:
        """
        Converts the given {@link OmfRecord} to a generic OMF record {@link DataType}
        @param record The OMF record to convert
        @param name The name of the OMF record
        @return A {@link DataType} for the given OMF record
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

