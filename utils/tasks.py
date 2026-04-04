# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later


from typing import Callable, Optional, Any
from weakref import WeakMethod
from PySide6.QtCore import QObject, Signal, Slot, QThread, QRunnable, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit


class TaskSignals(QObject):
    """Signals for worker thread communication with GUI thread"""

    # Real-time data transmission
    data_ready = Signal(object)  # Can emit any type of data

    # Task completion signals
    finished = Signal(object)  # Emit final result
    error = Signal(object)  # Emit error message


class GenericTask(QRunnable, TaskSignals):
    """
    Generic worker for running tasks in thread pool

    Features:
    - Real-time data transmission to GUI thread via signals
    - Support for progress updates
    - Automatic cleanup
    - Type-safe result passing

    Usage:
        def my_task(param1, param2):
            # Do work
            return result

        worker = GenericWorker(my_task, arg1, arg2)
        worker.finished.connect(handle_result)
        QThreadPool.globalInstance().start(worker)
    """

    def __init__(self, function: Callable):
        super().__init__()
        self.function = function

    def __del__(self):
        print(f"task delete (id: {id(self)})")

    def run(self):
        """Execute the task in thread pool"""

        if QThread().isMainThread():
            self.error.emit("Cannot run tasks in the main thread")
            return

        try:
            result = self.function()
            self.finished.emit(result)
        except Exception as e:
            error_msg = str(e)
            self.error.emit(error_msg)
        finally:
            pass

    @staticmethod
    def packet(function: Callable) -> Callable:
        """
        Decorator to automatically run methods in thread pool

        Usage:
            class MyWorker(TaskSignals):
                @GenericTask.packet
                def connect(self):
                    return self._connect()

                @GenericTask.packet
                def execute(self, command):
                    return self._execute(command)
        """
        from functools import wraps
        import weakref

        @wraps(function)
        def wrapper(self, *args, **kwargs):

            weakSelf = weakref.ref(self)

            def implementation() -> Any:
                obj = weakSelf()
                if not obj:
                    raise RuntimeError("Object has been deleted")
                return function(obj, *args, **kwargs)

            task = GenericTask(implementation)

            def onFinished(result):
                obj = weakSelf()
                if obj:
                    obj.finished.emit(result)

            def onError(msg):
                obj = weakSelf()
                if obj:
                    obj.error.emit(msg)

            def onData(data):
                obj = weakSelf()
                if obj:
                    obj.data_ready.emit(data)

            task.finished.connect(onFinished)
            task.error.connect(onError)
            task.data_ready.connect(onData)
            task.setAutoDelete(True)

            from PySide6.QtCore import QThreadPool

            QThreadPool.globalInstance().start(task)

        return wrapper
