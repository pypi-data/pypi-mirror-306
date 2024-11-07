from typing import List
from typing import overload
import db
import ghidra.framework.data
import ghidra.framework.model
import ghidra.framework.options
import ghidra.program.database
import ghidra.program.database.bookmark
import ghidra.program.database.code
import ghidra.program.database.data
import ghidra.program.database.external
import ghidra.program.database.function
import ghidra.program.database.map
import ghidra.program.database.mem
import ghidra.program.database.module
import ghidra.program.database.references
import ghidra.program.database.reloc
import ghidra.program.database.symbol
import ghidra.program.model.address
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.program.model.listing
import ghidra.program.model.pcode
import ghidra.program.model.symbol
import ghidra.program.model.util
import ghidra.program.util
import ghidra.util
import ghidra.util.task
import java.io
import java.lang
import java.util
import utility.function


class ProgramDB(ghidra.framework.data.DomainObjectAdapterDB, ghidra.program.model.listing.Program, ghidra.program.util.ChangeManager):
    """
    Database implementation for Program.
    """

    ADDED_VARIABLE_STORAGE_MANAGER_VERSION: int = 10
    ANALYSIS_OPTIONS_MOVED_VERSION: int = 9
    AUTO_PARAMETERS_ADDED_VERSION: int = 19
    COMPOUND_VARIABLE_STORAGE_ADDED_VERSION: int = 18
    CONTENT_TYPE: unicode = u'Program'
    EXTERNAL_FUNCTIONS_ADDED_VERSION: int = 17
    METADATA_ADDED_VERSION: int = 11
    RELOCATION_STATUS_ADDED_VERSION: int = 26



    @overload
    def __init__(self, name: unicode, language: ghidra.program.model.lang.Language, compilerSpec: ghidra.program.model.lang.CompilerSpec, consumer: object):
        """
        Constructs a new ProgramDB
        @param name the name of the program
        @param language the Language used by this program
        @param compilerSpec compiler specification
        @param consumer the object that is using this program.
        @throws IOException if there is an error accessing the database.
        """
        ...

    @overload
    def __init__(self, dbh: db.DBHandle, openMode: ghidra.framework.data.OpenMode, monitor: ghidra.util.task.TaskMonitor, consumer: object):
        """
        Constructs a new ProgramDB
        @param dbh a handle to an open program database.
        @param openMode one of:
         		READ_ONLY: the original database will not be modified
         		UPDATE: the database can be written to.
         		UPGRADE: the database is upgraded to the latest schema as it is opened.
        @param monitor TaskMonitor that allows the open to be canceled.
        @param consumer the object that keeping the program open.
        @throws IOException if an error accessing the database occurs.
        @throws VersionException if database version does not match implementation, UPGRADE may be possible.
        @throws CancelledException if instantiation is canceled by monitor
        @throws LanguageNotFoundException if a language cannot be found for this program
        """
        ...



    def addCloseListener(self, listener: ghidra.framework.model.DomainObjectClosedListener) -> None: ...

    def addConsumer(self, consumer: object) -> bool: ...

    def addDomainFileListener(self, listener: ghidra.framework.data.DomainObjectFileListener) -> None: ...

    def addListener(self, l: ghidra.framework.model.DomainObjectListener) -> None: ...

    def addSynchronizedDomainObject(self, domainObj: ghidra.framework.model.DomainObject) -> None:
        """
        Synchronize the specified domain object with this domain object
         using a shared transaction manager.  If either or both is already shared,
         a transition to a single shared transaction manager will be
         performed.
        @param domainObj
        @throws LockException if lock or open transaction is active on either
         this or the specified domain object
        """
        ...

    def addTransactionListener(self, listener: ghidra.framework.model.TransactionListener) -> None:
        """
        Adds the given transaction listener to this domain object
        @param listener the new transaction listener to add
        """
        ...

    def canLock(self) -> bool: ...

    def canRedo(self) -> bool: ...

    def canSave(self) -> bool: ...

    def canUndo(self) -> bool: ...

    def categoryAdded(self, categoryID: long, eventType: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None:
        """
        Notification that a category was added.
        @param categoryID the id of the datatype that was added.
        @param eventType the type of change (should always be CATEGORY_ADDED)
        @param oldValue always null
        @param newValue new value depends on the type.
        """
        ...

    def categoryChanged(self, categoryID: long, eventType: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None:
        """
        Notification that a category was changed.
        @param categoryID the id of the datatype that was added.
        @param eventType the type of change.
        @param oldValue old value depends on the type.
        @param newValue new value depends on the type.
        """
        ...

    def checkExclusiveAccess(self) -> None: ...

    def clearUndo(self) -> None: ...

    def createAddressSetPropertyMap(self, mapName: unicode) -> ghidra.program.model.util.AddressSetPropertyMap: ...

    def createIntRangeMap(self, mapName: unicode) -> ghidra.program.database.IntRangeMapDB: ...

    def createOverlaySpace(self, overlaySpaceName: unicode, baseSpace: ghidra.program.model.address.AddressSpace) -> ghidra.program.database.ProgramOverlayAddressSpace: ...

    def createPrivateEventQueue(self, listener: ghidra.framework.model.DomainObjectListener, maxDelay: int) -> ghidra.framework.model.EventQueueID: ...

    def dataTypeAdded(self, dataTypeID: long, eventType: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None:
        """
        Notification that a datatype was added.
        @param dataTypeID the id if the datatype that was added.
        @param eventType should always be DATATYPE_ADDED
        @param oldValue always null
        @param newValue the datatype added.
        """
        ...

    def dataTypeChanged(self, dataTypeID: long, eventType: ghidra.program.util.ProgramEvent, isAutoChange: bool, oldValue: object, newValue: object) -> None:
        """
        notification the a datatype has changed
        @param dataTypeID the id of the datatype that changed.
        @param eventType the type of the change (moved, renamed, etc.)
        @param isAutoChange true if change was an automatic change in response to 
         another datatype's change (e.g., size, alignment), else false in which case this
         change will be added to program change-set to aid merge conflict detection.
        @param oldValue the old datatype.
        @param newValue the new datatype.
        """
        ...

    def dbError(self, e: java.io.IOException) -> None: ...

    def deleteAddressRange(self, startAddr: ghidra.program.model.address.Address, endAddr: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Deletes given range from the program.
        @param startAddr the first address in the range.
        @param endAddr the last address in the range.
        @param monitor the task monitor to use while deleting information in the given range.
        @throws RollbackException if the user cancelled the operation via the task monitor.
        """
        ...

    def deleteAddressSetPropertyMap(self, mapName: unicode) -> None: ...

    def deleteIntRangeMap(self, mapName: unicode) -> None: ...

    def endTransaction(self, transactionID: int, commit: bool) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def fireEvent(self, ev: ghidra.framework.model.DomainObjectChangeRecord) -> None:
        """
        Fires the specified event.
        @param ev event to fire
        """
        ...

    def flushEvents(self) -> None: ...

    def flushPrivateEventQueue(self, id: ghidra.framework.model.EventQueueID) -> None: ...

    def flushWriteCache(self) -> None: ...

    def forceLock(self, rollback: bool, reason: unicode) -> None: ...

    def getAddressFactory(self) -> ghidra.program.database.ProgramAddressFactory: ...

    def getAddressMap(self) -> ghidra.program.database.map.AddressMapDB:
        """
        Returns this programs address map.
         NOTE: This method should be dropped from the {@link Program} interface to help
         discourage the its use external to this implementation since bad assumptions 
         are frequently made about address keys which may not be ordered or sequential
         across an entire address space.
        """
        ...

    def getAddressSetPropertyMap(self, mapName: unicode) -> ghidra.program.model.util.AddressSetPropertyMap: ...

    def getAllRedoNames(self) -> List[unicode]: ...

    def getAllUndoNames(self) -> List[unicode]: ...

    def getBookmarkManager(self) -> ghidra.program.database.bookmark.BookmarkDBManager: ...

    def getChangeSet(self) -> ghidra.framework.data.DomainObjectDBChangeSet:
        """
        Returns the change set corresponding to all unsaved changes in this domain object.
        @return the change set corresponding to all unsaved changes in this domain object
        """
        ...

    def getChangeStatus(self) -> bool:
        """
        Return "changed" status
        @return true if this object has changed
        """
        ...

    def getChanges(self) -> ghidra.program.model.listing.ProgramChangeSet: ...

    def getClass(self) -> java.lang.Class: ...

    def getCodeManager(self) -> ghidra.program.database.code.CodeManager: ...

    def getCompiler(self) -> unicode: ...

    def getCompilerSpec(self) -> ghidra.program.model.lang.CompilerSpec: ...

    def getConsumerList(self) -> List[object]: ...

    @overload
    @staticmethod
    def getContentHandler(contentType: unicode) -> ghidra.framework.data.ContentHandler:
        """
        Get the {@link ContentHandler} associated with the specified content-type.
        @param contentType domain object content type
        @return content handler
        @throws IOException if no content handler can be found
        """
        ...

    @overload
    @staticmethod
    def getContentHandler(dobj: ghidra.framework.model.DomainObject) -> ghidra.framework.data.ContentHandler:
        """
        Get the {@link ContentHandler} associated with the specified domain object
        @param dobj domain object
        @return content handler
        @throws IOException if no content handler can be found
        """
        ...

    @overload
    @staticmethod
    def getContentHandler(dobjClass: java.lang.Class) -> ghidra.framework.data.ContentHandler:
        """
        Get the {@link ContentHandler} associated with the specified domain object class
        @param dobjClass domain object class
        @return content handler
        @throws IOException if no content handler can be found
        """
        ...

    @staticmethod
    def getContentHandlers() -> java.util.Set:
        """
        Get all {@link ContentHandler}s
        @return collection of content handlers
        """
        ...

    def getCreationDate(self) -> java.util.Date: ...

    def getCurrentTransactionInfo(self) -> ghidra.framework.model.TransactionInfo: ...

    def getDBHandle(self) -> db.DBHandle:
        """
        Returns the open handle to the underlying database.
        """
        ...

    def getDataTypeManager(self) -> ghidra.program.database.data.ProgramDataTypeManager: ...

    def getDefaultPointerSize(self) -> int: ...

    def getDescription(self) -> unicode: ...

    def getDomainFile(self) -> ghidra.framework.model.DomainFile: ...

    def getEquateTable(self) -> ghidra.program.database.symbol.EquateManager: ...

    def getExecutableFormat(self) -> unicode: ...

    def getExecutableMD5(self) -> unicode: ...

    def getExecutablePath(self) -> unicode: ...

    def getExecutableSHA256(self) -> unicode: ...

    def getExternalManager(self) -> ghidra.program.database.external.ExternalManagerDB: ...

    def getFunctionManager(self) -> ghidra.program.database.function.FunctionManagerDB: ...

    def getGlobalNamespace(self) -> ghidra.program.model.symbol.Namespace: ...

    def getImageBase(self) -> ghidra.program.model.address.Address: ...

    def getIntRangeMap(self, mapName: unicode) -> ghidra.program.database.IntRangeMap: ...

    def getLanguage(self) -> ghidra.program.model.lang.Language: ...

    def getLanguageCompilerSpecPair(self) -> ghidra.program.model.lang.LanguageCompilerSpecPair: ...

    def getLanguageID(self) -> ghidra.program.model.lang.LanguageID: ...

    def getListing(self) -> ghidra.program.model.listing.Listing: ...

    def getLock(self) -> ghidra.util.Lock: ...

    def getMaxAddress(self) -> ghidra.program.model.address.Address: ...

    def getMemory(self) -> ghidra.program.database.mem.MemoryMapDB: ...

    def getMetadata(self) -> java.util.Map: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getModificationNumber(self) -> long: ...

    def getName(self) -> unicode: ...

    def getNamespaceManager(self) -> ghidra.program.database.symbol.NamespaceManager: ...

    def getOptions(self, propertyListName: unicode) -> ghidra.framework.options.Options: ...

    def getOptionsNames(self) -> List[unicode]:
        """
        Returns all properties lists contained by this domain object.
        @return all property lists contained by this domain object.
        """
        ...

    def getPreferredRootNamespaceCategoryPath(self) -> ghidra.program.model.data.CategoryPath: ...

    def getProgramContext(self) -> ghidra.program.model.listing.ProgramContext: ...

    def getProgramUserData(self) -> ghidra.program.model.listing.ProgramUserData: ...

    def getRedoName(self) -> unicode: ...

    def getReferenceManager(self) -> ghidra.program.database.references.ReferenceDBManager: ...

    @overload
    def getRegister(self, regName: unicode) -> ghidra.program.model.lang.Register: ...

    @overload
    def getRegister(self, addr: ghidra.program.model.address.Address) -> ghidra.program.model.lang.Register: ...

    @overload
    def getRegister(self, varnode: ghidra.program.model.pcode.Varnode) -> ghidra.program.model.lang.Register: ...

    @overload
    def getRegister(self, addr: ghidra.program.model.address.Address, size: int) -> ghidra.program.model.lang.Register: ...

    def getRegisters(self, addr: ghidra.program.model.address.Address) -> List[ghidra.program.model.lang.Register]: ...

    def getRelocationTable(self) -> ghidra.program.database.reloc.RelocationManager: ...

    def getStoredVersion(self) -> int: ...

    def getSymbolTable(self) -> ghidra.program.database.symbol.SymbolManager: ...

    def getSynchronizedDomainObjects(self) -> List[ghidra.framework.model.DomainObject]:
        """
        Return array of all domain objects synchronized with a
         shared transaction manager.
        @return returns array of synchronized domain objects or
         null if this domain object is not synchronized with others.
        """
        ...

    def getTreeManager(self) -> ghidra.program.database.module.TreeManager: ...

    def getUndoName(self) -> unicode: ...

    def getUndoStackDepth(self) -> int:
        """
        Returns the undo stack depth.
         (The number of items on the undo stack)
         This method is for JUnits.
        @return the undo stack depth
        """
        ...

    def getUniqueProgramID(self) -> long: ...

    def getUsrPropertyManager(self) -> ghidra.program.model.util.PropertyMapManager: ...

    def hasExclusiveAccess(self) -> bool: ...

    def hasTerminatedTransaction(self) -> bool: ...

    def hashCode(self) -> int: ...

    def invalidate(self) -> None: ...

    def invalidateWriteCache(self) -> None: ...

    def isChangeable(self) -> bool: ...

    def isChanged(self) -> bool: ...

    def isClosed(self) -> bool: ...

    def isLanguageUpgradePending(self) -> bool:
        """
        Determine if program initialization requires a language upgrade
        @return true if language upgrade is pending
        """
        ...

    def isLocked(self) -> bool: ...

    def isSendingEvents(self) -> bool: ...

    def isTemporary(self) -> bool: ...

    def isUsedBy(self, consumer: object) -> bool:
        """
        Returns true if the given consumer is using this object.
        """
        ...

    def lock(self, reason: unicode) -> bool: ...

    def moveAddressRange(self, fromAddr: ghidra.program.model.address.Address, toAddr: ghidra.program.model.address.Address, length: long, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Moves all information stored in the given range to the new location
        @param fromAddr the first address in the range to be moved
        @param toAddr the address to move to
        @param length the number of addresses to move
        @param monitor the task monitor to use while deleting information in the given range
        @throws AddressOverflowException if there is a problem moving address ranges
        @throws RollbackException if the user cancelled the operation via the task monitor
        """
        ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def openTransaction(self, description: unicode) -> db.Transaction: ...

    @overload
    def parseAddress(self, addrStr: unicode) -> List[ghidra.program.model.address.Address]: ...

    @overload
    def parseAddress(self, addrStr: unicode, caseSensitive: bool) -> List[ghidra.program.model.address.Address]: ...

    def programTreeAdded(self, id: long, eventType: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None:
        """
        Notification that a program tree was added.
        @param id the id of the program tree that was added.
        @param eventType the type of change
        @param oldValue old value is null
        @param newValue new value depends the tree that was added.
        """
        ...

    def programTreeChanged(self, id: long, eventType: ghidra.program.util.ProgramEvent, affectedObj: object, oldValue: object, newValue: object) -> None:
        """
        Notification that a program tree was changed.
        @param id the id of the program tree that was changed.
        @param eventType the {@link EventType} for this event
        @param affectedObj the object that was changed
        @param oldValue old value depends on the type of the change
        @param newValue old value depends on the type of the change
        """
        ...

    def redo(self) -> None: ...

    def release(self, consumer: object) -> None: ...

    def releaseSynchronizedDomainObject(self) -> None:
        """
        Release this domain object from a shared transaction manager.  If
         this object has not been synchronized with others via a shared
         transaction manager, this method will have no affect.
        @throws LockException if lock or open transaction is active
        """
        ...

    def removeCloseListener(self, listener: ghidra.framework.model.DomainObjectClosedListener) -> None: ...

    def removeDomainFileListener(self, listener: ghidra.framework.data.DomainObjectFileListener) -> None: ...

    def removeListener(self, l: ghidra.framework.model.DomainObjectListener) -> None: ...

    def removeOverlaySpace(self, overlaySpaceName: unicode) -> bool: ...

    def removePrivateEventQueue(self, id: ghidra.framework.model.EventQueueID) -> bool: ...

    def removeTransactionListener(self, listener: ghidra.framework.model.TransactionListener) -> None:
        """
        Removes the given transaction listener from this domain object.
        @param listener the transaction listener to remove
        """
        ...

    def renameOverlaySpace(self, overlaySpaceName: unicode, newName: unicode) -> None: ...

    def restoreImageBase(self) -> None: ...

    def save(self, comment: unicode, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def saveToPackedFile(self, outputFile: java.io.File, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    @overload
    def setChanged(self, changeRecord: ghidra.program.util.ProgramChangeRecord) -> None: ...

    @overload
    def setChanged(self, event: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None: ...

    @overload
    def setChanged(self, event: ghidra.program.util.ProgramEvent, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address, oldValue: object, newValue: object) -> None: ...

    def setCompiler(self, compiler: unicode) -> None: ...

    def setEffectiveImageBase(self, imageBase: ghidra.program.model.address.Address) -> None: ...

    def setEventsEnabled(self, v: bool) -> None: ...

    def setExecutableFormat(self, format: unicode) -> None: ...

    def setExecutableMD5(self, md5: unicode) -> None: ...

    def setExecutablePath(self, path: unicode) -> None: ...

    def setExecutableSHA256(self, sha256: unicode) -> None: ...

    def setImageBase(self, base: ghidra.program.model.address.Address, commit: bool) -> None: ...

    def setLanguage(self, newLanguage: ghidra.program.model.lang.Language, newCompilerSpecID: ghidra.program.model.lang.CompilerSpecID, forceRedisassembly: bool, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def setName(self, newName: unicode) -> None: ...

    @overload
    def setObjChanged(self, eventType: ghidra.program.util.ProgramEvent, affected: object, oldValue: object, newValue: object) -> None: ...

    @overload
    def setObjChanged(self, eventType: ghidra.program.util.ProgramEvent, addr: ghidra.program.model.address.Address, affectedObj: object, oldValue: object, newValue: object) -> None: ...

    def setPreferredRootNamespaceCategoryPath(self, categoryPath: unicode) -> None: ...

    def setPropertyChanged(self, propertyName: unicode, codeUnitAddr: ghidra.program.model.address.Address, oldValue: object, newValue: object) -> None: ...

    def setPropertyRangeRemoved(self, propertyName: unicode, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None: ...

    def setRegisterValuesChanged(self, register: ghidra.program.model.lang.Register, start: ghidra.program.model.address.Address, end: ghidra.program.model.address.Address) -> None: ...

    def setTemporary(self, state: bool) -> None: ...

    def sourceArchiveAdded(self, sourceArchiveID: ghidra.util.UniversalID, eventType: ghidra.program.util.ProgramEvent) -> None: ...

    def sourceArchiveChanged(self, sourceArchiveID: ghidra.util.UniversalID, eventType: ghidra.program.util.ProgramEvent) -> None: ...

    @overload
    def startTransaction(self, description: unicode) -> int: ...

    @overload
    def startTransaction(self, description: unicode, listener: ghidra.framework.model.AbortedTransactionListener) -> int: ...

    def symbolAdded(self, symbol: ghidra.program.model.symbol.Symbol, eventType: ghidra.program.util.ProgramEvent, addr: ghidra.program.model.address.Address, oldValue: object, newValue: object) -> None:
        """
        Notification that a symbol was added.
        @param symbol the symbol that was added.
        @param eventType the type of change
        @param addr the address of the symbol that added
        @param oldValue old value depends on the type of the change
        @param newValue old value depends on the type of the change
        """
        ...

    def symbolChanged(self, symbol: ghidra.program.model.symbol.Symbol, eventType: ghidra.program.util.ProgramEvent, addr: ghidra.program.model.address.Address, affectedObj: object, oldValue: object, newValue: object) -> None:
        """
        Notification that a symbol was changed.
        @param symbol the symbol that was changed.
        @param eventType the type of change
        @param addr the address of the symbol that changed
        @param affectedObj the object that was changed
        @param oldValue old value depends on the type of the change
        @param newValue old value depends on the type of the change
        """
        ...

    def tagChanged(self, tag: ghidra.program.model.listing.FunctionTag, eventType: ghidra.program.util.ProgramEvent, oldValue: object, newValue: object) -> None:
        """
        Notification that a {@link FunctionTag} was changed. This can be either an
         edit or a delete.
        @param tag the tag that was changed.
        @param eventType the type of change
        @param oldValue old value
        @param newValue new value
        """
        ...

    def tagCreated(self, tag: ghidra.program.model.listing.FunctionTag, eventType: ghidra.program.util.ProgramEvent) -> None:
        """
        Notification that a new {@link FunctionTag} was created.
        @param tag the tag that was created.
        @param eventType the type of change
        """
        ...

    def toString(self) -> unicode: ...

    def undo(self) -> None: ...

    def unlock(self) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @overload
    def withTransaction(self, __a0: unicode, __a1: utility.function.ExceptionalCallback) -> None: ...

    @overload
    def withTransaction(self, __a0: unicode, __a1: utility.function.ExceptionalSupplier) -> object: ...

    @property
    def addressFactory(self) -> ghidra.program.database.ProgramAddressFactory: ...

    @property
    def addressMap(self) -> ghidra.program.database.map.AddressMapDB: ...

    @property
    def bookmarkManager(self) -> ghidra.program.database.bookmark.BookmarkDBManager: ...

    @property
    def changeable(self) -> bool: ...

    @property
    def changed(self) -> None: ...  # No getter available.

    @changed.setter
    def changed(self, value: ghidra.program.util.ProgramChangeRecord) -> None: ...

    @property
    def changes(self) -> ghidra.program.model.listing.ProgramChangeSet: ...

    @property
    def codeManager(self) -> ghidra.program.database.code.CodeManager: ...

    @property
    def compiler(self) -> unicode: ...

    @compiler.setter
    def compiler(self, value: unicode) -> None: ...

    @property
    def compilerSpec(self) -> ghidra.program.model.lang.CompilerSpec: ...

    @property
    def creationDate(self) -> java.util.Date: ...

    @property
    def dataTypeManager(self) -> ghidra.program.database.data.ProgramDataTypeManager: ...

    @property
    def defaultPointerSize(self) -> int: ...

    @property
    def description(self) -> unicode: ...

    @property
    def effectiveImageBase(self) -> None: ...  # No getter available.

    @effectiveImageBase.setter
    def effectiveImageBase(self, value: ghidra.program.model.address.Address) -> None: ...

    @property
    def equateTable(self) -> ghidra.program.database.symbol.EquateManager: ...

    @property
    def executableFormat(self) -> unicode: ...

    @executableFormat.setter
    def executableFormat(self, value: unicode) -> None: ...

    @property
    def executableMD5(self) -> unicode: ...

    @executableMD5.setter
    def executableMD5(self, value: unicode) -> None: ...

    @property
    def executablePath(self) -> unicode: ...

    @executablePath.setter
    def executablePath(self, value: unicode) -> None: ...

    @property
    def executableSHA256(self) -> unicode: ...

    @executableSHA256.setter
    def executableSHA256(self, value: unicode) -> None: ...

    @property
    def externalManager(self) -> ghidra.program.database.external.ExternalManagerDB: ...

    @property
    def functionManager(self) -> ghidra.program.database.function.FunctionManagerDB: ...

    @property
    def globalNamespace(self) -> ghidra.program.model.symbol.Namespace: ...

    @property
    def imageBase(self) -> ghidra.program.model.address.Address: ...

    @property
    def language(self) -> ghidra.program.model.lang.Language: ...

    @property
    def languageID(self) -> ghidra.program.model.lang.LanguageID: ...

    @property
    def languageUpgradePending(self) -> bool: ...

    @property
    def listing(self) -> ghidra.program.model.listing.Listing: ...

    @property
    def maxAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def memory(self) -> ghidra.program.database.mem.MemoryMapDB: ...

    @property
    def metadata(self) -> java.util.Map: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def name(self) -> unicode: ...

    @name.setter
    def name(self, value: unicode) -> None: ...

    @property
    def namespaceManager(self) -> ghidra.program.database.symbol.NamespaceManager: ...

    @property
    def preferredRootNamespaceCategoryPath(self) -> ghidra.program.model.data.CategoryPath: ...

    @property
    def programContext(self) -> ghidra.program.model.listing.ProgramContext: ...

    @property
    def programUserData(self) -> ghidra.program.model.listing.ProgramUserData: ...

    @property
    def referenceManager(self) -> ghidra.program.database.references.ReferenceDBManager: ...

    @property
    def relocationTable(self) -> ghidra.program.database.reloc.RelocationManager: ...

    @property
    def storedVersion(self) -> int: ...

    @property
    def symbolTable(self) -> ghidra.program.database.symbol.SymbolManager: ...

    @property
    def treeManager(self) -> ghidra.program.database.module.TreeManager: ...

    @property
    def uniqueProgramID(self) -> long: ...

    @property
    def usrPropertyManager(self) -> ghidra.program.model.util.PropertyMapManager: ...