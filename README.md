# youth_growth_Skill — ai-skill（本地脚手架）与青少年成长工具

项目根目录文件夹名为 **`youth_growth_Skill`**；下文命令均假定你已在该目录下执行（例如 `cd ~/Downloads/youth_growth_Skill`）。

本目录在仅有 `DEVELOPMENT.md` 约定的情况下，补齐了最小可运行的 **Flask + Skill Registry + youth_growth API**，便于后续与官方 `learnscape-sg/ai-skill` 仓库对齐合并。

## 环境

- Python 3.11+
- `pip install -r requirements.txt`

可选环境变量（见 `.env.example`）：

- `HTTP_PORT`：默认 `5005`
- `ENV`：`dev` 时 `run.py` 开启 debug

## 启动服务

```bash
python run.py
```

浏览器 Demo UI（最小页面）：

```text
http://127.0.0.1:5005/
```

健康检查：

```bash
curl -s -X POST http://localhost:5005/health
```

## 独立 Demo（不启动 HTTP）

```bash
python demo/youth_growth_demo.py -i demo/sample_input.json
```

## API 示例

问卷模板：

```bash
curl -s -X POST http://localhost:5005/youth_growth/v1_0/questionnaire/template \
  -H "Content-Type: application/json" -d '{}'
```

评估（核心）：

```bash
curl -s -X POST http://localhost:5005/youth_growth/v1_0/assess \
  -H "Content-Type: application/json" \
  -d @demo/sample_input.json
```

仅年度曲线：

```bash
curl -s -X POST http://localhost:5005/youth_growth/v1_0/curve \
  -H "Content-Type: application/json" \
  -d '{"questionnaire":{}, "birth":{"year":2012,"month":6,"day":15}}'
```

Skill 列表 / 调用：

```bash
curl -s -X POST http://localhost:5005/skills/v1_0/list -H "Content-Type: application/json" -d '{}'
curl -s -X POST http://localhost:5005/skills/v1_0/youth_growth_assessment/invoke \
  -H "Content-Type: application/json" -d @demo/sample_input.json
```

## 测试

```bash
pytest tests/ -v
```

## 说明

- 问卷输入已支持 SDQ 友好短题映射（0-2 分），评分逻辑位于 `util/youth_growth/scoring.py`。
- 年度曲线数据位于 `util/youth_growth/curve_engine.py`，由资料归纳并结构化为可绘制预测曲线。
- 五行分型优先使用出生日期日干映射；若提供 `birth.hour`（0-23），会换算传统时辰并按完整八字四柱参与计算（`util/youth_growth/profile_mapper.py`）。
- 危机关键词扫描见 `util/youth_growth/safety.py`，生产环境需持续运营迭代。
