# <MCU_SHORT> 硬件上下文（<BOARD_NAME>）

> **用途**：供 AI 辅助 STM32 软件开发默认读取。本文件只收录常用且经过核对的板级硬件事实；未列出的引脚、网络或资源不表示不存在或可以直接使用。
>
> **内容边界**：不收录完整 MCU 引脚表、完整网络与 BOM、完整时钟树、NVIC 或 DMA 分配。完整连接关系按需查询参考硬件网表；网络端点不等同于焊桥、跳线或可选器件的实际装配状态。

| 元信息 | 内容 |
|---|---|
| 板卡 / 硬件设计 | <BOARD_NAME> / <DESIGN_ID>；<TARGET_VARIANT_IF_APPLICABLE> |
| 实际开发目标 MCU | **<TARGET_MCU>**（<MCU_COMPONENT>，<PACKAGE>） |
| 原理图设计基准 MCU | **<DESIGN_MCU>**（<MCU_COMPONENT>）；<IF_DIFFERENT_DEVELOPER_CONFIRMED_RELATION_OR_SAME_AS_TARGET> |
| 核心文件 | `<MCU_SHORT>_hardware_context.md` |
| 参考网表 | [`./<MCU_SHORT>_hardware_netlist.json`](./<MCU_SHORT>_hardware_netlist.json)（Schema v1.1） |
| 硬件事实 | [`./process/<DESIGN_ID_LOWER>_hardware_facts.md`](./process/<DESIGN_ID_LOWER>_hardware_facts.md) |
| 版本 / 日期 | <VERSION> / <YYYY-MM-DD> |
| 阅读导航 | 开发约束 → 硬件事实 → 参考数据检索 → 原始资料与待确认事项 |

## 1. 开发约束与缺失处理规则

1. **目标器件：**
   软件外设能力、复用功能（AF）及电气约束以 **<TARGET_MCU>** 对应资料为准。若原理图设计基准 MCU 与目标 MCU 不同，必须先由开发者确认两者的设计适用关系，不能自行视为兼容。
2. **事实权威：**
   表一记录 MCU 引脚与网络连接事实；表二记录板载资源及其功能。表二 `MCU Pins` 必须引用表一 `Pin` 的完整键。连接端点以参考硬件网表为依据，功能和配置条件结合硬件事实记录、原理图及开发板手册核实。
3. **默认配置：**
   焊桥、跳线和可选器件按对应板卡资料注明的默认配置描述，具体生效条件写入 `Condition`。DNF 或明确未装配的电路不得当作默认可用资源；实际表现与资料不符时再核查实板配置。
4. **按需查证：**
   本文件没有列出某个引脚、网络或资源时，先查询硬件事实记录与参考硬件网表，再根据需要核对原理图、用户手册及目标 MCU 数据手册。未列出不代表空闲；不得依据网络名称臆测外设或 AF 功能。
5. **关键缺失：**
   影响软件任务且尚未确认的关键硬件事实以 `HCF-xxx` 编号，并在第 4.2 节登记；依赖此事实的实现须先确认，不受影响的开发任务可以继续。
6. **状态语义：**
   两表 `Status` 使用 `已确认`、`条件`、`待确认`。`已确认` 为资料支持的连接或功能事实；`条件` 为受已知焊桥、跳线或装配要求限制的功能；`待确认` 为依据不足或存在未解决冲突。状态不代表已完成实物测试。

## 2. 硬件事实

### 2.1 表一：MCU 引脚映射表（引脚事实权威）

`Pin` 使用参考硬件网表 `mcu_pin_index` 中完整的引脚键；`Net` 保留网表的原始网络名；`Connection` 记录主要器件端点；`Condition` 说明使用条件及默认配置。本表只收录软件开发常用的关键引脚，不复制完整引脚索引。

| Pin | Net | Board Function | Connection | Condition | Status |
|---|---|---|---|---|---|
| `<PIN_NUMBER>/<PIN_NAME>` | `<NET_NAME>` | <BOARD_FUNCTION> | <COMPONENT_PIN_ENDPOINTS> | <HARDWARE_CONDITION_OR_—> | <STATUS> |

### 2.2 表二：硬件资源表（资源与功能事实权威）

`Resource` 使用器件位号或大写下划线组合资源名；`MCU Pins` 必须逐项引用表一 `Pin` 完整键，多个键以英文分号 `;` 分隔。无可配置 MCU 引脚的资源填写 `—`。`Condition` 单独记录资源的生效条件。

| Resource | Function | MCU Pins | Interface | Connection | Condition | Status |
|---|---|---|---|---|---|---|
| `<RESOURCE_ID>` | <RESOURCE_FUNCTION> | `<PIN_NUMBER>/<PIN_NAME>` | <INTERFACE> | <COMPONENTS_AND_CONNECTIONS> | <HARDWARE_CONDITION_OR_—> | <STATUS> |

**关联校验：**
表一 <PIN_ROW_COUNT> 条；表二 <RESOURCE_ROW_COUNT> 条、<PIN_REF_COUNT> 次 MCU 引脚引用。表二所有 `MCU Pins` 引用应在表一找到完全一致的 `Pin` 键；表一引脚—网络及关键器件端点须与参考网表一致。<ACTUAL_CHECK_RESULT_AND_LIMITATIONS>。

## 3. 参考数据检索指引

### 3.1 参考文件

- [标准化参考硬件网表](./<MCU_SHORT>_hardware_netlist.json)：包含 `metadata`、`components`、`nets`、`mcu_pin_index`，用于按需查询完整连接，不作为每次软件开发的默认输入。
- [硬件事实记录](./process/<DESIGN_ID_LOWER>_hardware_facts.md)：保存更完整的引脚映射、板载资源、配置条件和资料依据。
- [原始 MCP 网表](./process/<DESIGN_ID_LOWER>_netlist.json)：保留原始提取结果，需追溯时查询。

### 3.2 查询入口与触发条件

当核心上下文没有覆盖当前任务所需的引脚、网络或资源时，先查硬件事实记录，必要时查询参考硬件网表。

| 查询需求 | 查询入口 | 查询方式 |
|---|---|---|
| MCU 引脚对应网络和全部端点 | `mcu_pin_index` | 以表一完整 `Pin` 键检索 |
| 网络全部端点与来源页 | `nets` | 以原始网络名检索 |
| 器件值、封装及来源页 | `components` | 以器件位号检索 |
| 某个器件各引脚所属网络 | `nets` | 搜索 `endpoints` 中以 `位号.` 开头的端点 |

### 3.3 数据使用注意事项

- `mcu_pin_index` 收录目标主 MCU 的已连接引脚；未出现在核心表中不代表引脚空闲。
- `nets.endpoints` 包含目标 MCU 引脚和其他器件端点；具体端点键和网络名应保持源数据原样。
- 网络连接、板级装配状态和 MCU 外设复用能力是不同的事实，不可相互替代。
- 参考网表中的 DNF 器件端点、焊桥端点不直接代表实际导通；默认配置按对应资料记录。

## 4. 原始资料索引与关键待确认事项

### 4.1 原始硬件设计文件索引

- Altium 工程：`Altium_Designer/<PROJECT_FILE>.PrjPcb`。
- 原理图及相关设计文件：`Altium_Designer/`。
- 开发板原理图 PDF：`references/<SCHEMATIC_PDF>`。
- 开发板用户手册：`references/<USER_MANUAL_PDF>`。
- 目标 MCU 数据手册：`references/<MCU_DATASHEET_PDF>`。
- MCP 查询记录：`process/<DESIGN_ID_LOWER>_hardware_query.md`。

### 4.2 关键待确认事项

<IF_NONE_WRITE_当前无待确认的关键硬件事项；如有则按下列格式逐项填写>

- **HCF-001：<QUESTION_TITLE>**
  <WHAT_IS_UNCONFIRMED_AND_WHICH_TASKS_DEPEND_ON_IT>。

---

> **模板使用说明（生成正式文件时删除本段）**
>
> 1. 用对应开发板的硬件事实记录填写内容，并使用参考网表核对引脚、网络和端点；不要复制其他开发板的硬件事实。
> 2. 删除全部 `<...>` 占位符和不适用条目，表格中的示例行必须用真实记录替换；没有 HCF 事项时删除示例 HCF 项。
> 3. 不强制各开发板表格行数一致；保持四节结构及两张表的固定列名。
> 4. 若设计 MCU 与目标 MCU 不一致，先取得开发者确认，再记录对应关系；不得自行推断兼容性。
> 5. 核心文件宜保持精简，优先收录常用软件接口；完整连接、低频资料及详细证据留在事实记录和参考网表中。
