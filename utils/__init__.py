from pathlib import Path
from importlib import import_module

from utils.config import plugins_dir, logger
from utils.utils import scheduler, PLUGINS

scheduler.start()

def import_plugin(plugin):
    """ 根据插件名称导入对应的python模块 """
    try:
        import_module(plugin)
        logger.info(f'{plugin} imported successfully')
        return True
    except Exception as e:
        logger.error(f'failed to import :{plugin}\n {e}')
        return False

def load_plugin():
    # 初始化插件
    PLUGINS.init()
    # 导入插件管理模块
    import_plugin('utils.pm')
    # 遍历插件目录下的所有python文件，以数据排序
    root = Path('data/plugins')
    for path in sorted(root.glob("*.py")):
        module_path = '.'.join(path.parent.parts + (path.stem,))
        import_plugin(module_path)
