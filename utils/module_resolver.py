from utils.tasks import TaskSignals, GenericTask


class ModuleResolver(TaskSignals):
    """Asynchronously identifies the compilation module name for a given file path.

    Usage:
        resolver = ModuleResolver(filepath)
        resolver.finished.connect(on_resolved)   # receives module name str
        resolver.error.connect(on_error)          # receives error message str
        resolver.resolve()
    """

    def __init__(self, filepath: str):
        super().__init__()
        self._filepath = filepath

    @GenericTask.packet
    def resolve(self):
        """Resolve the module name for the file path in a background thread."""
        return self._identify_module(self._filepath)

    def _identify_module(self, filepath: str) -> str:
        # TODO: Replace with actual module identification interface call.
        # The interface receives a file path and returns the module name string.
        raise NotImplementedError("模块识别接口未实现")
