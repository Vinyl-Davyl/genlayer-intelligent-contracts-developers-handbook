# GenLayer Intelligent Contracts Cheatsheet

> Quick reference for building on GenLayer

---

## Contract Structure

```python
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class MyContract(gl.Contract):
    # Storage fields (persisted on-chain)
    counter: u32
    name: str

    # Constructor (undecorated, called once on deploy)
    def __init__(self, name: str):
        self.name = name

    # Read-only method
    @gl.public.view
    def get_name(self) -> str:
        return self.name

    # State-modifying method
    @gl.public.write
    def set_name(self, name: str):
        self.name = name

    # Payable method
    @gl.public.write.payable
    def deposit(self):
        pass
```

---

## Type System

| Python Type | GenLayer Type | Notes |
|-------------|---------------|-------|
| `int` | `u32`, `i64`, `u256`, `bigint` | Use sized integers |
| `list` | `DynArray[T]` | Persistent array |
| `dict` | `TreeMap[K, V]` | Persistent map |
| `str` | `str` | Supported directly |
| `bool` | `bool` | Supported directly |
| `bytes` | `bytes` | Supported directly |

---

## Non-Deterministic Operations

### Web Requests
```python
# GET request
response = gl.nondet.web.get(url)
body = response.body.decode("utf-8")

# Render HTML page
html = gl.nondet.web.render(url, mode="html")

# Screenshot
image = gl.nondet.web.render(url, mode="screenshot")
```

### LLM Calls
```python
# Basic prompt
result = gl.nondet.exec_prompt("Your prompt here")

# JSON response
result = gl.nondet.exec_prompt(prompt, response_format="json")

# With images (max 2)
result = gl.nondet.exec_prompt(prompt, images=[img_data])
```

---

## Equivalence Patterns

```python
# Exact match
result = gl.eq_principle.strict_eq(fn)

# LLM-compared outputs
result = gl.eq_principle.prompt_comparative(fn, principle="...")

# Leader-only with criteria validation
result = gl.eq_principle.prompt_non_comparative(fn, criteria="...")

# Custom leader/validator logic
result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
```

---

## CLI Commands

```bash
# Setup
genlayer init                    # Initialize environment
genlayer up                      # Start local network

# Deployment
genlayer deploy --contract <path> --args <args>

# Interaction
genlayer call --contract <addr> --method <name>
genlayer write --contract <addr> --method <name> --args <args>

# Network
genlayer network set testnet
genlayer network info

# Account
genlayer account create
genlayer account list

# Linting
genvm-lint check contracts/my_contract.py
```

---

## Testing

```bash
# Direct mode (fast, no Docker)
pytest tests/direct/ -v

# Integration mode
gltest tests/integration/ -v -s
```

### Mocking
```python
direct_vm.mock_web(r"pattern", {"status": 200, "body": "..."})
direct_vm.mock_llm(r"pattern", "mock response")
direct_vm.strict_mocks = True  # Error on unmatched mocks
```

### Fixtures
- `direct_vm` &mdash; VM context with cheatcodes
- `direct_deploy` &mdash; In-memory contract deployment
- `direct_alice`, `direct_bob`, `direct_charlie` &mdash; Test addresses
- `direct_owner` &mdash; Default sender
- `direct_accounts` &mdash; List of 10 test addresses

---

## Rules of Non-Determinism

| Allowed INSIDE nondet blocks | Allowed OUTSIDE nondet blocks |
|------------------------------|-------------------------------|
| `gl.nondet.web.get()` | `self.field = value` (storage write) |
| `gl.nondet.web.render()` | `gl.get_contract_at()` (cross-contract) |
| `gl.nondet.exec_prompt()` | `.emit()` (events) |
| Local variable operations | Nested nondet blocks (**NO**) |

---

## Error Handling

```python
# Reject bad LLM output (triggers leader rotation)
raise gl.UserError("Invalid response format")
```

---

## Resources

| Resource | URL |
|----------|-----|
| Documentation | https://docs.genlayer.com |
| GenLayer Studio | Browser-based IDE for prototyping |
| CLI Reference | https://docs.genlayer.com/api-references/genlayer-cli |
| JS SDK | https://docs.genlayer.com/api-references/genlayer-js |
| Python SDK | https://docs.genlayer.com/api-references/genlayer-py |
| Boilerplate | https://github.com/genlayerlabs/genlayer-project-boilerplate |
