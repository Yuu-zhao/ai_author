"""页面模块"""
from ui.pages.home import render as render_home
from ui.pages.basic_info import render as render_basic_info
from ui.pages.outline import render as render_outline
from ui.pages.settings import render as render_settings
from ui.pages.characters import render as render_characters
from ui.pages.story_state import render as render_story_state

__all__ = [
    'render_home',
    'render_basic_info',
    'render_outline',
    'render_settings',
    'render_characters',
    'render_story_state',
]

