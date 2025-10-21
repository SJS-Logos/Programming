#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# ------------------------------------------------------------
# Step 1 — Parse abstract interface class from C++ header
# ------------------------------------------------------------
import re

def extract_braced_block(text, start_index):
    """
    Returns the substring between matching braces starting at text[start_index],
    handling nested braces correctly.

    Parameters:
        text (str): The full text to scan.
        start_index (int): Index of the opening '{' character.

    Returns:
        (block_text, end_index): 
            block_text is the string between braces (excluding the braces).
            end_index is the index *after* the matching '}'.
    
    Raises:
        ValueError: if braces are unbalanced or start_index is invalid.
    """
    if start_index < 0 or start_index >= len(text) or text[start_index] != '{':
        raise ValueError("start_index must point to an opening brace '{'")

    brace_count = 1
    i = start_index + 1
    while i < len(text) and brace_count > 0:
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
        i += 1

    if brace_count != 0:
        raise ValueError("Unbalanced braces in input text")

    return text[start_index + 1 : i - 1], i


def parse_interface(header_text):
    """
    Finds the first C++ abstract interface class (not enum/struct/union) in header_text
    and returns its name and body text (without braces).
    """
    # Regex to find a non-enum/struct/union class declaration
    class_match = re.search(r'(?<!enum\s)\bclass\s(\w+).*\s*{', header_text)
    if not class_match:
        raise ValueError("No abstract class found")

    class_name = class_match.group(1)
    start_index = class_match.end() - 1  # points to '{'

    class_body, _ = extract_braced_block(header_text, start_index)

    # Match pure virtual methods
    method_pattern = re.compile(
        r'virtual\s+([\w:<>&\s*\[\]]+?)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*=\s*0\s*;',
        re.MULTILINE
    )

    methods = []
    for m in method_pattern.finditer(class_body):
        return_type, name, args, const = m.groups()
        methods.append({
            "return_type": return_type.strip(),
            "name": name.strip(),
            "args": args.strip(),
            "const": bool(const)
        })

    if not methods:
        raise ValueError(f"No abstract class found (no pure virtual methods) looking in {class_body}")

    return class_name, methods


# ------------------------------------------------------------
# Step 2 — Generate bridge header and source files
# ------------------------------------------------------------
TPL_H = """// Auto generated file
#pragma once
#include <memory>

class {class_name};

class {bridge_name} {{
public:
    explicit {bridge_name}(std::unique_ptr<{class_name}>&& impl);

{methods_decl}
private:
    std::unique_ptr<{class_name}> impl_;
}};

// Factory constructor taking the real interface
std::unique_ptr<{bridge_name}> make{bridge_name}(std::unique_ptr<{class_name}>&& impl);
"""

TPL_CPP = """// Auto generated file
#include "{bridge_name}.h"
#include "{class_name}.h"

{bridge_name}::{bridge_name}(std::unique_ptr<{class_name}>&& impl)
    : impl_(std::move(impl)) {{}}

{methods_impl}

std::unique_ptr<{bridge_name}> make{bridge_name}(std::unique_ptr<{class_name}>&& impl) {{
    return std::make_unique<{bridge_name}>(std::move(impl));
}}
"""

# ------------------------------------------------------------
# Step 3 — Render methods
# ------------------------------------------------------------
def generate_method_declarations(methods):
    result = []
    for m in methods:
        const_str = " const" if m["const"] else ""
        result.append(f"    {m['return_type']} {m['name']}({m['args']}){const_str};")
    return "\n".join(result)


def generate_method_implementations(class_name, bridge_name, methods):
    result = []
    for m in methods:
        const_str = " const" if m["const"] else ""
        ret = "" if m["return_type"] == "void" else "return "
        args = m["args"]
        arg_names = ", ".join([a.strip().split()[-1] for a in args.split(",") if a.strip()]) if args else ""
        result.append(
            f"{m['return_type']} {bridge_name}::{m['name']}({args}){const_str} {{\n"
            f"    {ret}impl_->{m['name']}({arg_names});\n"
            f"}}\n"
        )
    return "\n".join(result)


# ------------------------------------------------------------
# Step 4 — Main generation
# ------------------------------------------------------------
def generate_files(header_file):
    with open(header_file, "r", encoding="utf-8") as f:
        header_text = f.read()

    try:
        class_name, methods = parse_interface(header_text)
    except ValueError as e:
        print(f"[BridgeGen] {e}")
        return

    bridge_name = class_name + "Bridge"
    methods_decl = generate_method_declarations(methods)
    methods_impl = generate_method_implementations(class_name, bridge_name, methods)

    h_out = TPL_H.format(
        class_name=class_name,
        bridge_name=bridge_name,
        methods_decl=methods_decl,
    )

    cpp_out = TPL_CPP.format(
        class_name=class_name,
        bridge_name=bridge_name,
        methods_impl=methods_impl,
    )

    header_dir = Path(header_file).parent
    h_path = header_dir / f"{bridge_name}.h"
    cpp_path = header_dir / f"{bridge_name}.cpp"

    with open(h_path, "w", encoding="utf-8") as f:
        f.write(h_out)
    with open(cpp_path, "w", encoding="utf-8") as f:
        f.write(cpp_out)

    print(f"[BridgeGen] Generated {h_path.name} and {cpp_path.name}")


# ------------------------------------------------------------
# Step 5 — Command line entry
# ------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bridgegen.py <interface-header>")
        sys.exit(1)

    generate_files(sys.argv[1])
