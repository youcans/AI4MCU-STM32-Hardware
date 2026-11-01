# STM32G431RB 硬件上下文（NUCLEO-G431RB）

> **用途**：供 AI 辅助 STM32 软件开发默认读取。这里只收录常用且已核对的板级事实；未列出的引脚、网络或资源不代表空闲。
>
> **内容边界**：完整引脚、网络和端点按需查询硬件事实记录及参考网表。网表端点不代表焊桥导通、跳帽位置或可选器件实装。

| 元信息 | 内容 |
|---|---|
| 板卡 / 硬件设计 | NUCLEO-G431RB / MB1367；目标设计变体 G431RB |
| 实际开发目标 MCU | **STM32G431RBT6**（U13，LQFP64） |
| 原理图设计基准 MCU | **STM32G474RET6**（U13）；开发者已确认 G431RB 变体中 U13 的引脚、供电及外围连接适用于后续开发，不据此推断两款 MCU 的全部功能兼容 |
| 核心文件 | `g431rb_hardware_context.md` |
| 参考网表 | [`./g431rb_hardware_netlist.json`](./g431rb_hardware_netlist.json)（Schema v1.1；MB1367 共享基础设计，非 G431RB 变体专属网表） |
| 硬件事实 | [`./process/mb1367_hardware_facts.md`](./process/mb1367_hardware_facts.md) |
| 版本 / 日期 | v1.0 / 2026-10-31 |
| 阅读导航 | 开发约束 → 硬件事实 → 参考数据检索 → 原始资料与待确认事项 |

## 1. 开发约束与缺失处理规则

1. **目标器件：** 软件外设、AF 及电气约束以 STM32G431RBT6 资料为准。开发者对 G431RB 变体 U13 连接适用性的确认已记录；共享基础设计网表中的 U13 型号仍为 STM32G474RET6。
2. **事实权威：** 表一给出所选 MCU 引脚与原始网络，表二给出常用资源。表二 `MCU Pins` 引用表一完整 `Pin` 键；同网端点以参考网表为准，板级功能与配置取自[硬件事实记录](./process/mb1367_hardware_facts.md)及其中引用的原理图、手册。
3. **默认配置：** `Condition` 记录资料规定的默认焊桥、跳帽及替代连接。DNF 或未装配支路不视为默认可用；资料中的默认状态不等于实物已测状态。
4. **按需查证：** 本文件未列出时，先查硬件事实记录与参考网表，再按需核对 G431RB 原理图、UM2505 和 STM32G431 数据手册。不得由网络名推断外设 AF，也不得由端点推断焊桥导通。
5. **关键缺失：** 影响实现的未确认事项以 `HCF-xxx` 记在 4.2 节。依赖该事实的实现先确认；其他开发任务可继续。
6. **状态语义：** `已确认` 表示资料支持的连接或功能；`条件` 表示功能受已知配置或装配条件限制；`待确认` 表示资料冲突或缺少必要证据。状态均不代表实板测试结果。

## 2. 硬件事实

### 2.1 表一：MCU 引脚映射表（引脚事实权威）

`Pin` 与 `Net` 沿用参考网表 `mcu_pin_index`；`Connection` 仅列该网的关键同网端点。跨焊桥的去向及默认状态在 `Condition` 说明。

| Pin | Net | Board Function | Connection | Condition | Status |
|---|---|---|---|---|---|
| 1/VBAT | VBAT | 备份域供电 | CN7.33、SB38.2 | SB38 ON 接 VDD；OFF 时可由 CN7.33 外供；实板未测 | 条件 |
| 2/PC13 | PC13 | 默认 B1 USER 输入 | CN7.23、SB16.2 | 默认 SB16 ON、SB21 OFF；B1 可改接 PA0 | 条件 |
| 3/PC14 | NetSB31_2 | LSE 输入 | SB31.2、SB32.2 | 默认 SB31 ON、SB32 OFF，经 X2 32.768 kHz 晶体 | 条件 |
| 4/PC15 | NetSB29_2 | LSE 输出 | SB30.2、SB29.2 | 默认 SB30 ON、SB29 OFF，经 X2 32.768 kHz 晶体 | 条件 |
| 5/PF0 | NetSB26_2 | HSE 输入 | SB26.2、SB27.2、SB28.2 | 默认 SB26 ON、SB27/SB28 OFF，经 X3 24 MHz 晶体；MCO 为替代配置 | 条件 |
| 6/PF1 | NetSB24_2 | HSE 输出 | SB25.2、SB24.2 | 默认 SB25 ON、SB24 OFF，经 X3 24 MHz 晶体 | 条件 |
| 7/PG10 | T_NRST | 目标 MCU 复位 | B2.1、CN4.12、CN6.3 | B2 与调试复位同网 | 已确认 |
| 8/PC0 | PC0 | Arduino A5 候选 | SB36.1 | 默认 SB36 ON 才到 CN8.6；PA15/SB37 为替代路径 | 条件 |
| 9/PC1 | PC1 | Arduino A4 候选 | SB35.1 | 默认 SB35 ON 才到 CN8.5；PB9/SB34 为替代路径 | 条件 |
| 12/PA0 | PA0 | Arduino A0；可选 B1 | CN8.1、CN7.28、SB21.2 | A0 直连；B1 改接需 SB21 ON、SB16 OFF | 条件 |
| 13/PA1 | PA1 | Arduino A1 | CN8.2、CN7.30 | — | 已确认 |
| 14/PA2 | PA2 | 默认 LPUART1_TX / ST-LINK VCP | SB17.2、SB18.1 | 默认 SB17 ON、SB18 OFF；Arduino D1 为替代配置 | 条件 |
| 16/VDD | VDD | MCU 数字供电 | JP6.2、L1.1、SB38.1 | 默认 JP6 ON 接 3V3；JP5 [1-2] 选 ST-LINK USB 5 V 源 | 条件 |
| 17/PA3 | PA3 | 默认 LPUART1_RX / ST-LINK VCP | SB23.2、SB22.1 | 默认 SB23 ON、SB22 OFF；Arduino D0 为替代配置 | 条件 |
| 18/PA4 | PA4 | Arduino A2 | CN8.3、CN7.32 | — | 已确认 |
| 19/PA5 | PA5 | Arduino D13 / SPI1_SCK；可选 LD2 | CN5.6、CN10.11、SB6.1 | D13 直连；LD2 须 SB6 ON，C05 图示闭合 | 条件 |
| 20/PA6 | PA6 | Arduino D12 / SPI1_MISO | CN5.5、CN10.13 | — | 已确认 |
| 21/PA7 | PA7 | Arduino D11 / SPI1_MOSI | CN5.4、CN10.15 | — | 已确认 |
| 22/PC4 | PC4 | 默认 USART1_TX / Arduino D1 | SB13.1、SB12.2 | 默认 SB13 ON、SB12 OFF；VCP 为替代配置 | 条件 |
| 23/PC5 | PC5 | 默认 USART1_RX / Arduino D0 | SB19.1、SB20.2 | 默认 SB19 ON、SB20 OFF；VCP 为替代配置 | 条件 |
| 24/PB0 | PB0 | Arduino A3 | CN8.4、CN7.34 | — | 已确认 |
| 27/VSSA | AGND | MCU 模拟地 | SB11.2、C43.1 | SB11 ON 才接 GND；资料标为保留勿改 | 条件 |
| 28/VREF+ | VREFP | 模拟参考输入 | L2.2、SB10.2、CN10.7 | 默认 JP8 [1-2] 选 VREF；[2-3] 选 VDD | 条件 |
| 29/VDDA | AVDD | MCU 模拟供电 | L1.2、SB8.2、C43.2 | C05 图示 L1 通路、SB8 不装 | 条件 |
| 44/PA10 | PA10 | Arduino D2 | CN9.3、CN10.33 | D2 直连；勿与手册表 17 的 PD2 标签混淆 | 已确认 |
| 49/PA13 | PA13 | SWDIO | CN7.13、SB40.2 | 经 SB40 接 ST-LINK SWD；C05 图示闭合 | 条件 |
| 50/PA14 | PA14 | SWCLK | CN7.15、SB41.2 | 经 SB41 接 ST-LINK SWD；C05 图示闭合 | 条件 |
| 56/PB3 | PB3 | Arduino D3；可选 SWO | CN9.4、CN10.31、SB15.1 | D3 直连；SWO 须 SB15 ON | 条件 |
| 59/PB6 | PB6 | Arduino D10 / SPI 片选位置 | CN5.3、CN10.17 | 外设用途由固件配置 | 已确认 |
| 61/PB8 | PB8 | BOOT0；可选 Arduino D15/SCL | JP7.1、SB2.2、SB4.1 | JP7 默认 OFF；SB2 可接 CN5.10；手册 SB2 标签冲突，见 HCF-001 | 待确认 |
| 62/PB9 | PB9 | Arduino D14/SDA | CN5.9、CN10.5、SB34.2 | D14 直连；A4 替代路径须 SB34 ON，C05 图示不装 | 条件 |

### 2.2 表二：硬件资源表（资源与功能事实权威）

`MCU Pins` 引用表一完整键，多个键用英文分号分隔。跨焊桥路径写在 `Connection`，其生效配置写在 `Condition`。

| Resource | Function | MCU Pins | Interface | Connection | Condition | Status |
|---|---|---|---|---|---|---|
| JP5_U12_JP6 | 目标 MCU 3.3 V 供电 | 16/VDD | Power | JP5 选择 5 V 源；U12 输出经 SB5 到 3V3；JP6.1=3V3、JP6.2=VDD | 默认 JP5 [1-2]、JP6 ON；实板位置未测 | 条件 |
| L1_SB11 | 模拟供电与地 | 27/VSSA; 29/VDDA | Power | VDD 经 L1 到 AVDD；AGND 经 SB11 到 GND | C05 图示 L1 通路、SB8 不装；SB11 保留勿改 | 条件 |
| JP8_U14 | VREF+ 选择 | 28/VREF+ | Power | U13.28=VREFP，JP8 选择 U14 参考源或 VDD | 默认 JP8 [1-2] 选 VREF；[2-3] 选 VDD | 条件 |
| SB38_VBAT | 备份域供电 | 1/VBAT | Power | U13.1=VBAT 连 SB38.2、CN7.33；SB38.1=VDD | SB38 闭合才由 VDD 供电；否则需核对外供 | 条件 |
| X3 | 目标 MCU 默认 HSE 晶体 | 5/PF0; 6/PF1 | Clock | PF0 经 SB26 到 X3.1；PF1 经 SB25 到 X3.3 | 默认 SB25/26 ON；MCO/外部时钟为替代配置 | 条件 |
| X2 | 目标 MCU 默认 LSE 晶体 | 3/PC14; 4/PC15 | Clock | PC14 经 SB31 到 X2.2；PC15 经 SB30 到 X2.1 | 默认 SB30/31 ON | 条件 |
| B2 | 用户复位按键 | 7/PG10 | Reset | B2.1 与 U13.7 同在 T_NRST，亦接 CN4.12 | — | 已确认 |
| B1 | 用户输入按键 | 2/PC13; 12/PA0 | GPIO | B_USER 经 SB16 接 PC13，或经 SB21 接 PA0 | 默认 SB16 ON、SB21 OFF | 条件 |
| STLINK_SWD | ST-LINK 调试与目标复位 | 7/PG10; 49/PA13; 50/PA14 | SWD | PA13–SB40–T_SWDIO/CN4.4；PA14–SB41–T_SWCLK/CN4.6；T_NRST–CN4.12 | SWD 须 SB40/41 导通；C05 图示闭合 | 条件 |
| STLINK_VCP | ST-LINK 虚拟串口 | 14/PA2; 17/PA3 | LPUART1 | PA2–SB17–T_VCP_TX；PA3–SB23–T_VCP_RX | 默认 SB17/23 ON、SB18/22 OFF | 条件 |
| CN9_USART1 | Arduino D1/D0 串口 | 22/PC4; 23/PC5 | USART1 | PC4 经 SB13 到 CN9.2/D1；PC5 经 SB19 到 CN9.1/D0 | 默认 SB13/19 ON、SB12/20 OFF | 条件 |
| CN8_A0_A3 | Arduino 模拟输入位置 | 12/PA0; 13/PA1; 18/PA4; 24/PB0 | ADC / GPIO | PA0/PA1/PA4/PB0 分别直连 CN8.1/2/3/4 | ADC 模式及通道由固件按目标 MCU 配置 | 已确认 |
| CN8_A4_A5 | Arduino 模拟输入复用位置 | 9/PC1; 8/PC0 | ADC / GPIO | PC1 经 SB35 到 CN8.5/A4；PC0 经 SB36 到 CN8.6/A5 | 默认 SB35/36 ON、SB34/37 不装；改变来源须核对实板 | 条件 |
| CN5_SPI | Arduino D13–D10 的 SPI 位置 | 19/PA5; 20/PA6; 21/PA7; 59/PB6 | SPI1 / GPIO | PA5/PA6/PA7/PB6 分别直连 CN5.6/5/4/3 | SPI AF 与片选方式由固件配置 | 已确认 |
| CN5_I2C | Arduino D14/D15 的 I2C 位置 | 62/PB9; 61/PB8 | I2C / GPIO | PB9 直连 CN5.9/D14；PB8 经 SB2 到 CN5.10/D15 | SB2 导通才有 PB8 路径；手册标签冲突见 HCF-001 | 待确认 |
| LD2 | 用户绿色 LED | 19/PA5 | GPIO | PA5–SB6–R29/Q1–LD2 | SB6 ON 才可驱动；C05 图示闭合，PA5 高电平点亮 | 条件 |
| JP7 | BOOT0 跳帽 | 61/PB8 | Boot | JP7.1 与 U13.61 同属 PB8；JP7.2 接下拉支路 | 手册默认 JP7 OFF；实际启动还取决于选项字节，见 HCF-005 | 待确认 |
| CN9_D2_D3 | 常用 Arduino 数字输入输出 | 44/PA10; 56/PB3 | GPIO | PA10 直连 CN9.3/D2；PB3 直连 CN9.4/D3 | PB3 另可经 SB15 接 SWO；Arduino D2 勿误认作 PD2 | 已确认 |

**关联校验：** 表一 31 条；表二 18 条、35 次 MCU 引脚引用。表一键唯一，键与原始网络均在参考网表 `mcu_pin_index` 中匹配；表一所列同网端点均在 `nets[Net].endpoints` 中。表二所有 `MCU Pins` 引用均能在表一找到，无法匹配 0 项。跨焊桥的连接与默认状态依据硬件事实记录，不以端点存在推定实板导通。

## 3. 参考数据检索指引

### 3.1 参考文件

- [标准化参考硬件网表](./g431rb_hardware_netlist.json)：含 `metadata`、`components`、`nets`、`mcu_pin_index`，供按需查完整连接；来自 MB1367 共享基础设计。
- [硬件事实记录](./process/mb1367_hardware_facts.md)：含全部 64 个 U13 引脚键、更多板载资源、配置条件及资料差异。
- [原始 MCP 网表](./process/mb1367_netlist.json)：保留原始提取结果，需追溯时查询。

### 3.2 查询入口与触发条件

当前任务涉及未收录引脚、网络或资源时，先查硬件事实记录，必要时查参考网表。

| 查询需求 | 查询入口 | 查询方式 |
|---|---|---|
| MCU 引脚对应网络和全部端点 | `mcu_pin_index` | 以完整 `Pin` 键检索 |
| 网络全部端点与来源页 | `nets` | 以原始网络名检索 |
| 器件值、封装及来源页 | `components` | 以器件位号检索 |
| 器件各引脚所属网络 | `nets` | 查找 `endpoints` 中以 `位号.` 开头的端点 |

### 3.3 数据使用注意事项

- 未列入核心表的引脚仍可能有连接；完整索引见 `mcu_pin_index`。
- `nets.endpoints` 记录同网端点；焊桥两侧可能属于不同网络。
- 网络连接、实板装配状态和目标 MCU 外设 AF 能力须分别查证；DNF 端点不代表可用连接。

## 4. 原始资料索引与关键待确认事项

### 4.1 原始硬件设计文件索引

- Altium 工程：`Altium_Designer/mb1367.PrjPcb`；原理图及相关设计文件在 `Altium_Designer/`。
- 开发板原理图：[NUCLEO-G431RB_Schematic_MB1367-c05.pdf](./references/NUCLEO-G431RB_Schematic_MB1367-c05.pdf)。
- 用户手册：[NUCLEO-G431RB_UserManual_UM2505.pdf](./references/NUCLEO-G431RB_UserManual_UM2505.pdf)。
- 目标 MCU 数据手册：[STM32G431-Datasheet_DS12589.pdf](./references/STM32G431-Datasheet_DS12589.pdf)。
- MCP 查询与开发者确认记录：[mb1367_hardware_log.md](./process/mb1367_hardware_log.md)。

### 4.2 关键待确认事项

- **HCF-001：SB2 的 Arduino D14/D15 标签冲突。** UM2505 Rev 7 表 12 将 PB8 经 SB2 写作 D14；同手册表 15、C05 原理图和网表端点指向 CN5.10/D15/SCL。若软件使用该 I2C 引出，先核对接口标号及实板 SB2 状态。
- **HCF-002：HSE 替代模式的 PF0/PF1 后缀冲突。** UM2505 表 12 对 SB24/SB28 的 OSC_IN/OUT 文字与数据手册、C05 原理图不一致；默认 X3 路径按图纸记录。改用外部时钟、MCO 或 GPIO 前核对目标配置。
- **HCF-003：PD2 的 D2 标签冲突。** UM2505 表 17 对 PD2 写 D2，而 Arduino D2 在表 15、网表为 PA10–CN9.3。使用 Arduino D2 时按 PA10；若需 PD2，另查硬件事实记录。
- **HCF-004：实板装配与修订状态未核实。** 开发者确认了 G431RB 变体 U13 连接适用性，但本次未测焊桥、跳帽、晶体及可选器件，也未核实实板修订号。依赖替代串口、MCO、A4/A5 改接或分离供电的任务须先核对实板。
- **HCF-005：BOOT0 选项字节未读取。** JP7 默认 OFF 来自手册；实际启动行为还受 `nSWBOOT0`、`nBOOT0` 设置影响。涉及启动模式或下载恢复时须读取目标配置。
