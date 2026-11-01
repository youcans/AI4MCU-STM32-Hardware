# STM32 硬件信息标准化工作流

**项目：** AI4MCU-STM32-Hardware  
**文件：** `workflows/hardware_workflow.md`  
**版本：** v0.4.1（双开发板验证后，独立执行与日志机制的小范围修订）

## 1. 目标与适用范围

将具有 **Altium Designer 工程文件**的 STM32 开发板硬件资料，整理为可供 AI 协同软件开发使用的两类标准化结果：

- `<mcu>_hardware_context.md`：精简的核心硬件上下文，供 AI 开发默认读取。
- `<mcu>_hardware_netlist.json`：完整的参考硬件网表，供连接关系按需查询。

工作流共六步，按“准备资料 → MCP 提取 → 网表转换 → 硬件事实整理 → 核心上下文生成 → 联合审核”依次执行。每步确认输入、执行操作、保存输出并记录结果。已安装工具只检查和复用，不重复安装。

本流程已在 NUCLEO-C542RC（MB2213）及 NUCLEO-G431RB（MB1367）完成端到端验证；不同开发板的具体参数、引脚及资源必须以其自身资料为准。

## 2. 前置条件与文件组织

### 2.1 统一执行环境

- **VS Code：** 打开 `AI4MCU-STM32-Hardware` 项目目录。
- **Codex 对话窗口：** 使用已注册的 `altium-monkey` MCP 执行工程查询；使用 Codex 整理硬件事实、生成核心上下文并审核。
- **VS Code 的 PowerShell 终端：** 检查文件、运行 Python 转换程序。
- **Python：** 使用经验证可执行的解释器；不要求当前工程根目录存在 `.venv`。转换程序使用 Python 标准库。

执行命令必须说明所在终端及当前目录。PowerShell 命令先切换到项目根目录，或直接使用绝对路径。Codex 提示词中使用**明确的文件名和绝对路径**，避免依赖对话记忆。

首次执行时，在 VS Code 的 PowerShell 终端检查：

```powershell
Set-Location "C:\AI4MCU-STM32-Hardware"
codex mcp list
Test-Path "C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe"
Test-Path "C:\tools\altium-monkey-mcp\.venv\Scripts\altium-monkey-mcp.exe"
& "C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe" -c "import sys; print(sys.version); print(sys.executable); print('Python execution OK')"
```

以上为 **C542RC 验证时使用的环境路径示例**；其他计算机应替换为实际 MCP 安装路径。另在 Codex 对话窗口检查 `altium-monkey` 的工具是否已暴露。**工具已暴露不等于能够读取工程**，实际工程读取由第 3.2 步验证。若 MCP 注册的设计 MCU 或工具路径存在异常，应先解决问题再继续。

### 2.2 开发板资料与目录

在开始处理前，确认目标开发板型号、目标 MCU 完整型号、板卡设计编号、Altium 工程路径、原理图及技术资料。Altium 工程须包含关联 `.SchDoc` 等文件；PDF 原理图、开发板用户手册、MCU 数据手册作为功能和配置依据，参考手册按需使用。

```text
AI4MCU-STM32-Hardware/
├── standards/
│   ├── hardware_netlist_spec.md
│   ├── hardware_facts_spec.md
│   └── hardware_context_template.md
├── tools/
│   └── generate_hardware_netlist.py
├── workflows/
│   ├── hardware_workflow.md
│   └── hardware_progress.md
├── prompts/
└── boards/
    └── <board-name>/
        ├── Altium_Designer/
        ├── references/
        ├── process/
        ├── <mcu>_hardware_context.md        # 最终生成
        └── <mcu>_hardware_netlist.json       # 最终生成
```

约定：`<board-name>` 为开发板目录名，`<design>` 为板卡设计编号的小写形式（例如 `mb2213`），`<mcu>` 为目标型号简写（例如 `c542rc`）。基础及中间文件使用 `<design>` 前缀；两类最终文件使用 `<mcu>` 前缀；审核文件按被审核对象命名。开发板根目录只保留两类最终结果，其他过程文件放入 `process/`。

## 3. 六步标准处理流程

### 使用前填写一次参数

先核对原始文件名、设计变体及目标 MCU。以下变量应填写为**真实值**，然后在本章各条 Codex 提示词中替换占位符；不可把尖括号形式直接提交给 Codex。`<root>`、`<project>` 等替换后必须是完整绝对路径，扩展资料按实际提供情况填写，不能臆造文件。

| 占位符 | 含义 | 已验证实例（G431RB） |
|---|---|---|
| `<root>` | 项目根目录绝对路径 | `C:\AI4MCU-STM32-Hardware` |
| `<board-name>` | 开发板目录名 | `nucleo-g431rb` |
| `<board>` | 开发板完整型号 | `NUCLEO-G431RB` |
| `<design>` | 设计编号小写 | `mb1367` |
| `<design-id>` | 设计编号原始大小写 | `MB1367` |
| `<mcu>` | 目标型号简写 | `g431rb` |
| `<target-mcu>` | 目标 MCU 完整型号 | `STM32G431RBT6` |
| `<design-mcu>` | 基础设计 MCU 完整型号 | `STM32G474RET6` |
| `<mcu-component>` | 主 MCU 位号 | `U13` |
| `<project>` | `.PrjPcb` 的绝对路径（文件名以实际为准） | `C:\AI4MCU-STM32-Hardware\boards\nucleo-g431rb\Altium_Designer\mb1367.PrjPcb` |
| `<variant>` | 目标设计变体名称 | `G431RB` |
| `<schematic-pdf>` | 原理图 PDF 绝对路径 | 在 `references/` 确认 |
| `<user-manual-pdf>` | 用户手册 PDF 绝对路径 | 在 `references/` 确认 |
| `<datasheet-pdf>` | MCU 数据手册 PDF 绝对路径 | 在 `references/` 确认 |
| `<reference-manual-pdf>` | MCU 参考手册绝对路径（可选） | 在 `references/` 确认；若无文件则删除提示词中对应整行 |

以下路径统一由这些参数构造，复制到 Codex 时应替换为真实**绝对路径**。**提交前检查是否仍存在未替换的 `<...>` 占位符；可选参考手册未提供时，删除提示词中的整行“参考手册（如已提供）<reference-manual-pdf>”，不要把占位符交给 Codex：**

```text
<root>\standards\hardware_netlist_spec.md
<root>\standards\hardware_facts_spec.md
<root>\standards\hardware_context_template.md
<root>\boards\<board-name>\process\<design>_hardware_log.md
<root>\boards\<board-name>\process\<design>_netlist.json
<root>\boards\<board-name>\<mcu>_hardware_netlist.json
<root>\boards\<board-name>\process\<design>_hardware_netlist_validation.md
<root>\boards\<board-name>\process\<design>_hardware_facts.md
<root>\boards\<board-name>\<mcu>_hardware_context.md
<root>\boards\<board-name>\process\<mcu>_hardware_context_netlist_review.md
```

**统一日志规则：** 本轮所有 Codex/MCP 操作均追加到 `process/<design>_hardware_log.md`，每项写明实际指令、工具调用及结果、简要结论；已存在时只追加，绝不覆盖。PowerShell 转换阶段使用第3.3节的脚本自行追加**真实执行命令、输出、退出码和警告**。历史日志改名时检查文件内部链接或引用，不补造历史执行信息。`workflows/hardware_progress.md` 是独立的项目实践记录，不替代开发板日志。

### 3.1 原始硬件资料准备

**输入：** 开发板 Altium 工程、原理图和参考资料。  
**操作：** 在 `Altium_Designer/` 保存完整工程及关联 `.SchDoc` 等文件；在 `references/` 保存原理图 PDF、用户手册、MCU 数据手册（参考手册按需）；确认板卡型号、设计编号、修订号、设计变体与目标 MCU。  
**输出：** 完整资料目录。  
**操作记录：** 本步骤完成后，在 **VS Code PowerShell 终端**运行以下脚本，只修改参数区的真实路径与板卡信息。脚本检查资料文件是否存在，将实际清单与检查结论**追加**到统一日志；不改动原始资料。`$referenceManual` 不提供时填空字符串，其他三份 PDF 须填写实际绝对路径。工程引用的 `.SchDoc` 是否完整仍须结合工程资料或后续 MCP 读取判断，仅检查目录内文件不能证明工程可编译。

```powershell
# 参数区：替换为当前开发板的真实值
$root = "C:\AI4MCU-STM32-Hardware"
$boardName = "nucleo-g431rb"
$board = "NUCLEO-G431RB"
$designId = "MB1367"
$variant = "G431RB"
$targetMcu = "STM32G431RBT6"
$project = "C:\AI4MCU-STM32-Hardware\boards\nucleo-g431rb\Altium_Designer\mb1367.PrjPcb"
$schematic = "C:\AI4MCU-STM32-Hardware\boards\nucleo-g431rb\references\NUCLEO-G431RB_Schematic_MB1367-c05.pdf"
$userManual = "C:\AI4MCU-STM32-Hardware\boards\nucleo-g431rb\references\NUCLEO-G431RB_UserManual_UM2505.pdf"
$datasheet = "C:\AI4MCU-STM32-Hardware\boards\nucleo-g431rb\references\STM32G431-Datasheet_DS12589.pdf"
$referenceManual = "C:\AI4MCU-STM32-Hardware\boards\nucleo-g431rb\references\STM32G4_ReferenceManual_RM0440.pdf"

Set-Location -LiteralPath $root
$base = Join-Path $root "boards\$boardName"
$logFile = Join-Path $base ("process\" + $designId.ToLowerInvariant() + "_hardware_log.md")
$altiumDir = Join-Path $base "Altium_Designer"
$refDir = Join-Path $base "references"
$processDir = Join-Path $base "process"
$checks = @(
    [PSCustomObject]@{ Name = "Altium 工程"; Path = $project; Required = $true },
    [PSCustomObject]@{ Name = "原理图 PDF"; Path = $schematic; Required = $true },
    [PSCustomObject]@{ Name = "用户手册 PDF"; Path = $userManual; Required = $true },
    [PSCustomObject]@{ Name = "MCU 数据手册"; Path = $datasheet; Required = $true }
)
if (-not [string]::IsNullOrWhiteSpace($referenceManual)) {
    $checks += [PSCustomObject]@{ Name = "参考手册"; Path = $referenceManual; Required = $false }
}
$checks = @($checks | ForEach-Object {
    [PSCustomObject]@{ Name = $_.Name; Path = $_.Path; Required = $_.Required;
        Exists = (Test-Path -LiteralPath $_.Path -PathType Leaf) }
})
$schematicFiles = @(Get-ChildItem -LiteralPath $altiumDir -Filter "*.SchDoc" -Recurse -File -ErrorAction SilentlyContinue)
$dirsOk = ((Test-Path -LiteralPath $altiumDir -PathType Container) -and
           (Test-Path -LiteralPath $refDir -PathType Container) -and
           (Test-Path -LiteralPath $processDir -PathType Container))
$ready = ($dirsOk -and $schematicFiles.Count -gt 0 -and
          @($checks | Where-Object { $_.Required -and -not $_.Exists }).Count -eq 0)
$checkText = ($checks | Format-Table Name, Exists, Path -AutoSize | Out-String).TrimEnd()
Write-Host $checkText
Write-Host "SchDoc 数量：$($schematicFiles.Count)；目录齐全：$dirsOk；资料就位：$ready"
$logText = @(
    '', '## 3.1 原始硬件资料准备',
    ('执行时间：' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
    "执行终端：VS Code PowerShell；根目录：$root",
    "开发板：$board；设计编号：$designId；变体：$variant；目标 MCU：$targetMcu",
    "Altium 工程：$project",
    "SchDoc 数量：$($schematicFiles.Count)",
    '', '文件存在性检查：', '```text', $checkText, '```',
    "目录齐全：$dirsOk；必要资料就位：$ready",
    '说明：原理图修订与资料一致性、工程内部引用仍须人工或后续 MCP 核查。'
) -join "`r`n"
Add-Content -LiteralPath $logFile -Value $logText -Encoding UTF8
if (-not $ready) { throw "3.1 资料未就位；已记录检查结果，请补齐后重新检查。" }
```

**完成条件：** 必要文件存在，目标开发板与工程可明确对应；3.1 的实际资料清单与检查结果已追加日志。资料不齐时先补齐，不使用历史生成成果代替原始资料。

### 3.2 原始网表提取

**工具：** VS Code 的 Codex 对话窗口 + `altium-monkey` MCP。  
**输入：** `<project>` 及关联原理图。  
**输出：** `process/<design>_hardware_log.md` 和 `process/<design>_netlist.json`。

以下四条提示词**按顺序分别执行**，每条都要替换完整路径和具体参数。工具调用必须真实发生，不能仅根据以前的日志整理结论。

**3.2（1）工程概况：**

```text
请使用 altium-monkey MCP，对工程 <project> 执行只读概况查询。
调用 list_projects、project_info，确认工程实际可读，记录原理图数量、
器件数量、网络数量、设计变体及编译诊断信息。
将本次实际提示词、MCP 调用参数与结果及简要结论追加到
<root>\boards\<board-name>\process\<design>_hardware_log.md。
不存在则新建，不覆盖已有记录。不修改工程，不导出网表。
完成后输出任务摘要。
```

**3.2（2）主 MCU：**

```text
请使用 altium-monkey MCP 查询工程 <project> 中的主 MCU。
目标开发板 <board>；目标变体 <variant>；候选目标 MCU <target-mcu>。
调用 search_components 和 get_component，记录主 MCU 位号、
基础设计 MCU 型号、封装、引脚及网络连接，并核对变体覆盖信息。
如果基础设计 MCU 与目标 MCU 不同，列出差异并请求开发者确认
目标板实际型号和引脚、供电、外围连接的适用关系；确认前不要自行认定兼容。
对于工具返回的省略信息明确标注。
将本次实际提示词、调用参数与结果及结论追加到
<root>\boards\<board-name>\process\<design>_hardware_log.md。
不覆盖旧记录，不修改工程或导出网表。完成后输出摘要。
```

若设计与目标 MCU 不同，应先取得开发者确认，**将确认内容及其证据边界追加日志**，再进入关键网络查询；此后把实际查得的 `<design-mcu>`、`<mcu-component>` 填回参数表。

**3.2（3）关键网络：**

```text
请使用 altium-monkey MCP 查询工程 <project> 的关键网络。
目标开发板 <board>，目标 MCU <target-mcu>，基础设计 MCU <design-mcu>，
主 MCU 位号 <mcu-component>，目标变体 <variant>。
调用 search_nets 与 get_net，查询复位、供电、时钟、SWD/JTAG
及本板相关接口网络，记录实际查询次数、网络、器件和全部返回端点。
核对主 MCU 引脚—网络映射，明确省略信息、不同网络之间的焊桥关系
及 MCP 结果的变体适用范围；不从网表推定实板装配或焊桥导通。
将本次实际提示词、MCP 调用参数与结果及简要结论追加到
<root>\boards\<board-name>\process\<design>_hardware_log.md。
不覆盖已有日志，不修改工程或导出网表。完成后输出摘要。
```

**3.2（4）原始网表导出：**

```text
请调用 mcp__altium_monkey__export_netlist_json，对工程 <project>
导出完整原始网表 JSON，保存到
<root>\boards\<board-name>\process\<design>_netlist.json。
保持 MCP 原始数据，不手工修改、不标准化、不自行进行变体筛选。
检查文件存在、JSON 可解析，记录器件数、网络数和文件字节数；
明确是否为共享基础设计网表，不将未过滤的网表称为目标变体专属网表。
将本次实际提示词、MCP 调用结果及简要结论追加到
<root>\boards\<board-name>\process\<design>_hardware_log.md。
不覆盖已有日志，不修改 Altium 工程。完成后输出任务摘要。
```

**完成条件：** MCP 实际读取成功；导出原始 JSON 可解析、统计与实际结果一致；设计变体的导出范围已明确；四次任务均有真实操作日志。

### 3.3 标准化参考网表生成

**工具：** VS Code 的 PowerShell 终端 + Python `tools/generate_hardware_netlist.py`。  
**规范：** `standards/hardware_netlist_spec.md`。  
**输入：** `process/<design>_netlist.json`、目标 MCU、设计 MCU、主 MCU 位号。  
**输出：** `<mcu>_hardware_netlist.json` 与 `process/<design>_hardware_netlist_validation.md`，同时追加统一日志。

在 **VS Code PowerShell 终端**执行下面脚本。**仅修改开头的参数赋值，其他部分通用**；路径参数是 PowerShell 字符串，不是 Codex 提示词。示例初始值是已验证的 G431RB 环境，换板时必须全部核对。使用 Windows PowerShell 5.1 可运行的命令。

```powershell
# 参数区：每块板核对并修改真实值
$root = "C:\AI4MCU-STM32-Hardware"
$boardName = "nucleo-g431rb"
$design = "mb1367"
$designId = "MB1367"
$mcu = "g431rb"
$targetMcu = "STM32G431RBT6"
$designMcu = "STM32G474RET6"
$mcuComponent = "U13"
$pythonExe = "C:\tools\altium-monkey-mcp\.venv\Scripts\python.exe"

Set-Location -LiteralPath $root
$spec = Join-Path $root "standards\hardware_netlist_spec.md"
$converter = Join-Path $root "tools\generate_hardware_netlist.py"
$base = Join-Path $root "boards\$boardName"
$inputFile = Join-Path $base "process\${design}_netlist.json"
$outputFile = Join-Path $base "${mcu}_hardware_netlist.json"
$reportFile = Join-Path $base "process\${design}_hardware_netlist_validation.md"
$logFile = Join-Path $base "process\${design}_hardware_log.md"

foreach ($path in @($spec, $converter, $inputFile, $pythonExe)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "必要输入不存在：$path"
    }
}

# 记录已有文件时间戳，防止转换失败时误把历史输出认作本次成果
$previousOutput = Get-Item -LiteralPath $outputFile -ErrorAction SilentlyContinue
$previousReport = Get-Item -LiteralPath $reportFile -ErrorAction SilentlyContinue
$oldOutputTime = if ($null -ne $previousOutput) { $previousOutput.LastWriteTimeUtc } else { $null }
$oldReportTime = if ($null -ne $previousReport) { $previousReport.LastWriteTimeUtc } else { $null }

$argsList = @(
    $converter, '--input', $inputFile, '--output', $outputFile,
    '--report', $reportFile, '--board-name', $designId,
    '--target-mcu', $targetMcu, '--design-mcu', $designMcu,
    '--mcu-component', $mcuComponent
)
$quotedArgs = @($argsList | ForEach-Object { '"' + ($_ -replace '"', '`"') + '"' })
$commandText = '& "' + $pythonExe + '" ' + ($quotedArgs -join ' ')

# 捕获本次标准输出、错误输出和退出码
$oldPreference = $ErrorActionPreference
try {
    $ErrorActionPreference = 'Continue'
    $outputText = (& $pythonExe @argsList 2>&1 | Out-String)
    $exitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $oldPreference
}
Write-Host $outputText
Write-Host "转换程序退出码：$exitCode"

# 仅将本次新写入的文件视为有效输出；旧文件不作为本次依据
$newOutput = Get-Item -LiteralPath $outputFile -ErrorAction SilentlyContinue
$newReport = Get-Item -LiteralPath $reportFile -ErrorAction SilentlyContinue
$outputFresh = ($null -ne $newOutput -and
    ($null -eq $oldOutputTime -or $newOutput.LastWriteTimeUtc -gt $oldOutputTime))
$reportFresh = ($null -ne $newReport -and
    ($null -eq $oldReportTime -or $newReport.LastWriteTimeUtc -gt $oldReportTime))

# 只在本次输出文件已更新且程序退出码为 0 时验证 JSON
$jsonCheck = '未执行（转换失败或输出未更新）'
$jsonOk = $false
if ($exitCode -eq 0 -and $outputFresh) {
    try {
        $verifyCode = "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); keys=('metadata','components','nets','mcu_pin_index'); missing=[k for k in keys if k not in d]; assert not missing, 'Missing keys: '+str(missing); print('JSON parse and required keys OK')"
        $verifyOutput = (& $pythonExe -c $verifyCode $outputFile 2>&1 | Out-String).TrimEnd()
        $verifyExitCode = $LASTEXITCODE
        $jsonOk = ($verifyExitCode -eq 0)
        $jsonCheck = $verifyOutput
    } catch {
        $jsonCheck = $_.Exception.Message
    }
}

# 非阻断性警告如实保留；报告的结构结论须人工复核
$reportText = '本次校验报告不存在或未更新；不引用旧报告。'
if ($exitCode -eq 0 -and $reportFresh) {
    $reportText = Get-Content -LiteralPath $reportFile -Raw -Encoding UTF8
}
$basicOk = ($exitCode -eq 0 -and $outputFresh -and $reportFresh -and $jsonOk)
$conclusion = if ($basicOk) {
    '基本检查通过；仍须阅读本次校验报告，确认无阻断性结构错误并保留全部警告。'
} else {
    '未通过基本检查；请检查退出码、文件是否本次更新以及 JSON 校验结果。'
}

$logLines = @(
    '', '## 3.3 标准化参考网表转换',
    ('执行时间：' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
    '执行终端：VS Code PowerShell',
    '实际执行命令：', '```powershell', $commandText, '```',
    '', '程序实际输出：', '```text', $outputText.TrimEnd(), '```',
    "退出码：$exitCode",
    "本次输出文件已更新：$outputFresh；本次校验报告已更新：$reportFresh",
    "JSON 检查通过：$jsonOk；详细结果：$jsonCheck",
    "输出文件：$outputFile", "校验报告：$reportFile",
    '', '本次校验报告：', '```text', $reportText.TrimEnd(), '```',
    "简要结论：$conclusion"
)
Add-Content -LiteralPath $logFile -Value ($logLines -join "`r`n") -Encoding UTF8
Write-Host $conclusion
if (-not $basicOk) { throw '3.3 基本检查未通过；请查看已追加的日志。' }
```

脚本可自动记录真实命令、终端输出、退出码、转换统计（包含在程序输出中）、异常警告、文件更新状态及 JSON 的基本结构检查；**不把 JSON 解析与字段存在视为完整网表结构验证**。操作人员还须阅读本次校验报告，确认无阻断性结构错误，并把最终“通过/未通过”判断及报告警告追加到同一日志。若程序失败或新报告未生成，脚本不会引用旧报告。若修改通用转换程序，应对既有样例回归验证。

**完成条件：** 程序正常退出，标准化 JSON 可解析且包含 `metadata`、`components`、`nets`、`mcu_pin_index`；本次生成的校验报告已检查并确认无阻断错误；统一日志包含真实命令、输出、退出码、转换统计、警告与最终人工审核结论。

### 3.4 硬件事实整理

**工具：** VS Code 的 Codex 对话窗口。  
**规范：** `standards/hardware_facts_spec.md`。  
**主要连接依据：** `<mcu>_hardware_netlist.json`。  
**功能及配置依据：** 原理图 PDF、用户手册、目标 MCU 数据手册；参考手册按需。  
**输出：** `process/<design>_hardware_facts.md`。

**可复用 Codex 提示词：** 若没有参考手册，**删除下列提示词中“参考手册（如已提供）”这一整行**；不能保留未替换的占位符。

```text
请按照 <root>\standards\hardware_facts_spec.md 整理 <board> 的硬件事实。
目标 MCU <target-mcu>；基础设计 MCU <design-mcu>；
主 MCU 位号 <mcu-component>；目标变体 <variant>；设计编号 <design-id>。
主要连接依据：
<root>\boards\<board-name>\<mcu>_hardware_netlist.json
功能及配置依据：
原理图 <schematic-pdf>
用户手册 <user-manual-pdf>
MCU 数据手册 <datasheet-pdf>
参考手册（如已提供）<reference-manual-pdf>
请严格按规范的章节和字段生成：
表一 Pin | Net | Board Function | Connection | Condition | Status；
表二 Resource | Function | MCU Pins | Interface | Connection | Status。
以网表确定 MCU 引脚、网络及实际端点；以原理图及手册确定功能、
默认配置和装配条件；不得根据网络名推断 MCU 功能或实板装配状态。
核对引脚键唯一性、全部非空 MCU Pins 引用及关键器件/端点；
无法确定的信息列为待确认事项，并说明共享工程/设计变体的验证边界。
保存到：
<root>\boards\<board-name>\process\<design>_hardware_facts.md
将本次实际提示词、执行结果、检查数量及简要结论追加到：
<root>\boards\<board-name>\process\<design>_hardware_log.md
不覆盖旧日志，不修改输入文件，不调用 Altium MCP。
完成后输出引脚数、资源数、引用与连接核对结果、待确认事项。
```

**完成条件：** 两表符合规范；引脚键唯一，非空 `MCU Pins` 均引用表一；关键连接核对通过，无法确定项明确保留。两块板验证表明**事实表行数不必相同**。

### 3.5 核心硬件上下文生成

**工具：** VS Code 的 Codex 对话窗口。  
**格式模板：** `standards/hardware_context_template.md`。  
**主要内容来源：** `process/<design>_hardware_facts.md`。  
**连接核对依据：** `<mcu>_hardware_netlist.json`。  
**输出：** `<mcu>_hardware_context.md`（开发板根目录）。

**可复用 Codex 提示词：**

```text
请依据以下资料生成 <board> 的精简核心硬件上下文。
模板：<root>\standards\hardware_context_template.md
事实记录：<root>\boards\<board-name>\process\<design>_hardware_facts.md
参考网表：<root>\boards\<board-name>\<mcu>_hardware_netlist.json
目标 MCU <target-mcu>；基础设计 MCU <design-mcu>；
主 MCU 位号 <mcu-component>；目标变体 <variant>；设计编号 <design-id>。
严格遵守模板四节结构和元信息。
表一字段：Pin | Net | Board Function | Connection | Condition | Status。
表二字段：Resource | Function | MCU Pins | Interface | Connection | Condition | Status。
仅保留 AI 软件开发常用引脚、资源、配置条件与待确认事项；
不要复制全部事实记录或网表，不读取其他开发板的核心上下文。
用参考网表核对 Pin、Net、端点及表间 MCU Pins；
明确目标 MCU/基础设计 MCU 区别和共享网表范围；
不得把焊桥连接关系当成实板装配证明。
将结果保存到：
<root>\boards\<board-name>\<mcu>_hardware_context.md
将实际提示词、执行结果、检查数量和简要结论追加到：
<root>\boards\<board-name>\process\<design>_hardware_log.md
不覆盖旧日志，不修改事实记录、网表或模板，不调用 Altium MCP。
完成后输出核心引脚数、资源数、表间引用与连接核对结果。
```

**完成条件：** 遵守通用模板，内容精简、关键连接可核对，可用作 AI 开发的默认上下文。

### 3.6 数据关联与一致性检查

**工具：** VS Code 的 Codex 对话窗口。  
**审核对象：** `<mcu>_hardware_context.md` 和 `<mcu>_hardware_netlist.json`。  
**辅助依据：** `process/<design>_hardware_facts.md`。  
**输出：** `process/<mcu>_hardware_context_netlist_review.md`。

**可复用 Codex 提示词：**

```text
请对 <board> 的两类最终硬件文件做只读数据关联与一致性审核。
审核对象：
<root>\boards\<board-name>\<mcu>_hardware_context.md
<root>\boards\<board-name>\<mcu>_hardware_netlist.json
辅助依据：
<root>\boards\<board-name>\process\<design>_hardware_facts.md
目标 MCU <target-mcu>；基础设计 MCU <design-mcu>；
主 MCU 位号 <mcu-component>；目标变体 <variant>。
检查：
1. 核心两表字段、Pin 键唯一性及所有非空 MCU Pins 引用。
2. 核心引脚—网络、器件端点及必要下游同网连接。
3. 参考网表 components、nets、mcu_pin_index 的内部关联完整性。
4. 核心文件与事实记录的状态、配置条件及待确认事项一致性。
区分阻断性连接错误、非阻断性元数据差异和实板/资料待确认事项；
不得把共享基础设计网表视为目标变体专属网表或实板装配证明。
将检查数量、通过项、异常、未解决事项和最终结论写入：
<root>\boards\<board-name>\process\<mcu>_hardware_context_netlist_review.md
将实际提示词、审核结果和简要结论追加到：
<root>\boards\<board-name>\process\<design>_hardware_log.md
不覆盖日志、不修改三份审核依据、不调用 Altium MCP。
若有阻断性错误，明确应返回的处理步骤；完成后输出任务摘要。
```

**完成条件：** 审核报告已生成、关键数据关联通过且无阻断错误；有阻断错误则返回对应步骤修正后重新审核；非阻断性差异要记录影响范围。

## 4. 成果使用与记录要求

**开发时：** 默认提供 `<mcu>_hardware_context.md`；需要未列出的引脚、器件或完整网络时，按需读取 `<mcu>_hardware_netlist.json`，必要时进一步查 `process/<design>_hardware_facts.md` 和原始资料。网表不是目标 MCU 的外设功能或实板装配证明。

**执行时：** 每一步均应明确使用的软件或终端、输入文件、执行命令或 Codex 提示词、输出文件和完成条件。3.1 和 3.3 使用 PowerShell 追加真实执行记录；Codex 执行的每项操作均要求同步追加实际提示词和结果。3.3 的自动基本检查不代替对报告阻断错误的人工确认；不根据缺失历史补造操作或结果。

**文档职责：**

- `workflows/hardware_workflow.md`：说明以后**如何执行**，保留通用规则、可直接复用的提示词模板和转换脚本。
- `workflows/hardware_progress.md`：记录某次完整实践**实际如何执行及其结果**；可随验证过程持续补充。
- `boards/<board-name>/process/<design>_hardware_log.md`：保留该开发板整个六步流程中的资料就位检查、Codex/MCP 提示词及调用结果，以及 PowerShell 转换命令、输出、退出码与核查依据。

## 5. 双开发板验证基线

NUCLEO-C542RC / MB2213 和 NUCLEO-G431RB / MB1367 均完成六步工作流。以下数字为实际执行记录，**不是其他开发板的预设目标**：

| 阶段 | C542RC 验证结果 | G431RB 验证结果 |
|---|---|---|
| 原始网表导出 | 269 个元器件、182 条网络 | 202 个元器件、143 条网络 |
| 标准化参考网表 | 269 个元器件、182 条网络、866 个端点、64 条 MCU 引脚索引；6 个器件缺少封装属性的警告 | 202 个元器件、143 条网络、653 个端点、64 条 MCU 引脚索引；63 项属性缺失警告 |
| 硬件事实记录 | 40 条 MCU 引脚、14 项资源 | 64 条 MCU 引脚、25 项资源 |
| 核心硬件上下文 | 30 条 MCU 引脚、13 项资源 | 31 条 MCU 引脚、18 项资源 |
| 联合审核 | 31 次表间引脚引用通过；无阻断性连接矛盾；来源页元数据差异已记录 | 35 次表间引脚引用通过；无阻断性连接错误；5 项待确认事项保留 |

详细执行记录参见 `workflows/hardware_progress.md` 及两块开发板各自 `process/<design>_hardware_log.md`。C542RC 日志已由开发者更名为 `mb2213_hardware_log.md`。v0.4 新增统一日志命名、PowerShell 自动追加日志和可复制的 Codex 提示词；v0.4.1 修正 3.3 的固定路径与旧报告混用风险，补充 JSON 基本校验、3.1 资料检查日志以及可选参考手册占位符说明。上述新脚本尚待 Windows PowerShell 5.1 实际执行验证，不应混同于已验证的硬件数据处理能力。
