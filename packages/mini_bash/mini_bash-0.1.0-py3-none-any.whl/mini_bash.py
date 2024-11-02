#!/usr/bin/env python3

# Copyright 2024 (author: lamnt45)


# technical
import typing as tp
import subprocess



### FUNCTIONS
def mini_bash(cmd: str) -> tp.Tuple[str]:
    cmd = 'set -Eeuo pipefail\n' + cmd
    Result = subprocess.run(
        cmd,
        executable     = '/bin/bash',
        shell          = True,
        capture_output = True,
        text           = True,
    )
    if Result.returncode != 0:
        raise RuntimeError(
            '> cant execute:\n' + cmd[:1000] + '\n' + '> stderr:\n' + Result.stderr
        )
    return Result.stdout, Result.stderr
