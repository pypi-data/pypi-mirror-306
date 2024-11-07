from typing import overload
import ghidra.app.util
import ghidra.framework.options
import ghidra.program.model.address
import java.awt
import java.lang


class LibrarySearchPathDummyOption(ghidra.app.util.Option):
    """
    A dummy Option used to render a button that will allow the user to edit the global
     list of library search paths
    """





    def __init__(self, name: unicode):
        """
        Creates a new {@link LibrarySearchPathDummyOption}
        @param name The name of the option
        """
        ...



    def copy(self) -> ghidra.app.util.Option: ...

    def equals(self, __a0: object) -> bool: ...

    def getArg(self) -> unicode:
        """
        {@return the command line argument for this option (could be null)}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCustomEditorComponent(self) -> java.awt.Component: ...

    def getGroup(self) -> unicode:
        """
        {@return the group name for this option; may be null if group was not specified}
        """
        ...

    def getName(self) -> unicode:
        """
        {@return the name of this option}
        """
        ...

    def getState(self) -> ghidra.framework.options.SaveState:
        """
        {@return the current project state associated with this option (could be null)}
        """
        ...

    def getStateKey(self) -> unicode:
        """
        {@return the state key name (could be null)}
        """
        ...

    def getValue(self) -> object:
        """
        {@return the value of this option}
        """
        ...

    def getValueClass(self) -> java.lang.Class: ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def parseAndSetValueByType(self, str: unicode, addressFactory: ghidra.program.model.address.AddressFactory) -> bool:
        """
        Set the value for this option by parsing the given string and converting it to the option's
         type.  Fails if this option doesn't have a type associated with it, or if an unsupported
         type is needed to be parsed.
        @param str The value to set, in string form.
        @param addressFactory An address factory to use for when the option trying to be set is an Address.
         If null, an exception will be thrown for Address type options.
        @return True if the value was successfully parsed and set; otherwise, false.
        """
        ...

    def setOptionListener(self, listener: ghidra.app.util.OptionListener) -> None: ...

    def setValue(self, object: object) -> None:
        """
        Set the value for this option.
        @param object value of this option
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
    def customEditorComponent(self) -> java.awt.Component: ...

    @property
    def valueClass(self) -> java.lang.Class: ...