from pathlib import Path
from utils.config import plugins_dir, logger
from utils.utils import scheduler, PLUGINS

scheduler.start()
PLUGINS.init()
__import__('utils.plugins_manage')

def import_plugin(plugin):
    try:
        __import__(plugin)
        return True
    except Exception as e:
        logger.error(f'failed to import :{plugin}n {e}')
        return False

root = Path('data/plugins')
[import_plugin('.'.join(path.parent.parts + (path.stem,)))
 for path in root.glob('*.py')]