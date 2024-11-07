from typing import overload
import docking
import java.awt
import java.awt.event
import java.lang
import java.util


class FunctionSupplierContext(docking.ActionContext, object):
    """
    A "mix-in" interface that specific implementers of ActionContext may also implement if
     they can supply functions in their action context. Actions that want to work on functions
     can look for this interface, which can used in a variety of contexts.
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getComponentProvider(self) -> docking.ComponentProvider: ...

    def getContextObject(self) -> object: ...

    def getEventClickModifiers(self) -> int: ...

    def getFunctions(self) -> java.util.Set:
        """
        Returns the set of functions that this context object can supply.
        @return the set of functions that this context object can supply
        """
        ...

    def getMouseEvent(self) -> java.awt.event.MouseEvent: ...

    def getSourceComponent(self) -> java.awt.Component: ...

    def getSourceObject(self) -> object: ...

    def hasAnyEventClickModifiers(self, __a0: int) -> bool: ...

    def hasFunctions(self) -> bool:
        """
        Returns true if this context can supply one or more functions.
        @return true if this context can supply one or more functions
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def setContextObject(self, __a0: object) -> docking.ActionContext: ...

    def setEventClickModifiers(self, __a0: int) -> None: ...

    def setMouseEvent(self, __a0: java.awt.event.MouseEvent) -> docking.ActionContext: ...

    def setSourceComponent(self, __a0: java.awt.Component) -> docking.ActionContext: ...

    def setSourceObject(self, __a0: object) -> docking.ActionContext: ...

    def toString(self) -> unicode: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def componentProvider(self) -> docking.ComponentProvider: ...

    @property
    def contextObject(self) -> object: ...

    @contextObject.setter
    def contextObject(self, value: object) -> None: ...

    @property
    def eventClickModifiers(self) -> int: ...

    @eventClickModifiers.setter
    def eventClickModifiers(self, value: int) -> None: ...

    @property
    def functions(self) -> java.util.Set: ...

    @property
    def mouseEvent(self) -> java.awt.event.MouseEvent: ...

    @mouseEvent.setter
    def mouseEvent(self, value: java.awt.event.MouseEvent) -> None: ...

    @property
    def sourceComponent(self) -> java.awt.Component: ...

    @sourceComponent.setter
    def sourceComponent(self, value: java.awt.Component) -> None: ...

    @property
    def sourceObject(self) -> object: ...

    @sourceObject.setter
    def sourceObject(self, value: object) -> None: ...