import os
import subprocess
import platform
from setuptools import setup, find_packages
from xiaoqiangclub import log, VERSION

UNSUPPORTED_DEPENDENCIES = {
    'linux': ['pywin32'],  # Linux 系统不需要的依赖
    'darwin': ['pywin32'],  # macOS 系统不需要的依赖
}


def get_long_description():
    """获取详细描述"""
    try:
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        return 'XiaoqiangClub 自用工具包'
    except Exception as e:
        log.error(f"读取 README.md 失败: {e}")
        return 'XiaoqiangClub 自用工具包'


def execute_command(command):
    """执行终端命令并返回输出"""
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        log.error(f"执行命令失败: {e}")
        return ""


def get_requirements():
    """获取依赖项列表"""
    try:
        # 执行 pip freeze 命令并获取输出
        result = execute_command('pip freeze')
        if result:
            all_requirements = [line.strip() for line in result.splitlines() if line.strip()]
            log.info(f"成功获取到 {len(all_requirements)} 个依赖项：{all_requirements}")
            return all_requirements
        return []
    except Exception as e:
        log.error(f"获取依赖项失败: {e}")
        return []


def get_platform_requirements():
    """根据平台返回平台特定的依赖，剔除不支持的依赖"""
    all_requirements = get_requirements()
    system_platform = platform.system().lower()

    # 获取当前平台的禁用依赖
    platform_unsupported = UNSUPPORTED_DEPENDENCIES.get(system_platform, [])

    # 从所有依赖中删除不支持的依赖
    filtered_requirements = [req for req in all_requirements if req not in platform_unsupported]

    log.info(f"平台 {system_platform} 上安装的依赖项: {filtered_requirements}")
    return filtered_requirements


setup(
    name='xiaoqiangclub',
    version=VERSION,
    author='xiaoqiangclub',
    author_email='xiaoqiangclub@hotmail.com',
    description='XiaoqiangClub 自用工具包',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/xiaoqiangclub/xiaoqiangclub',
    install_requires=get_platform_requirements(),  # 动态设置 install_requires，过滤不支持的平台依赖
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'cli_tool_template_generator = xiaoqiangclub.templates.template_generator.cli_tool_template_generator:generate_cli_tool_template',
        ],
    },
)
