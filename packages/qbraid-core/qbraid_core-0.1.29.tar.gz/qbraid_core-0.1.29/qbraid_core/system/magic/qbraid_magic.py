# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining custom qBraid IPython magic commands.

"""

import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Optional

from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class SysMagics(Magics):
    """
    Custom IPython Magics class to allow running
    qBraid-CLI commands from within Jupyter notebooks.

    """

    @staticmethod
    def restore_env_var(var_name: str, original_value: Optional[str]) -> None:
        """
        Restore or remove an environment variable based on its original value.
        """
        if original_value is None:
            os.environ.pop(var_name, None)
        else:
            os.environ[var_name] = original_value

    @line_magic
    def qbraid(self, line):
        """
        Executes qBraid-CLI command using the sys.executable
        from a Jupyter Notebook kernel.
        """
        original_path = os.getenv("PATH")
        original_show_progress = os.getenv("QBRAID_CLI_SHOW_PROGRESS")
        python_dir = str(Path(sys.executable).parent)

        try:
            os.environ["PATH"] = python_dir + os.pathsep + original_path
            os.environ["QBRAID_CLI_SHOW_PROGRESS"] = "false"

            command = ["qbraid"] + shlex.split(line)
            subprocess.run(command, check=True)

        finally:
            self.restore_env_var("PATH", original_path)
            self.restore_env_var("QBRAID_CLI_SHOW_PROGRESS", original_show_progress)


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(SysMagics)
