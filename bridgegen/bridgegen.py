import os
import sys
import re
from textwrap import indent

def load_template(name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "templates", name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_interface(header_text):
    class_match = re.search(r'class\s+(\w+)\s*\{', header_text)
    if not class_match:
        raise ValueError("No class found")

    class_name = class_match.group(1)
    method_pattern = re.compile(
        r'virtual\s+([\w:<>&\s*]+?)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*=\s*0\s*;'
    )

    methods = []
    for match in method_pattern.finditer(header_text):
        ret, name, args, const = match.groups()
        methods.append((ret.strip(), name.strip(), args.strip(), bool(const)))
    return class_name, methods

def format_forward_call(ret, name, args, const):
    if args.strip():
        arg_names = [a.strip().split()[-1] for a in args.split(',') if a.strip()]
        call_args = ", ".join(arg_names)
    else:
        call_args = ""

    if ret == "void":
        return f"if (impl_) impl_->iface->{name}({call_args});"
    else:
        return f"return impl_ ? impl_->iface->{name}({call_args}) : {default_return(ret)};"

def default_return(ret_type):
    if ret_type.endswith("*") or ret_type.startswith("std::"):
        return "{}"
    if ret_type in ("int", "short", "long", "float", "double", "bool"):
        return "0"
    return "{}"

def generate_files(interface_path):
    with open(interface_path, "r", encoding="utf-8") as f:
        content = f.read()

    class_name, methods = parse_interface(content)
    bridge_name = f"{class_name}Bridge"

    tpl_h = load_template("bridge_header.tpl")
    tpl_cpp = load_template("bridge_cpp.tpl")

    header_methods = []
    cpp_methods = []

    for ret, name, args, const in methods:
        const_kw = " const" if const else ""
        header_methods.append(f"    {ret} {name}({args}){const_kw};")

        body = format_forward_call(ret, name, args, const)
        cpp_method = f"{ret} {bridge_name}::{name}({args}){const_kw} {{\n{indent(body, '    ')}\n}}"
        cpp_methods.append(cpp_method)

    h_out = tpl_h.format(
        CLASS=bridge_name,
        METHODS="\n".join(header_methods)
    )

    cpp_out = tpl_cpp.format(
        CLASS=bridge_name,
        INTERFACE=class_name,
        METHODS="\n\n".join(cpp_methods)
    )

    base = os.path.splitext(os.path.basename(interface_path))[0]
    with open(f"{base}Bridge.h", "w", encoding="utf-8") as f:
        f.write(h_out)
    with open(f"{base}Bridge.cpp", "w", encoding="utf-8") as f:
        f.write(cpp_out)

    print(f"✅ Generated {base}Bridge.h and {base}Bridge.cpp")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_bridge.py <interface_header.h>")
        sys.exit(1)
    generate_files(sys.argv[1])
