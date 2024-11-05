"""Custom exceptions."""


class ModuleInUseError(Exception):
    """Exception raised when attempting to unload a kernel module that is in use."""

    def __init__(self, module_name: str) -> None:
        self.module_name = module_name
        self.message = f'Module {module_name} is in use and cannot be unloaded.'
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'ModuleInUseError: {self.message}'
