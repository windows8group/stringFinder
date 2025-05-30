from .funcs.rules import ATranslateRule

filesToUse : set[str] = set()
dirsToUse  : set[str] = set()
outputPath : str = r"C:\Users\lebao3105\Projects\WhatsWinRT\WhatsWinUWP\WhatsWinUWP.Shared\Strings\en-US\Resources.resw"
quoteChar  : set[str] = {"'", '"'}
outputObjs : dict[str, ATranslateRule] = {}