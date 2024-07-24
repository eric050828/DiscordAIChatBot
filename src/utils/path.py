import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def path(*paths) -> str:
    return os.path.join(PROJECT_ROOT, *paths)