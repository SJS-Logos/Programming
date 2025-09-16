# Abstrakte datatyper
En abstrakt datatype (**ADT**) er et teoretisk begreb inden for software og datalogi, der beskriver en datatype udelukkende gennem dens operationer (hvad man kan gøre med den) og de egenskaber, disse operationer har, uden at specificere hvordan den er implementeret.

En ADT definerer altså et abstrakt interface (f.eks. en stak med push, pop og peek), mens der kan findes flere forskellige konkrete implementationer (f.eks. en stak baseret på et array eller en linket liste). Implementationen kan skiftes ud uden at ændre brugen af ADT’en, så længe kontrakten for operationerne bevares.

# Praktiske implementationer

## Objektorienteret og ADT
I objektorienteret programmering udtrykkes en ADT typisk som et **interface** eller en **abstrakt klasse**. Kontrakten beskrives gennem de metoder, som klassen stiller til rådighed, mens implementationen er gemt i en eller flere konkrete klasser.

```cpp
struct IStream {
    virtual int read(char* buf, size_t n) = 0;
    virtual int write(const char* buf, size_t n) = 0;
    virtual ~IStream() {}
};
```

Her vil der så være en konkret implementation f.eks.
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

Der er to problemer med den konkrete implementation
- Hvis der bliver lavet ændringer i "private" delen af FStream, ændrer klassens størrelse sig.
- Der introduceres en (skjult) afhængighed af cstdio i de moduler der bruger modulet. 

Begge problemer kan føre til langsommere kompilering og større afhængighedskæder.
To af de tunge drenge fra C++ standard commitee (Herb Sutter og Scott Myers) beskrev i bogen "Exceptional C++" hvorledes man kan gemme "afhængigheder". 

![Exceptional C++](ExceptionalCpp.png)

Løsningen bliver brugt i stor stil i QT's biblioteker, og kendes idag under navnet "Pimpl" idiomet (**p**ointer to **impl**ementation). 

Løsningen bruger en feature fra C/C++ der kaldes **opaque data type**:

En **opaque data type** er en type, hvor indholdet (endnu) ikke er defineret. Opaque betyder "gennemsigtig". 
Man kan oprette pegere til en **opaque data type** men ikke objekter af selve typen. |
I C- og C++-standardbibliotekerne (og i mange POSIX- og systembiblioteker) møder man ofte opaque data typer, f.eks.: 

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
// file.cpp:
```

```cpp
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