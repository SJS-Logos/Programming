#pragma once

// Public stable interface 
struct IWork {
    virtual void DoWork() = 0;
    virtual ~IWork() = default;
};
