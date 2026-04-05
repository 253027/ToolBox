# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Optional, Any
from PySide6.QtCore import QObject, Signal, Slot, QThread, QRunnable, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit
import paramiko
from .tasks import TaskSignals, GenericTask


class SSHTask(TaskSignals):
    """
    SSH worker using thread pool for connection and command execution

    Features:
    - Non-blocking SSH operations
    - Real-time output streaming to GUI
    - Thread-safe result retrieval
    - Support for multiple commands

    Usage:
        ssh = SSHTask(hostname, port, username, password)
        ssh.finished.connect(on_connected)
        ssh.error.connect(on_error)
        ssh.data_ready.connect(on_data_received)
        ssh.connect()
        ssh.execute("ls -la")
    """

    def __init__(
        self,
        hostname: str,
        port: int,
        username: str,
        password: Optional[str] = None,
        key_file: Optional[str] = None,
    ):
        super().__init__()
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.ssh_client: Optional[paramiko.SSHClient] = None

    def _connect(self) -> None:
        """Internal method to establish SSH connection"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.key_file:
                self.ssh_client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_file,
                    allow_agent=False,
                    look_for_keys=False,
                )
            else:
                self.ssh_client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    allow_agent=False,
                    look_for_keys=False,
                )
        except Exception as e:
            # Clean up the client on failure
            if hasattr(self, "ssh_client") and self.ssh_client:
                try:
                    self.ssh_client.close()
                except Exception:
                    pass
                self.ssh_client = None
            # Re-raise to let the decorator handle it
            raise

    @GenericTask.packet
    def connect(self):
        """Start SSH connection in background thread"""
        return self._connect()

    @GenericTask.packet
    def execute(self, command: str):
        """Execute SSH command in background thread, streaming output line by line via data_ready"""
        if not self.ssh_client:
            raise RuntimeError("SSH client is not connected")
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        output_lines = []
        for line in stdout:
            stripped = line.rstrip("\n")
            self.data_ready.emit(stripped)
            output_lines.append(stripped)
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            raise RuntimeError(stderr.read().decode("utf-8").strip())
        return "\n".join(output_lines)

    def clear(self) -> bool:
        """Close SSH connection"""
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
        return True

    def __del__(self):
        """Cleanup on deletion"""
        print("SSH Task deleted")
        self.clear()
