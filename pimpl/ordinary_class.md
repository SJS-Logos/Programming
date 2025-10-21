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
