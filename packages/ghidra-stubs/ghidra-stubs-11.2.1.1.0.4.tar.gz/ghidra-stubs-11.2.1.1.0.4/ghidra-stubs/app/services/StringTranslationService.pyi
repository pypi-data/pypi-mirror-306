from typing import List
from typing import overload
import ghidra.app.services
import ghidra.framework.plugintool
import ghidra.program.model.listing
import ghidra.util
import java.lang


class StringTranslationService(object):
    """
    Interface for providing string translating services.
 
     Implementations of this interface are usually done via a Plugin
     and then registered via Plugin's registerServiceProvided().
    """






    class TranslateOptions(java.lang.Record):
        NONE: ghidra.app.services.StringTranslationService.TranslateOptions



        def __init__(self, __a0: bool): ...



        def autoTranslate(self) -> bool: ...

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







    @staticmethod
    def createStringTranslationServiceHelpLocation(pluginClass: java.lang.Class, sts: ghidra.app.services.StringTranslationService) -> ghidra.util.HelpLocation:
        """
        Helper that creates a {@link HelpLocation} based on the plugin and sts.
        @param pluginClass Plugin that provides the string translation service
        @param sts {@link StringTranslationService}
        @return HelpLocation with topic equal to the plugin name and anchor something like
         "MyTranslationServiceName_String_Translation_Service".
        """
        ...

    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    @staticmethod
    def getCurrentStringTranslationServices(tool: ghidra.framework.plugintool.PluginTool) -> List[ghidra.app.services.StringTranslationService]:
        """
        Returns a sorted list of the currently enabled StringTranslationService service providers.
        @param tool {@link PluginTool}
        @return sorted list of currently enabled StringTranslationServices
        """
        ...

    def getHelpLocation(self) -> ghidra.util.HelpLocation:
        """
        Returns the {@link HelpLocation} instance that describes where to direct the user
         for help when they hit f1.
        @return {@link HelpLocation} instance or null.
        """
        ...

    def getTranslationServiceName(self) -> unicode:
        """
        Returns the name of this translation service.  Used when building menus to allow
         the user to pick a translation service.
        @return string name.
        """
        ...

    def hashCode(self) -> int: ...

    def notify(self) -> None: ...

    def notifyAll(self) -> None: ...

    def toString(self) -> unicode: ...

    def translate(self, __a0: ghidra.program.model.listing.Program, __a1: List[object], __a2: ghidra.app.services.StringTranslationService.TranslateOptions) -> None: ...

    @overload
    def wait(self) -> None: ...

    @overload
    def wait(self, __a0: long) -> None: ...

    @overload
    def wait(self, __a0: long, __a1: int) -> None: ...

    @property
    def helpLocation(self) -> ghidra.util.HelpLocation: ...

    @property
    def translationServiceName(self) -> unicode: ...