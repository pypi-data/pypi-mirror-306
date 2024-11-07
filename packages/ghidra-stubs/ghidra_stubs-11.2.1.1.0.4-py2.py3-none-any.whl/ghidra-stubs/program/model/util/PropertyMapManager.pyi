from typing import Iterator
from typing import overload
import ghidra.program.model.address
import ghidra.program.model.util
import ghidra.util.task
import java.lang


class PropertyMapManager(object):
    """
    Interface for managing a set of PropertyManagers.
    """









    def createIntPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.IntPropertyMap:
        """
        Creates a new IntPropertyMap with the given name.
        @param propertyName the name for the new property.
        @return newly created integer object map
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createLongPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.LongPropertyMap:
        """
        Creates a new LongPropertyMap with the given name.
        @param propertyName the name for the new property.
        @return newly created long object map
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createObjectPropertyMap(self, propertyName: unicode, objectClass: java.lang.Class) -> ghidra.program.model.util.ObjectPropertyMap:
        """
        Creates a new ObjectPropertyMap with the given name.
        @param <T> {@link Saveable} property value type
        @param propertyName the name for the new property.
        @param objectClass {@link Saveable} implementation class
        @return newly created {@link Saveable} object map
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createStringPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.StringPropertyMap:
        """
        Creates a new StringPropertyMap with the given name.
        @param propertyName the name for the new property.
        @return newly created string object map
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def createVoidPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.VoidPropertyMap:
        """
        Creates a new VoidPropertyMap with the given name.
        @param propertyName the name for the new property.
        @return newly created void map
        @exception DuplicateNameException thrown if a PropertyMap already
         exists with that name.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getIntPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.IntPropertyMap:
        """
        Returns the IntPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @return existing map or null if not found
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not an IntPropertyMap.
        """
        ...

    def getLongPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.LongPropertyMap:
        """
        Returns the LongPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @return existing map or null if not found
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not an LongPropertyMap.
        """
        ...

    def getObjectPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.ObjectPropertyMap:
        """
        Returns the ObjectPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @return existing map or null if not found
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not an ObjectPropertyMap.
        """
        ...

    def getPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.PropertyMap:
        """
        Returns the PropertyMap with the given name or null if no PropertyMap
         exists with that name.
        @return existing map or null if not found
        @param propertyName the name of the property to retrieve.
        """
        ...

    def getStringPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.StringPropertyMap:
        """
        Returns the StringPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @return existing map or null if not found
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not a StringPropertyMap.
        """
        ...

    def getVoidPropertyMap(self, propertyName: unicode) -> ghidra.program.model.util.VoidPropertyMap:
        """
        Returns the VoidPropertyMap associated with the given name.
        @param propertyName the name of the property to retrieve.
        @return existing map or null if not found
        @throws TypeMismatchException if a propertyMap named propertyName
         exists but is not a VoidPropertyMap.
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def propertyManagers(self) -> Iterator[unicode]:
        """
        Returns an iterator over the names of all existing PropertyMaps.
        """
        ...

    @overload
    def removeAll(self, addr: ghidra.program.model.address.Address) -> None:
        """
        Removes any property at the given address from all defined 
         PropertyMaps.
        @param addr the address at which to remove all property values.
        """
        ...

    @overload
    def removeAll(self, startAddr: ghidra.program.model.address.Address, endAddr: ghidra.program.model.address.Address, monitor: ghidra.util.task.TaskMonitor) -> None:
        """
        Removes all properties in the given range from all user 
         defined PropertyMaps. 
         The specified start and end addresses must form a valid range within
         a single {@link AddressSpace}.
        @param startAddr the first address in the range of addresses where 
         propertie values are to be removed.
        @param endAddr the last address in the range of addresses where 
         propertie values are to be removed.
        @param monitor monitors progress
        @throws CancelledException if the user cancelled the operation.
        """
        ...

    def removePropertyMap(self, propertyName: unicode) -> bool:
        """
        Removes the PropertyMap with the given name.
        @param propertyName the name of the property to remove.
        @return true if a PropertyMap with that name was found (and removed)
        """
        ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

