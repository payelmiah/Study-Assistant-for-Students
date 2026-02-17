import importlib, traceback, os, sys

print('CWD:', os.getcwd())
print('sys.path[0]:', sys.path[0])
print('sys.path sample:', sys.path[:5])

# Ensure workspace root is on sys.path
root = os.getcwd()
if root not in sys.path:
    sys.path.insert(0, root)

try:
    m = importlib.import_module('app.api.health')
    print('OK', m)
    print(dir(m))
except Exception:
    traceback.print_exc()
