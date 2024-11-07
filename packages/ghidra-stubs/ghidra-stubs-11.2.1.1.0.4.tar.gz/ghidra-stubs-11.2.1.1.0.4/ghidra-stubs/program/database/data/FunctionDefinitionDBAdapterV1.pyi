from typing import overload
import db
import ghidra.program.database.data
import java.lang


class FunctionDefinitionDBAdapterV1(ghidra.program.database.data.FunctionDefinitionDBAdapter, db.RecordTranslator):
    """
    Version 1 implementation for accessing the Function Signature Definition database table. 
 
     NOTE: Use of tablePrefix introduced with this adapter version.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getRecordCount(self) -> int: ...

    def getRecords(self) -> db.RecordIterator: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    def translateRecord(self, oldRec: db.DBRecord) -> db.DBRecord: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

