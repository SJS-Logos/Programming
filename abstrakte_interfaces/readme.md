# Fra SOLID til kontrakter gennem abstrakte interfaces

---

## 1. SOLID som fundament
- **S**ingle Responsibility Principle  
  → Hver klasse bør have ét klart ansvar.

- **O**pen/Closed Principle  
  → Klasser skal være åbne for udvidelse, men lukkede for modifikation.

- **L**iskov Substitution Principle  
  → Abstrakte kontrakter sikrer at implementeringer kan udskiftes frit.

- **I**nterface Segregation Principle  
  → Små, veldefinerede interfaces forebygger afhængighed af irrelevante detaljer.

- **D**ependency Inversion Principle  
  → Afhæng af abstraktioner, ikke af konkrete implementationer.

---

## 2. Problemet med konkrete klasser i headers
- Når vi skriver **class MyConcrete { ... }** i en header, introducerer vi:  
  - En **direkte afhængighed** til den konkrete implementering.  
  - Større **kompilerings afhængigheder** (ændringer i implementeringen breder sig).  
  - Et implicit **brud på Open/Closed og Dependency Inversion**.

- Klientkoden ender med at kende til interne detaljer, den egentlig ikke burde vide.

---

## 3. Abstrakte interfaces som kontrakter
- Et **rent interface** definerer kun *kontrakten*:

```cpp
struct IFoo {
    virtual void doSomething() = 0;
    virtual ~IFoo() {}
};
```

- Fordele:  
  - Koden afhænger kun af **stabile kontrakter**, ikke af konkrete implementeringer.  
  - Understøtter **udskiftelige implementeringer** (Liskov).  
  - Reducerer **kompilationsafhængigheder**.  
  - Fremmer **Dependency Inversion**.

---

## 4. Factories som naturligt bindeled
- I stedet for at eksponere konkrete klasser i headers:  
  - Definér en **factory-funktion** der returnerer en **pointer til kontrakten**:

```cpp
std::unique_ptr<IFoo> createFoo();
```

- Konsekvenser:  
  - Klientkoden kender kun til **kontrakten (IFoo)**.  
  - Implementeringen af `createFoo()` kan ændres frit uden at bryde klienter.  
  - Matcher **Open/Closed**: nye implementationer kan tilføjes uden ændring af eksisterende kode.

---

## 5. Konklusion
- **SOLID peger i retning af kontrakter**:  
  - Interfaces giver stabilitet, fleksibilitet og lav kobling.

- **Konkrete klasser i headers er en læk af implementation**.

- **Factories** giver en elegant mekanisme til at skjule detaljer og returnere kontrakter.

- Derfor: Vi bør tænke **”abstrakt først”** – konkrete klasser er interne detaljer, ikke en del af API’et.
