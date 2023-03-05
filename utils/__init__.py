from pathlib import Path
from importlib import import_module

from utils.config import plugins_dir, logger
from utils.utils import scheduler, PLUGINS

scheduler.start()

def import_plugin(plugin):
    try:
        import_module(plugin)
        return True
    except Exception as e:
        logger.error(f'failed to import :{plugin}\n {e}')
        return False

def load_plugin():

    PLUGINS.init()

    import_plugin('utils.plugins_manage')

    root = 'data/plugins'

    for path in sorted(Path(root).glob("*.py")):
        module_path = '.'.join(path.parent.parts + (path.stem,))
        import_plugin(module_path)
