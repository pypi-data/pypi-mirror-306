from typing import List
from typing import overload
import ghidra.app.util.bin
import ghidra.app.util.bin.format.omf
import java.lang


class AbstractOmfRecordFactory(object):
    """
    Classes that implement this interface can read various flavors of the OMF format
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getEndRecordType(self) -> int:
        """
        Gets a valid record type that can end a supported OMF binary
        @return A valid record types that can end a supported OMF binary
        """
        ...

    def getReader(self) -> ghidra.app.util.bin.BinaryReader:
        """
        {@return the reader associated with this factory}
        """
        ...

    def getStartRecordTypes(self) -> List[int]:
        """
        Gets a {@link List} of valid record types that can start a supported OMF binary
        @return A {@link List} of valid record types that can start a supported OMF binary
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def readNextRecord(self) -> ghidra.app.util.bin.format.omf.OmfRecord:
        """
        Reads the next {@link OmfRecord} pointed to by the reader
        @return The next read {@link OmfRecord}
        @throws IOException if there was an IO-related error
        @throws OmfException if there was a problem with the OMF specification
        """
        ...

    def reset(self) -> None:
        """
        Reset this factory's reader to index 0
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
    def endRecordType(self) -> int: ...

    @property
    def reader(self) -> ghidra.app.util.bin.BinaryReader: ...

    @property
    def startRecordTypes(self) -> List[object]: ...