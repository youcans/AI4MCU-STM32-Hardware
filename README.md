# AI4MCU-STM32-Hardware

**中文** | [English](README_en.md)

**基于 Codex、altium-monkey-mcp 和 Python 的 STM32 硬件信息提取工作流**

- 项目名称：AI4MCU-STM32-Hardware
- GitHub 仓库：[AI4MCU-STM32-Hardware](https://github.com/youcans/AI4MCU-STM32-Hardware)
- 作者：Huang Xiaofeng & Huang Shan
- 邮箱：ai4mcu@qq.com
- GitHub：[@youcans](https://github.com/youcans)

---

## 项目简介

AI4MCU-STM32-Hardware 是一个面向 STM32 嵌入式软件 AI 协同开发的硬件信息提取项目。项目将 Altium Designer 工程解析、原始网表导出、硬件信息标准化、核心硬件上下文生成和数据一致性检查组织为可复用的工作流。

开发者使用 VS Code、Codex、altium-monkey-mcp 和 Python，结合开发板原理图及技术手册，将原始硬件资料转换为 AI 可直接使用的两类标准化硬件文件：

- **核心硬件上下文（`<mcu>_hardware_context.md`）**：保存常用 MCU 引脚、板载资源、功能、配置条件与待确认事项，供 AI 编程时**默认读取**。
- **参考硬件网表（`<mcu>_hardware_netlist.json`）**：保存元器件、网络连接及 MCU 引脚索引，供 AI 在需要更详细连接信息时**按需查询**。

项目遵循：

> **准确、清晰、简洁。**

> **统一流程，保留依据；实际验证，再迭代。**

---

## 项目组成

```text
AI4MCU-STM32-Hardware/
├── README.md
├── .gitignore
├── standards/                         # 通用规范与模板
│   ├── hardware_netlist_spec.md
│   ├── hardware_facts_spec.md
│   └── hardware_context_template.md
├── tools/                             # 通用转换程序
│   └── generate_hardware_netlist.py
├── workflows/                         # 工作流与实践记录
│   ├── hardware_workflow.md
│   └── hardware_progress.md
└── boards/
    ├── nucleo-c542rc/
    │   ├── Altium_Designer/           # 原始工程
    │   ├── references/                # 原理图与技术资料
    │   ├── process/                   # 过程数据与日志
    │   ├── c542rc_hardware_context.md
    │   └── c542rc_hardware_netlist.json
    └── nucleo-g431rb/
        ├── Altium_Designer/           # 原始工程
        ├── references/                # 原理图与技术资料
        ├── process/                   # 过程数据与日志
        ├── g431rb_hardware_context.md
        └── g431rb_hardware_netlist.json
```

主要目录说明：

- `standards/`：参考网表规范、硬件事实规范和核心上下文模板。
- `tools/`：将 MCP 原始 JSON 网表转换为标准化参考网表的 Python 程序。
- `workflows/`：保存工作流执行指南和实践记录。
- `boards/`：按开发板分别保存最终硬件信息和本地原始资料目录。
- `prompts/`：预留的提示词目录；通用 Codex 提示词目前写在工作流文档中。

`Altium_Designer/`、`references/` 和 `process/` 目录通过 `.gitkeep` 保留目录结构，具体文件被 `.gitignore` 排除，不上传到仓库。使用者需要自行准备原始资料，执行后在本地生成过程文件。

---

## 提取STM32硬件信息工作流

### 六步标准处理流程

| 步骤 | 主要工作 | 输出 |
|---|---|---|
| 1. 原始硬件资料准备 | 整理 Altium 工程、原理图和技术手册 | 完整的资料目录 |
| 2. 原始网表提取 | 使用 Codex 调用 altium-monkey-mcp 查询工程并导出网表 | `<design>_netlist.json` |
| 3. 标准化参考网表生成 | 运行 Python 转换程序并检查关联关系 | `<mcu>_hardware_netlist.json`、校验报告 |
| 4. 硬件事实整理 | 结合参考网表、原理图及手册整理 MCU 引脚与资源 | `<design>_hardware_facts.md` |
| 5. 核心硬件上下文生成 | 按通用模板提炼常用硬件信息 | `<mcu>_hardware_context.md` |
| 6. 数据关联与一致性检查 | 联合审核上下文、参考网表和事实记录 | 审核报告 |

流程中，`<design>` 为板卡设计编号的小写形式（如 `mb1367`），`<mcu>` 为目标 MCU 简写（如 `g431rb`）。原始与中间文件保存在 `process/`，两类最终文件放在开发板目录根部。

完整操作说明、PowerShell 命令、Codex 通用提示词和完成条件见：

**[workflows/hardware_workflow.md](workflows/hardware_workflow.md)**

### 数据使用原则

AI 编程时优先读取精简的核心硬件上下文；当其中的信息不足时，再按文档中的检索指引读取参考网表或硬件事实记录。网表反映设计连接，不能单凭网络端点推断实际焊桥导通、器件装配或 MCU 选项字节状态。

---

## 快速开始

### 1. 获取项目

在 Windows PowerShell 中克隆仓库：

```powershell
git clone https://github.com/youcans/AI4MCU-STM32-Hardware.git C:\AI4MCU-STM32-Hardware
Set-Location "C:\AI4MCU-STM32-Hardware"
```

如使用其他项目路径，执行时应同步修改工作流命令和 Codex 提示词中的绝对路径。

### 2. 准备工具

- 安装 VS Code，并配置可用的 Codex 环境。
- 安装并注册 [altium-monkey-mcp](https://github.com/youcans/AI4MCU-STM32-Hardware) 所需的 MCP 服务；实际安装来源及配置方法以工作流文档和该工具的官方说明为准。
- 准备可用的 Python 解释器。`generate_hardware_netlist.py` 使用 Python 标准库，不要求在本仓库中创建 `.venv`。

在 VS Code 的 PowerShell 终端检查 MCP 注册状态：

```powershell
Set-Location "C:\AI4MCU-STM32-Hardware"
codex mcp list
```

确认 `altium-monkey` 已启用，并在 Codex 中验证相关 MCP 工具可访问。**工具已注册不代表工程一定能成功读取**，还应在工程查询时进行实际验证。

### 3. 准备开发板资料

以 NUCLEO-G431RB 为例，将完整的 MB1367 Altium 工程（含 `.PrjPcb` 和相关 `.SchDoc` 文件）放入：

```text
boards/nucleo-g431rb/Altium_Designer/
```

将开发板原理图 PDF、用户手册、MCU 数据手册和按需使用的参考手册放入：

```text
boards/nucleo-g431rb/references/
```

新开发板可在 `boards/` 下按相同结构建立目录。

### 4. 执行工作流

在 VS Code 中打开本项目，按照 **[hardware_workflow.md](workflows/hardware_workflow.md)** 的顺序执行六步流程。按文档填写目标开发板名称、工程绝对路径、设计编号、目标 MCU、基础设计 MCU 和主 MCU 位号，再使用相应的 Codex 提示词和 PowerShell 命令。

每个阶段保留实际操作记录，统一追加到：

```text
boards/<board-name>/process/<design>_hardware_log.md
```

转换后检查程序退出码、JSON 结构与校验报告；生成核心上下文后执行联合审核。若出现阻断性连接问题，修正后重新审核。

### 5. 使用生成的硬件文件

完成并通过审核后，在 AI 软件开发工程中配置对应的核心硬件上下文作为默认硬件资料；需要更具体的器件、网络和端点信息时，再查询参考网表。

---

## 已验证的开发板

| 开发板 | 板卡设计编号 | 目标 MCU | 标准化参考网表 | 核心硬件上下文 |
|---|---|---|---|---|
| NUCLEO-C542RC | MB2213 | STM32C542RCT6 | [JSON](boards/nucleo-c542rc/c542rc_hardware_netlist.json) | [Markdown](boards/nucleo-c542rc/c542rc_hardware_context.md) |
| NUCLEO-G431RB | MB1367 | STM32G431RBT6 | [JSON](boards/nucleo-g431rb/g431rb_hardware_netlist.json) | [Markdown](boards/nucleo-g431rb/g431rb_hardware_context.md) |

两块开发板均完成了原始网表提取、标准化转换、硬件事实整理、核心上下文生成和文件级关联审核，未发现阻断性连接矛盾。验证结果不等同于对实板所有焊桥、装配选项和外设功能的全面测试。

在 NUCLEO-C542RC 的 GPIO_EXTI 实验中，Codex 读取了 `c542rc_hardware_context.md`，完成了按键外部中断及 LED 控制程序的开发，构建、烧录和实板运行验证通过。这是标准化硬件信息支持 AI 协同开发的一个应用案例。

---

## 运行环境与适用范围

- **开发环境**：VS Code、Codex、PowerShell 和 Python。
- **硬件设计信息提取**：altium-monkey-mcp，用于读取受支持的 Altium 工程数据。
- **功能与配置核对**：开发板原理图、用户手册和 MCU 数据手册；参考手册按需使用。
- **目前验证范围**：NUCLEO-C542RC 与 NUCLEO-G431RB 两个板卡设计案例。

本项目重点解决**硬件信息的提取、整理和供 AI 使用**，不替代开发者对目标设计变体、装配状态及实物硬件的确认。对于其他 STM32 开发板，应按工作流重新提取、检查并验证。

---

## 许可证与第三方资料

本项目代码和文档的使用条件以仓库根目录 `LICENSE` 文件为准（如已提供）。Altium 原始工程、ST 官方原理图、用户手册、芯片手册、BOM 等第三方资料不随本仓库发布，其版权和使用条件由各自权利人规定。

本仓库不包含 `Altium_Designer/`、`references/`、`process/` 中的实际资料或过程文件，只保留目录占位文件。使用者需要自行从合法来源获取对应资料。

---

## 联系方式

- 项目名称：AI4MCU-STM32-Hardware
- GitHub 仓库：[AI4MCU-STM32-Hardware](https://github.com/youcans/AI4MCU-STM32-Hardware)
- 作者：Huang Xiaofeng & Huang Shan
- 邮箱：ai4mcu@qq.com
- GitHub：[@youcans](https://github.com/youcans)
