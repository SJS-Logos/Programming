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
