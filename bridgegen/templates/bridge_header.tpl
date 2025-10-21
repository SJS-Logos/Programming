#pragma once
#include <memory>

class {INTERFACE};

class {CLASS} {{
public:
    explicit {CLASS}(std::unique_ptr<{INTERFACE}>&& impl);

    {CLASS}({CLASS}&&) noexcept;

{METHODS}

private:
    std::unique_ptr<{INTERFACE}> impl_;
}};

// Factory constructor taking the real interface
std::unique_ptr<{CLASS}> make{CLASS}(std::unique_ptr<{INTERFACE}>&& impl);
