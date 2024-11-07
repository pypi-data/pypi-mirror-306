from wexample_config.const.types import DictConfig
from wexample_filestate.config_value.readme_content_option_value import ReadmeContentConfigValue
from wexample_filestate.const.disk import DiskItemType
from wexample_helpers.const.types import *

from wexample_wex_addon_app.const.globals import (
    APP_FILE_APP_CONFIG,
    APP_FILE_APP_ENV, APP_DIR_APP_DATA_NAME,
)
from wexample_wex_core.utils.workdir import Workdir


class AppWorkdir(Workdir):
    def prepare_value(self, config: Optional[DictConfig] = None) -> DictConfig:
        from wexample_config.config_value.filter.trim_config_value_filter import TrimConfigValueFilter

        config = super().prepare_value(config)

        config.update({
            "mode": "777",
            "mode_recursive": True,
        })

        children = config["children"]

        children.append({
            "name": 'README.md',
            "type": DiskItemType.FILE,
            "should_exist": True,
            "default_content": ReadmeContentConfigValue(
                templates=[],
                parameters={}
            ),
        })

        children.append({
            "name": 'version.txt',
            "type": DiskItemType.FILE,
            "should_exist": True,
            "default_content": f"0.0.1",
            "content_filter": TrimConfigValueFilter
        })

        children.append({
            "name": '.gitignore',
            "type": DiskItemType.FILE,
            "should_exist": True,
            "content_filter": TrimConfigValueFilter
        })

        children.append({
            "name": APP_DIR_APP_DATA_NAME,
            "type": DiskItemType.DIRECTORY,
            "should_exist": True,
            "children": [
                {
                    "name": APP_FILE_APP_ENV,
                    "type": DiskItemType.FILE,
                    "should_exist": True
                },
                {
                    "name": APP_FILE_APP_CONFIG,
                    "type": DiskItemType.FILE,
                    "should_exist": True
                },
                {
                    "name": "tmp",
                    "type": DiskItemType.DIRECTORY,
                    "should_exist": True
                }
            ]
        })

        return config
