// Hybrid approach
// This is a combination of the pIMPL idiom and the Abstract Interface
// It separates concerns between the two models: 
//   pIMPL is responsible for clearing out VTable fragility
//   Abstract Interface is for SOLID compliance and development of model.

// Public-facing wrapper (no vtables exposed!)
// This is what is exposed through library API
// WorkPimpl.h
#include <memory>
struct IWork; // no exposure of internals - opaque

// A simple bridge, with a dependency injected opaque IWork
class WorkPimpl {
public:
    WorkPimpl(std::unique_ptr<IWork> pimpl);
    void DoWork();
private:
    std::unique_ptr<IWork> pimpl_; // points to abstract interface
};

// IWork.h
// Public stable interface 
struct IWork {
    virtual void DoWork() = 0;
    virtual ~IWork() = default;
};

// MyWork.h
// Factory returns abstract implementations
// include IWork.h
std::unique_ptr<IWork> CreateMyWork();

// MyWork.cpp
#include <iostream>

struct MyWork : IWork {
    void DoWork() override { 
      std::cout << "Do something" << std::endl;
    }
};

std::unique_ptr<IWork> CreateMyWork()
{
   return std::make_unique<MyWork>();
}


// WorkPimple.cpp
// include IWork.h

WorkPimpl::WorkPimpl(std::unique_ptr<IWork> pimpl) : pimpl_(std::move(pimpl)) 
{}

void WorkPimpl::DoWork() { pimpl_->DoWork(); } // non-virtual bridge


int main()
{
   WorkPimpl pimplWork(CreateMyWork());
   pimplWork.DoWork();
}
