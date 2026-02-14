When packaging a Python project, two common formats are source distributions (sdist) and wheels. Here’s how they differ:

## 1. Source Distribution (*sdist*)
- File Format: Typically a `.tar.gz` archive (`mypackage-0.1.tar.gz`).
- Contains: The raw source code, `setup.py` or `pyproject.toml`, and necessary metadata.
- Requires build step: Needs to be compiled before installation. When installing, pip will build a wheel or install directly from source.
- Platform Independence: Works across different operating systems, but the package may need to be compiled on the target system if it requires external C or Rust dependencies.
How to create an sdist:

```bash
python setup.py sdist
```

or using the `build` module:

```bash
python -m build --sdist
```

## 2. Wheels
- File Format: A `.whl` file (`mypackage-0.1-py3-none-any.whl` or `mypackage-0.1-cp39-win_amd64.whl`).
- Contains: Pre-built, ready-to-install package files.
- Faster Installation: No need for compilation; files are directly copied into the appropriate locations.
- Platform-Specific or Universal:
  - Pure python wheels (e.g., `mypackage-0.1-py3-none-any.whl`) can run on any platform.
  - Platform-specific wheels (e.g., `mypackage-0.1-cp39-win_amd64.whl`) are compiled for a specific Python version and OS.
- Preferred by pip: If both sdist and wheel are available, pip installs the wheel.

How to create a wheel:

```bash
python setup.py bdist_wheel
```

or using the `build` module:

```
python -m build --wheel
```

### Wheels file naming format

A Python wheel file follows a structured naming convention that encodes important metadata about the package. A typical wheel filename looks like this:

```
mypackage-1.0.0-py3-none-any.whl
```

#### **Format Breakdown**
The general structure of a wheel filename is:

```
{distribution}-{version}-{python_tag}-{abi_tag}-{platform_tag}.whl
```

| **Component**      | **Description**                                           | **Example**        |
|--------------------|-----------------------------------------------------------|--------------------|
| **distribution**   | The package name                                          | `mypackage`        |
| **version**        | The package version                                       | `1.0.0`            |
| **python_tag**     | Compatible Python versions                                | `py3`, `cp39`      |
| **abi_tag**        | ABI (Application Binary Interface) compatibility          | `none`, `cp39m`    |
| **platform_tag**   | Target platform or OS                                     | `any`, `win_amd64` |

---

#### **Detailed Explanation**
1. **Distribution Name**
   - Corresponds to the package name as registered on PyPI.
   - Example: `mypackage`, `numpy`, `requests`.

2. **Version**
   - Matches the package’s version following [PEP 440](https://peps.python.org/pep-0440/).
   - Example: `1.0.0`, `2.3.1.post1`, `0.9.8b`.

3. **Python Tag**
   - Specifies which Python versions the wheel supports.
   - Common values:
     - `py3` → Any Python 3 version.
     - `py38`, `py39`, `py310` → Specific Python versions.
     - `cp39` → CPython 3.9.
     - `py2.py3` → Compatible with both Python 2 and 3.

4. **ABI Tag (Application Binary Interface)**
   - Defines compatibility with a specific ABI.
   - Common values:
     - `none` → Pure Python package (no compiled extensions).
     - `cp39m` → Compiled for CPython 3.9 with a specific ABI.
     - `abi3` → Compatible with multiple versions.

5. **Platform Tag**
   - Indicates the operating system and architecture compatibility.
   - Common values:
     - `any` → Works on all platforms (pure Python).
     - `win_amd64` → Windows 64-bit.
     - `manylinux2014_x86_64` → Linux (manylinux standard).
     - `macosx_10_9_x86_64` → macOS.

---

## **Examples**
| **Wheel Filename**                                | **Meaning**                                                                 |
|---------------------------------------------------|-----------------------------------------------------------------------------|
| `mypackage-1.0.0-py3-none-any.whl`                | Pure Python package, compatible with any Python 3 version and any platform. |
| `mypackage-1.0.0-cp39-cp39-win_amd64.whl`         | Compiled package for CPython 3.9, Windows 64-bit.                           |
| `mypackage-2.1.0-py2.py3-none-any.whl`            | Works on both Python 2 & 3, no compiled extensions.                         |
| `numpy-1.21.2-cp39-cp39-manylinux2014_x86_64.whl` | Compiled for CPython 3.9 on Linux (manylinux2014).                          |

## Key Differences
| Feature               | *sdist*                       | *Wheel*                                         |
|-----------------------|-------------------------------|-------------------------------------------------|
| File Extension        | `.tar.gz`                     | `.whl`                                          |
| Compilation Needed?   | During installation           | During packaging                                |
| Speed of Installation | Slower                        | Faster                                          |
| Platform Independent? | Yes                           | Depends (can be universal or platform-specific) |
| Preferred by pip?     | Only if no wheel is available | Yes                                             |

## Which One to Use?
- For PyPI distribution: Provide both an sdist and a wheel
- For faster installation: Prefer wheels
- For projects with compiled extensions (C, C++, Rust): Use wheels to avoid requiring users to compile the code
