#!/usr/bin/env python3
"""Compatibility entry point for the current panel conversion policy."""
from pathlib import Path
from runpy import run_path
_policy = run_path(str(Path(__file__).with_name('panel-conversion.py')))
normalize_whatsapp = _policy['normalize_panel']
if __name__ == '__main__':
    run_path(str(Path(__file__).with_name('panel-conversion.py')), run_name='__main__')
