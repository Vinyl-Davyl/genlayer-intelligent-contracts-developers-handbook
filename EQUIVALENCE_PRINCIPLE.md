# The Equivalence Principle: A Technical Deep Dive

> How GenLayer achieves consensus on non-deterministic computation

---

## The Problem: Non-Determinism Breaks Traditional Consensus

Every blockchain consensus mechanism assumes **deterministic execution** &mdash; given the same inputs, every node produces the exact same output. This is how Ethereum works: every validator runs the same EVM bytecode and gets byte-identical results.

But what happens when your contract calls an LLM? Or fetches a live web page?

- **LLM outputs vary** between identical prompts (temperature, model version, hardware)
- **Web data changes** between requests (timestamps, counters, dynamic content)
- **API responses differ** by milliseconds, load balancing, caching

Traditional consensus would reject every non-deterministic transaction. GenLayer solves this with the **Equivalence Principle**.

---

## Core Insight: Semantic Equivalence Over Byte Identity

The Equivalence Principle allows outputs from different validators to be considered **valid** as long as they meet predefined standards of equivalence &mdash; even if they are not byte-identical.

```
Traditional Consensus:
  Validator A output: 0xABCD1234
  Validator B output: 0xABCD1234  ✅ Match
  Validator C output: 0xABCD1235  ❌ Rejected

GenLayer Equivalence:
  Validator A output: {"sentiment": "positive", "score": 87}
  Validator B output: {"sentiment": "positive", "score": 85}  ✅ Equivalent
  Validator C output: {"sentiment": "negative", "score": 23}  ❌ Divergent
```

---

## The Leader-Validator Architecture

Every non-deterministic operation follows this pattern:

```
                    Transaction
                        |
                        v
              +---------+---------+
              |    Leader Node    |
              |  Executes first   |
              |  Proposes result  |
              +---------+---------+
                        |
            +-----------+-----------+
            |           |           |
            v           v           v
      +-----------+-----------+-----------+
      |Validator 1|Validator 2|Validator 3|
      | Verifies  | Verifies  | Verifies  |
      | Votes ✅  | Votes ✅  | Votes ❌  |
      +-----------+-----------+-----------+
            |           |           |
            v           v           v
         Majority agrees → Result accepted
```

The leader executes the non-deterministic operation and proposes a result. Validators then verify whether the result is acceptable.

---

## Four Equivalence Patterns

### 1. Strict Equality (`strict_eq`)

```python
result = gl.eq_principle.strict_eq(my_function)
```

**How it works:** Every validator executes the function independently. All results must be **exactly identical**.

**When to use:**
- Boolean outputs (`True`/`False`)
- Deterministic data extraction from web pages
- Canonicalized JSON (sorted keys, consistent formatting)

**When NOT to use:**
- Free-text LLM responses
- Floating-point calculations
- Data with timestamps or volatile fields

### 2. Comparative (`prompt_comparative`)

```python
result = gl.eq_principle.prompt_comparative(
    my_function,
    principle="Results should agree on the overall sentiment and main topics"
)
```

**How it works:** Both leader and validators execute the same function. Then an LLM compares the results against your stated principle to determine equivalence.

**When to use:**
- Text summaries where wording may differ
- Analysis where conclusions matter more than exact phrasing
- Data with acceptable numerical margins

### 3. Non-Comparative (`prompt_non_comparative`)

```python
result = gl.eq_principle.prompt_non_comparative(
    leader_function,
    criteria="Output must be valid JSON with 'score' (1-100) and 'category' (string)"
)
```

**How it works:** Only the leader executes the function. Validators evaluate the leader's output against predefined criteria without re-executing.

**When to use:**
- Expensive computations (save validator resources)
- Quality validation where re-execution is unnecessary
- Outputs where format/structure matters more than exact values

### 4. Custom Validation (`run_nondet_unsafe`)

```python
def leader_fn():
    price = fetch_price()
    return price

def validator_fn(leader_result) -> bool:
    my_price = fetch_price()
    return abs(leader_result.calldata - my_price) / my_price <= 0.02

result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
```

**How it works:** You write both the leader logic and the validator logic. The validator receives the leader's result and returns `True` (accept) or `False` (reject).

**When to use:**
- Custom tolerance thresholds (e.g., 2% price deviation)
- Complex multi-field validation
- Domain-specific equivalence rules

---

## Decision Matrix

| Scenario | Pattern | Rationale |
|----------|---------|-----------|
| "Does page X contain keyword Y?" | `strict_eq` | Boolean output, deterministic |
| "Summarize this article" | `prompt_comparative` | Text varies, meaning stable |
| "Generate a risk assessment" | `prompt_non_comparative` | Expensive, validate quality |
| "Fetch ETH price" | `run_nondet_unsafe` | Custom tolerance (2%) |
| "Classify sentiment" | `strict_eq` | Enum output, limited options |
| "Extract structured data from HTML" | `prompt_comparative` | Data may vary slightly |

---

## Security Considerations

1. **Validators must genuinely verify** &mdash; returning `True` unconditionally defeats consensus
2. **Tolerance thresholds should be tight** &mdash; too loose allows manipulation
3. **Reject when uncertain** &mdash; better to fail than accept bad data
4. **Test with adversarial inputs** &mdash; ensure validators catch manipulated leader results

---

## Further Reading

- [GenLayer Equivalence Principle Docs](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)
- [Non-Determinism Handling](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
- [Optimistic Democracy](https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy)
