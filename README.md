# 灵气靖朝录 - AI 写作系统

这是一个专为小说长期写作设计的 Python AI 写作系统。它不是教学 Demo，而是作者级工程骨架。

## 特性

- ✅ 长期设定不崩
- ✅ 每章强约束写作
- ✅ AI 永远是"副作者"
- ✅ 随时可升级 RAG / 本地模型
- ✅ 适合长期连载写作

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件，添加你的 OpenAI API Key：

```
OPENAI_API_KEY=your_api_key_here
```

### 3. 运行方式

#### 方式一：使用 Streamlit UI（推荐）

```bash
streamlit run ui.py
```

浏览器会自动打开，提供完整的数据管理和 AI 生成功能：

**🤖 AI 对话生成页面：**
- 实时查看当前数据状态（世界观、角色、剧情状态）
- 输入章节号和写作目标
- 一键生成章节，支持 Prompt 预览
- 实时显示生成结果，支持下载

**🌍 世界观管理：**
- 查看/编辑现有世界观文件
- 新建世界观设定
- 删除不需要的世界观文件

**👤 角色管理：**
- 查看/编辑角色卡
- 新建角色
- 删除角色

**📖 剧情状态：**
- 编辑当前剧情状态
- 记录已发生事件、风险和写作禁区

**📚 章节管理：**
- 查看/编辑已生成的章节
- 删除章节
- 下载章节文件

**UI 特点：**
- ✅ 完整的增删改查功能
- ✅ 所有操作直接保存到 `data/` 目录，数据安全可靠
- ✅ 可视化编辑，无需手动编辑文件
- ✅ 专门的 AI 对话生成界面，支持 Prompt 预览
- ✅ 实时数据统计和预览

#### 方式二：命令行运行

```bash
python main.py
```

#### 方式三：使用辅助脚本

```bash
python scripts/new_chapter.py 第14章 "夜访邻里，侧面展现风声"
```

## 项目结构

```
novel-ai-writer/
├── README.md
├── requirements.txt
├── config.py              # 配置文件
├── main.py                # 主入口
├── ui.py                  # Streamlit UI 界面
│
├── data/                  # 数据目录
│   ├── world/            # 世界观设定
│   ├── characters/       # 角色设定
│   ├── plot/             # 剧情状态
│   └── chapters/         # 生成的章节
│
├── prompts/              # Prompt 模板
│   └── chapter_prompt.txt
│
├── writer/               # 核心模块
│   ├── loader.py        # 数据加载
│   ├── retriever.py     # 角色检索
│   ├── prompt_builder.py # Prompt 构建
│   ├── generator.py     # AI 生成
│   └── utils.py         # 工具函数
│
└── scripts/             # 辅助脚本
    └── new_chapter.py
```

## 使用说明

### 修改设定

- 世界观：编辑 `data/world/world.md`
- 角色设定：在 `data/characters/` 目录下添加或修改角色卡
- 剧情状态：更新 `data/plot/story_state.md`

### 生成章节

1. **直接运行 main.py**：修改 `main.py` 中的参数后运行
2. **使用脚本**：`python scripts/new_chapter.py <章节号> "<章节目标>"`

### 更换 AI 模型

如需使用 Claude 或本地模型，只需修改 `writer/generator.py` 中的 `generate_chapter` 函数即可。

## 推荐工作流程

### 写章前
1. 在 UI 左侧编辑「剧情状态」，更新当前剧情进展
2. 如有新角色或世界观变化，同步更新对应设定

### 生成章
1. 在 UI 中间输入章节号和明确的「本章目标」
2. 点击「生成章节」按钮
3. 等待 AI 生成完成

### 生成后
1. 查看生成的章节内容
2. 手动更新「剧情状态」，记录本章发生了什么
3. 如有需要，微调角色设定或世界观

**核心原则：**
- UI 只是操作面板，真正的权威数据永远在 `data/` 里
- 每次生成前更新剧情状态，AI 会越写越稳
- 保持设定的连贯性，AI 会像你的副作者一样理解故事

## 注意事项

- 确保 `.env` 文件已配置正确的 API Key
- 生成的章节会保存在 `data/chapters/` 目录
- 系统会严格按照设定和规则生成内容，确保长期一致性
- UI 中的所有修改都会直接保存到文件，无需担心数据丢失

