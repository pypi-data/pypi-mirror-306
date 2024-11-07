from typing import overload
import ghidra.program.model.address
import java.lang


class AddressCorrelationRange(object):
    """
    A simple object that holds an AddressCorrelation address range and then name of the 
     correlation.s
    """





    def __init__(self, range: ghidra.program.model.address.AddressRange, correlatorName: unicode): ...



    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getCorrelatorName(self) -> unicode: ...

    def getMinAddress(self) -> ghidra.program.model.address.Address: ...

    def getRange(self) -> ghidra.program.model.address.AddressRange: ...

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
    def correlatorName(self) -> unicode: ...

    @property
    def minAddress(self) -> ghidra.program.model.address.Address: ...

    @property
    def range(self) -> ghidra.program.model.address.AddressRange: ...