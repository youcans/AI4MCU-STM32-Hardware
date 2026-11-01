#!/usr/bin/env python3
"""Convert an altium-monkey-mcp netlist export to hardware_netlist.json."""
import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path


def clean(value):
    if value is None:
        return None
    value = str(value).replace("\u200b", "").replace("\ufeff", "").strip()
    return value or None


def natural_key(value):
    return tuple((0, int(x)) if x.isdigit() else (1, x.casefold())
                 for x in re.split(r"(\d+)", value) if x)


def normalize_pin(number, name):
    number, name = clean(number), clean(name)
    if not number or not name:
        raise ValueError(f"target MCU pin missing number/name: {number!r}/{name!r}")
    match = re.fullmatch(r"(P[A-K]\d{1,2})(?:\s*[-\u2013\u2014]\s*.*)?",
                         name, flags=re.IGNORECASE)
    return f"{number}/{match.group(1).upper() if match else name}"


def endpoint_key(endpoint):
    match = re.fullmatch(r"(\d+)/(.+)", endpoint)
    if match:
        return (0, int(match.group(1)), match.group(2).casefold())
    designator, sep, pin = endpoint.rpartition(".")
    if not sep or not designator or not pin:
        raise ValueError(f"invalid endpoint: {endpoint!r}")
    return (1, natural_key(designator), natural_key(pin))


def source_page(component):
    return clean((component.get("source_page") or {}).get("source_sheet_file"))


def build(source, args):
    errors, warnings = [], []
    missing_attrs, missing_component_sources, missing_net_sources = [], [], []
    duplicate_endpoints = []
    components = {}

    # Components: all source components, keyed by original designator.
    for c in source["components"]:
        d = clean(c.get("designator"))
        if not d:
            errors.append("component with missing designator")
            continue
        if d in components:
            errors.append(f"duplicate component designator: {d}")
            continue
        p = c.get("parameters") or {}
        typ = clean(p.get("Part_Type"))
        value = clean(p.get("Value")) or clean(c.get("value"))
        footprint = clean(c.get("footprint"))
        page = source_page(c)
        components[d] = {
            "type": typ,
            "value": value,
            "footprint": footprint,
            "source_page": page
        }
        for field, val in (("type", typ), ("value", value), ("footprint", footprint)):
            if val is None:
                missing_attrs.append((d, field))
        if page is None:
            missing_component_sources.append(d)

    if args.mcu_component not in components:
        errors.append(f"target MCU component not found: {args.mcu_component}")
    elif components[args.mcu_component]["value"] != args.design_mcu:
        errors.append(
            f"design_mcu mismatch: metadata={args.design_mcu!r}, "
            f"{args.mcu_component}.value={components[args.mcu_component]['value']!r}"
        )

    # Nets: all nets keyed by the unchanged original network name.
    nets, pin_to_net, pin_numbers = {}, {}, {}
    terminal_count = 0
    for n in source["nets"]:
        name = n.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"missing/blank net name: {name!r}")
            continue
        if name in nets:
            errors.append(f"duplicate net name: {name!r}")
            continue
        terminals = n.get("terminals")
        if not isinstance(terminals, list):
            errors.append(f"net {name!r} has no terminals list")
            continue

        eps, seen = [], set()
        for t in terminals:
            terminal_count += 1
            d, pnum = clean(t.get("designator")), clean(t.get("pin"))
            if not d or not pnum:
                errors.append(f"net {name!r}: terminal missing designator/pin")
                continue
            if d not in components:
                errors.append(f"net {name!r}: unknown component endpoint {d}.{pnum}")
                continue
            if d == args.mcu_component:
                try:
                    ep = normalize_pin(pnum, t.get("pin_name"))
                except ValueError as exc:
                    errors.append(f"net {name!r}: {exc}")
                    continue
                old_net = pin_to_net.get(ep)
                if old_net is not None and old_net != name:
                    errors.append(f"MCU pin {ep} assigned to both {old_net!r} and {name!r}")
                    continue
                pin_to_net[ep] = name
                pin_numbers[ep] = int(pnum)
            else:
                ep = f"{d}.{pnum}"

            if ep in seen:
                duplicate_endpoints.append((name, ep))
                continue
            seen.add(ep)
            eps.append(ep)

        if not eps:
            errors.append(f"net {name!r} has no component-pin endpoints")
        try:
            eps.sort(key=endpoint_key)
        except ValueError as exc:
            errors.append(f"net {name!r}: {exc}")

        pages = sorted({
            page_name
            for item in (n.get("source_pages") or [])
            if (page_name := clean((item or {}).get("source_sheet_file"))) is not None
        }, key=natural_key)
        if not pages:
            missing_net_sources.append(name)
        nets[name] = {"endpoints": eps, "source_pages": pages}

    components = dict(sorted(components.items(), key=lambda item: natural_key(item[0])))
    nets = dict(sorted(nets.items(), key=lambda item: natural_key(item[0])))

    # The sole reverse index, derived from nets.
    index = {}
    for pin in sorted(pin_to_net, key=lambda x: (pin_numbers[x], x)):
        net_name = pin_to_net[pin]
        index[pin] = {
            "pin": pin,
            "net": net_name,
            "endpoints": list(nets[net_name]["endpoints"])
        }

    # Validate endpoint references and index equality.
    component_keys = set(components)
    for net_name, net in nets.items():
        for ep in net["endpoints"]:
            if re.fullmatch(r"\d+/.+", ep):
                if ep not in index:
                    errors.append(f"net {net_name!r}: target MCU endpoint not indexed: {ep}")
            else:
                d, sep, pnum = ep.rpartition(".")
                if not sep or d not in component_keys or not pnum:
                    errors.append(f"net {net_name!r}: invalid endpoint reference: {ep}")

    for key, item in index.items():
        if item["pin"] != key:
            errors.append(f"index key/pin mismatch: {key}")
        if item["net"] not in nets:
            errors.append(f"index references unknown net: {key} -> {item['net']}")
        elif item["endpoints"] != nets[item["net"]]["endpoints"]:
            errors.append(f"index endpoints mismatch: {key}")

    # Every connected target MCU terminal must have exactly one index key.
    if set(index) != set(pin_to_net):
        errors.append("target MCU connected-pin set differs from index keys")

    if errors:
        raise ValueError("\n".join(errors))

    if duplicate_endpoints:
        warnings.append(f"duplicate endpoint entries deduplicated: {len(duplicate_endpoints)}")
    if missing_attrs:
        warnings.append(f"missing component attributes stored as null: {len(missing_attrs)}")
    if missing_component_sources:
        warnings.append(f"components missing source_page: {len(missing_component_sources)}")
    if missing_net_sources:
        warnings.append(f"nets missing source_pages: {len(missing_net_sources)}")

    output = {
        "metadata": {
            "schema_version": "1.1",
            "board_name": args.board_name,
            "source_netlist": Path(args.input).name,
            "target_mcu": args.target_mcu,
            "design_mcu": args.design_mcu,
            "mcu_component": args.mcu_component,
            "generated_at": args.generated_at
        },
        "components": components,
        "nets": nets,
        "mcu_pin_index": index
    }

    # Final structural checks.
    endpoint_total = sum(len(n["endpoints"]) for n in nets.values())
    shared_nets = {}
    for pin, item in index.items():
        shared_nets.setdefault(item["net"], []).append(pin)
    shared_nets = {k: v for k, v in shared_nets.items() if len(v) > 1}

    report = {
        "components": len(components),
        "nets": len(nets),
        "terminal_records_in_source": terminal_count,
        "endpoints_in_output_nets": endpoint_total,
        "target_mcu_connected_pins_indexed": len(index),
        "networks_shared_by_multiple_target_mcu_pins": shared_nets,
        "duplicate_endpoints_deduplicated": len(duplicate_endpoints),
        "components_missing_attributes": len(set(d for d, _ in missing_attrs)),
        "missing_attribute_field_counts": dict(collections.Counter(f for _, f in missing_attrs)),
        "components_missing_source_page": len(missing_component_sources),
        "nets_missing_source_pages": len(missing_net_sources),
        "unique_source_pages": sorted({
            p for c in components.values() if (p := c["source_page"]) is not None
        } | {
            p for n in nets.values() for p in n["source_pages"]
        }, key=natural_key),
        "warnings": warnings
    }
    return output, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="mb1367_netlist.json")
    parser.add_argument("--output", default="mb1367_hardware_netlist.json")
    parser.add_argument("--report", default="mb1367_hardware_netlist_validation.md")
    parser.add_argument("--board-name", default="mb1367")
    parser.add_argument("--target-mcu", default="STM32G431RBT6")
    parser.add_argument("--design-mcu", default="STM32G474RET6")
    parser.add_argument("--mcu-component", default="U13")
    parser.add_argument("--generated-at", default=dt.date.today().isoformat())
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    report_path = Path(args.report)
    if not input_path.is_file():
        parser.error(f"input file not found: {input_path}")

    source = json.loads(input_path.read_text(encoding="utf-8"))
    output, report = build(source, args)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    lines = [
        "# mb1367_hardware_netlist.json 生成与校验报告",
        "",
        f"- 规范版本：`{output['metadata']['schema_version']}`",
        f"- 原始文件：`{input_path.name}`",
        f"- 输出文件：`{output_path.name}`",
        f"- 目标 MCU：`{args.target_mcu}`（设计基准：`{args.design_mcu}`，器件：`{args.mcu_component}`）",
        f"- 生成日期：`{args.generated_at}`",
        "",
        "## 数据统计",
        "",
        "| 检查项 | 结果 |",
        "|---|---:|",
        f"| 元器件 | {report['components']} |",
        f"| 网络 | {report['nets']} |",
        f"| 原始 terminals 记录 | {report['terminal_records_in_source']} |",
        f"| 输出网络端点 | {report['endpoints_in_output_nets']} |",
        f"| 目标 MCU 已连接引脚索引 | {report['target_mcu_connected_pins_indexed']} |",
        f"| 重复端点（已去重） | {report['duplicate_endpoints_deduplicated']} |",
        f"| 缺少 source_page 的元器件 | {report['components_missing_source_page']} |",
        f"| 缺少 source_pages 的网络 | {report['nets_missing_source_pages']} |",
        "",
        "## 属性缺失",
        "",
        f"- 存在至少一个最小属性缺失的元器件：{report['components_missing_attributes']} 个",
        f"- 缺失字段计数：`{json.dumps(report['missing_attribute_field_counts'], ensure_ascii=False)}`",
        "- 缺失的 `type`、`value`、`footprint` 按规范保存为 `null`；不使用 description 推断。",
        "",
        "## 多 MCU 引脚共网",
        ""
    ]
    if report["networks_shared_by_multiple_target_mcu_pins"]:
        for net_name, pins in report["networks_shared_by_multiple_target_mcu_pins"].items():
            lines.append(f"- `{net_name}`：{'; '.join(f'`{p}`' for p in pins)}")
    else:
        lines.append("- 无")
    lines += ["", "## 来源页", ""]
    lines += [f"- `{p}`" for p in report["unique_source_pages"]]
    lines += ["", "## 校验结论", "",
              "- 生成过程未发现结构性错误。",
              "- 所有非 MCU 端点均引用 `components` 中存在的器件位号。",
              "- 所有目标 MCU 引脚端点均进入 `mcu_pin_index`。",
              "- 每条索引记录的 `pin` 与对象键一致。",
              "- 每条索引记录的 `net` 均存在于 `nets`。",
              "- 每条索引记录的 `endpoints` 与对应网络完全一致。",
              "- `nets.endpoints` 包含目标 MCU 引脚自身。",
              "- 来源页按原始网表提取；不推断 PDF 页码。",
              "",
              "## 警告", ""]
    lines += [f"- {w}" for w in report["warnings"]] if report["warnings"] else ["- 无"]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\n生成文件：{output_path.resolve()}")
    print(f"校验报告：{report_path.resolve()}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
