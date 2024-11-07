from typing import Iterator
from typing import List
from typing import overload
import db
import ghidra.program.database.map
import ghidra.program.model.data
import ghidra.program.model.lang
import ghidra.util
import ghidra.util.task
import java.io
import java.lang
import java.util
import utility.function


class DataTypeManagerDB(object, ghidra.program.model.data.DataTypeManager):
    """
    Base class for DB-backed data type managers. 
     Important Notes:
 
     When invoking DataType#isEquivalent(DataType) involving
     DataTypeDB objects it is important to invoke the method on DataTypeDB. This
     will ensure that the internal optimization mechanisms are used.
     It is important that the use of DataType#clone(DataTypeManager)
     and DataType#copy(DataTypeManager) be avoided when possible to ensure
     full benefit of the #equivalenceCache and #resolveCache.
 
    """

    BAD_DATATYPE_ID: long = -0x2L
    BUILT_IN_ARCHIVE_KEY: long = 0x1L
    BUILT_IN_ARCHIVE_UNIVERSAL_ID: ghidra.util.UniversalID
    BUILT_IN_DATA_TYPES_NAME: unicode = u'BuiltInTypes'
    DEFAULT_CALLING_CONVENTION_ID: int = 1
    DEFAULT_DATATYPE_ID: long = 0x0L
    LOCAL_ARCHIVE_KEY: long = 0x0L
    LOCAL_ARCHIVE_UNIVERSAL_ID: ghidra.util.UniversalID
    NULL_DATATYPE_ID: long = -0x1L
    UNKNOWN_CALLING_CONVENTION_ID: int = 0







    def addDataType(self, originalDataType: ghidra.program.model.data.DataType, handler: ghidra.program.model.data.DataTypeConflictHandler) -> ghidra.program.model.data.DataType: ...

    def addDataTypeManagerListener(self, l: ghidra.program.model.data.DataTypeManagerChangeListener) -> None: ...

    def addDataTypes(self, dataTypes: java.util.Collection, handler: ghidra.program.model.data.DataTypeConflictHandler, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def addInvalidatedListener(self, listener: ghidra.program.model.data.InvalidatedListener) -> None: ...

    def allowsDefaultBuiltInSettings(self) -> bool: ...

    def allowsDefaultComponentSettings(self) -> bool: ...

    def associateDataTypeWithArchive(self, datatype: ghidra.program.model.data.DataType, archive: ghidra.program.model.data.SourceArchive) -> None: ...

    def close(self) -> None: ...

    def contains(self, dataType: ghidra.program.model.data.DataType) -> bool: ...

    def containsCategory(self, path: ghidra.program.model.data.CategoryPath) -> bool: ...

    def createCategory(self, path: ghidra.program.model.data.CategoryPath) -> ghidra.program.model.data.Category: ...

    def dataTypeChanged(self, dt: ghidra.program.model.data.DataType, isAutoChange: bool) -> None:
        """
        Notification when data type is changed.
        @param dt data type that is changed
        @param isAutoChange true if change was an automatic change in response to
         another datatype's change (e.g., size, alignment).
        """
        ...

    def dataTypeSettingsChanged(self, dt: ghidra.program.model.data.DataType) -> None:
        """
        Notification when data type settings have changed.
        @param dt data type that is changed
        """
        ...

    def dbError(self, e: java.io.IOException) -> None:
        """
        Handles IOExceptions
        @param e the exception to handle
        """
        ...

    def dedupeAllConflicts(self, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        De-duplicate equivalent conflict datatypes which share a common base data type name and
         are found to be equivalent.
        @param monitor task monitor
        @throws CancelledException if task is cancelled
        """
        ...

    def dedupeConflicts(self, dataType: ghidra.program.model.data.DataType) -> bool:
        """
        De-duplicate equivalent conflict datatypes which share a common base data type name and
         are found to be equivalent.
        @param dataType data type whose related conflict types should be de-duplicated
        @return true if one or more datatypes were de-duplicted or dde-conflicted, else false
        """
        ...

    def disassociate(self, dataType: ghidra.program.model.data.DataType) -> None: ...

    def dispose(self) -> None: ...

    def endTransaction(self, __a0: int, __a1: bool) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def findDataType(self, dataTypePath: unicode) -> ghidra.program.model.data.DataType: ...

    def findDataTypeForID(self, datatypeID: ghidra.util.UniversalID) -> ghidra.program.model.data.DataType: ...

    @overload
    def findDataTypes(self, __a0: unicode, __a1: List[object]) -> None: ...

    @overload
    def findDataTypes(self, __a0: unicode, __a1: List[object], __a2: bool, __a3: ghidra.util.task.TaskMonitor) -> None: ...

    def findEnumValueNames(self, value: long, enumValueNames: java.util.Set) -> None: ...

    def fixupComposites(self, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Fixup all composites and thier components which may be affected by a data organization
         change include primitive type size changes and alignment changes.  It is highly recommended
         that this program be open with exclusive access before invoking this method to avoid 
         excessive merge conflicts with other users.
        @param monitor task monitor
        @throws CancelledException if processing cancelled - data types may not properly reflect
         updated compiler specification
        """
        ...

    def flushEvents(self) -> None: ...

    def getAddressMap(self) -> ghidra.program.database.map.AddressMap: ...

    def getAllComposites(self) -> Iterator[ghidra.program.model.data.Composite]: ...

    @overload
    def getAllDataTypes(self) -> Iterator[ghidra.program.model.data.DataType]: ...

    @overload
    def getAllDataTypes(self, __a0: List[object]) -> None: ...

    def getAllFunctionDefinitions(self) -> Iterator[ghidra.program.model.data.FunctionDefinition]: ...

    def getAllStructures(self) -> Iterator[ghidra.program.model.data.Structure]: ...

    def getCallingConvention(self, name: unicode) -> ghidra.program.model.lang.PrototypeModel: ...

    def getCallingConventionID(self, name: unicode, restrictive: bool) -> int:
        """
        Get (and assign if needed thus requiring open transaction) the ID associated with the 
         specified calling convention name.  If name is a new convention and the number of stored
         convention names exceeds 127 the returned ID will correspond to the unknown calling 
         convention.
        @param name calling convention name
        @param restrictive if true an error will be thrown if name is not defined by 
         {@link GenericCallingConvention} or the associated compiler specification if 
         datatype manager has an associated program architecture.
        @return calling convention ID
        @throws IOException if database IO error occurs
        @throws InvalidInputException if restrictive is true and name is not defined by 
         {@link GenericCallingConvention} or the associated compiler specification if 
         datatype manager has an associated program architecture.
        """
        ...

    def getCallingConventionName(self, id: int) -> unicode:
        """
        Get calling convention name corresponding to existing specified id.
        @param id calling convention ID
        @return calling convention name if found else unknown
        """
        ...

    @overload
    def getCategory(self, id: long) -> ghidra.program.model.data.Category:
        """
        Get the category for the given ID.
        @return null if no category exists with the given ID.
        """
        ...

    @overload
    def getCategory(self, path: ghidra.program.model.data.CategoryPath) -> ghidra.program.model.data.Category: ...

    def getCategoryCount(self) -> int: ...

    def getClass(self) -> java.lang.Class: ...

    def getDataOrganization(self) -> ghidra.program.model.data.DataOrganization: ...

    @overload
    def getDataType(self, dataTypeID: long) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, dataTypePath: unicode) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, dataTypePath: ghidra.program.model.data.DataTypePath) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, path: ghidra.program.model.data.CategoryPath, name: unicode) -> ghidra.program.model.data.DataType: ...

    @overload
    def getDataType(self, sourceArchive: ghidra.program.model.data.SourceArchive, datatypeID: ghidra.util.UniversalID) -> ghidra.program.model.data.DataType: ...

    def getDataTypeCount(self, includePointersAndArrays: bool) -> int: ...

    @overload
    def getDataTypes(self, path: ghidra.program.model.data.CategoryPath) -> List[ghidra.program.model.data.DataType]:
        """
        Gets the datatypes in the given category path
        @param path the category path in which to look for datatypes
        @return array of datatypes contained with specified category
        """
        ...

    @overload
    def getDataTypes(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> List[ghidra.program.model.data.DataType]: ...

    def getDataTypesContaining(self, dataType: ghidra.program.model.data.DataType) -> java.util.Set: ...

    def getDefaultCallingConvention(self) -> ghidra.program.model.lang.PrototypeModel: ...

    def getDefinedCallingConventionNames(self) -> java.util.Collection: ...

    def getFavorites(self) -> List[ghidra.program.model.data.DataType]: ...

    def getID(self, dt: ghidra.program.model.data.DataType) -> long: ...

    def getKnownCallingConventionNames(self) -> java.util.Collection: ...

    def getLastChangeTimeForMyManager(self) -> long: ...

    def getLocalSourceArchive(self) -> ghidra.program.model.data.SourceArchive: ...

    def getName(self) -> unicode: ...

    @overload
    def getPointer(self, dt: ghidra.program.model.data.DataType) -> ghidra.program.model.data.Pointer: ...

    @overload
    def getPointer(self, dt: ghidra.program.model.data.DataType, size: int) -> ghidra.program.model.data.Pointer: ...

    def getProgramArchitecture(self) -> ghidra.program.model.lang.ProgramArchitecture: ...

    def getProgramArchitectureSummary(self) -> unicode: ...

    def getResolvedID(self, dt: ghidra.program.model.data.DataType) -> long: ...

    def getRootCategory(self) -> ghidra.program.model.data.Category: ...

    @overload
    def getSourceArchive(self, fileID: unicode) -> ghidra.program.model.data.SourceArchive: ...

    @overload
    def getSourceArchive(self, sourceID: ghidra.util.UniversalID) -> ghidra.program.model.data.SourceArchive: ...

    def getSourceArchives(self) -> List[ghidra.program.model.data.SourceArchive]: ...

    def getType(self) -> ghidra.program.model.data.ArchiveType: ...

    def getUniqueName(self, path: ghidra.program.model.data.CategoryPath, baseName: unicode) -> unicode: ...

    def getUniversalID(self) -> ghidra.util.UniversalID: ...

    @overload
    def getUnusedConflictName(self, dt: ghidra.program.model.data.DataType) -> unicode:
        """
        This method gets a ".conflict" name that is not currently used by any data
         types in the datatype's category within this data type manager.  If the baseName without
         conflict suffix is not used that name will be returned.
         <br>
         NOTE: The original datatype name will be returned unchanged for pointers and arrays since 
         they cannot be renamed.
        @param dt datatype who name is used to establish non-conflict base name
        @return the unused conflict name or original name for datatypes whose name is automatic
        """
        ...

    @overload
    def getUnusedConflictName(self, path: ghidra.program.model.data.CategoryPath, dt: ghidra.program.model.data.DataType) -> unicode:
        """
        This method gets a ".conflict" name that is not currently used by any data
         types in the indicated category within this data type manager.  If the baseName without
         conflict suffix is not used that name will be returned.
         <br>
         NOTE: The original datatype name will be returned unchanged for pointers and arrays since 
         they cannot be renamed.
         <br>
         NOTE: Otherwise, if category does not exist the non-conflict name will be returned.
        @param path the category path of the category where the new data type live in
                     the data type manager.
        @param dt datatype who name is used to establish non-conflict base name
        @return the unused conflict name
        """
        ...

    def hashCode(self) -> int: ...

    def invalidateCache(self) -> None:
        """
        Invalidates the cache.
        """
        ...

    def isChanged(self) -> bool: ...

    def isFavorite(self, dataType: ghidra.program.model.data.DataType) -> bool: ...

    def isUpdatable(self) -> bool: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def notifyRestored(self) -> None:
        """
        This method should be invoked following an undo/redo or a transaction rollback situation.
         This will notify {@link DataTypeManagerChangeListenerHandler} and its listeners that this 
         manager has just been restored (e.g., undo/redo/rollback).
        """
        ...

    def openTransaction(self, __a0: unicode) -> db.Transaction: ...

    def remove(self, dataType: ghidra.program.model.data.DataType, monitor: ghidra.util.task.TaskMonitor) -> bool: ...

    def removeDataTypeManagerListener(self, l: ghidra.program.model.data.DataTypeManagerChangeListener) -> None: ...

    def removeInvalidatedListener(self, listener: ghidra.program.model.data.InvalidatedListener) -> None: ...

    def removeSourceArchive(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> None: ...

    def replaceDataType(self, existingDt: ghidra.program.model.data.DataType, replacementDt: ghidra.program.model.data.DataType, updateCategoryPath: bool) -> ghidra.program.model.data.DataType: ...

    def replaceSourceArchive(self, oldSourceArchive: ghidra.program.model.data.SourceArchive, newSourceArchive: ghidra.program.model.data.SourceArchive) -> None:
        """
        Replace one source archive (oldDTM) with another (newDTM). Any data types
         whose source was the oldDTM will be changed to have a source that is the
         newDTM. The oldDTM will no longer be referenced as a source by this data type
         manager.
        @param oldSourceArchive data type manager for the old source archive
        @param newSourceArchive data type manager for the new source archive
        @throws IllegalArgumentException if the oldDTM isn't currently a source
                                          archive for this data type manager or if the
                                          old and new source archives already have the
                                          same unique ID.
        """
        ...

    def resolve(self, dataType: ghidra.program.model.data.DataType, handler: ghidra.program.model.data.DataTypeConflictHandler) -> ghidra.program.model.data.DataType: ...

    def resolveSourceArchive(self, sourceArchive: ghidra.program.model.data.SourceArchive) -> ghidra.program.model.data.SourceArchive: ...

    def setFavorite(self, dataType: ghidra.program.model.data.DataType, isFavorite: bool) -> None: ...

    def setName(self, __a0: unicode) -> None: ...

    def sourceArchiveChanged(self, sourceArchiveID: ghidra.util.UniversalID) -> None: ...

    def startTransaction(self, __a0: unicode) -> int: ...

    def toString(self) -> unicode: ...

    def updateID(self) -> None: ...

    @overload
    def updateSourceArchiveName(self, archiveFileID: unicode, name: unicode) -> bool: ...

    @overload
    def updateSourceArchiveName(self, sourceID: ghidra.util.UniversalID, name: unicode) -> bool: ...

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
    def addressMap(self) -> ghidra.program.database.map.AddressMap: ...

    @property
    def allComposites(self) -> java.util.Iterator: ...

    @property
    def allDataTypes(self) -> java.util.Iterator: ...

    @property
    def allFunctionDefinitions(self) -> java.util.Iterator: ...

    @property
    def allStructures(self) -> java.util.Iterator: ...

    @property
    def categoryCount(self) -> int: ...

    @property
    def changed(self) -> bool: ...

    @property
    def dataOrganization(self) -> ghidra.program.model.data.DataOrganization: ...

    @property
    def defaultCallingConvention(self) -> ghidra.program.model.lang.PrototypeModel: ...

    @property
    def definedCallingConventionNames(self) -> java.util.Collection: ...

    @property
    def favorites(self) -> List[object]: ...

    @property
    def knownCallingConventionNames(self) -> java.util.Collection: ...

    @property
    def lastChangeTimeForMyManager(self) -> long: ...

    @property
    def localSourceArchive(self) -> ghidra.program.model.data.SourceArchive: ...

    @property
    def name(self) -> unicode: ...

    @name.setter
    def name(self, value: unicode) -> None: ...

    @property
    def programArchitecture(self) -> ghidra.program.model.lang.ProgramArchitecture: ...

    @property
    def programArchitectureSummary(self) -> unicode: ...

    @property
    def rootCategory(self) -> ghidra.program.model.data.Category: ...

    @property
    def sourceArchives(self) -> List[object]: ...

    @property
    def type(self) -> ghidra.program.model.data.ArchiveType: ...

    @property
    def universalID(self) -> ghidra.util.UniversalID: ...

    @property
    def updatable(self) -> bool: ...