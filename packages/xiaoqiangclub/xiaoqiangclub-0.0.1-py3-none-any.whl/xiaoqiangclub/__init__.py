# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/25 18:06
# 文件名称： __init__.py
# 项目描述： 自用工具包
# 开发工具： PyCharm
from xiaoqiangclub.config.constants import (VERSION, UA)
from xiaoqiangclub.config.log_config import (logger_xiaoqiangclub, log)
from xiaoqiangclub.utils.logger import LoggerBase
from xiaoqiangclub.utils.decorators import (get_caller_info, log_execution_time, try_log_exceptions,
                                            log_function_call, retry, cache_result, validate_before_execution)
from xiaoqiangclub.utils.network_utils import (get_response, get_response_async)
from xiaoqiangclub.utils.deduplication import Deduplication
from xiaoqiangclub.utils.time_utils import (get_current_weekday, get_current_date, get_current_time, get_full_time_info)
from xiaoqiangclub.api.chatbot import WeChatBotAPI
from xiaoqiangclub.api.xunlei import xunlei
from xiaoqiangclub.api.xunlei.xunlei import Xunlei
from xiaoqiangclub.api.xunlei.xunlei_base import XunleiBase
from xiaoqiangclub.api.xunlei.xunlei_cloud_disk import XunleiCloudDisk
from xiaoqiangclub.api.xunlei.xunlei_remote_downloader import XunleiRemoteDownloader
from xiaoqiangclub.api.hao6v import hao6v
from xiaoqiangclub.api.message_push import (email_sender, wechat_sender, dingtalk_sender, bark_sender, telegram_sender,
                                            igot_sender, push_plus_sender, an_push_sender, feishu_sender,
                                            discord_sender,
                                            whatsapp_sender, async_sender, sender)
from xiaoqiangclub.api.message_push.sender import MessagePush
from xiaoqiangclub.api.message_push.async_sender import AsyncMessagePush
from xiaoqiangclub.gui.show_subtitles import ShowSubtitles
from xiaoqiangclub.gui import (logo, show_message, show_subtitles, mouse_keyboard_clipboard_listener, windows_manager)
from xiaoqiangclub.scripts import (zip, tiny_db, module_installer)
from xiaoqiangclub.scripts.tiny_db import TinyDBManager
from xiaoqiangclub.scripts.text_splitter import text_splitter
from xiaoqiangclub.scripts.module_installer import ModuleInstaller
from xiaoqiangclub.sound.play_system_sound import play_system_sound

__title__ = "xiaoqiangclub"
__description__ = "一个基于Python3的自用工具包"
__version__ = VERSION

__all__ = [
    'VERSION', 'UA',
    'logger_xiaoqiangclub', 'log',
    'LoggerBase',
    'get_caller_info', 'log_execution_time', 'try_log_exceptions',
    'log_function_call', 'retry', 'cache_result', 'validate_before_execution',
    'get_response', 'get_response_async',
    'Deduplication',
    'get_current_weekday', 'get_current_date', 'get_current_time', 'get_full_time_info',
    'WeChatBotAPI',
    'xunlei', 'Xunlei', 'XunleiBase', 'XunleiCloudDisk', 'XunleiRemoteDownloader',
    'email_sender', 'wechat_sender', 'dingtalk_sender', 'bark_sender', 'telegram_sender', 'igot_sender',
    'push_plus_sender', 'an_push_sender', 'feishu_sender', 'discord_sender', 'whatsapp_sender',
    'async_sender', 'MessagePush', 'AsyncMessagePush',
    'hao6v',
    'ShowSubtitles',
    'logo', 'show_message', 'show_subtitles', 'mouse_keyboard_clipboard_listener', 'windows_manager',
    'zip', 'tiny_db', 'TinyDBManager', 'text_splitter',
    'play_system_sound'
]
