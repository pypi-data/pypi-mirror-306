from typing import overload
import ghidra.program.model.address
import ghidra.program.model.util
import java.lang


class LongPropertyMap(ghidra.program.model.util.PropertyMap, object):
    """
    Property manager that deals with properties that are of
      long type.
    """









    @overload
    def add(self, addr: ghidra.program.model.address.Address, value: long) -> None:
        """
        Add a long value at the specified address.
        @param addr address for the property
        @param value value of the property
        """
        ...

    @overload
    def add(self, addr: ghidra.program.model.address.Address, value: object) -> None: ...

    def equals(self, __a0: object) -> bool: ...

    def get(self, __a0: ghidra.program.model.address.Address) -> object: ...

    def getClass(self) -> java.lang.Class: ...

    def getFirstPropertyAddress(self) -> ghidra.program.model.address.Address: ...

    def getLastPropertyAddress(self) -> ghidra.program.model.address.Address: ...

    def getLong(self, addr: ghidra.program.model.address.Address) -> long:
        """
        Get the long value at the given address.
        @param addr the address from where to get the long value
        @return long property value
        @throws NoValueException if there is no property value at addr.
        """
        ...

    def getName(self) -> unicode: ...

    def getNextPropertyAddress(self, __a0: ghidra.program.model.address.Address) -> ghidra.program.model.address.Address: ...

    def getPreviousPropertyAddress(self, __a0: ghidra.program.model.address.Address) -> ghidra.program.model.address.Address: ...

    @overload
    def getPropertyIterator(self) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getPropertyIterator(self, __a0: ghidra.program.model.address.AddressSetView) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getPropertyIterator(self, __a0: ghidra.program.model.address.Address, __a1: bool) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getPropertyIterator(self, __a0: ghidra.program.model.address.AddressSetView, __a1: bool) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getPropertyIterator(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address) -> ghidra.program.model.address.AddressIterator: ...

    @overload
    def getPropertyIterator(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address, __a2: bool) -> ghidra.program.model.address.AddressIterator: ...

    def getSize(self) -> int: ...

    def getValueClass(self) -> java.lang.Class: ...

    def hasProperty(self, __a0: ghidra.program.model.address.Address) -> bool: ...

    def hashCode(self) -> int: ...

    @overload
    def intersects(self, __a0: ghidra.program.model.address.AddressSetView) -> bool: ...

    @overload
    def intersects(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address) -> bool: ...

    def moveRange(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address, __a2: ghidra.program.model.address.Address) -> None: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def remove(self, __a0: ghidra.program.model.address.Address) -> bool: ...

    def removeRange(self, __a0: ghidra.program.model.address.Address, __a1: ghidra.program.model.address.Address) -> bool: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def firstPropertyAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def lastPropertyAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def name(self) -> unicode: ...

    @property
    def propertyIterator(self) -> ghidra.program.model.address.AddressIterator: ...

    @property
    def size(self) -> int: ...

    @property
    def valueClass(self) -> java.lang.Class: ...