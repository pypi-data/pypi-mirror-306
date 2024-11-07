from typing import overload
import ghidra.framework.options
import java.lang


class CustomOption(object):
    CUSTOM_OPTION_CLASS_NAME_KEY: unicode = u'CUSTOM_OPTION_CLASS'







    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def readState(self, properties: ghidra.framework.options.GProperties) -> None:
        """
        Read state from the given properties
        @param properties container of state information
        """
        ...

    def toString(self) -> unicode:
        """
        Subclasses should implement this method to provide a formatted string value of this option 
         value.  The returned value will be used in support of the 
         {@link Options#getValueAsString(String)} and {@link Options#getDefaultValueAsString(String)}.
        @return option value as string
        """
        ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    def writeState(self, properties: ghidra.framework.options.GProperties) -> None:
        """
        Write state into the given properties
        @param properties container of state information
        """
        ...

