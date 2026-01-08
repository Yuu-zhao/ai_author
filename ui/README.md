# UI模块结构说明

## 目录结构

```
ui/
├── __init__.py          # UI模块初始化
├── app.py              # 主应用入口（路由和页面配置）
├── utils.py            # 工具函数（文件操作等）
├── components.py       # 公共组件（侧边栏、统计等）
├── pages/             # 页面模块
│   ├── __init__.py    # 页面模块导出
│   ├── home.py        # 首页（章节生成和管理）
│   ├── basic_info.py  # 基本信息管理
│   ├── outline.py      # 剧情大纲管理
│   ├── settings.py     # 设定管理
│   ├── characters.py   # 角色管理
│   └── story_state.py # 剧情状态管理
└── README.md          # 本文件
```

## 模块说明

### `app.py` - 主应用入口
- 负责页面配置和路由
- 初始化session state
- 调用各个页面模块的render函数

### `utils.py` - 工具函数
- `get_files()` - 获取目录下的文件
- `save_file()` - 保存文件
- `delete_file()` - 删除文件

### `components.py` - 公共组件
- `render_sidebar_navigation()` - 渲染侧边栏导航
- `render_sidebar_stats()` - 渲染侧边栏统计信息
- `init_session_state()` - 初始化session state

### `pages/` - 页面模块
每个页面模块都包含一个 `render()` 函数，负责渲染该页面的所有UI元素。

- **home.py** - 首页，包含章节生成、章节详情、章节目录等功能
- **basic_info.py** - 基本信息管理（书名、简介、标签）
- **outline.py** - 剧情大纲管理
- **settings.py** - 设定管理（世界观、修炼体系等）
- **characters.py** - 角色管理
- **story_state.py** - 剧情状态管理

## 使用方式

运行应用：
```bash
streamlit run ui.py
```

`ui.py` 文件现在只是一个简单的入口，实际逻辑都在 `ui/` 模块中。

## 优势

1. **模块化** - 每个页面独立，便于维护
2. **可读性** - 代码结构清晰，职责分明
3. **可扩展** - 新增页面只需在 `pages/` 下添加新模块
4. **可测试** - 每个模块可以独立测试
5. **可复用** - 公共组件和工具函数可在多个页面复用

