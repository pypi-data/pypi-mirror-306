from typing import overload
import db
import ghidra.program.database.util
import java.lang


class FunctionDefinitionDBAdapter(object, ghidra.program.database.util.DBRecordAdapter):
    """
    Adapter to access the Function Signature Definition database table.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getRecordCount(self) -> int: ...

    def getRecords(self) -> db.RecordIterator:
        """
        Gets an iterator over all function signature definition data type records.
        @return the function definition data type record iterator.
        @throws IOException if the database can't be accessed.
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

