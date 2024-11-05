# _*_ coding : UTF-8 _*_
# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/22 15:01
# 文件名称： module_installer.py
# 项目描述： python模块检测安装
# 开发工具： PyCharm
import importlib
import subprocess
import sys
from typing import Dict
from xiaoqiangclub.config.log_config import log


class ModuleInstaller:
    def __init__(self, module_mapping: Dict[str, str], check_and_install: bool = True):
        """
        模块安装器，用于检测和安装指定的模块。

        :param module_mapping: 模块安装名称与导入名称的映射字典（安装模块的名称和导入名称可能不同），例如：
                               module_mapping = {'opencv-python': 'cv2',
                                                 'Pillow': 'PIL',
                                                 'pywin32': 'win32api'}
        :param check_and_install: 是否自动检测并安装未安装的模块（默认是True）
        """
        self.module_mapping = module_mapping
        if check_and_install:
            self.check_and_install()

    def install_module(self, package: str, mirror: str = 'https://pypi.tuna.tsinghua.edu.cn/simple') -> None:
        """
        安装指定的模块

        :param package: 要安装的模块名称
        :param mirror: 镜像地址（默认是清华大学镜像）
        """
        log.info(f"正在安装 {package}...")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install_module', '-i', mirror, '-U', package])

    def check_module(self, package: str) -> bool:
        """
        检查指定的模块是否已安装

        :param package: 模块导入名称
        :return: 是否已安装
        """
        try:
            importlib.import_module(package)
            log.info(f"{package} 已安装")
            return True
        except ImportError:
            log.error(f"{package} 未安装")
            return False

    def check_and_install(self) -> None:
        """
        检查模块是否已安装，若未安装则进行安装
        """
        is_installed: bool = False
        for install_name, import_name in self.module_mapping.items():
            if not self.check_module(import_name):
                is_installed = True
                self.install(install_name)

        # 验证安装
        if is_installed:
            self.verify_installation()

    def verify_installation(self) -> None:
        """
        验证所有模块是否成功安装
        """
        for install_name, import_name in self.module_mapping.items():
            try:
                module = importlib.import_module(import_name)
                if hasattr(module, '__version__'):
                    log.info(f"{import_name} 安装成功，版本: {module.__version__}")
                else:
                    log.info(f"{import_name} 安装成功，但未找到版本信息")
            except ImportError:
                raise ImportError(f"{import_name} 安装失败，请手动安装：pip install_module {install_name}")


# 使用示例
if __name__ == "__main__":
    module_mapping = {
        'opencv-python': 'cv2',
        'Pillow': 'PIL',
        'pywin32': 'win32api'
    }
    installer = ModuleInstaller(module_mapping, check_and_install=True)
