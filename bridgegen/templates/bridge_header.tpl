#pragma once
#include <memory>

class {CLASS} {{
public:
    {CLASS}();
    ~{CLASS}();

    {CLASS}({CLASS}&&) noexcept;
    {CLASS}& operator=({CLASS}&&) noexcept;

{METHODS}

private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
}};
