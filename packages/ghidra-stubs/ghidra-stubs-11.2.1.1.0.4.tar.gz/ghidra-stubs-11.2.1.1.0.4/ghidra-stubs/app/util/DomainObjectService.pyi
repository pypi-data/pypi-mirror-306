from typing import overload
import ghidra.framework.model
import java.lang


class DomainObjectService(object):
    """
    Simple interface for getting a DomainObject. This is used to delay the opening of
     a domainObject until it is needed.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDomainObject(self) -> ghidra.framework.model.DomainObject:
        """
        Get the domain object to be exported
        @return domain object or null if export limited to domain file
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

    @property
    def domainObject(self) -> ghidra.framework.model.DomainObject: ...