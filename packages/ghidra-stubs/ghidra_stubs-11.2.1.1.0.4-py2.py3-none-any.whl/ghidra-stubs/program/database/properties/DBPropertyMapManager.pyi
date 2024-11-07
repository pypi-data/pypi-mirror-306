from typing import Iterator
from typing import overload
import ghidra.framework.data
import ghidra.program.database
import ghidra.program.model.address
import ghidra.program.model.util
import ghidra.util.task
import java.lang


class DBPropertyMapManager(object, ghidra.program.model.util.PropertyMapManager, ghidra.program.database.ManagerDB):
    """
    Manages generic address keyed properties.
    """





    def __init__(self, handle: db.DBHandle, changeMgr: ghidra.program.util.ChangeManager, addrMap: ghidra.program.database.map.AddressMap, openMode: ghidra.framework.data.OpenMode, lock: ghidra.util.Lock, monitor: ghidra.util.task.TaskMonitor):
        """
        Constructs a new DBPropertyMapManager
        @param handle the database handle
        @param changeMgr the change manager
        @param addrMap the address map
        @param openMode the program open mode.
        @param lock the program synchronization lock
        @param monitor the task monitor
        @throws IOException if an IO error occurs
        @throws VersionException if a version error occurs
        @throws CancelledException if task is cancelled
        """
        ...



    def createIntPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.IntPropertyMap:
        """
        Creates a new IntPropertyMap with the given name.
        @param propertyName the name of the property to create.
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createLongPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.LongPropertyMap:
        """
        Creates a new LongPropertyMap with the given name.
        @param propertyName the name of the property to create.
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createObjectPropertyMap(self, propertyName: unicode, objectClass: java.lang.Class) -> ghidra.program.model.util.ObjectPropertyMap: ...

    def createStringPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.StringPropertyMap:
        """
        Creates a new StringPropertyMap with the given name.
        @param propertyName the name of the property to create.
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createVoidPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.VoidPropertyMap:
        """
        Creates a new VoidPropertyMap with the given name.
        @param propertyName the name of the property to create.
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def deleteAddressRange(self, startAddr: ghidra.program.model.address.Address, endAddr: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def dispose(self) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getIntPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.IntPropertyMap:
        """
        Returns the IntPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not an IntPropertyMap.
        """
        ...

    def getLongPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.LongPropertyMap:
        """
        Returns the LongPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not an LongPropertyMap.
        """
        ...

    def getObjectPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.ObjectPropertyMap:
        """
        Returns the ObjectPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not an ObjectPropertyMap.
        """
        ...

    def getPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.PropertyMap:
        """
        Returns the PropertyMap with the given name or null if no PropertyMap
         exists with that name.
        @param propertyName the name of the property to retrieve.
        """
        ...

    def getStringPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.StringPropertyMap:
        """
        Returns the StringPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not a StringPropertyMap.
        """
        ...

    def getVoidPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.VoidPropertyMap:
        """
        Returns the VoidPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not a VoidPropertyMap.
        """
        ...

    def hashCode(self) -> int: ...

    def invalidateCache(self, all: bool) -> None: ...

    def moveAddressRange(self, fromAddr: ghidra.program.model.address.Address, toAddr: ghidra.program.model.address.Address, length: long, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def programReady(self, openMode: ghidra.framework.data.OpenMode, currentRevision: int, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def propertyManagers(self) -> Iterator[unicode]: ...

    @overload
    def removeAll(self, addr: ghidra.program.model.address.Address) -> None: ...

    @overload
    def removeAll(self, startAddr: ghidra.program.model.address.Address, endAddr: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> None: ...

    def removePropertyMap(self, propertyName: unicode) -> bool: ...

    def setProgram(self, program: ghidra.program.database.ProgramDB) -> None: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def program(self) -> None: ...  # No getter available.

    @program.setter
    def program(self, value: ghidra.program.database.ProgramDB) -> None: ...