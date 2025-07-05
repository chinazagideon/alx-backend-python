#!/usr/bin/env python3
"""
Script to copy README content from python-generators-0x00/README.md to root README.md
This can be run locally or used as a reference for the GitHub Action
"""

import os
import sys
from pathlib import Path

def update_readme():
    """Copy README content from python-generators-0x00 to root"""
    source_path = Path("python-generators-0x00/README.md")
    target_path = Path("README.md")
    
    if not source_path.exists():
        print(f"Error: Source file {source_path} not found")
        sys.exit(1)
    
    # Read source content
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add a header to indicate this is auto-generated
    header = """# ALX Python Tasks

> **Note**: This README is automatically generated from `python-generators-0x00/README.md`

---
"""
    
    # Write to target
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(header + content)
    
    print(f"Successfully updated {target_path} from {source_path}")
    print(f"Content length: {len(content)} characters")

if __name__ == "__main__":
    update_readme() 