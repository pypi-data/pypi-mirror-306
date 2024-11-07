from typing import List
from typing import overload
import ghidra.framework.model
import ghidra.framework.model.TransactionInfo
import java.lang


class SynchronizedTransaction(object, ghidra.framework.model.TransactionInfo):
    """
    SynchronizedTransaction represents an atomic undoable operation performed
     on a synchronized set of domain objects.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDescription(self) -> unicode: ...

    def getID(self) -> long: ...

    def getOpenSubTransactions(self) -> List[unicode]: ...

    def getStatus(self) -> ghidra.framework.model.TransactionInfo.Status: ...

    def hasCommittedDBTransaction(self) -> bool: ...

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

