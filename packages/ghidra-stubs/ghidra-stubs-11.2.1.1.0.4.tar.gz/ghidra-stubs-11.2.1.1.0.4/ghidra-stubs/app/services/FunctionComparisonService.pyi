from typing import overload
import ghidra.features.base.codecompare.model
import ghidra.program.model.listing
import java.lang
import java.util
import utility.function


class FunctionComparisonService(object):
    """
    Service interface to create comparisons between functions which will be displayed
     side-by-side in a function comparison window. Each side in the 
     display will allow the user to select one or more functions 
 
     Concurrent usage: All work performed by this service will be done asynchronously on the
     Swing thread.
    """









    @overload
    def addToComparison(self, function: ghidra.program.model.listing.Function) -> None:
        """
        Adds the given function to each side the last created comparison window or creates
         a new comparison if none exists. The right panel will be changed to show the new function.
         Note that this method will not add to any provider created via the
         {@link #createCustomComparison(FunctionComparisonModel, Callback)}. Those providers
         are private to the client that created them. They take in a model, so if the client wants
         to add to those providers, it must retain a handle to the model and add functions directly
         to the model.
        @param function the function to be added to the last function comparison window
        """
        ...

    @overload
    def addToComparison(self, functions: java.util.Collection) -> None:
        """
        Adds the given functions to each side the last created comparison window or creates
         a new comparison if none exists. The right panel will be change to show a random function
         from the new functions. Note that this method will not add to any comparison windows created
         with a custom comparison model.
        @param functions the functions to be added to the last function comparison window
        """
        ...

    @overload
    def createComparison(self, functions: java.util.Collection) -> None:
        """
        Creates a function comparison window where each side can display any of the given functions.
        @param functions the functions to compare
        """
        ...

    @overload
    def createComparison(self, left: ghidra.program.model.listing.Function, right: ghidra.program.model.listing.Function) -> None:
        """
        Creates a function comparison window for the two given functions. Each side can select
         either function, but initially the left function will be shown in the left panel and the
         right function will be shown in the right panel.
        @param left the function to initially show in the left panel
        @param right the function to initially show in the right panel
        """
        ...

    def createCustomComparison(self, model: ghidra.features.base.codecompare.model.FunctionComparisonModel, closeListener: utility.function.Callback) -> None:
        """
        Creates a custom function comparison window. The default model shows all functions on both
         sides. This method allows the client to provide a custom comparison model which can have
         more control over what functions can be selected on each side. One such custom model
         is the {@link MatchedFunctionComparisonModel} which gives a unique set of functions on the
         right side, depending on what is selected on the left side.
         <P>
         Note that function comparison windows created with this method are considered private for the
         client and are not available to be chosen for either of the above "add to" service methods. 
         Instead, the client that uses this model can retain a handle to the model and add or remove
         functions directly on the model.
        @param model the custom function comparison model
        @param closeListener an optional callback if the client wants to be notified when the 
         associated function comparison windows is closed.
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

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

