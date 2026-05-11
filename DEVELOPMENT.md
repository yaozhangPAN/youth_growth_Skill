# 开发与测试指南

## 分支策略

```
release（生产环境）
   └── staging（预发布 / QA 测试）
          └── yourname/feat/xxx（你的功能分支）
```

**规则：**
- 功能分支必须从 `release` 切出，不能从 `staging` 或 `main` 切
- 所有代码必须先合并到 `staging` 才能上 `release`
- 合并到 `release` 必须在 GitHub 上提交 **Pull Request，并获得 Code Review 审批**

> **推荐使用 IDE（VS Code）完成所有 Git 操作**，避免手敲命令出错。下方每个步骤都优先说明 IDE 操作方式，命令行仅作备用参考。

### 日常开发流程

#### 第一步：从 release 切出功能分支

**VS Code 操作：**
1. 点击左下角状态栏的分支名（如 `release`）
2. 在弹出的搜索框顶部选择 **「Create new branch from...」**
3. 输入新分支名，格式：`yourname/feat/your-feature-name`
4. 选择 `release` 作为来源分支
5. VS Code 会自动切换到新分支

> 切分支前先确保本地 `release` 是最新的：在 VS Code 底部状态栏点击同步图标（↑↓），或在源代码管理面板菜单中选择 **「拉取」**。

```bash
# 命令行备用
git checkout release && git pull origin release
git checkout -b yourname/feat/your-feature-name
```

---

#### 第二步：开发、暂存、提交

**VS Code 操作：**
1. 开发完成后，点击左侧活动栏的 **源代码管理图标**（或 `Ctrl+Shift+G` / `Cmd+Shift+G`）
2. 在「更改」列表中，逐个点击文件旁的 **`+`** 将需要提交的文件加入暂存区（不要直接点「暂存所有更改」，避免把不该提交的文件带进去）
3. 在顶部输入框填写提交信息，格式：`[TICKET-000] 简短描述`
4. 点击 **「提交」** 按钮（✓）

```bash
# 命令行备用
git add src/your_file.py
git commit -m "[TICKET-000] 简短描述"
```

---

#### 第三步：本地自测

本地自测通过后再进行下一步，参见文末[测试清单](#测试清单)。

---

#### 第四步：推送分支并提 PR 到 staging

**VS Code 操作：**
1. 在源代码管理面板点击顶部菜单（`···`）→ **「推送」**，或点击底部状态栏的同步图标
2. 首次推送会提示「是否发布分支」，点击确认
3. VS Code 通常会弹出提示「在 GitHub 上创建 Pull Request」，点击即可跳转；或直接去 GitHub 仓库页面，会有黄色横幅提示，点击 **「Compare & pull request」**
4. **注意：base 分支选 `staging`**，不要选 `release`
5. 填写 PR 标题和描述，提交

```bash
# 命令行备用
git push origin yourname/feat/your-feature-name
```

---

#### 第五步：通知测试同学

staging 部署完成后（通常几分钟内），通知测试同学进行测试，告知改动的接口和测试要点。

---

#### 第六步：测试通过后，提 PR 到 release

1. 在 GitHub 上新开一个 PR：**base = `release`，compare = `staging`**
2. 该 PR 需要至少一名成员 Code Review 审批后才能合并
3. 合并后会自动触发生产部署

---

#### 常用 Git 操作速查（VS Code）

| 操作 | VS Code 方式 |
|---|---|
| 切换分支 | 点击左下角分支名 → 选择目标分支 |
| 拉取最新代码 | 源代码管理面板 `···` → 拉取，或底部状态栏同步图标 |
| 暂存文件 | 源代码管理面板，文件旁点击 `+` |
| 撤销暂存 | 已暂存区文件旁点击 `-` |
| 提交 | 填写信息后点击 ✓ |
| 推送 | 源代码管理面板 `···` → 推送，或底部同步图标 |
| 查看改动 | 点击源代码管理面板中的文件，左右对比 diff |
| 丢弃本地修改 | 文件旁点击 `↺`（谨慎操作，不可撤销） |

---

## 本地环境搭建

### 前置要求

- Python 3.11+
- pip

### 首次初始化

```bash
# 克隆仓库
git clone https://github.com/learnscape-sg/ai-skill.git
cd ai-skill

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入 API Key 等配置（参考 .env.example 中的说明）
```

### 环境变量说明（`.env`）

| 变量 | 说明 |
|---|---|
| `LLM_PROVIDER` | `gemini` 或 `openai` |
| `GEMINI_API_KEY` | Gemini API Key（使用 Gemini 时填写） |
| `GEMINI_MODEL` | 如 `gemini-2.0-flash` |
| `OPENAI_API_KEY` | OpenAI API Key（使用 OpenAI 时填写） |
| `HTTP_PORT` | 默认 `5005` |
| `ENV` | 本地填 `dev`，生产填 `prod` |

### 启动服务

```bash
# 开发模式（Flask 内置服务器，支持热重载）
python run.py

# 生产模式（Gunicorn，与服务器一致）
bash run.sh
```

服务启动后访问 `http://localhost:5005`

### 健康检查

```bash
curl -X POST http://localhost:5005/health
# → {"status": "ok", "service": "wms-ai-skill"}
```

---

## 架构说明

```
apps/          ← API 服务层（HTTP 路由、请求校验、响应格式化）
  ├── chat/
  ├── exam_extract/
  ├── pdf/
  ├── skills/       ← Skill 管理 API（列表、调用、下载）
  ├── vision/
  └── voice/

skills/        ← Skill 层（可复用的 AI 能力，供 apps 或其他 skill 调用）
  ├── internal/     ← 内置 skill，随代码库一起维护
  └── external/     ← 动态下载的第三方 skill

util/          ← 基础设施层（被 apps 和 skills 共同依赖的底层工具）
  ├── llm/          ← LLM 客户端封装、agent helper
  ├── skill_registry.py  ← Skill 注册表（singleton，启动时加载所有 skill）
  ├── cache_helper/ ← 进程内任务表、其他短生命周期状态
  ├── conversation/ ← 多轮对话记忆
  ├── agents/       ← 通用 agent 工具
  └── sys_helper/   ← 日志、全局变量
```

**`apps` 层高于 `skills` 层；`util` 层在最底下。**

- `apps` 负责 HTTP 层的事：路由、请求解析、入参校验、统一响应格式、错误码
- `skills` 负责 AI 逻辑：调 LLM、工具调用、外部服务集成
- `apps` 可以调用 `skills`，但 `skills` 不能反向依赖 `apps`
- `skills` 应保持独立，可以脱离 HTTP 上下文单独使用和测试
- `util` 任何层都可以 import，但 `util` 自己不依赖 `apps` 或 `skills`

---

## Skill 和 Util 的区别

两者都是「可复用的代码」，但定位完全不同。**写新代码前先想清楚归哪一边，能避免大部分架构走样。**

### 一句话区分

- **Skill** = 一个对外暴露的 **AI 能力**，可以被 LLM agent 当工具调用
- **Util** = 给代码用的 **基础设施 / 工具函数**，不对外暴露

### 详细对比

| 维度 | Skill (`skills/internal/<name>/`) | Util (`util/<name>/`) |
|---|---|---|
| **核心职责** | AI 能力（调 LLM、视觉识别、文件解析等） | 基础工具（日志、缓存、HTTP 客户端、注册表） |
| **典型例子** | `exam_extract`、`question_explain`、`vision_ocr`、`document_parser`、`web_search` | `llm/LLMHelper`、`cache_helper/task_store`、`sys_helper/log_helper`、`skill_registry` |
| **是否含 LLM 调用** | 通常是 | 通常不是（`util/llm` 例外，但只是**封装** LLM 客户端，不做业务） |
| **加载方式** | 启动时由 registry 自动扫描加载，singleton | 普通 Python 模块，直接 `import` |
| **调用方式** | `get_registry().get("name")` → 拿 SkillWrapper 调方法 | `from util.xxx import yyy` |
| **必须的文件** | `SKILL.md`（元数据）+ 可选 `skill.py`（自定义逻辑） | 任意 `.py` 文件 |
| **对外可见性** | 通过 `/skills/v1_0/list` 列出，`/skills/v1_0/<name>/invoke` 调用 | 仅代码内部使用，对 HTTP 不可见 |
| **能被 LLM agent 当 tool 用** | ✅ 是 | ❌ 不是 |
| **能动态下载安装** | ✅ external skill 可以从 GitHub 下载 | ❌ 必须随代码部署 |
| **依赖方向** | 可以依赖 util；可以依赖其他 skill；不能依赖 apps | 不能依赖 apps 或 skills（最底层） |

### 决策树：新代码该放哪？

```
要写一段可复用的逻辑
  │
  ├─ 它是 AI 能力吗？（调 LLM、做语义判断、生成内容、agent tool）
  │    ├─ 是 → 放 skills/internal/<name>/
  │    │
  │    └─ 否 ↓
  │
  ├─ 它会被多个 skill 或多个 apps 共用吗？
  │    ├─ 是 → 放 util/<category>/
  │    │
  │    └─ 否 ↓
  │
  └─ 只服务于某个具体业务模块？
       └─ 放 apps/<module>/business/ 当成业务编排逻辑
```

### 几个容易拿不准的边界例子

| 场景 | 归处 | 理由 |
|---|---|---|
| LLM 客户端封装（`LLMHelper.get_llm()`） | **util/llm** | 是基础设施，不是能力本身。Skill 调用它来做事 |
| 进程内任务表（async task store） | **util/cache_helper** | 通用工具，多个业务模块都可能用 |
| 解析 CSV / XLSX / 文本型 PDF / 文件类型识别 | **util/document_parser** | 纯 Python 库调用，不依赖 LLM |
| 图片视觉 OCR / 扫描版 PDF 兜底 / LLM 整理 Markdown | **skill (`document_parser`)** | 依赖 LLM 视觉，对外作为 AI 能力暴露 |
| 把汉字转拼音（pypinyin 调用） | **业务编排里直接用** | 单一职责的纯函数，不复杂、不通用，不值得包成 skill 或 util |
| Skill 注册表本身（`get_registry()`） | **util** | 是 skill **基础设施**，不是 skill |
| 解析 LLM 返回的 JSON | **util (`graph_agent_helper.parse_json_from_llm_response`)** | 工具函数，所有 skill 都用 |

> **同名混合场景的处理**：`document_parser` 是一个典型例子 —— 同一套「解析文件」概念，纯 Python 部分（CSV/XLSX/文本 PDF）放在 `util/document_parser`，AI 增强部分（图片 OCR、扫描页兜底）放在 `skills/internal/document_parser`。Skill 内部 import util 来复用纯逻辑；调用方按需选层：纯解析直接 `from util.document_parser import parse_csv`，需要 OCR 走 `get_registry().get("document_parser")`。

### 反模式（不要这样做）

❌ **把 prompt 直接写在 business 文件里** —— 应该收进 skill。Prompt 是 AI 能力的一部分。

❌ **Skill 内部 `from apps.xxx import yyy`** —— 反向依赖。Skill 应该独立可测，不依赖具体 HTTP 层。

❌ **在 business 里直接 `from skills.internal.xxx.skill import XxxSkill` 然后 `XxxSkill()`** —— 绕过 registry，导致重复实例化、行为不一致。永远走 `get_registry().get(name)`。

❌ **把通用工具放进 skill** —— 比如把"汉字转拼音"做成一个 skill。它不是 AI 能力，无意义的抽象。

❌ **在 util 里写业务逻辑** —— util 应该是领域无关的。如果某个工具只服务于一个业务，放进那个业务的 business 模块即可。

---

## 如何创建一个新 Skill

每个 skill 存放在 `skills/internal/<skill-name>/` 目录下，至少需要一个 `SKILL.md` 文件。

### 方式 A：纯 LLM 指令 skill（无需写 Python）

新建 `skills/internal/my_skill/SKILL.md`：

```markdown
---
name: my_skill
description: 这个 skill 的一句话描述
version: 1.0.0
---

# My Skill

在这里描述 skill 的功能和行为，这段内容会作为 system prompt 传给 LLM。

## 指令

- 指令 1
- 指令 2
```

不需要 Python 文件。Skill loader 会自动用这些指令调用 LLM 执行 `run()`。

### 方式 B：自定义逻辑 skill

新建 `SKILL.md`（frontmatter 同上），再新建 `skills/internal/my_skill/skill.py`：

```python
from skills.base_skill import BaseSkill

class MySkill(BaseSkill):
    name = "my_skill"
    description = "一句话描述"
    version = "1.0.0"

    def run(self, user_input: str, **kwargs) -> str:
        # 自定义逻辑
        return f"结果：{user_input}"
```

`BaseSkill.run()` 是唯一入口，由 `/skills/v1_0/invoke` API 调用。

### 方式 C：附加参考文档

新建 `skills/internal/my_skill/reference.md`，用于存放结构化数据、模板或查找表。  
Skill loader 会自动将其追加到 system prompt，同时也可通过 `/skills/v1_0/<name>/reference` 接口单独获取。

### 验证 skill 已加载

```bash
curl -X POST http://localhost:5005/skills/v1_0/list
```

返回列表中应能看到你的 skill。若没有，排查：
- `SKILL.md` frontmatter 中 `name` 字段是否填写
- `skill.py` 是否有语法错误
- 目录是否在 `skills/internal/` 或 `skills/external/` 下

### 调用 skill

```bash
curl -X POST http://localhost:5005/skills/v1_0/my_skill/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "测试输入"}'
```

---

## 如何新增 API 模块

1. 创建 `apps/my_module/`，包含 `__init__.py` 和 `v1_0/` 子目录
2. 在 `apps/my_module/v1_0/__init__.py` 中注册 blueprint：

```python
from flask import Blueprint
blueprint = Blueprint("my_module_v1_0", __name__)
```

3. 在 `apps/my_module/v1_0/routes.py` 中写路由：

```python
from flask import jsonify, request
from apps.my_module.v1_0 import blueprint

@blueprint.route("/my_module/v1_0/my-endpoint", methods=["POST"])
def my_endpoint():
    data = request.get_json() or {}
    # 调用 skill 或业务逻辑
    return jsonify({"code": 200, "msg": "success!", "data": {}}), 200
```

4. 在 [apps/__init__.py](apps/__init__.py) 中注册 blueprint：

```python
for module_name in [..., "my_module.v1_0"]:
```

URL 命名规范：`/<模块>/<版本>/<动作>`，例如 `/exam_extract/v1_0/extract-vocabulary`

---

## 单元测试规范

> **每开发一个新功能都必须配套单测** —— 不论是 apps 服务、skill，还是 util 工具。没有单测的 PR 不应被合入 staging。

### 目录布局

`tests/` 放在项目根目录，**镜像源码结构**：

```
tests/
├── util/
│   ├── cache_helper/
│   │   └── test_task_store.py
│   └── document_parser/
│       ├── test_detect.py
│       ├── test_csv_parser.py
│       ├── test_xlsx_parser.py
│       └── test_pdf_parser.py
├── skills/
│   └── internal/
│       ├── exam_extract/test_skill.py
│       ├── question_explain/test_skill.py
│       └── document_parser/test_skill.py
└── apps/
    ├── exam_extract/v1_0/test_routes.py
    └── ...
```

文件名统一 `test_<模块>.py`，函数名统一 `def test_<行为>()`。

### 三层测试不同的写法

| 层 | 测什么 | 是否 mock LLM | 工具 |
|---|---|---|---|
| **util** | 纯函数输入 → 输出 | ❌ 不需要，util 本就不依赖 LLM | `pytest`，断言 + fixture |
| **skill** | 方法的业务行为 | ✅ **建议 mock**（速度快、确定性、不烧 API 配额） | `pytest` + `unittest.mock.patch("util.llm.LLMHelper.get_llm")` |
| **apps** | HTTP 请求 → 响应 | ✅ mock skill registry 返回值 | Flask `app.test_client()` |

### 关键约束

1. **不要在测试里打真实 LLM**（除非显式标记 `@pytest.mark.integration`）。CI 跑 LLM 调用慢且不稳定，会让单测失去"快速反馈"的价值。
2. **util 测试要彻底纯净**：测 `util.document_parser` 应该完全不会触发 langchain import。这是验证架构边界的方式。
3. **测试用例要覆盖边界**：空输入、非法格式、缺字段、超长文本、中英文混合 —— 不要只测 happy path。
4. **共用 fixture 放 `conftest.py`**：每个 `tests/<dir>/` 下需要的 mock 数据、fake LLM client 等。

### 运行方式

```bash
# 全部
pytest tests/

# 单个文件
pytest tests/util/document_parser/test_csv_parser.py -v

# 仅 util（不依赖外部服务，CI 必跑）
pytest tests/util/ -v

# 包含 LLM 真实调用（开发本地偶尔跑一遍）
pytest -m integration
```

CI / `pytest tests/` 跑通是 staging PR 的必要条件。

---

## AI 协作开发的测试代码处理

用 Claude / Cursor / Copilot 帮忙写代码时，AI 经常会**临时生成一段验证脚本**（比如 `test_quick.py`、`debug_pdf.py`、`verify_skill.py` 之类）。这类一次性脚本必须区别对待。

### 判断标准（"留还是删"）

问自己一句话：**这段测试明天还能保护我不写出 bug 吗？**

| 类型 | 例子 | 处理 |
|---|---|---|
| **回归测试** —— 描述了某个功能的正确行为 | `test_csv_parser.py` 里测「空 CSV 应返回原文」 | ✅ **保留**，整理后放进 `tests/` 对应目录 |
| **临时验证脚本** —— 只是确认"我刚写的能跑" | `verify_my_new_skill.py` 在根目录调一遍方法看输出 | ❌ **跑完即删**，不要进 git |
| **AI 生成的探索代码** —— 试错过程中产生的 mock / fake 文件 | 根目录冒出来 `mock_pdf.py`、`sample_data.json` | ❌ **删除**，或者整理后放进 `tests/fixtures/` |
| **打印调试代码** —— 一堆 `print()` 验证流程 | `quick_test.py` 满屏 print | ❌ **删除**，正式测试用 assertion 而不是 print |

### 流程

1. 让 AI 写功能代码
2. 让 AI 顺手写**正式单测**（明确说"放到 `tests/` 对应目录，用 pytest 风格 assert"）
3. 如果中间 AI 生成了**临时验证脚本**（比如根目录的 `test_xxx.py`），跑通确认无误后 **`rm` 删除 + 不要 `git add`**
4. 提交前 `git status` 检查根目录有没有不该出现的 `.py` 文件 / `.pkl` / `.json` 等遗留物

### 反例（**不要这样做**）

❌ 根目录留一堆 `quick_test.py` / `debug.py` / `verify.py` 没人敢删，怕影响什么
❌ 一次性脚本被 `git add .` 误推进仓库
❌ AI 生成的 5 行打印脚本占着 `tests/` 目录的位置，看起来好像有覆盖率，实际上没断言
❌ 把生产代码里的临时 `print()` 当作测试

### 一句话总结

> **会被 CI 跑、有 assertion、能描述行为契约的，是单测；只是开发中验证一下的，跑完就删。**

---

## 测试清单

### 推送到 staging 之前（开发自测）

- [ ] 本地服务正常启动，无报错（`python run.py`）
- [ ] 目标接口返回预期结果（curl 或 Postman 测试）
- [ ] 边界情况已测试：空输入、非法文件类型、缺少必填字段
- [ ] **新增/修改的功能都已配套单测，`pytest tests/` 全绿**
- [ ] **根目录没有遗留临时脚本**（`git status` 确认）
- [ ] 代码中没有硬编码的密钥或 API Key
- [ ] `.env` 未被提交（已在 `.gitignore` 中）

### 合并到 staging 之后（QA 测试）

- [ ] 通知测试同学，说明改动的接口和建议的测试用例
- [ ] 测试同学完成测试并明确给出通过结论（PR 评论或消息）
- [ ] 如有问题，在当前功能分支修复后重新推 staging，再次通知测试

### 提 PR 合并到 release 之前

- [ ] 已收到测试同学的通过确认
- [ ] PR 描述清楚说明了改动内容和原因
- [ ] 至少获得一名成员的 Code Review 审批（由 branch protection 强制执行）
- [ ] 与 `release` 分支无冲突
