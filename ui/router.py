"""路由管理模块"""
import streamlit as st
from typing import Dict, Tuple, Callable


# 路由配置
ROUTES: Dict[str, Tuple[str, str]] = {
    "home": ("🏠 首页", "home"),
    "basic_info": ("📝 基本信息", "basic_info"),
    "outline": ("📋 剧情大纲", "outline"),
    "settings": ("⚙️ 设定管理", "settings"),
    "characters": ("👤 角色管理", "characters"),
    "story_state": ("📖 剧情状态", "story_state")
}


def get_current_route() -> str:
    """获取当前路由"""
    query_params = st.query_params
    current_route = query_params.get("page", ["home"])[0]
    
    # 如果路由不存在，默认为首页
    if current_route not in ROUTES:
        current_route = "home"
    
    return current_route


def get_route_name(route_key: str) -> str:
    """获取路由名称"""
    return ROUTES.get(route_key, ("🏠 首页", "home"))[0]


def navigate_to(route_key: str):
    """导航到指定路由"""
    if route_key in ROUTES:
        st.query_params["page"] = route_key
        st.rerun()


def get_route_url(route_key: str) -> str:
    """获取路由URL"""
    return f"?page={route_key}"

