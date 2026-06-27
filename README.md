# SeekGain QuantFlow

SeekGain QuantFlow 是析境 SeekGain 的 AI 量化工作流与策略回测平台。它面向 A 股投资者、个人宽客和投研团队，把自然语言策略想法拆解为可运行、可审计、可复盘的量化研究流程。

> 说人话，做量化。

![SeekGain](https://www.seekgain.cn/logo.png)

## 核心能力

### AI 策略生成

- 用自然语言描述选股、择时、风控和仓位逻辑
- 自动拆分为选股器、风控择时器、个股择时器、仓位管理器和技术因子草稿
- 支持小白模式和进阶模式，兼顾快速体验与代码级编辑

### 策略实验室

- 策略构建：组合回测配置、策略命名、保存和一键回测
- 策略市场：发现、复用和发布策略模板
- 我的策略：保存、管理和再次运行个人策略
- 回测历史：追踪运行记录并对比任务结果
- 实盘买入：为实盘候选提供执行前检查入口

### 真实成交约束

- PIT 数据约束：只使用信号日当时可见数据
- T+1 交易规则：按 A 股成交路径拆分信号日、目标日和持仓日
- 涨跌停、停牌、成交额、滑点和容量约束
- 无法成交原因与收益结果同屏复核

### 市场中心

- 市场广度、风险热度、涨跌分布和情绪仪表盘
- A 股宽基指数、全球指数、北向资金和融资融券
- 行业/概念热力图与成分股定位
- 每日自动复盘和候选池更新

### 会员与算力

- 基础功能永久免费
- VIP / SVIP 权益、回测折扣、并发能力和算力余额
- 支持会员套餐、算力充值、订单和支付结算台

## 适用场景

- A 股量化策略研究
- 自然语言生成选股与回测策略
- 市场状态判断与每日盘后复盘
- 策略模板沉淀、发布和复用
- 团队投研流程标准化

## 技术架构

本项目已按 SeekGain 产品语义完成工程级重命名与内容替换。

```text
seekgain_quantflow/
├── src/
│   ├── common/          # 通用配置、连接器、日志和工具
│   ├── seekgain_backtest/  # 回测引擎
│   ├── seekgain_ml/        # 机器学习组件
│   ├── seekgain_plugins/   # 工作流节点与插件系统
│   ├── seekgain_server/    # FastAPI 服务
│   ├── seekgain_trading/   # 交易执行模块
│   └── seekgain_web/       # 前端静态资源
├── user_data/           # 用户数据目录
├── pyproject.toml       # Python 项目配置
├── Dockerfile
└── README.md
```

> 源码包、目录、导入路径和命令行入口均已统一为 `seekgain_*` 命名。

## 安装运行

### 环境要求

- Python 3.12+
- MongoDB / Redis / MySQL 等外部服务按实际部署配置
- 建议使用虚拟环境或 `uv`

### 安装

```bash
git clone https://github.com/SeekGainAI/seekgain_quantflow.git
cd seekgain_quantflow
pip install -e .
```

### 启动服务

```bash
python src/seekgain_server/main.py
```

启动后可访问：

```text
策略实验室：http://127.0.0.1:8000/backtest/
市场中心：http://127.0.0.1:8000/market/
```

## 自定义工作节点

开发者可以在 `src/seekgain_plugins/custom/` 中编写自定义插件。插件需要继承 `BaseWorkNode`，并实现：

- `input_model`
- `output_model`
- `run`

示例：

```python
from typing import Optional, Type
from seekgain_plugins.base import BaseWorkNode, work_node
from pydantic import BaseModel


class InputModel(BaseModel):
    number1: int
    number2: int


class OutputModel(BaseModel):
    result: int


@work_node(name="示例-两数求和", group="测试节点")
class ExamplePluginAddition(BaseWorkNode):
    @classmethod
    def input_model(cls) -> Optional[Type[BaseModel]]:
        return InputModel

    @classmethod
    def output_model(cls) -> Optional[Type[BaseModel]]:
        return OutputModel

    def run(self, input: InputModel) -> OutputModel:
        return OutputModel(result=input.number1 + input.number2)
```

## 许可证

本项目采用 AGPL-3.0 许可证。
