from typing import List
from typing import overload
import ghidra.program.database.symbol
import ghidra.program.model.address
import ghidra.program.model.listing
import ghidra.program.model.symbol
import ghidra.program.util
import ghidra.util
import ghidra.util.task
import java.lang


class FunctionSymbol(ghidra.program.database.symbol.SymbolDB):
    """
    Symbol class for functions.
 
     Symbol Data Usage:
       EXTERNAL:
       	String stringData - external memory address/label
    """





    def __init__(self, symbolMgr: ghidra.program.database.symbol.SymbolManager, cache: ghidra.program.database.DBObjectCache, address: ghidra.program.model.address.Address, record: db.DBRecord):
        """
        Construct a new FunctionSymbol
        @param symbolMgr the symbol manager.
        @param cache symbol object cache
        @param address the address for this symbol.
        @param record the record for this symbol.
        """
        ...



    def delete(self) -> bool: ...

    def doSetNameAndNamespace(self, newName: unicode, newNamespace: ghidra.program.model.symbol.Namespace, source: ghidra.program.model.symbol.SourceType, checkForDuplicates: bool) -> None: ...

    def equals(self, obj: object) -> bool: ...

    def getAddress(self) -> ghidra.program.model.address.Address: ...

    def getClass(self) -> java.lang.Class: ...

    def getDataTypeId(self) -> long: ...

    def getID(self) -> long: ...

    def getKey(self) -> long:
        """
        Get the database key for this object.
        """
        ...

    @overload
    def getName(self) -> unicode: ...

    @overload
    def getName(self, includeNamespace: bool) -> unicode: ...

    def getObject(self) -> object: ...

    def getParentNamespace(self) -> ghidra.program.model.symbol.Namespace: ...

    def getParentSymbol(self) -> ghidra.program.model.symbol.Symbol: ...

    def getPath(self) -> List[unicode]: ...

    def getProgram(self) -> ghidra.program.model.listing.Program: ...

    def getProgramLocation(self) -> ghidra.program.util.ProgramLocation: ...

    def getReferenceCount(self) -> int: ...

    @overload
    def getReferences(self) -> List[ghidra.program.model.symbol.Reference]: ...

    @overload
    def getReferences(self, monitor: ghidra.util.task.TaskMonitor) -> List[ghidra.program.model.symbol.Reference]: ...

    def getSource(self) -> ghidra.program.model.symbol.SourceType: ...

    def getSymbolStringData(self) -> unicode:
        """
        Returns the symbol's string data which has different meanings depending on the symbol type
         and whether or not it is external
        @return the symbol's string data
        """
        ...

    def getSymbolType(self) -> ghidra.program.model.symbol.SymbolType:
        """
        @see ghidra.program.model.symbol.Symbol#getSymbolType()
        """
        ...

    def hasMultipleReferences(self) -> bool: ...

    def hasReferences(self) -> bool: ...

    def hashCode(self) -> int: ...

    @overload
    def isDeleted(self) -> bool: ...

    @overload
    def isDeleted(self, lock: ghidra.util.Lock) -> bool:
        """
        Returns true if this object has been deleted. Note: once an object has been deleted, it will
         never be "refreshed". For example, if an object is ever deleted and is resurrected via an
         "undo", you will have get a fresh instance of the object.
        @param lock object cache lock object
        @return true if this object has been deleted.
        """
        ...

    def isDeleting(self) -> bool: ...

    def isDescendant(self, namespace: ghidra.program.model.symbol.Namespace) -> bool: ...

    def isDynamic(self) -> bool: ...

    def isExternal(self) -> bool: ...

    def isExternalEntryPoint(self) -> bool: ...

    def isGlobal(self) -> bool: ...

    def isPinned(self) -> bool: ...

    def isPrimary(self) -> bool: ...

    def isValidParent(self, parent: ghidra.program.model.symbol.Namespace) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setDataTypeId(self, value: long) -> None:
        """
        Sets the generic symbol data 1.
        @param value the value to set as symbol data 1.
        """
        ...

    def setInvalid(self) -> None:
        """
        Invalidate this object. This does not necessarily mean that this object can never be used
         again. If the object can refresh itself, it may still be useable.
        """
        ...

    def setName(self, newName: unicode, source: ghidra.program.model.symbol.SourceType) -> None: ...

    def setNameAndNamespace(self, newName: unicode, newNamespace: ghidra.program.model.symbol.Namespace, source: ghidra.program.model.symbol.SourceType) -> None: ...

    def setNamespace(self, newNamespace: ghidra.program.model.symbol.Namespace) -> None: ...

    def setPinned(self, pinned: bool) -> None: ...

    def setPrimary(self) -> bool:
        """
        @see ghidra.program.model.symbol.Symbol#setPrimary()
        """
        ...

    def setSource(self, newSource: ghidra.program.model.symbol.SourceType) -> None:
        """
        Sets this symbol's source as specified.
        @param newSource the new source type (IMPORTED, ANALYSIS, USER_DEFINED)
        @throws IllegalArgumentException if you try to change the source from default or to default
        """
        ...

    def setSymbolStringData(self, stringData: unicode) -> None:
        """
        Sets the symbol's string data field. This field's data has different uses depending on the 
         symbol type and whether or not it is external.
        @param stringData the string to store in the string data field
        """
        ...

    def setVariableOffset(self, offset: int) -> None:
        """
        Sets the symbol's variable offset. For parameters, this is the ordinal, for locals, it is 
         the first use offset
        @param offset the value to set as the symbols variable offset.
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
    def external(self) -> bool: ...

    @property
    def object(self) -> object: ...

    @property
    def pinned(self) -> bool: ...

    @pinned.setter
    def pinned(self, value: bool) -> None: ...

    @property
    def primary(self) -> bool: ...

    @property
    def programLocation(self) -> ghidra.program.util.ProgramLocation: ...

    @property
    def referenceCount(self) -> int: ...

    @property
    def symbolType(self) -> ghidra.program.model.symbol.SymbolType: ...