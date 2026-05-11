# 青少年成长评估规则说明（开发拆解版）

> 面向：后端/算法/前端/测试  
> 目标：明确当前版本的输入规范、执行顺序、阈值与可扩展点  
> 版本：v1.0.0（当前代码实现）

> 2026-05 更新：默认输入量表切换为 `sdq_friendly_short_v1`（10 题，0-2 分），并保留旧版 1-5 维度兼容。

## 1. 主要入口与模块

- HTTP 入口：`POST /youth_growth/v1_0/assess`
  - 文件：`apps/youth_growth/v1_0/routes.py`
- Skill 编排：`skills/internal/youth_growth_assessment/SKILL.py`
- 核心规则模块：
  - 问卷评分：`util/youth_growth/scoring.py`
  - 危机扫描：`util/youth_growth/safety.py`
  - 分型映射：`util/youth_growth/profile_mapper.py`
  - 年度曲线：`util/youth_growth/curve_engine.py`

## 2. 输入数据契约（逻辑层）

`assess` 支持字段：

- `birth`（object，可选）
  - `year` / `month` / `day`
- `questionnaire`（object，必填）
  - 默认维度键见 `DEFAULT_DIMENSION_KEYS`
  - 可选 `self_harm_signal`
  - 可选兴趣倾向 `affinity_*`
  - 可选文本 `notes` 或 `free_text`
- `element_type` 或 `dominant_element`（string，可选）

### 路由校验规则

- `questionnaire` 缺失或非 object -> `400`
- `birth` 若存在但非 object -> `400`

## 3. 执行流水线（按顺序）

1. 路由层构建 payload 并调用 Skill
2. `crisis_from_questionnaire()` 危机判定
3. `compute_scores()` 计算维度、分数、分层、flags
4. `resolve_element()` 计算五行 key 与来源说明
5. `build_profile()` 组装画像文案
6. `get_yearly_curve()` + `peaks_and_troughs()` 生成年度曲线
7. `_actions_for_risk()` 生成建议
8. 若危机触发，覆盖建议与曲线说明
9. 输出最终 JSON（`ensure_ascii=False`）

## 4. 问卷标准化规则

文件：`util/youth_growth/scoring.py`

- 标准化函数：`normalize_questionnaire(raw)`
- 钳制规则：每个维度通过 `_clamp_int` 限制在 `[1, 5]`
- 缺省值：默认 `3`
- `self_harm_signal` 仅当传入时参与结果维度

默认维度（8 项）：

- `emotion_dysregulation`
- `stress_level`
- `social_isolation`
- `academic_pressure`
- `sleep_quality`（正向项）
- `attention_focus`
- `mood_low_energy`
- `risk_behaviors`

## 5. 心理健康分公式（0~100）

函数：`compute_mental_wellbeing_score(dimensions)`

### 5.1 中间量

- `sleep_contrib = (sleep_quality - 1) / 4 * 100`
- `stress_like = mean([emotion_dysregulation, stress_level, social_isolation, academic_pressure, attention_focus, mood_low_energy, risk_behaviors])`
- `stress_penalty = (stress_like - 1) / 4 * 70`
- `base = 100 - stress_penalty`
- `score = 0.65 * base + 0.35 * sleep_contrib`

### 5.2 自伤信号修正

若存在 `self_harm_signal`：

- `>= 4`：`score -= 35`
- `>= 3`：`score -= 20`
- `>= 2`：`score -= 8`

最终：`score = clamp(score, 0, 100)`，保留 1 位小数。

## 6. 风险等级与 flags

函数：`risk_tier_from_score(wellbeing)`

- `wellbeing >= 70` -> `low`
- `45 <= wellbeing < 70` -> `medium`
- `< 45` -> `high`

函数：`summarize_flags(dimensions)`

- `stress_level >= 4` -> `elevated_stress`
- `sleep_quality <= 2` -> `poor_sleep`
- `social_isolation >= 4` -> `social_distress`
- `mood_low_energy >= 4` -> `low_mood_energy`
- `self_harm_signal >= 3` -> `self_harm_concern`

## 7. 危机判定规则

文件：`util/youth_growth/safety.py`

### 7.1 触发条件

`crisis_from_questionnaire(q)` 返回 `(bool, reasons)`

- 文本命中危机关键词：
  - 来源字段：`notes` 或 `free_text`
  - 关键词示例：`不想活`、`自杀`、`自残`、`结束生命`、`割腕`、`跳楼`
  - reason：`free_text_keyword`
- `self_harm_signal >= 4`
  - reason：`self_harm_signal_high`

### 7.2 触发后的覆盖逻辑

在 `SKILL.py` 中：

- `recommended_actions` 强制切到危机版本
- `growth_curve.note` 替换为“先处理安全与支持”

## 8. 五行分型逻辑

文件：`util/youth_growth/profile_mapper.py`

函数：`resolve_element(birth, questionnaire, element_override)`

优先级：

1. 显式覆盖 `element_override`（且在 `ELEMENT_KEYS`）
2. 出生日期日干计算（仅要有 birth，就走真实历法，`birth_day_stem`）
3. 问卷倾向推断（仅在没有可用 birth 时）
4. 默认问卷推断兜底

### 8.1 问卷倾向映射

函数：`infer_element_from_questionnaire(q)`  
按最大值选择：

- `water` <- `affinity_logic_math`
- `metal` <- `affinity_rules_precision`
- `earth` <- `affinity_stability_practice`
- `wood` <- `affinity_nature_humanities`
- `fire` <- `affinity_expression_performance`

### 8.2 出生日期日干计算（真实历法）

函数：`infer_element_from_birth(year, month, day)`

- 使用库：`lunar-python`
- 路径：`Solar.fromYmd(y, m, d).getLunar().getDayGan()`
- 日干映射五行：
  - 甲/乙 -> 木
  - 丙/丁 -> 火
  - 戊/己 -> 土
  - 庚/辛 -> 金
  - 壬/癸 -> 水

说明：这是按日干取五行（日主）的真实历法计算，不再使用占位哈希。

## 9. 画像与曲线生成

### 9.1 画像

函数：`build_profile(element)`

输出：

- `element_key`
- `element_label_zh`
- `psychology_tag`
- `psychology_summary`
- `subject_strengths`

### 9.2 曲线

文件：`util/youth_growth/curve_engine.py`

- 数据源：`_CURVES` 静态矩阵
- 年份：`2026..2031`
- 每年字段：
  - `year`
  - `pillar_tag`
  - `psych_state`
  - `learning_focus`
  - `wellbeing_hint`
  - `joy_index`
  - `concern`
  - `guidance`

`peaks_and_troughs(curve)`：

- 以 `learning_focus` 为比较基准
- min -> `trough_years`
- max -> `peak_years`

## 10. 建议生成规则

函数：`_actions_for_risk(tier, crisis)`

- `crisis=True` -> 返回危机动作模板（固定 2 条）
- 非危机：
  - `high` -> 3 条（专业评估 + 家庭支持 + 学业拆解）
  - `medium` -> 2 条（作息运动 + 家校协同）
  - `low` -> 2 条（日常沟通 + 优势强化）

## 11. 输出契约（核心字段）

返回结构（摘）：

- `meta.skill` / `meta.version` / `meta.element_resolution`
- `safety_notice`
- `crisis_escalation` / `crisis_reasons`
- `mental_health_observation`
  - `dimensions`
  - `mental_wellbeing_score`
  - `risk_tier`
  - `flags`
- `profile`
- `growth_curve.years` / `growth_curve.summary` / `growth_curve.note`
- `recommended_actions`

## 12. 可扩展点建议

- 危机词表：
  - 文件：`safety.py` 中 `_CRISIS_PATTERNS`
  - 建议引入词权重、否定词处理、上下文窗口
- 评分权重：
  - 文件：`scoring.py`
  - 可配置化（环境变量或配置文件）
- 分型策略：
  - 若后续要支持更完整八字，可继续扩展到年/月/日/时四柱联动
- 曲线矩阵：
  - 文件：`curve_engine.py`
  - 建议迁移到可版本化数据文件（JSON/YAML）
- 输出可解释性：
  - 增加 `explanations` 字段，逐项说明“哪些输入导致该结论”

## 13. 测试建议（最小集）

- 路由校验：
  - questionnaire 缺失、类型错误、birth 类型错误
- 评分边界：
  - 全 1、全 5、sleep 极端值、自伤阈值 2/3/4
- 危机触发：
  - notes 命中关键词、自伤高分、两者同时触发
- 分型优先级：
  - override > affinity > birth > default
- 曲线摘要：
  - `peaks_and_troughs` 在固定曲线下输出稳定

## 14. 当前模型定位声明（给开发）

这是“**规则引擎 + 历法计算（日干五行）**”的组合，不是医学诊断模型，也不是统计学习模型。  
在修改任何阈值、权重、词表前，建议同步更新：

- 对外产品文案
- 接口文档示例
- 回归测试基线
