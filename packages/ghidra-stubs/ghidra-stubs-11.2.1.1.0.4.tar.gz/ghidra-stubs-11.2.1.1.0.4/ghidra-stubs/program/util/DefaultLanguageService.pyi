from typing import List
from typing import overload
import ghidra.program.model.lang
import java.lang


class DefaultLanguageService(object, ghidra.program.model.lang.LanguageService):
    """
    Default Language service used gather up all the languages that were found
     during the class search (search was for language providers)
    """









    def equals(self, __a0: object) -> bool: ...

    def getClass(self) -> java.lang.Class: ...

    def getDefaultLanguage(self, processor: ghidra.program.model.lang.Processor) -> ghidra.program.model.lang.Language: ...

    @staticmethod
    def getDefinedExternalToolNames(languageId: unicode, tool: unicode, includeDeprecated: bool) -> List[unicode]:
        """
        Returns external names for specified language associated with other
         tools. For example, x86 languages are usually referred to as "metapc" by
         IDA-PRO.
        @param languageId language to search against
        @param tool name of external tool to search against
        @param includeDeprecated include deprecated LanguageDescriptions
        @return external names for this language associated with tool
        """
        ...

    def getExternalLanguageDescriptions(self, externalProcessorName: unicode, externalTool: unicode, endianness: ghidra.program.model.lang.Endian, size: int) -> List[ghidra.program.model.lang.LanguageDescription]: ...

    def getLanguage(self, languageID: ghidra.program.model.lang.LanguageID) -> ghidra.program.model.lang.Language: ...

    @overload
    def getLanguageCompilerSpecPairs(self, query: ghidra.program.model.lang.ExternalLanguageCompilerSpecQuery) -> List[ghidra.program.model.lang.LanguageCompilerSpecPair]: ...

    @overload
    def getLanguageCompilerSpecPairs(self, query: ghidra.program.model.lang.LanguageCompilerSpecQuery) -> List[ghidra.program.model.lang.LanguageCompilerSpecPair]: ...

    def getLanguageDescription(self, languageID: ghidra.program.model.lang.LanguageID) -> ghidra.program.model.lang.LanguageDescription: ...

    @overload
    def getLanguageDescriptions(self, includeDeprecatedLanguages: bool) -> List[ghidra.program.model.lang.LanguageDescription]: ...

    @overload
    def getLanguageDescriptions(self, processor: ghidra.program.model.lang.Processor) -> List[ghidra.program.model.lang.LanguageDescription]: ...

    @overload
    def getLanguageDescriptions(self, processor: ghidra.program.model.lang.Processor, endianness: ghidra.program.model.lang.Endian, size: int, variant: unicode) -> List[ghidra.program.model.lang.LanguageDescription]: ...

    @staticmethod
    def getLanguageService() -> ghidra.program.model.lang.LanguageService:
        """
        Returns the single instance of the DefaultLanguageService.
        @return the language service
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

