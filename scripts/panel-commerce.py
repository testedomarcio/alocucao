#!/usr/bin/env python3
"""Compatibility entry point: preserve both assisted and online ordering."""
from pathlib import Path
from runpy import run_path

def normalize_page(text):
    return run_path(str(Path(__file__).resolve().parent / 'hybrid-commerce.py'))['normalize_hybrid'](text)

if __name__ == '__main__':
    run_path(str(Path(__file__).resolve().parent / 'hybrid-commerce.py'), run_name='__main__')
