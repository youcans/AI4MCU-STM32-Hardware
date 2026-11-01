# AI4MCU-STM32-Hardware

[中文](README.md) | **English**

**An STM32 hardware information extraction workflow based on Codex, altium-monkey-mcp, and Python**

- Project name: AI4MCU-STM32-Hardware
- GitHub repository: [AI4MCU-STM32-Hardware](https://github.com/youcans/AI4MCU-STM32-Hardware)
- Authors: Huang Xiaofeng & Huang Shan
- Email: ai4mcu@qq.com
- GitHub: [@youcans](https://github.com/youcans)

---

## Project Overview

AI4MCU-STM32-Hardware is a hardware information extraction project for AI-assisted STM32 embedded software development. It organizes Altium Designer project parsing, raw netlist export, hardware information standardization, core hardware context generation, and data consistency checks into a reusable workflow.

Using VS Code, Codex, altium-monkey-mcp, and Python, together with development board schematics and technical manuals, developers can convert raw hardware design materials into two types of standardized hardware files that AI can use directly:

- **Core hardware context (`<mcu>_hardware_context.md`)**: Stores commonly used MCU pins, onboard resources, functions, configuration conditions, and items requiring confirmation; **read by default** during AI-assisted programming.
- **Reference hardware netlist (`<mcu>_hardware_netlist.json`)**: Stores components, net connections, and MCU pin indexes; **queried on demand** when AI needs more detailed connection information.

The project follows these principles:

> **Accurate, clear, and concise.**

> **A unified workflow with traceable evidence; validate in practice, then iterate.**

---

## Project Structure

```text
AI4MCU-STM32-Hardware/
├── README.md
├── .gitignore
├── standards/                         # Shared specifications and templates
│   ├── hardware_netlist_spec.md
│   ├── hardware_facts_spec.md
│   └── hardware_context_template.md
├── tools/                             # General-purpose conversion script
│   └── generate_hardware_netlist.py
├── workflows/                         # Workflow guide and practice records
│   ├── hardware_workflow.md
│   └── hardware_progress.md
├── prompts/                           # Reserved directory
└── boards/
    ├── nucleo-c542rc/
    │   ├── Altium_Designer/           # Original design project (not included in the repository)
    │   ├── references/                # Schematics and technical documents (not included)
    │   ├── process/                   # Intermediate data and logs (not included)
    │   ├── c542rc_hardware_context.md
    │   └── c542rc_hardware_netlist.json
    └── nucleo-g431rb/
        ├── Altium_Designer/
        ├── references/
        ├── process/
        ├── g431rb_hardware_context.md
        └── g431rb_hardware_netlist.json
```

Main directories:

- `standards/`: Reference netlist specification, hardware facts specification, and core hardware context template.
- `tools/`: Python script for converting raw MCP JSON netlists into standardized reference netlists.
- `workflows/`: Workflow execution guide and practice records.
- `boards/`: Final hardware information and local source-material directories, organized by development board.
- `prompts/`: Reserved directory for prompts; the reusable Codex prompts are currently included in the workflow document.

The `Altium_Designer/`, `references/`, and `process/` directories are retained with `.gitkeep` files. Their actual contents are excluded by `.gitignore` and are not uploaded to the repository. Users must prepare the original materials themselves; intermediate files are generated locally when the workflow runs.

---

## STM32 Hardware Information Extraction Workflow

### Six-Step Standard Process

| Step | Main task | Output |
|---|---|---|
| 1. Prepare source hardware materials | Organize the Altium project, schematics, and technical manuals | Complete source-material directory |
| 2. Extract the raw netlist | Use Codex with altium-monkey-mcp to query the project and export the netlist | `<design>_netlist.json` |
| 3. Generate a standardized reference netlist | Run the Python converter and check relationships | `<mcu>_hardware_netlist.json`, validation report |
| 4. Organize hardware facts | Use the reference netlist, schematics, and manuals to document MCU pins and resources | `<design>_hardware_facts.md` |
| 5. Generate the core hardware context | Extract commonly used hardware information using a shared template | `<mcu>_hardware_context.md` |
| 6. Check data relationships and consistency | Jointly review the context, reference netlist, and hardware facts | Review report |

In this workflow, `<design>` is the lowercase board design number (for example, `mb1367`), and `<mcu>` is the abbreviated target MCU identifier (for example, `g431rb`). Raw and intermediate files are stored in `process/`; the two final files are placed in the development board's root directory.

For complete instructions, PowerShell commands, reusable Codex prompts, and completion criteria, see:

**[workflows/hardware_workflow.md](workflows/hardware_workflow.md)**

### Data Usage Principles

For AI-assisted programming, read the concise core hardware context first. If it lacks the required details, follow its retrieval instructions to consult the reference netlist or hardware facts record. A netlist describes design connectivity; the presence of net endpoints alone does not establish actual solder-bridge continuity, component assembly, or MCU option-byte settings.

---

## Quick Start

### 1. Get the Project

Clone the repository in Windows PowerShell:

```powershell
git clone https://github.com/youcans/AI4MCU-STM32-Hardware.git C:\AI4MCU-STM32-Hardware
Set-Location "C:\AI4MCU-STM32-Hardware"
```

If you use another project path, update the absolute paths in the workflow commands and Codex prompts accordingly.

### 2. Prepare the Tools

- Install VS Code and configure a working Codex environment.
- Install and register the MCP service required by [altium-monkey-mcp](https://github.com/youcans/AI4MCU-STM32-Hardware); refer to the workflow document and the tool's official instructions for the actual installation source and configuration.
- Prepare a working Python interpreter. `generate_hardware_netlist.py` uses the Python standard library and does not require a `.venv` in this repository.

Check MCP registration in the VS Code PowerShell terminal:

```powershell
Set-Location "C:\AI4MCU-STM32-Hardware"
codex mcp list
```

Confirm that `altium-monkey` is enabled and verify that the corresponding MCP tools are accessible in Codex. **Registration alone does not guarantee that an Altium project can be read successfully**; this must also be verified by an actual project query.

### 3. Prepare Development Board Materials

For NUCLEO-G431RB, place the complete MB1367 Altium project (including `.PrjPcb` and associated `.SchDoc` files) in:

```text
boards/nucleo-g431rb/Altium_Designer/
```

Place the development board schematic PDF, user manual, MCU datasheet, and reference manual when needed in:

```text
boards/nucleo-g431rb/references/
```

For another development board, create a directory with the same structure under `boards/`.

### 4. Run the Workflow

Open this project in VS Code and follow the six steps in **[hardware_workflow.md](workflows/hardware_workflow.md)**. Fill in the target board name, absolute project path, design number, target MCU, base design MCU, and main MCU reference designator as instructed, then use the corresponding Codex prompts and PowerShell commands.

Keep records of actual operations at every stage by appending them to:

```text
boards/<board-name>/process/<design>_hardware_log.md
```

After conversion, check the process exit code, JSON structure, and validation report. After generating the core hardware context, perform the joint review. If a blocking connection issue is found, correct it and repeat the review.

### 5. Use the Generated Hardware Files

After generation and review are complete, configure the corresponding core hardware context as the default hardware reference in your AI-assisted software development project. Query the reference netlist when more specific component, net, or endpoint information is needed.

---

## Validated Development Boards

| Development board | Board design number | Target MCU | Standardized reference netlist | Core hardware context |
|---|---|---|---|---|
| NUCLEO-C542RC | MB2213 | STM32C542RCT6 | [JSON](boards/nucleo-c542rc/c542rc_hardware_netlist.json) | [Markdown](boards/nucleo-c542rc/c542rc_hardware_context.md) |
| NUCLEO-G431RB | MB1367 | STM32G431RBT6 | [JSON](boards/nucleo-g431rb/g431rb_hardware_netlist.json) | [Markdown](boards/nucleo-g431rb/g431rb_hardware_context.md) |

Both boards completed raw netlist extraction, standardized conversion, hardware facts organization, core context generation, and file-level relationship reviews without any blocking connection inconsistencies. These results do not constitute comprehensive testing of all solder bridges, assembly options, or peripheral functions on physical boards.

In the NUCLEO-C542RC GPIO_EXTI experiment, Codex read `c542rc_hardware_context.md` and developed a button external-interrupt and LED control program. The build, firmware flashing, and on-board runtime verification all passed. This is one example of standardized hardware information supporting AI-assisted development.

---

## Environment and Scope

- **Development environment**: VS Code, Codex, PowerShell, and Python.
- **Hardware design information extraction**: altium-monkey-mcp, for reading supported Altium project data.
- **Functional and configuration verification**: Development board schematics, user manuals, and MCU datasheets; reference manuals as needed.
- **Currently validated scope**: Two board design examples, NUCLEO-C542RC and NUCLEO-G431RB.

The project focuses on **extracting and organizing hardware information for AI use**. It does not replace developer confirmation of the target design variant, assembly state, or physical hardware. For other STM32 development boards, follow the workflow to extract, check, and validate the information again.

---

## License and Third-Party Materials

The terms of use for this project's code and documentation are governed by the `LICENSE` file in the repository root (if provided). Third-party materials such as original Altium projects, official ST schematics, user manuals, MCU manuals, and BOMs are not distributed with this repository; their copyrights and terms of use remain with their respective rights holders.

This repository does not include actual materials or intermediate files from `Altium_Designer/`, `references/`, or `process/`; only directory placeholder files are retained. Users must obtain the relevant materials themselves from lawful sources.

---

## Contact

- Project name: AI4MCU-STM32-Hardware
- GitHub repository: [AI4MCU-STM32-Hardware](https://github.com/youcans/AI4MCU-STM32-Hardware)
- Authors: Huang Xiaofeng & Huang Shan
- Email: ai4mcu@qq.com
- GitHub: [@youcans](https://github.com/youcans)
