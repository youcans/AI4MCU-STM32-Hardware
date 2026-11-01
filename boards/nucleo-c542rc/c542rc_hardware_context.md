# C542RC 硬件上下文（NUCLEO-C542RC）

> **用途**：供 AI 辅助 STM32 软件开发默认读取。本文件只收录常用且经过核对的板级硬件事实；未列出的引脚、网络或资源不表示不存在或可以直接使用。
>
> **内容边界**：不收录完整 MCU 引脚表、完整网络与 BOM、完整时钟树、NVIC 或 DMA 分配。完整连接关系按需查询参考硬件网表；网络端点不等同于焊桥、跳线或可选器件的实际装配状态。

| 元信息 | 内容 |
|---|---|
| 板卡 / 硬件设计 | NUCLEO-C542RC / MB2213；目标变体 C542RC |
| 实际开发目标 MCU | **STM32C542RCT6**（U1，LQFP64） |
| 原理图设计基准 MCU | **STM32C562RET6**（U1）；开发者已确认 NUCLEO-C542RC 与 NUCLEO-C562RE 共用 MB2213 参考设计，不据此推定全部外设功能相同 |
| 核心文件 | `c542rc_hardware_context.md` |
| 参考网表 | [`./c542rc_hardware_netlist.json`](./c542rc_hardware_netlist.json)（Schema v1.1） |
| 硬件事实 | [`./process/mb2213_hardware_facts.md`](./process/mb2213_hardware_facts.md) |
| 版本 / 日期 | v0.1 / 2026-10-31 |
| 阅读导航 | 开发约束 → 硬件事实 → 参考数据检索 → 原始资料与待确认事项 |

## 1. 开发约束与缺失处理规则

1. **目标器件：**
   软件外设能力、复用功能（AF）及电气约束以 **STM32C542RCT6** 对应资料为准。开发者已确认目标板与 NUCLEO-C562RE 共用 MB2213 参考设计；不得自行视为 MCU 全功能兼容。标准化网表仍保留 STM32C562RET6 设计值。
2. **事实权威：**
   表一记录 MCU 引脚与网络连接事实；表二记录板载资源及其功能。表二 `MCU Pins` 必须引用表一 `Pin` 的完整键。连接端点以[参考硬件网表](./c542rc_hardware_netlist.json)为依据，功能和配置条件沿用[硬件事实记录](./process/mb2213_hardware_facts.md)中已核实的资料依据。
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
| `1/PE2` | `PE2` | CAN FD 收发器待机控制 | CN7.21; SB32.2 | SB32 手册默认 ON；经 SB32 到 U7.8；1=待机，0=高速模式 | 条件 |
| `2/PC13` | `PC13` | 用户按键输入 | B1.1; B1.2; R13.2; CN7.23 | B1 按下为高；配置输入并软件消抖，不驱动为低 | 已确认 |
| `3/PC14` | `OSC32_IN` | LSE 晶体输入 | R1.2; SB1.1 | 默认 R1/R2 ON、SB1/SB2 OFF，经 R1 到 X2；改作外部时钟/GPIO 需重配 | 条件 |
| `4/PC15` | `OSC32_OUT` | LSE 晶体输出 | R2.2; SB2.1 | 默认 R1/R2 ON、SB1/SB2 OFF，经 R2 到 X2 | 条件 |
| `5/PH0` | `OSC_IN` | HSE 晶体输入 / 可选 STLINK MCO | R3.2; SB3.2; SB5.2 | 默认 R3/R4 ON、SB3/SB4/SB5 OFF，经 R3 到 X3；改用 MCO 或外部时钟须重配 | 条件 |
| `6/PH1` | `OSC_OUT` | HSE 晶体输出 | R4.2; SB4.2 | 默认 R3/R4 ON、SB3/SB4 OFF，经 R4 到 X3 | 条件 |
| `7/NRST` | `NRST` | 低有效复位 | B2.3; B2.4; CN4.12; CN6.3; CN7.14 | — | 已确认 |
| `13/VREF+` | `VREFP` | 模拟参考正端 | R17.2; SB13.2; C16.2; C17.2 | 默认 R17 ON、SB13 OFF，从 VDD_MCU 供参考；外部 AREF 要求 SB13 ON、R17 OFF | 条件 |
| `14/PA0` | `PA0` | Arduino A0 / 模拟扩展 | CN7.28; CN8.1 | — | 已确认 |
| `15/PA1` | `PA1` | Arduino A1 / 模拟扩展 | CN7.30; CN8.2 | — | 已确认 |
| `16/PA2` | `PA2` | USART2 TX / STLINK VCP | CN7.9; SB26.1 | 默认 SB26 ON、SB46 OFF；经 SB26 到 STLINK VCP；与 CN7 共享 | 条件 |
| `17/PA3` | `PA3` | USART2 RX / STLINK VCP | CN7.11; SB12.1 | 默认 SB12 ON；经 SB12 到 STLINK VCP；与 CN7 共享 | 条件 |
| `21/PA5` | `PA5` | 用户 LED / Arduino D13 | CN5.6; CN10.11; SB8.1 | SB8 默认 ON，经 R10、Q1 驱动 LD1；输出高点亮；与 D13 共享 | 条件 |
| `22/PA6` | `PA6` | Arduino D12 / SPI MISO | CN5.5; CN10.13 | — | 已确认 |
| `23/PA7` | `PA7` | Arduino D11 / SPI MOSI | CN5.4; CN10.15 | — | 已确认 |
| `24/PC4` | `PC4` | 用户 USB VBUS 检测 | CN10.34; SB33.2 | SB33 默认 ON，经 SB33 接 VBUS_DETECT；与 CN10.34 共享 | 条件 |
| `28/PB2` | `PB2` | LIN 休眠控制预留 | CN10.22; SB52.1 | SB52、U23 在 C542RC 原理图标 DNF，不作为默认功能 | 条件 |
| `39/PC8` | `PC8` | LIN TX 预留 | SB53.1 | SB53、U23 标 DNF，不作为默认功能 | 条件 |
| `40/PC9` | `PC9` | LIN RX 预留 | SB10.1; SB9.1; SB11.1 | SB10、U23 标 DNF；其他焊桥路径须另核对 | 条件 |
| `44/PA11` | `USB_FS_N` | USB FS D− | U12.5; SB23.2 | 经 U12 到 CN13；SB23 默认 ON 时也共享 CN10.14，扩展走线可能影响性能 | 条件 |
| `45/PA12` | `USB_FS_P` | USB FS D+ | U12.6; SB25.2 | 经 U12 到 CN13；SB25 默认 ON 时也共享 CN10.12 | 条件 |
| `46/PA13 (JTMS/SWDIO)` | `DBG.SWDIO` | SWDIO | CN4.4; R48.2; SB14.2 | SB14 默认 ON，调试信号与 CN7.13 共享 | 条件 |
| `49/PA14 (JTCK/SWCLK)` | `DBG.SWCLK` | SWCLK | CN4.6; R50.2; SB16.2 | SB16 默认 ON，调试信号与 CN7.15 共享 | 条件 |
| `50/PA15 (JTDI)` | `NetR16_2` | JTAG JTDI / 扩展 | R16.2 | 经 R16 到 CN4.10；SB18 默认 ON 时与 CN7.17 共享；启用 JTAG 需软件配置 | 条件 |
| `55/(JTDO/TRACESWO) PB3` | `DBG.SWO` | SWO 跟踪输出 | CN4.8; R49.2; SB20.1 | SB20 默认 ON，调试信号与 CN10.31 共享 | 条件 |
| `58/PB6` | `PB6` | Arduino D15 / I2C、I3C SCL | CN5.10; CN10.3 | — | 已确认 |
| `59/PB7` | `PB7` | Arduino D14 / I2C、I3C SDA | CN5.9; CN10.5 | — | 已确认 |
| `60/PH2` | `PH2_BOOT0` | BOOT0 / 启动键 | CN7.7; SB6.1 | SB6 默认 ON；复位时 B3 未按下=0/用户 Flash，按下=1/系统存储器 | 条件 |
| `61/PB8` | `PB8` | CAN FD RX | SB36.1; SB37.1; SB50.1 | SB36 手册默认 ON，经 SB36 到 U7.4；其他焊桥不可假定同时导通 | 条件 |
| `62/PB9` | `PB9` | CAN FD TX | SB34.2; C13.1; R33.2 | SB34 手册默认 ON，经 SB34 到 U7.1；C13、R33 在目标原理图标 DNF | 条件 |

### 2.2 表二：硬件资源表（资源与功能事实权威）

`Resource` 使用器件位号或大写下划线组合资源名；`MCU Pins` 必须逐项引用表一 `Pin` 完整键，多个键以英文分号 `;` 分隔。无可配置 MCU 引脚的资源填写 `—`。`Condition` 单独记录资源的生效条件。

| Resource | Function | MCU Pins | Interface | Connection | Condition | Status |
|---|---|---|---|---|---|---|
| `B1` | 用户按键输入 | `2/PC13` | GPIO | B1; R13; U3 | PC13 按下高；输入模式、软件消抖，勿输出低 | 已确认 |
| `B2` | MCU 低有效复位 | `7/NRST` | NRST | B2; CN4; CN6; CN7 | — | 已确认 |
| `B3` | 启动模式按键 | `60/PH2` | BOOT | B3; SB6; R12 | SB6 默认 ON；复位时按键决定 BOOT0 电平 | 条件 |
| `LD1` | 绿色用户 LED | `21/PA5` | GPIO | LD1; Q1; R10; SB8; CN5.6 | SB8 默认 ON；PA5 高点亮；与 Arduino D13 共享 | 条件 |
| `X2` | 32.768 kHz LSE 晶体 | `3/PC14; 4/PC15` | LSE | X2; R1; R2; C19; C20 | 默认 R1/R2 ON、SB1/SB2 OFF；启用 RTC/LSE 仍需软件配置 | 条件 |
| `X3` | 24 MHz HSE 晶体 | `5/PH0; 6/PH1` | HSE | X3; R3; R4; C18; C21 | 默认 R3/R4 ON、SB3/SB4/SB5 OFF；STLINK MCO 为另行配置的替代路径 | 条件 |
| `SWD_DEBUG` | 下载、调试及可选 SWO/JTAG | `7/NRST; 46/PA13 (JTMS/SWDIO); 49/PA14 (JTCK/SWCLK); 50/PA15 (JTDI); 55/(JTDO/TRACESWO) PB3` | SWD/SWO/JTAG | STLINK-V3EC; CN4; R48; R50; R16; R49; SB14; SB16; SB18; SB20 | SB14/16/18/20 默认 ON；调试脚与扩展接口共享，JTAG 需另行软件配置 | 条件 |
| `VCP_UART` | STLINK 虚拟串口 | `16/PA2; 17/PA3` | USART2 | STLINK-V3EC; SB26; SB12; R52; R53 | C542RC 使用 PA2/PA3；默认 SB26/SB12 ON、SB46 OFF | 条件 |
| `USB_FS` | 用户 Type-C USB FS Device / VBUS 检测 | `24/PC4; 44/PA11; 45/PA12` | USB | CN13; U12; SB33; SB23; SB25; R21; R22 | SB23/25/33 手册默认 ON；PA11/12 与 CN10 共享；SB51 为 DNF，Host 非默认功能 | 条件 |
| `CAN_FD` | CAN FD 收发接口 | `1/PE2; 61/PB8; 62/PB9` | FDCAN | U7; U11; CN18; SB32; SB36; SB34; JP9; R29 | SB32/36/34 手册默认 ON；JP9 决定 120 Ω 终端；手册位号 U22 与网表/原理图 U7 不一致，见 HCF-002 | 条件 |
| `LIN_RESERVED` | LIN 电路预留，默认不可用 | `28/PB2; 39/PC8; 40/PC9` | LIN | U23; CN11; JP2; SB52; SB53; SB10 | 目标原理图将这些关键器件及焊桥标 DNF；启用前需确认装配和供电 | 条件 |
| `ARDUINO_EXPANSION` | Arduino Uno V3 与 ST morpho 常用扩展引脚 | `14/PA0; 15/PA1; 21/PA5; 22/PA6; 23/PA7; 58/PB6; 59/PB7` | GPIO/ADC/SPI/I2C/I3C | CN5; CN8; CN7; CN10；A0=CN8.1、A1=CN8.2、D11=CN5.4、D12=CN5.5、D13=CN5.6、D14=CN5.9、D15=CN5.10 | PA5 与 LD1 共用；外设复用须核对目标 MCU AF 及其他占用 | 条件 |
| `POWER_SELECT` | 板级 5 V 选择、3V3 生成及 MCU 电流测量 | — | POWER | JP1; U6; JP5; VDD_MCU | JP1 默认 [1–2] 选 5V_STLK，JP5 默认短接；拆 JP5 可测 MCU 电流或经 JP5.2 外供；须遵守手册电压限制 | 条件 |

**关联校验：**
表一 30 条；表二 13 条、31 次 MCU 引脚引用（29 个不同引脚）。表二所有 `MCU Pins` 引用均在表一找到完全一致的 `Pin` 键；表一 30 组引脚—网络和 73 个直接器件端点与参考网表一致，另有 21 组资源下游同网端点核对通过。校验仅覆盖表内设计连接，不证明实板装配状态。

## 3. 参考数据检索指引

### 3.1 参考文件

- [标准化参考硬件网表](./c542rc_hardware_netlist.json)：包含 `metadata`、`components`、`nets`、`mcu_pin_index`，用于按需查询完整连接，不作为每次软件开发的默认输入。
- [硬件事实记录](./process/mb2213_hardware_facts.md)：保存更完整的引脚映射、板载资源、配置条件和资料依据。
- [原始 MCP 网表](./process/mb2213_netlist.json)：保留原始提取结果，需追溯时查询。

### 3.2 查询入口与触发条件

当核心上下文没有覆盖当前任务所需的引脚、网络或资源时，先查硬件事实记录，必要时查询参考硬件网表。

| 查询需求 | 查询入口 | 查询方式 |
|---|---|---|
| MCU 引脚对应网络和全部端点 | `mcu_pin_index` | 以表一完整 `Pin` 键检索 |
| 网络全部端点与来源页 | `nets` | 以原始网络名检索 |
| 器件值、封装及来源页 | `components` | 以器件位号检索 |
| 某个器件各引脚所属网络 | `nets` | 搜索 `endpoints` 中以 `位号.` 开头的端点 |

### 3.3 数据使用注意事项

- `mcu_pin_index` 收录目标主 MCU U1 的已连接引脚；未出现在核心表中不代表引脚空闲。
- `nets.endpoints` 包含 MCU 引脚和其他器件端点；U1 使用完整 `Pin` 键，其余器件使用 `位号.引脚号`，网络名保持源数据原样。
- 网络连接、板级装配状态和目标 MCU 外设复用能力是不同的事实，不可相互替代。
- 参考网表中的 DNF 器件端点、焊桥端点不直接代表实际导通；默认配置按对应资料记录。

## 4. 原始资料索引与关键待确认事项

### 4.1 原始硬件设计文件索引

- Altium 工程：`Altium_Designer/MB2213.PrjPcb`（包含 C542RC 等变体）。
- 原理图及相关设计文件：`Altium_Designer/`。
- 开发板原理图 PDF：[NUCLEO-C542RC_Schematic_MB2213-b02.pdf](./references/NUCLEO-C542RC_Schematic_MB2213-b02.pdf)。
- 开发板用户手册：[NUCLEO-C542RC_UserManual_UM3615.pdf](./references/NUCLEO-C542RC_UserManual_UM3615.pdf)。
- 目标 MCU 数据手册：[STM32C542-DataSheet_DS15135.pdf](./references/STM32C542-DataSheet_DS15135.pdf)。
- MCP 查询记录：[mb2213_hardware_query.md](./process/mb2213_hardware_query.md)；具体资料页码见[硬件事实记录](./process/mb2213_hardware_facts.md)。

### 4.2 关键待确认事项

- **HCF-001：目标变体全网独立验证。**
  参考网表保留 STM32C562RET6 设计值；目标 C542RC 原理图确认 U1 为 STM32C542RCT6，本文关键引脚已核对。若任务依赖未列出的变体专属装配或网络差异，须先核对 C542RC 原理图、BOM 或实板，不把共享网表直接当成变体专属编译结果。
- **HCF-002：CAN 收发器位号差异。**
  UM3615 p.27 写 U22；C542RC 原理图 p.9 及参考网表写 `U7=MCP2562FDT-H/SN`。本文连接按 U7 记录；涉及器件采购、装配或维护时需确认位号差异。
