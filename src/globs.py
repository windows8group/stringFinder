import os
import typing
import watchdog
import watchdog.events
from libtextworker.get_config import GetConfig

@typing.final
class Settings(GetConfig):

#region Properties
    @property
    def source_dirs(this) -> list[str]:
        return this["source_dirs"]
    
    @source_dirs.setter
    def source_dirs(this, value: list[str]):
        this["source_dirs"] = value
    
    @source_dirs.deleter
    def source_dirs(this): raise NotImplementedError()

    @property
    def source_files(this) -> list[str]:
        return this["source_files"]

    @source_files.setter
    def source_files(this, value: list[str]):
        this["source_files"] = value

    @source_files.deleter
    def source_files(this): raise NotImplementedError()

    @property
    def output_dir(this) -> str:
        return this["output_dir"]

    @output_dir.setter
    def output_dir(this, value: str):
        this["output_dir"] = value

    @output_dir.deleter
    def output_dir(this): raise NotImplementedError()

    @property
    def languages(this) -> list[str]:
        return this["languages"]

    @languages.setter
    def languages(this, value: list[str]):
        this["languages"] = value

    @languages.deleter
    def languages(this): raise NotImplementedError()

    @property
    def filename(this) -> str:
        return this["filename"]
    
    @filename.setter
    def filename(this, value: str):
        this["filename"] = value

    @filename.deleter
    def filename(this): raise NotImplementedError()
#endregion

    def __init__(this):
        GetConfig.__init__(this, {
            "source_dirs": [],
            "source_files": [],
            "output_dir": "",
            "languages": ["en-US", "vi-VN"],
            "filename": "Resources"
        }, os.path.expanduser("~/.stringFinder/settings.json"), True)
    

    # def Get(this, name: str) -> object:
    def __getitem__(this, name: str) -> object:
        if not name in this.sections(): return this.OEM[name]
        return this[name]

    def on_any_event(this, event: watchdog.events.FileSystemEvent):
        # Reread the file
        GetConfig.on_any_event(this, event)

        # Only care about paths that we are using
        # Nothing(?) to do now

silent: bool = False
settings: Settings = Settings()