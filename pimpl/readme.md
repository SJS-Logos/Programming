# Abstract data types
An abstract data type (ADT) is a theoretical concept in software and computer science that describes a data type solely through its operations (what can be done with it) and the properties of those operations, without specifying how it is implemented.

An ADT thus defines an abstract interface (e.g., a stack with push, pop, and peek), while multiple different concrete implementations may exist (e.g., a stack based on an array or a linked list). The implementation can be swapped out without changing the use of the ADT, as long as the contract for the operations is preserved.
# Praktiske implementationer

## Object oriented programming and ADT
In object-oriented programming, an ADT is typically expressed as an **interface** or an **abstract class**. The contract is described through the methods that the class provides, while the implementation is hidden in one or more concrete classes.
```cpp
struct IStream {
    virtual int read(char* buf, size_t n) = 0;
    virtual int write(const char* buf, size_t n) = 0;
    virtual ~IStream() {}
};
```

A concrete implemention could be:
```cpp
#include <cstdio>

struct FStream : public IStream {
    int read(char* buf, size_t n) override { ... }
    int write(const char* buf, size_t n) override { ... }
    ~FStream() override { ... }

private:
    FILE* _file;
};
```

There are two problems with the concrete implementation:

If changes are made to the private part of FStream, the size of the class changes.

A (hidden) dependency on cstdio is introduced in the modules that use the module.

Both problems can lead to slower compilation and larger dependency chains.
Two of the heavyweights from the C++ standards committee (Herb Sutter and Scott Meyers) described in the book Exceptional C++ how dependencies can be hidden.

![Exceptional C++](ExceptionalCpp.png)

The solution is widely used in the Qt libraries and is today known as the Pimpl idiom (pointer to implementation).

The solution uses a feature from C/C++ called an opaque data type:


```c
FILE* f = fopen(...); // API arbejder med FILE*, men skjuler definitionen
```

I C++ defineres en **opaque data type** ved
```cpp
struct classname;
```
eller
```cpp
class classname;
```


**Opaque data type** har gjort det muligt at opdatere system biblioteker, uden at genoversætte de biblioteker der bruger dem.

Jeg har kopieret boost's eksempel på en "Pimpl"

## The "Pimpl" idiom
A C++ specific variation of the incomplete class pattern is the "Pimpl" idiom. The incomplete class is not exposed to the user; it is hidden behind a forwarding facade. shared_ptr can be used to implement a "Pimpl":


```cpp
// file.hpp:

class file
{
private:

    class impl;
    shared_ptr<impl> pimpl_;

public:

    file(char const * name, char const * mode);

    // compiler generated members are fine and useful

    void read(void * data, size_t size);
};
```

```cpp
// file.cpp:
#include "file.hpp"

class file::impl
{
private:

    impl(impl const &);
    impl & operator=(impl const &);

    // private data

public:

    impl(char const * name, char const * mode) { ... }
    ~impl() { ... }
    void read(void * data, size_t size) { ... }
};

file::file(char const * name, char const * mode): pimpl_(new impl(name, mode))
{
}

void file::read(void * data, size_t size)
{
    pimpl_->read(data, size);
}
```

The key thing to note here is that the compiler-generated copy constructor, assignment operator, and destructor all have a sensible meaning. As a result, file is CopyConstructible and Assignable, allowing its use in standard containers.



## Pimpl
## unique_ptr vs. shared_ptr

->