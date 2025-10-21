import sys
from clang.cindex import Index, CursorKind
from jinja2 import Template
from pathlib import Path

def parse_interface(filename):
    index = Index.create()
    tu = index.parse(filename, args=['-x', 'c++', '-std=c++17'])

    for cursor in tu.cursor.get_children():
        if cursor.kind == CursorKind.CLASS_DECL and cursor.is_abstract_record():
            methods = []
            for m in cursor.get_children():
                if m.kind == CursorKind.CXX_METHOD and m.is_pure_virtual_method():
                    params = [{"name": p.spelling, "type": p.type.spelling} for p in m.get_arguments()]
                    methods.append({
                        "name": m.spelling,
                        "return_type": m.result_type.spelling,
                        "params": params,
                        "default": "0" if m.result_type.spelling != "void" else ""
                    })
            return {
                "iface_name": cursor.spelling,
                "iface_header": Path(filename).name,
                "bridge_name": cursor.spelling[1:] + "Bridge",
                "methods": methods,
            }

def render_template(template_file, context):
    tpl = Template(Path(template_file).read_text())
    return tpl.render(context)

def main():
    if len(sys.argv) != 2:
        print("Usage: bridgegen.py <interface header>")
        return

    hdr = sys.argv[1]
    info = parse_interface(hdr)
    if not info:
        print("No abstract interface found in", hdr)
        return

    Path(info["bridge_name"] + ".h").write_text(render_template("bridge_h.inja", info))
    Path(info["bridge_name"] + ".cpp").write_text(render_template("bridge_cpp.inja", info))
    print(f"Generated {info['bridge_name']}.h/.cpp")

if __name__ == "__main__":
    main()
