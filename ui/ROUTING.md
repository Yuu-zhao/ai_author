# 路由系统说明

## 概述

应用已改为基于查询参数的路由系统，支持：
- ✅ URL 路由跳转（如 `?page=home`）
- ✅ 浏览器前进/后退按钮支持
- ✅ 可分享的链接
- ✅ 侧边栏导航按钮

## 路由配置

所有路由定义在 `ui/router.py` 中：

```python
ROUTES = {
    "home": ("🏠 首页", "home"),
    "basic_info": ("📝 基本信息", "basic_info"),
    "outline": ("📋 剧情大纲", "outline"),
    "settings": ("⚙️ 设定管理", "settings"),
    "characters": ("👤 角色管理", "characters"),
    "story_state": ("📖 剧情状态", "story_state")
}
```

## 使用方法

### 1. 获取当前路由

```python
from ui.router import get_current_route

current_route = get_current_route()  # 返回 "home", "basic_info" 等
```

### 2. 导航到指定路由

```python
from ui.router import navigate_to

# 在按钮点击时导航
if st.button("跳转到首页"):
    navigate_to("home")
```

### 3. 获取路由URL

```python
from ui.router import get_route_url

url = get_route_url("home")  # 返回 "?page=home"
```

### 4. 获取路由名称

```python
from ui.router import get_route_name

name = get_route_name("home")  # 返回 "🏠 首页"
```

## URL 示例

- 首页：`http://localhost:8501/?page=home`
- 基本信息：`http://localhost:8501/?page=basic_info`
- 剧情大纲：`http://localhost:8501/?page=outline`
- 设定管理：`http://localhost:8501/?page=settings`
- 角色管理：`http://localhost:8501/?page=characters`
- 剧情状态：`http://localhost:8501/?page=story_state`

## 添加新路由

1. 在 `ui/router.py` 的 `ROUTES` 中添加新路由：
```python
ROUTES = {
    # ... 现有路由
    "new_page": ("🆕 新页面", "new_page")
}
```

2. 在 `ui/app.py` 中添加路由映射：
```python
route_map = {
    # ... 现有映射
    "new_page": render_new_page
}
```

3. 创建对应的页面渲染函数（在 `ui/pages/` 目录下）

## 优势

1. **URL 可分享**：每个页面都有唯一的 URL，可以分享给他人
2. **浏览器支持**：支持浏览器的前进/后退按钮
3. **书签支持**：可以收藏特定页面
4. **SEO 友好**：URL 包含页面信息
5. **调试方便**：可以直接通过修改 URL 跳转到任意页面

