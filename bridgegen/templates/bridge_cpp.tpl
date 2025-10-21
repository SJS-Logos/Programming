#include "{CLASS}.h"
#include "{INTERFACE}.h"

{CLASS}::{CLASS}(std::unique_ptr<{INTERFACE}>&& impl) : impl_(std::move(impl)) {{ }}
{CLASS}::{CLASS}({CLASS}&&) noexcept = default;

{METHODS}

// Factory constructor taking the real interface
std::unique_ptr<{CLASS}> make{CLASS}(std::unique_ptr<{INTERFACE}>&& impl) {{
    return std::make_unique<{CLASS}>(std::move(impl));
}}
