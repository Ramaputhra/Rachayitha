import os
import sys

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # Check rachayitha code files
        candidate = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rachayitha code files", relative_path)
        if os.path.exists(candidate):
            return candidate
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
