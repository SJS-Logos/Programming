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

Løsningen bliver brugt i stor stil i QT's biblioteker, og kendes idag under navnet PIMPL idiomet.

Løsningen bruger en feature fra "C" der kaldes **opaque data type**:

C/C++ og **opaque data type**
En **opaque data type** er en type, hvor indholdet (endnu) ikke er defineret. Opaque betyder "gennemsigtig". 
Man kan oprette pegere til en **opaque data type** men ikke objekter af selve typen. |
I C- og C++-standardbibliotekerne (og i mange POSIX- og systembiblioteker) møder man ofte opaque data typer, f.eks.: 

```
FILE* f = fopen(...); // API arbejder med FILE*, men skjuler definitionen
```
Opaque Det har gjort det muligt at opdatere system biblioteker, uden at genoversætte de biblioteker der bruger dem.

## Forward declaration

- C++ understøtter **forward declaration** af klasser. Så længe en klasse ikke er defineret, kaldes den for **opaque**
  ```cpp
  class ForwardDefinedClass; // Kun en erklæring, ingen definition 
  class ForwardContainer {
    private:
    // Man kan oprette pegere til opaque definitioner
    std::unique_ptr<ForwardDefinedClass> _forwardDefinedClassInstance;
  };
  
  // cpp fil
  µµ
  class ForwardDefinedClass {
      // Her kommer der kød på klassen: Den holder op med at være **opaque**
  };

## Pimpl
## unique_ptr vs. shared_ptr