# AI4MCU-STM32-Hardware 项目工作进展记录

> 文档用途：持续记录 STM32 硬件信息标准化工作流的建立、验证过程、实际结果及待办事项。
>
> 项目目录：`C:\AI4MCU-STM32-Hardware`
>
> 版本：v0.1（C542RC 全流程验证记录）
>
> 当前状态：NUCLEO-C542RC 六步标准化工作流已执行完毕，联合审核已完成。

## 一、项目建立与工作流规划

1. **确定项目目标：**

   将此前在 NUCLEO-G431RB 上验证的硬件信息标准化方法固化为独立、可操作、可复现的工作流，并通过 NUCLEO-C542RC 验证其通用性。

2. **建立独立项目：**

   项目名称为 `AI4MCU-STM32-Hardware`，本地路径为 `C:\AI4MCU-STM32-Hardware`。已建立如下基本目录：

   ```text
   AI4MCU-STM32-Hardware/
   ├── standards/
   ├── tools/
   ├── workflows/
   ├── prompts/
   └── boards/
       ├── nucleo-g431rb/
       └── nucleo-c542rc/
   ```

3. **确定成果分类：**

   统一划分为通用标准、通用工具、操作规范和开发板专属成果。

4. **确定工作流初版：**

   已讨论确定六个步骤：原始硬件资料准备、原始网表提取、标准化参考网表生成、硬件事实整理、核心硬件上下文生成、数据关联与一致性检查。

   主工作流文档为 `workflows/hardware_workflow.md`，已修订至 v0.2，并经项目文件存在性检查确认。

5. **确定文件命名规则：**

   - 基础文件及中间文件采用板卡设计编号前缀，例如 `mb2213_netlist.json`、`mb2213_hardware_facts.md`。
   - 最终标准化文件采用目标 MCU 标识前缀，例如 `c542rc_hardware_context.md`、`c542rc_hardware_netlist.json`。
   - 审查报告按照被审查文件命名；G431 联合审核结果文件约定为 `g431rb_hardware_context_netlist_review.md`。
   - 若原理图设计 MCU 与目标 MCU 不同，需向开发者确认适用关系，不由 AI 自行判定。

## 二、NUCLEO-C542RC 原始资料准备

6. **收集硬件设计资料：**

   已确认以下文件清单：

   | 类型 | 文件 |
   |---|---|
   | Altium 工程 | `MB2213.PrjPcb` |
   | Altium 原理图 | 10 个 `.SchDoc` 文件（本地清单） |
   | PCB 文件 | `MB2213.PcbDoc` |
   | Altium 输出任务 | `MB2213.OutJob` |
   | 原理图 PDF | `NUCLEO-C542RC_Schematic_MB2213-b02.pdf` |
   | 开发板用户手册 | `NUCLEO-C542RC_UserManual_UM3615.pdf` |
   | MCU 参考手册 | `STM32C5-ReferenceManual_RM0522.pdf` |
   | MCU 数据手册 | `STM32C542-DataSheet_DS15135.pdf` |

   说明：本地清单列出 10 个 `.SchDoc`；后续 MCP 的 `project_info` 返回工程原理图数量为 12。这里分别保留原始记录，未擅自将两者视作同一统计口径。

7. **规范开发板目录：**

   已确认完成目录整理，采用如下组织方式：

   ```text
   boards/nucleo-c542rc/
   ├── Altium_Designer/              # Altium 工程和设计文件
   ├── references/                   # PDF 等原始参考资料
   ├── process/                      # 原始网表、中间成果、审核记录
   ├── c542rc_hardware_context.md
   └── c542rc_hardware_netlist.json
   ```

   开发板根目录原则上仅保留两个最终标准化输出文件。

## 三、VS Code 与 MCP 执行环境验证（实际操作记录）

本节记录在 **Windows / VS Code / PowerShell / Codex** 下的实际操作。下列命令注明执行位置；使用绝对路径的命令不依赖终端当前目录。部分 Codex 提示词取自当时提供给开发者的操作指令，开发者确认按提示词执行；尚无逐字完整会话导出，因此不将下列提示词或整理后的结果冒充 MCP 原始调用日志。

### 3.1 打开 VS Code 项目并准备 Codex

**目的：** 建立统一的项目工作入口，能够使用终端和 Codex 对话窗口。

**操作环境：** Windows 桌面，Visual Studio Code 图形界面。

**操作步骤：**

1. 启动 VS Code，选择“文件 → 打开文件夹”，打开 `C:\AI4MCU-STM32-Hardware`。
2. 开发者在 VS Code 中进行了 Python 配置相关操作并切换到 Python 配置；具体菜单选项和选中的解释器路径未在原始记录中提供，不能据此认定已配置项目级 Python 解释器。
3. 安装／启用 Codex 插件，打开 Codex 侧边栏。
4. 选择“终端 → 新建终端”，使用 PowerShell。打开项目后终端默认工作目录为 `C:\AI4MCU-STM32-Hardware`。

**实际结果：** VS Code 项目成功打开；Codex 对话窗口和 PowerShell 终端可用。

**简评：** 工作入口可用；Python 解释器的实际可执行性通过后续独立测试确认，不凭 VS Code 界面状态推断。

### 3.2 检查 Codex MCP 注册

**目的：** 判断此前注册的 MCP 服务在当前 VS Code / Codex 环境中是否仍然生效。

**操作环境：** VS Code Codex 侧边栏。开发者在 Codex 对话中输入下面的命令字符串，由 Codex 执行；这与直接在 PowerShell 终端输入命令不同。

**输入：**

```text
codex mcp list
```

**Codex 报告的输出：**

```text
Name             Status     Auth
altium-monkey    enabled    Unsupported
codex_app        disabled   Unsupported
cua_repl         enabled    Unsupported
node_repl        enabled    Unsupported
```

Codex 还报告一条 PATH 别名访问被拒绝的警告，但 `codex mcp list` 运行成功。

**简评：** 已确认 `altium-monkey` 注册且启用；此时尚未验证实际工程读取。

### 3.3 检查 MCP 配置文件

**目的：** 核对 MCP 服务的实际启动程序，确认沿用此前安装的虚拟环境。

**操作环境：** VS Code PowerShell 终端，默认目录 `C:\AI4MCU-STM32-Hardware`；此命令不依赖当前目录。

**输入命令：**

```powershell
notepad "$HOME\.codex\config.toml"
```

**实际检查到的配置：**

```toml
[mcp_servers.altium-monkey]
command = 'C:\tools\altium-monkey-mcp\.venv\Scripts\altium-monkey-mcp.exe'
```

此前已使用 Git 将 `altium-monkey-mcp` 源码克隆到 `C:\tools\altium-monkey-mcp`。

**简评：** 注册配置指向此前安装位置；无需凭此推断服务运行成功，后续通过工具暴露与实际调用验证。

### 3.4 验证 Codex 暴露的 MCP 工具

**目的：** 检查当前 Codex 会话能否访问所需 MCP 工具。

**操作环境：** VS Code Codex 对话窗口。

**输入提示词（当时给出的检查指令）：**

```text
请检查当前环境是否已连接 altium-monkey-mcp，并确认是否可以调用以下工具：
list_projects、project_info、search_components、get_component、search_nets、export_netlist_json。
只检查工具可用性，不读取工程，也不修改文件。
```

实际注册的服务名为 `altium-monkey`；查询时以当前会话暴露的工具为准。

**Codex 返回结果：** `altium-monkey` 为 enabled，当前会话实际暴露 **13 个工具**：

```text
list_projects
project_info
search_components
get_component
search_nets
export_netlist_json
components_near
get_bom
get_net
pcb_info
pcb_placement
render_pcb
render_schematic
```

**简评：** 13 个工具已暴露；此时仍未调用任何工程读取工具。

### 3.5 检查 uv、Python 及虚拟环境路径

**目的：** 区分 MCP 独立虚拟环境与新建硬件项目目录，确认可用 Python 解释器和启动程序。

**操作环境：** Windows PowerShell 或 VS Code PowerShell 终端；下表保留各命令的实际执行位置及结果。

| 执行位置 | 输入命令 | 实际结果 |
|---|---|---|
| PowerShell／VS Code PowerShell | `uv --version` | `uv 0.13.6 (329bf9448 2026-10-26 x86_64-pc-windows-msvc)` |
| PowerShell，`C:\tools\altium-monkey-mcp` | `Test-Path .\.venv\Scripts\python.exe` | `True` |
| VS Code PowerShell，`C:\AI4MCU-STM32-Hardware` | `Test-Path .\.venv\Scripts\python.exe` | `False` |
| VS Code PowerShell，切换到 `C:\tools\altium-monkey-mcp` | `Test-Path .\.venv\Scripts\python.exe` | `True` |
| VS Code PowerShell，`C:\AI4MCU-STM32-Hardware` | `python --version` | 无输出 |
| 同上 | `py -3.12 --version` | 命令无法识别，报错 |
| 同上 | `uv --version` | `uv 0.13.6 (329bf9448 2026-10-26 x86_64-pc-windows-msvc)` |
| 同上 | `& "C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe" --version` | `Python 3.12.16` |
| 同上 | `Test-Path "C:\tools\altium-monkey-mcp\.venv\Scripts\altium-monkey-mcp.exe"` | `True` |

**关于相对路径的实际测试：**

```powershell
# PowerShell，当前目录 C:\tools\altium-monkey-mcp
Test-Path .\.venv\Scripts\python.exe
# True

# VS Code PowerShell，当前目录 C:\AI4MCU-STM32-Hardware
Test-Path .\.venv\Scripts\python.exe
# False

# VS Code PowerShell 中切换到 MCP 目录
cd C:\tools\altium-monkey-mcp
Test-Path .\.venv\Scripts\python.exe
# True
```

**简评：** MCP 的 `.venv` 位于工具安装目录而非硬件项目目录，`False` 仅反映相对路径所指位置不同；全局 `python` 和 `py` 命令不可作为本次执行的可靠入口。

### 3.6 实测 Python 程序执行

**目的：** 不仅检查 Python 文件存在，还要验证虚拟环境解释器能实际执行代码。

**操作环境：** VS Code PowerShell 终端，当前目录 `C:\AI4MCU-STM32-Hardware`；使用绝对路径调用解释器。

**输入命令：**

```powershell
& "C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe" -c "import sys; print(sys.version); print(sys.executable); print('Python execution OK')"
```

**实际输出：**

```text
3.12.16 (main, Oct 26 2026, 14:10:56) [MSC v.1944 64 bit (AMD64)]
C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe
Python execution OK
```

**简评：** Python 3.12.16（64 位）实际执行通过。该验证针对 MCP 虚拟环境，不等于已在硬件项目根目录创建新的虚拟环境。

## 四、Altium 工程与硬件信息查询（实际操作记录）

本节操作均在 **VS Code 的 Codex 对话窗口**执行，通过已注册的 `altium-monkey` MCP 服务查询；不是在 PowerShell 中直接输入 `list_projects` 等工具名称。查询时工程路径为：

```text
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb
```

### 4.1 工程识别与项目概况查询

**目的：** 验证 MCP 能实际读取 MB2213 工程，获取工程规模和变体情况。

**输入提示词（当时提供的执行指令）：**

```text
请使用已注册的 altium-monkey MCP 服务，实际调用 list_projects 和 project_info，读取以下 Altium 工程：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb

请报告：
1. 工程是否正常读取。
2. 工程名称及完整路径。
3. 原理图数量。
4. 元器件数量。
5. 网络数量。
6. 设计变体（如有）。
7. 执行过程中是否出现错误或警告。

必须以 MCP 工具实际返回的数据为依据，不要根据文件名推测结果。
本次只读取工程，不导出网表，不修改工程文件。
```

**实际调用工具：** `list_projects`、`project_info`。

**Codex 实际输出结果：**

| 项目 | MCP 返回结果 |
|---|---|
| 工程读取 | 正常 |
| 工程名称 | `MB2213` |
| 工程参数 `Board_Name` | `NUCLEO-64 STM32H5/STM32C5 series` |
| 完整路径 | `C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb` |
| 原理图数量 | 12 |
| 元器件数量 | 269 |
| 网络数量 | 182 |
| 设计变体 | `C562RE_S`、`C562RE`、`H533RE`、`H503RB`、`C542RC` |
| 编译诊断 | `compile_diagnostics` 为空 |
| 工具调用 | 两次调用均未返回错误 |

**简评：** 实际工程读取通过；工程为包含 `C542RC` 在内的多变体参考设计。此前本地文件清单列出 10 个 `.SchDoc`，与 `project_info` 的 12 个原理图统计分别保留，不擅自解释差异。

### 4.2 MCU 元器件及引脚连接查询

**目的：** 找到主 MCU、确认设计型号和引脚连接，并识别目标开发板型号与设计型号是否一致。

**输入提示词（当时提供的执行指令）：**

```text
请使用已注册的 altium-monkey MCP 服务，继续分析以下 Altium 工程：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb

已通过 list_projects 和 project_info 确认该工程包含 C542RC 等5个设计变体。本次标准化目标为 NUCLEO-C542RC，必须区分目标变体和其他变体。

请执行以下操作：
1. 调用 search_components，查找工程中的 STM32 主 MCU 及其相关器件。
2. 确认 C542RC 变体对应的 MCU 器件位号、完整型号和封装。
3. 调用 get_component，查询目标 MCU 的引脚信息及其网络连接。
4. 如果 MCP 返回的器件型号是其他变体的设计基准型号，请明确区分原理图器件型号与 C542RC 目标型号，不要自行替换引脚或推断连接。

请报告 MCU 器件位号、设计型号、目标型号、封装、引脚数量及主要网络连接，并说明工具返回的信息是否足以确认 C542RC 变体。
本次只查询元器件及引脚，不导出网表，不修改工程文件。
```

**实际调用工具：** `search_components`、`get_component`。

**Codex 实际输出结果：**

| 项目 | MCP 返回结果 |
|---|---|
| 主 MCU 位号 | `U1` |
| 原理图设计型号 | `STM32C562RET6` |
| `value` / `library_ref` | `IC_STM32C562RET6` |
| 原理图封装参数 | `LQFP64 10x10mm` |
| PCB 封装名 | `ICC_LQFP64_10X10_P050_SOCKET_YAMAICHI_IC149-064-069-B5_NM` |
| U1 引脚数 | 64 |
| 另一个查询到的器件 | `U13` 为 `STLINK-V3EC` |
| MCP 是否确认目标型号 | 否，`search_components` 搜索 `C542` 返回空；`get_component(U1)` 只返回设计型号 |

**U1 主要引脚和网络：**

| U1 引脚 | 引脚名 | 网络 |
|---|---|---|
| 7 | NRST | `NRST` |
| 19、32、48、64 | VDD | `VDD_MCU` |
| 18、31、47、63 | VSS | `GND` |
| 13 | VREF+ | `VREFP` |
| 44、45 | PA11、PA12 | `USB_FS_N`、`USB_FS_P` |
| 46、49、55 | SWDIO、SWCLK、SWO | `DBG.SWDIO`、`DBG.SWCLK`、`DBG.SWO` |
| 60 | PH2-BOOT0 | `PH2_BOOT0` |
| 3～6 | 振荡器相关引脚 | `OSC32_IN`、`OSC32_OUT`、`OSC_IN`、`OSC_OUT` |

**开发者后续确认：** 目标 MCU 为 `STM32C542RCT6`。开发者提供 ST 官方说明，确认 `NUCLEO-C542RC` 和 `NUCLEO-C562RE` 基于同一 MB2213 参考设计。双方约定：**原理图设计 MCU 与目标 MCU 型号不同时，必须先向开发者确认，不由 AI 自行判断。** 本次已确认，可继续后续操作。

**简评：** 已取得 U1 的设计型号、封装和关键引脚连接；MCP 当前查询未按 `C542RC` 变体筛选，不能把 U1 的设计型号误写为目标型号。

### 4.3 关键网络搜索与连接验证

**目的：** 通过网络搜索和端点查询，验证复位、电源、时钟、调试和 USB 等关键连接能否实际检索。

**输入提示词（当时提供的执行指令）：**

```text
请使用 altium-monkey MCP，继续查询以下工程：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb

已确认：
- 目标开发板：NUCLEO-C542RC
- 目标变体：C542RC
- 目标 MCU：STM32C542RCT6
- 原理图设计 MCU：STM32C562RET6（U1）
- 两种型号共用 MB2213 参考设计。

请调用 search_nets，查询与 U1 相关的主要网络，重点检查复位、电源、时钟、SWD 调试和 USB 连接。
报告实际返回的网络名称、相关元器件及引脚，说明是否发现查询异常。
本次只查询网络，不修改工程，不导出网表。
```

**实际调用工具：** `search_nets`、`get_net`（Codex 进一步查询各网络端点）。

**Codex 实际输出结果：**

| 类别 | 网络名 | 端点数 | U1 引脚 | 其他相关元器件引脚 |
|---|---|---:|---|---|
| 复位 | `NRST` | 10 | `U1.7` | `B2.3/.4`、`C1.2`、`CN4.12`、`CN6.3`、`CN7.14`、`R56.2`、`U35.1`、`U4.1` |
| 电源 | `VDD_MCU` | 13 | `U1.19/.32/.48/.64` | `C8.2`、`C9.2`、`C10.2`、`C14.2`、`C15.2`、`JP5.2`、`R17.1`、`R32.1`、`R34.2` |
| 地 | `GND` | 212 | `U1.18/.31/.47/.63` | 另有 208 个端点，未逐一展开 |
| 参考电压 | `AGND` | 3 | `U1.12`（VREF−） | `CN10.32`、`SB31.2` |
| 参考电压 | `VREFP` | 6 | `U1.13`（VREF+） | `C12.1`、`C16.2`、`C17.2`、`R17.2`、`SB13.2` |
| 内部电源相关 | `NetC11_1` | 3 | `U1.30`（VCAP） | `C11.1`、`R33.1` |
| 低速时钟 | `OSC32_IN` | 3 | `U1.3` | `R1.2`、`SB1.1` |
| 低速时钟 | `OSC32_OUT` | 3 | `U1.4` | `R2.2`、`SB2.1` |
| 时钟 | `OSC_IN` | 4 | `U1.5` | `R3.2`、`SB3.2`、`SB5.2` |
| 时钟 | `OSC_OUT` | 3 | `U1.6` | `R4.2`、`SB4.2` |
| 调试 | `DBG.SWDIO` | 5 | `U1.46` | `CN4.4`、`R48.2`、`SB14.2`、`U30.1` |
| 调试 | `DBG.SWCLK` | 6 | `U1.49` | `CN4.6`、`R50.2`、`R7.1`、`SB16.2`、`U31.1` |
| 调试 | `DBG.SWO` | 5 | `U1.55` | `CN4.8`、`R49.2`、`SB20.1`、`U32.1` |
| USB | `USB_FS_N` | 3 | `U1.44`（PA11） | `SB23.2`、`U12.5` |
| USB | `USB_FS_P` | 3 | `U1.45`（PA12） | `SB25.2`、`U12.6` |

**实际检查结论：** 15 个网络均被 `search_nets` 找到；`get_net` 返回端点数与搜索结果一致；没有查询错误或警告。上述数据基于共享原理图，**未按 `C542RC` 变体筛选**。

**简评：** 关键网络和端点查询通过，可继续进行原始网表导出；开发者决定暂缓导出，先梳理工作记录。

### 4.4 原始 JSON 网表导出与检查

**操作环境：** VS Code 的 Codex 对话窗口；已注册的 `altium-monkey` MCP 服务。

**操作目的：** 导出 MB2213 工程完整原始 JSON 网表，并追加保存导出指令及执行结果。

**实际输入给 Codex 的指令：**

```text
请调用 `mcp__altium_monkey__export_netlist_json`，继续分析以下 Altium 工程：
`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb`
请执行以下操作：

1. 导出完整网表 JSON，
2. 保存到 `C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_netlist.json`。
3. 将本次操作指令和执行结果追加保存到 `C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_query.md`，不要覆盖已有内容。
4. 输出任务摘要。
```

**实际工具及参数：**

- 工具：`mcp__altium_monkey__export_netlist_json`
- `project`：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\Altium_Designer\MB2213.PrjPcb`
- `out_path`：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_netlist.json`

**实际输出：**

| 项目 | 结果 |
|---|---|
| MCP 执行 | `isError=false` |
| 导出文件 | `process/mb2213_netlist.json` |
| 文件大小 | 2,752,728 字节 |
| JSON 解析 | 成功 |
| `schema` | `altium_monkey.netlist.b0` |
| `generator` | `altium_monkey` |
| `components` | 269 |
| `nets` | 182 |
| 查询记录 | 已追加到 `process/mb2213_hardware_query.md` |

**异常记录：** 本地初次校验使用 `ConvertFrom-Json -AsHashtable`，当前 PowerShell 不支持该参数；随后改用 `ConvertFrom-Json` 成功解析，不影响导出结果。

**简评：** 原始网表已成功导出，且查询日志保留了指令、实际调用和结果。此次未按 `C542RC` 变体筛选，属于 MB2213 共享设计网表。

## 五、标准化参考网表生成（工作流 2.3）

### 5.1 转换前文件检查

**操作环境：** VS Code 集成 PowerShell 终端。

**操作目的：** 检查规范、转换程序、原始 JSON 网表及有关记录文档是否位于新项目中。

**实际执行命令：**

```powershell
Set-Location "C:\AI4MCU-STM32-Hardware"

$files = [ordered]@{
    "网表规范"     = "standards\hardware_netlist_spec.md"
    "转换程序"     = "tools\generate_hardware_netlist.py"
    "原始JSON网表" = "boards\nucleo-c542rc\process\mb2213_netlist.json"
    "MCP查询记录"  = "boards\nucleo-c542rc\process\mb2213_hardware_query.md"
    "工作流文档"   = "workflows\hardware_workflow.md"
    "工作进展记录" = "workflows\hardware_progress_v0.1.md"
}

$results = foreach ($item in $files.GetEnumerator()) {
    [PSCustomObject]@{
        文件 = $item.Key
        状态 = if (Test-Path -LiteralPath $item.Value -PathType Leaf) {
            "存在"
        } else {
            "缺失"
        }
        相对路径 = $item.Value
    }
}

$results | Format-Table -AutoSize
```

**实际输出：**

```text
文件         状态 相对路径
----         ---- --------
网表规范     存在 standards\hardware_netlist_spec.md
转换程序     存在 tools\generate_hardware_netlist.py
原始JSON网表 存在 boards\nucleo-c542rc\process\mb2213_netlist.json
MCP查询记录  存在 boards\nucleo-c542rc\process\mb2213_hardware_query.md
工作流文档   存在 workflows\hardware_workflow.md
工作进展记录 存在 workflows\hardware_progress_v0.1.md
```

**简评：** 六项文件均存在，可进入转换测试；该检查仅验证文件存在性，不等于审查其全部内容。

### 5.2 执行标准化转换

**操作环境：** VS Code 集成 PowerShell 终端，使用 MCP 项目已有的 Python 3.12.16 虚拟环境解释器。

**操作目的：** 复用 G431 的规范和 Python 转换程序，将 `mb2213_netlist.json` 转换为 C542RC 标准化参考硬件网表，同时生成校验报告。

**实际执行命令：**

```powershell
Set-Location "C:\AI4MCU-STM32-Hardware"

& "C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe" `
    ".\tools\generate_hardware_netlist.py" `
    --input ".\boards\nucleo-c542rc\process\mb2213_netlist.json" `
    --output ".\boards\nucleo-c542rc\c542rc_hardware_netlist.json" `
    --report ".\boards\nucleo-c542rc\process\mb2213_hardware_netlist_validation.md" `
    --board-name "MB2213" `
    --target-mcu "STM32C542RCT6" `
    --design-mcu "STM32C562RET6" `
    --mcu-component "U1"
```

**实际终端输出：**

```json
{
  "components": 269,
  "nets": 182,
  "terminal_records_in_source": 866,
  "endpoints_in_output_nets": 866,
  "target_mcu_connected_pins_indexed": 64,
  "networks_shared_by_multiple_target_mcu_pins": {
    "GND": ["18/VSS", "31/VSS", "47/VSS", "63/VSS"],
    "VDD_MCU": ["19/VDD", "32/VDD", "48/VDD", "64/VDD"]
  },
  "duplicate_endpoints_deduplicated": 0,
  "components_missing_attributes": 6,
  "missing_attribute_field_counts": {"footprint": 6},
  "components_missing_source_page": 0,
  "nets_missing_source_pages": 0,
  "unique_source_pages": [
    "Connectors.SchDoc", "External_Debug_Interface.SchDoc",
    "FDCAN.SchDoc", "LIN.SchDoc", "MCU_IOs.SchDoc",
    "MCU_Power.SchDoc", "Peripherals.SchDoc",
    "Power_Sources.SchDoc", "Project_Overview.SchDoc",
    "STLINK_V3EC.SchDoc", "Top.SchDoc", "USB_User.SchDoc"
  ],
  "warnings": ["missing component attributes stored as null: 6"]
}
```

**生成文件：**

- 最终参考网表：`boards/nucleo-c542rc/c542rc_hardware_netlist.json`
- 转换校验报告：`boards/nucleo-c542rc/process/mb2213_hardware_netlist_validation.md`

**报告中的校验结论（根据开发者提供的内容）：**

- 生成过程未发现结构性错误。
- 非 MCU 网络端点均能对应 `components` 中已有的器件位号。
- 目标 MCU 引脚网络端点均已进入 `mcu_pin_index`。
- 索引中的 `pin`、`net`、`endpoints` 与对应网络数据一致，且网络端点包含 MCU 引脚自身。
- 来源页从原始网表读取，不推断 PDF 页码。

**最终 JSON 的 `metadata`（开发者提供的摘录）：**

```json
{
  "schema_version": "1.1",
  "board_name": "MB2213",
  "source_netlist": "mb2213_netlist.json",
  "target_mcu": "STM32C542RCT6",
  "design_mcu": "STM32C562RET6",
  "mcu_component": "U1",
  "generated_at": "2026-10-31"
}
```

**简评：** 转换命令一次执行成功，得到 269 个元器件、182 个网络、866 个连接端点及 64 条目标 MCU 连网引脚索引。存在 6 个器件缺少 `footprint` 属性的警告，程序将缺失字段记为 `null`，尚未核实具体器件；不应将其说成“完全无警告”。源网表来自共享设计，标准化 JSON 写入的目标 MCU 标识是转换参数，不代表已执行变体专属网表导出。

## 六、硬件事实整理（工作流 2.4）

### 6.1 使用统一的硬件事实规范

**操作环境：** VS Code 的 Codex 对话窗口。

**目的：** 依据标准化参考网表和板级技术资料生成结构统一的硬件事实记录，供核心上下文生成使用。

**输入文件：**

- 规范：`C:\AI4MCU-STM32-Hardware\standards\hardware_facts_spec.md`（v0.1）。
- 参考网表：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_netlist.json`。
- 用户手册：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\references\NUCLEO-C542RC_UserManual_UM3615.pdf`。
- 原理图 PDF：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\references\NUCLEO-C542RC_Schematic_MB2213-b02.pdf`。
- MCU 数据手册：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\references\STM32C542-DataSheet_DS15135.pdf`。

**按最终规范执行的 Codex 指令（可复现用）：**

```text
请按照硬件事实规范：
C:\AI4MCU-STM32-Hardware\standards\hardware_facts_spec.md
整理 NUCLEO-C542RC 的硬件事实。

主要连接依据：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_netlist.json

功能与配置依据：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\references\NUCLEO-C542RC_UserManual_UM3615.pdf
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\references\NUCLEO-C542RC_Schematic_MB2213-b02.pdf
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\references\STM32C542-DataSheet_DS15135.pdf

目标 MCU：STM32C542RCT6，原理图器件 U1。
请按规范整理 MCU 引脚映射表和板载硬件资源表，保留必要配置条件、资料依据及待确认事项；检查两表的 MCU 引脚引用与网表连接。

输出：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_facts.md

将本次指令、结果和简要结论追加到：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_query.md
不要覆盖已有记录。完成后输出任务摘要。
```

**实际最终结果（根据 Codex 执行日志第 6 节）：**

| 检查项 | 结果 |
|---|---|
| 输出 | `process/mb2213_hardware_facts.md`，13,894 字节（规范化记录） |
| 表一 | 40 条引脚记录；`Pin / Net / Board Function / Connection / Condition / Status` |
| 表二 | 14 项资源；`Resource / Function / MCU Pins / Interface / Connection / Status` |
| 表间检查 | 42 次引脚引用，涉及 40 个不同引脚；未匹配引用为 0 |
| 端点检查 | 219 次显式器件端点引用均可在网表找到 |
| 重点连接 | 34 组资源到 MCU、16 组焊桥或下游连接，共 50 组，未发现不一致 |
| 日志 | 已追加到 `mb2213_hardware_query.md` 第 6 节 |

**简评：** 标准化参考网表可以作为整理连接事实的主要输入；功能及焊桥、DNF 等条件仍需以原理图和手册支持。上述统计是 Codex 报告的核对结果，未独立重复计算。本节指令为按最终规范整理的复现提示词；完整历史输入见板卡查询日志。

## 七、核心硬件上下文生成（工作流 2.5）

**操作环境：** VS Code 的 Codex 对话窗口。

**目的：** 直接依据通用模板和已整理的硬件事实生成精简核心上下文，不依赖其他开发板的实例文件。

**输入：**

- 模板：`C:\AI4MCU-STM32-Hardware\standards\hardware_context_template.md`。
- 硬件事实：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_facts.md`。
- 参考网表：`C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_netlist.json`。

**最终采用的 Codex 指令：**

```text
请使用以下核心硬件上下文模板：
C:\AI4MCU-STM32-Hardware\standards\hardware_context_template.md

以 NUCLEO-C542RC 的硬件事实记录为主要内容来源：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_facts.md

以标准化参考硬件网表作为连接核对依据：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_netlist.json

请严格按照模板的章节结构、表格字段和填写规则生成核心硬件上下文，保留软件开发需要的关键引脚、板载资源、配置条件和待确认事项，内容精简，并核对引脚、网络、器件及表间引用。

输出文件：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_context.md

将本次操作指令、执行结果和简要结论追加保存到：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_query.md
不要覆盖已有记录。不调用 Altium MCP，不修改硬件事实记录、参考网表和模板。完成后输出任务摘要。
```

**实际最终结果（根据 Codex 日志第 9 节）：**

| 检查项 | 结果 |
|---|---|
| 输出 | `boards/nucleo-c542rc/c542rc_hardware_context.md` |
| 文件结构 | 元信息、开发约束、两张硬件事实表、参考数据检索、原始资料索引与待确认事项；遵循模板四节 |
| MCU 引脚映射表 | 30 条；30 组 `Pin → Net` 均与事实记录及网表匹配 |
| 板载硬件资源表 | 13 项；31 次引脚引用涉及 29 个不同引脚，均匹配表一 |
| 器件端点 | 73 个直接端点均在对应网络中 |
| 下游连接 | 21 组同网关系通过 |
| 文件链接 | 12 个相对链接均指向存在文件 |
| 日志 | 已追加 `mb2213_hardware_query.md` 第 9 节 |

**简评：** 通用模板、硬件事实记录和参考网表足以生成 C542RC 核心上下文，未再读取 G431 实例作为格式依据。该结果为实际最终版；不讨论生成过程中的版本调整。

## 八、数据关联与一致性检查（工作流 2.6）

**操作环境：** VS Code 的 Codex 对话窗口。

**目的：** 对两个最终文件进行只读联合审核，核查表间引用、网表内部索引及与硬件事实记录的对应关系。

**实际输入的 Codex 指令：**

```text
请对 NUCLEO-C542RC 的两类标准化硬件信息文件进行数据关联与一致性检查。

审核文件：
1. 核心硬件上下文：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_context.md
2. 标准化参考硬件网表：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\c542rc_hardware_netlist.json

辅助核对文件：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_facts.md

请检查两张表的字段和引脚引用、引脚和网络与网表的一致性、网表内部 components/nets/mcu_pin_index 关联，以及重要配置条件和待确认事项是否与硬件事实记录一致。

审核报告保存到：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\c542rc_hardware_context_netlist_review.md

将本次指令、执行结果和简要结论追加到：
C:\AI4MCU-STM32-Hardware\boards\nucleo-c542rc\process\mb2213_hardware_query.md
不要覆盖已有日志，不修改被审核文件。完成后报告检查数量、通过情况和发现事项。
```

**实际输出（根据 Codex 查询日志第 10 节）：**

| 检查项 | 结果 |
|---|---|
| 审核报告 | `process/c542rc_hardware_context_netlist_review.md` |
| 核心表 | 表一 6 列、30 行；表二 7 列、13 行；31 次引脚引用全部匹配 |
| 核心连接 | 30 组引脚—网络、73 个直接端点、65 个资源器件/端点引用、21 组下游连接均通过 |
| 网表内部 | 269 器件、182 网络、64 MCU 引脚索引；866 个端点无重复 |
| 网表端点关联 | 802 个非 MCU 端点可解析到器件；64 条 MCU 索引与网络一致 |
| 事实对照 | 30 行核心引脚映射与事实记录一致；13 项资源状态一致；电源资源按模板省略电源/地引脚 |
| 非阻断事项 | 8 个 U1 端点涉及 5 条网络的 `source_pages` 字段差异；已有 HCF 待确认项继续保留 |
| 日志 | 已追加 `mb2213_hardware_query.md` 第 10 节 |

**简评：** 未发现阻断性连接矛盾。`source_pages` 差异属于需保留的数据溯源问题，不等于已发现连接错误。审查结论基于 Codex 返回的报告摘要，尚未独立复核原始审核报告。

## 九、最终交付文件

### 9.1 通用文件

| 类型 | 相对路径 |
|---|---|
| 参考网表规范 | `standards/hardware_netlist_spec.md` |
| 硬件事实规范 | `standards/hardware_facts_spec.md` |
| 核心上下文模板 | `standards/hardware_context_template.md` |
| Python 转换程序 | `tools/generate_hardware_netlist.py` |
| 主工作流 | `workflows/hardware_workflow.md` |
| 本工作记录 | `workflows/hardware_progress_v0.1.md` |

### 9.2 C542RC 开发板成果

| 用途 | 相对路径 |
|---|---|
| 最终：核心上下文 | `boards/nucleo-c542rc/c542rc_hardware_context.md` |
| 最终：参考网表 | `boards/nucleo-c542rc/c542rc_hardware_netlist.json` |
| 原始网表 | `boards/nucleo-c542rc/process/mb2213_netlist.json` |
| 硬件事实 | `boards/nucleo-c542rc/process/mb2213_hardware_facts.md` |
| MCP/AI 操作记录 | `boards/nucleo-c542rc/process/mb2213_hardware_query.md` |
| 转换校验报告 | `boards/nucleo-c542rc/process/mb2213_hardware_netlist_validation.md` |
| 联合审核报告 | `boards/nucleo-c542rc/process/c542rc_hardware_context_netlist_review.md` |

## 十、工作流进度与验证结论

| 工作流步骤 | 实际完成情况 |
|---|---|
| 2.1 原始硬件资料准备 | 已完成 |
| 2.2 原始网表提取及操作记录 | 已完成 |
| 2.3 参考网表转换及校验 | 已完成；转换程序复用成功 |
| 2.4 规范化硬件事实整理 | 已完成；两张固定字段事实表通过关联核对 |
| 2.5 根据独立模板生成核心上下文 | 已完成；无需依赖 G431 实例文件 |
| 2.6 数据关联与一致性检查 | 已完成；存在非阻断性来源页差异 |

**验证结论：** 在具备 Altium 工程的前提下，已完成 NUCLEO-C542RC 从原始资料到两类标准化硬件信息文件的完整流程。原转换程序无需修改；事实规范和核心上下文模板已实际使用。尚不能将本次结构及连接检查等同于实板装配验证或目标变体全部连接的独立编译验证。

**记录口径：** 本文以最终确认的流程和输出组织内容，省略中途方案变更、重复生成及调试试错。首次查询环节的保存机制由后续补充整理完成；复现时应在各项 Codex 指令中直接要求追加记录。未保留的原始工具参数或完整回显不予补造。
