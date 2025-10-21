# BridgeGen

**BridgeGen** is a Python-based utility for generating *bridge classes* from C++ abstract interface headers.

The bridge class wraps a `std::unique_ptr` to the abstract class and provides **non-virtual forwarding functions** that delegate to the virtual interface methods.

This is useful when:
- You want to maintain ABI/vtable stability across modules.
- You want a clean separation between the interface header and implementation.
- You want to automatically generate thin bridge wrappers around abstract interfaces.

---

## ⚙️ Installation

### 1. Install Python 3
Ensure that Python 3.8+ is installed and accessible in your system `PATH`.

```bash
python --version
```

If not installed, download it from:
[https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 2. Install Clang (for AST parsing)
BridgeGen uses **clang’s Python bindings** (`clang.cindex`) for parsing C++ headers.

#### Windows
You can install LLVM/Clang via:
```bash
choco install llvm
```

Then set the `LLVM_CONFIG` environment variable if needed:
```bash
set LLVM_CONFIG="C:\Program Files\LLVM\bin\llvm-config.exe"
```

#### Linux / macOS
```bash
sudo apt install clang python3-clang
```

or

```bash
brew install llvm
pip install clang
```

---

### 3. Python dependencies
Install the required Python modules:
```bash
pip install clang
```

---

## 🧩 Usage

### Basic syntax
```bash
python bridgegen.py <header-file>
```

Example:
```bash
python bridgegen.py MyInterface.h
```

This will:
- Parse the C++ abstract interface file (`MyInterface.h`).
- Generate:
  - `MyInterfaceBridge.h`
  - `MyInterfaceBridge.cpp`

Both files will be placed in the same directory as the input header.

---

## 🏗️ Input Structure

- This is the declaration of the abstract interface

#pragma once

```cpp
class IMyInterface {
    public:
    virtual void DoWork(int x) = 0;
    virtual ~IMyInterface() = default;
};
```

## 🏗️ Generated Structure

### Header file (`MyInterfaceBridge.h`)
- Declares an **opaque forward declaration** of the interface.
- Defines the **bridge class** that owns a `std::unique_ptr<Interface>`.
- Contains **non-virtual forwarding methods**.

Example:

```cpp
#pragma once
#include <memory>

class IMyInterface;

class IMyInterfaceBridge {
public:
    explicit IMyInterfaceBridge(std::unique_ptr<IMyInterface>&& impl);

    IMyInterfaceBridge(IMyInterfaceBridge&&) noexcept;

    void DoWork(int x);

private:
    std::unique_ptr<IMyInterface> impl_;
};
```

### Source file (`MyInterfaceBridge.cpp`)
- Includes the interface header.
- Implements the bridge methods that delegate to the virtual ones.

Example:
```cpp
#include "IMyInterfaceBridge.h"
#include "IMyInterface.h"

IMyInterfaceBridge::IMyInterfaceBridge(std::unique_ptr<IMyInterface>&& impl) : impl_(std::move(impl)) { }
IMyInterfaceBridge::IMyInterfaceBridge(IMyInterfaceBridge&&) noexcept = default;

void IMyInterfaceBridge::DoWork(int x) {
    if (impl_) impl_->DoWork(x);
}

// Factory constructor taking the real interface
std::unique_ptr<IMyInterfaceBridge> makeIMyInterfaceBridge(std::unique_ptr<IMyInterface>&& impl) {
    return std::make_unique<IMyInterfaceBridge>(std::move(impl));
}
```

---

## 📄 License
MIT License (free to use, modify, and distribute)
