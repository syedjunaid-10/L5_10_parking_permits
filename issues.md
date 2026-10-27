# Static Code Analysis - Identified Issues and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| **Insecure Pseudo-Random Generator (B311)** | Security (Bandit) | 11 | `random.randint` is not cryptographically secure for generating permit tokens. | Replaced `import random` with `import secrets` and used `secrets.randbelow()` for secure generation. |
| **Mutable Default Argument (W0102)** | Logic (Pylint) | 9 | `zone_records=[]` initializes a list once at definition, sharing it across all function calls. | Changed default to `zone_records=None` and initialized `zone_records = []` inside the function body. |
| **Overly Broad Exception Catching (W0702)** | Quality (Pylint) | 16, 22, 28, 38 | Bare `except:` catches critical system exits and masks unexpected crashes. | Replaced bare `except:` clauses with specific exceptions like `except (KeyError, ValueError, TypeError):`. |
| **Unsafe File Opening (W1514, R1732)** | Quality (Pylint) | 36, 41 | Using `open()` without a context manager (`with`) or explicit encoding risks file corruption and memory leaks. | Wrapped file operations in `with open(..., encoding="utf-8") as file:` to ensure safe automatic closing. |
| **PEP 8 Formatting & Naming (E302, C0103)** | Style (Flake8 / Pylint) | 45 | Missing two blank lines before functions, and `setExpiry` violates `snake_case` naming rules. | Added required blank lines, renamed function to `set_expiry`, and renamed global state `permits` to uppercase `PERMITS`. |