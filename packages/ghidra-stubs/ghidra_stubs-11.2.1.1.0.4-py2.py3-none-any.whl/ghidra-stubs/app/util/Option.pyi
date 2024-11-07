from typing import overload
import ghidra.app.util
import ghidra.framework.options
import ghidra.program.model.address
import java.awt
import java.lang


class Option(object):
    """
    Container class to hold a name, value, and class of the value.
    """





    @overload
    def __init__(self, name: unicode, valueClass: java.lang.Class):
        """
        Construct a new Option.
        @param name name of the option
        @param valueClass class of the option's value
        """
        ...

    @overload
    def __init__(self, name: unicode, value: object):
        """
        Construct a new Option.
        @param name name of the option
        @param value value of the option. Value can't be null with this constructor.
        @throws IllegalArgumentException if value is null
        """
        ...

    @overload
    def __init__(self, group: unicode, name: unicode, value: object):
        """
        Construct a new Option.
        @param group Name for group of options
        @param name name of the option
        @param value value of the option
        @throws IllegalArgumentException if value is null
        """
        ...

    @overload
    def __init__(self, name: unicode, value: object, valueClass: java.lang.Class, arg: unicode):
        """
        Construct a new Option
        @param name name of the option
        @param value value of the option
        @param valueClass class of the option's value
        @param arg the option's command line argument
        """
        ...

    @overload
    def __init__(self, name: unicode, valueClass: java.lang.Class, value: object, arg: unicode, group: unicode):
        """
        Construct a new Option
        @param name name of the option
        @param valueClass class of the option's value
        @param value value of the option
        @param arg the option's command line argument
        @param group Name for group of options
        """
        ...

    @overload
    def __init__(self, name: unicode, valueClass: java.lang.Class, value: object, arg: unicode, group: unicode, stateKey: unicode):
        """
        Construct a new Option
        @param name name of the option
        @param valueClass class of the option's value
        @param value value of the option
        @param arg the option's command line argument
        @param group Name for group of options
        @param stateKey state key name
        """
        ...



    def copy(self) -> ghidra.app.util.Option:
        """
        Creates a copy of this Option object.
        @return a copy of this Option object.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getArg(self) -> unicode:
        """
        {@return the command line argument for this option (could be null)}
        """
        ...

    def getClass(self) -> java.lang.Class: ...

    def getCustomEditorComponent(self) -> java.awt.Component:
        """
        Override if you want to provide a custom widget for selecting your
         options. 
         <p>
         Important! If you override this you MUST also override the {@link #copy()}
         method so it returns a new instance of your custom editor.
        @return the custom editor
        """
        ...

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

    def getValueClass(self) -> java.lang.Class:
        """
        {@return the class of the value for this option}
        """
        ...

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
    def arg(self) -> unicode: ...

    @property
    def customEditorComponent(self) -> java.awt.Component: ...

    @property
    def group(self) -> unicode: ...

    @property
    def name(self) -> unicode: ...

    @property
    def optionListener(self) -> None: ...  # No getter available.

    @optionListener.setter
    def optionListener(self, value: ghidra.app.util.OptionListener) -> None: ...

    @property
    def state(self) -> ghidra.framework.options.SaveState: ...

    @property
    def stateKey(self) -> unicode: ...

    @property
    def value(self) -> object: ...

    @value.setter
    def value(self, value: object) -> None: ...

    @property
    def valueClass(self) -> java.lang.Class: ...