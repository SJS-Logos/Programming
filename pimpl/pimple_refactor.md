# Refactoring a class as a pimple


```cpp

// file.h:

class file
{
private:
  FILE* file_;

public:

  file(char const * name, char const * mode);
  void read(void * data, size_t size);
};
```
 </td>

```cpp

// file.cpp:

#include "file.hpp"

file::file(char const * name, char const * mode)
{
    file_ = fopen(name, mode );
}

void file::read(void * data, size_t size)
{
    fread(data, size, 1, file_ );
}
```


```cpp
// file.h:

class file
{
private:

    class impl;
    shared_ptr<impl> pimpl_;

public:

    file(char const * name, char const * mode);
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

    FILE* file_;

public:

    impl(char const * name, char const * mode) { 
      file_ = fopen(name, mode );
    }
    void read(void * data, size_t size) {     
      fread(data, size, 1, file_ );
    }
    ~impl() { ... }
};

file::file(char const * name, char const * mode): pimpl_(new impl(name, mode))
{
}

void file::read(void * data, size_t size)
{
    pimpl_->read(data, size);
}
```
