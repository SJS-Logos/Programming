#include "{CLASS}.h"
#include "{INTERFACE}.h"

struct {CLASS}::Impl {{
    std::unique_ptr<{INTERFACE}> iface;
    Impl(std::unique_ptr<{INTERFACE}> i) : iface(std::move(i)) {{ }}
}};

{CLASS}::{CLASS}() : impl_(nullptr) {{ }}
{CLASS}::~{CLASS}() = default;
{CLASS}::{CLASS}({CLASS}&&) noexcept = default;
{CLASS}& {CLASS}::operator=({CLASS}&&) noexcept = default;

// Factory constructor taking the real interface
{CLASS} make{CLASS}(std::unique_ptr<{INTERFACE}> impl) {{
    {CLASS} bridge;
    bridge.impl_ = std::make_unique<{CLASS}::Impl>(std::move(impl));
    return bridge;
}}

{METHODS}
