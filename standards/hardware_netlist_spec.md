# 硬件网表规范(hardware_netlist.json)

版本：v1.1
状态：修订规范

本规范定义从 Altium MCP 原始网表转换而来的标准化硬件连接参考文件。

nucleo-g431rb 实例文件命名为 `g431rb_hardware_netlist.json`。


## 1. 用途与边界

- 用途：当精简的 `g431rb_hardware_context.md` 不足以回答连接问题时，按需查询完整器件、网络和 MCU 引脚连接事实。
- 保留：全部元器件、全部网络及其器件引脚端点；必要的器件最小属性和原理图来源页。
- 排除：PCB 布局、图形端点、坐标、符号几何、完整器件参数表，以及与电气连接或追溯无关的元数据。
- 事实权威：`components` 是器件最小属性的权威记录；`nets` 是完整网络—端点关系的权威记录；`mcu_pin_index` 是由 `nets` 派生的唯一反向索引，允许复制端点列表，不单独维护连接事实。
- 本文件记录设计连接，不证明焊桥、跳帽的实物装配状态，也不包含软件的 PLL、NVIC、DMA 等配置。

## 2. 顶层结构

JSON 顶层固定包含四个对象：

- `metadata`：板卡身份、目标 MCU 与原始数据来源。
- `components`：以原始器件位号为键的对象。
- `nets`：以原始网络名称为键的对象。
- `mcu_pin_index`：以目标 MCU 完整引脚值为键的派生索引对象。

示例：

```json
{
  "metadata": {
    "schema_version": "1.1",
    "board_name": "mb1367",
    "source_netlist": "mb1367_netlist.json",
    "target_mcu": "STM32G431RBT6",
    "design_mcu": "STM32G474RET6",
    "mcu_component": "U13",
    "generated_at": "2026-10-30"
  },
  "components": {
    "U13": {
      "type": "IC",
      "value": "STM32G474RET6",
      "footprint": "LQFP64",
      "source_page": "STM32_microcontroller_IOs.SchDoc"
    }
  },
  "nets": {
    "PA5": {
      "endpoints": [
        "19/PA5",
        "CN5.6",
        "CN10.11",
        "SB6.1"
      ],
      "source_pages": [
        "STM32_microcontroller_IOs.SchDoc",
        "Arduino_extension_connectors.SchDoc"
      ]
    }
  },
  "mcu_pin_index": {
    "19/PA5": {
      "pin": "19/PA5",
      "net": "PA5",
      "endpoints": [
        "19/PA5",
        "CN5.6",
        "CN10.11",
        "SB6.1"
      ]
    }
  }
}
```

示例仅说明结构及 PA5 连接方式，不是完整 MB1367 输出。实际生成时，`generated_at` 填写生成日期。

## 3. 字段定义

### 3.1 `metadata`（对象，字段必需）

| 字段 | 类型 | 含义 |
|---|---|---|
| `schema_version` | string | 本规范版本，当前为 `1.1` |
| `board_name` | string | 板卡设计标识，如 `mb1367` |
| `source_netlist` | string | 原始导出网表文件名 |
| `target_mcu` | string | 实际开发目标 MCU 型号 |
| `design_mcu` | string | 原理图所用基准 MCU 型号 |
| `mcu_component` | string | 目标板主 MCU 的器件位号，如 `U13` |
| `generated_at` | string | 实际生成日期，格式为 `YYYY-MM-DD` |

`target_mcu` 与 `design_mcu` 必须分别保留。不能由原理图器件型号推断实际开发目标 MCU；目标型号来自明确的板卡/项目输入。

### 3.2 `components`（对象，键为原始器件位号）

保留原始网表的全部元器件；每条记录固定四个属性：

| 字段 | 类型 | 提取来源 |
|---|---|---|
| `type` | string 或 null | `parameters.Part_Type` |
| `value` | string 或 null | 优先非空的 `parameters.Value`，否则非空的顶层 `value` |
| `footprint` | string 或 null | 顶层 `footprint` |
| `source_page` | string 或 null | `source_page.source_sheet_file` |

规则：

- 器件位号作为对象键，不重复存储 `designator`。
- 原始字段缺失或仅包含空白时保存 `null`，不推测、不使用 `description` 填充。
- 缺失字段由生成程序列入检查报告。

### 3.3 `nets`（对象，键为原始网络名称）

保留原始网表中的全部网络，包括不经过目标 MCU 的网络。每个网络名称作为对象键；对象值只包含以下字段：

| 字段 | 类型 | 含义 |
|---|---|---|
| `endpoints` | string[] | 该网络的全部器件引脚端点，包含 MCU 引脚自身 |
| `source_pages` | string[] | 该网络涉及的原理图文件名 |

不设置重复的 `name` 字段；网络名称以对象键为唯一权威值。不设置 `aliases` 字段。

**端点格式：**

- 目标 MCU（`metadata.mcu_component`）的引脚：`物理编号/规范化引脚名`，如 `19/PA5`、`7/PG10`、`61/PB8`。
- 其他器件（包括其他 MCU）的引脚：`位号.引脚号`，如 `CN7.23`、`SB6.1`、`U5.1`。
- `endpoints` 必须包含该网络的全部实际器件引脚端点，包括目标 MCU 引脚自身。不得只列出 MCU 引脚以外的连接端。
- 同一网络包含多个目标 MCU 引脚时，所有目标 MCU 引脚均以完整规范值出现在同一个端点列表中。
- 端点由原始网表的 `terminals` 生成，不使用图形 `endpoints` 代替；不保留仅代表图形标记或跨页符号的对象。
- 不根据图形对象擅自补接网络。

**去重与排序：**

- 同一网络中完全相同的规范化端点仅保留一次；重复情况必须在检查报告中报告。
- 目标 MCU 引脚端点排在前面，按物理引脚编号升序排列。
- 其他器件端点按器件位号、引脚号自然排序，例如 `CN7.2` 排在 `CN7.10` 之前。
- `source_pages` 使用原始网表明确提供的 `source_sheet_file`，去重并稳定排序；不推断 PDF 页码。
- 来源确实缺失时使用空数组 `[]` 并报告。

**网络对象生成规则：**

- 在生成对象前检查原始网络名称是否重复；重复网络名属于结构性错误，必须报告并停止生成，不得覆盖其中一条记录。
- `nets` 对象键必须与原始网络名称完全一致，不重命名、不修剪内部字符。

### 3.4 `mcu_pin_index`（对象，唯一派生反向索引）

对象键为目标 MCU 的完整 `Pin` 值，例如 `19/PA5`。每条记录固定三个字段：

| 字段 | 类型 | 约束 |
|---|---|---|
| `pin` | string | 必须与对象键完全相同 |
| `net` | string | 必须是 `nets` 中存在的对象键 |
| `endpoints` | string[] | 必须与对应 `nets` 记录的完整端点列表完全相同，包含该 MCU 引脚自身且顺序一致 |

规则：

- 仅索引目标板主 MCU 的有效连接引脚。
- 物理悬空引脚不进入索引。
- 多个目标 MCU 引脚共用一个网络时，每个引脚分别建立记录；各记录的 `endpoints` 均与该网络的完整端点列表一致，因此包含所有共网 MCU 引脚。
- 索引由 `nets` 自动生成，不手工维护。
- 索引按物理引脚编号稳定排序。
- 若某 MCU 引脚仅出现为单独端点、是否构成有效连接不明确，应报告异常，不得仅凭网络名自行判定为有效连接。

## 4. 目标 MCU 引脚名称规范化

- 完整格式固定为 `物理引脚编号/引脚名称`，并与核心文件表一的 `Pin` 完全一致。
- 处理原始引脚名称前，先去除首尾空白字符。
- 对于可明确识别的 GPIO 引脚名称，提取基础 GPIO 名称；基础名称之后由空格、连字符（`-`、`–`、`—`）及其附加功能标注构成的后缀不进入规范化名称。例如：`PG10-NRST` → `PG10`，`PB8-BOOT0` → `PB8`，`PC14 - OSC32_IN` → `PC14`，`PF0 - OSC_IN` → `PF0`。
- GPIO 基础名称统一为大写；提取时忽略基础名称与附加标注之间的空格及分隔符，不得把空格或分隔符带入规范化结果。
- 非 GPIO 专用引脚保留去除首尾空白后的原始名称，例如 `VREF+`；不得对其内部字符进行无依据的删除或替换。
- 只规范化目标 MCU 端点标识；原始网络名称不得修改。原始引脚名称可从未改写的 `source_netlist` 追溯。
- 不能确定物理编号或规范化名称时，生成程序必须报告并阻止该记录进入索引，不得猜测或静默忽略。

## 5. 缺失、冲突与一致性检查

转换程序必须检查：

1. `components` 的器件位号唯一；原始网络名称唯一，不能因对象键覆盖重复网络。
2. 所有原始 `terminals` 均被成功解析为端点；每个非目标 MCU 端点引用的器件位号必须存在于 `components`。
3. 目标 MCU 端点的物理编号和名称可以规范化；同一目标 MCU 引脚不得归属两个不同网络。
4. 目标 MCU 完整引脚值与核心文件表一采用同一规范；表一引用到的已连接引脚应能在索引中找到。
5. `mcu_pin_index` 的对象键等于 `pin`；每个 `net` 在 `nets` 中存在；`endpoints` 与对应网络完全一致，包括 MCU 引脚自身及端点顺序。
6. 每个符合索引条件的目标 MCU 引脚均有索引记录；物理悬空引脚不进入索引。
7. 端点重复、无法解析的端点、缺失器件属性、缺失来源页，以及无法判断连接有效性的单端点网络均在生成检查报告中明确列出。

结构性错误（重复键、连接端无法解析、索引矛盾）应判为生成失败，不得静默丢弃连接事实。非关键属性或来源页缺失可以保留 `null` 或 `[]` 并报告。生成检查报告是运行结果，不增加 JSON 的第五个顶层部分。

## 6. 规范冻结结论

JSON 顶层固定为 `metadata`、`components`、`nets`、`mcu_pin_index` 四部分。`components`、`nets` 和 `mcu_pin_index` 均为对象，分别以器件位号、原始网络名称和目标 MCU 完整引脚值为键。

`nets` 保存完整网络连接事实，`endpoints` 包含网络上的全部器件引脚端点，包括目标 MCU 引脚自身；`mcu_pin_index` 仅用于目标 MCU 引脚的快速查询。实现时依此规范转换和校验，不擅自增加字段或改变端点表示格式。
