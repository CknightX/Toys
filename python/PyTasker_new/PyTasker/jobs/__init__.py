"""
auto load all modules
"""
import os
ignore = [
    'test_job'
]

base_path = os.path.dirname(__file__)

modules = os.listdir(base_path)
for module in modules:
    if module == '__pycache__':
        continue
    if module == os.path.basename(__file__):
        continue
    if os.path.isdir(os.path.join(base_path,module)) and module not in ignore:
        exec(f'from .{module} import *',globals())