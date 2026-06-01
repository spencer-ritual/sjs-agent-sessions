# Ritual SC PR Notes (Part 2): StakeHub Contract Port

Reviewed PR:

- `ritual-sc-internal#203`: Add BSC-derived Ritual staking contracts

Follow-on notes that extend `sjs-agent-sessions/stakehub/ritual-sc.md`.

## Ritual SC-Specific Review Notes

| Priority | Issue | Notes |
| --- | --- | --- |
| Nit | Do not delete the signature comments carried over from BNB/BSC. | The upstream BSC contracts annotate functions and storage with signature/intent comments (the `// create validator need to lock 1 BNB`-style inline notes and the per-function header comments). Keep them in the port. They help with debugging by preserving the original BSC semantics next to the Ritual code, so a reviewer can quickly see what behavior was inherited versus changed. Stripping them removes the cheapest available cross-reference back to the upstream source. |
| Nit | Same for the storage-mapping documentation comments. | The BSC contracts label each mapping/field with a `key => value` comment that explains what the storage slot means (for example `// validator consensus address => validator operator address` above `consensusToOperator`). The port deletes these. Keep them. For mappings whose `address`/`bytes`/`bytes32` key and value types are otherwise opaque, these one-line comments are often the only inline indication of intent, which makes them disproportionately useful when debugging storage reads/writes and when diffing layout against BSC. |

## Evidence

Examples of deleted storage-mapping documentation comments (`ritual-vs-bsc-stakehub.diff`, around line 163-189):

```diff
     EnumerableSet.AddressSet private _validatorSet;
-    // validator operator address => validator info
     mapping(address => Validator) private _validators;
-    // validator moniker set(hash of the moniker)
     mapping(bytes32 => bool) private _monikerSet;
-    // validator consensus address => validator operator address
     mapping(address => address) public consensusToOperator;
```

The retained mappings keep their non-obvious key/value types but lose the one-line explanation of what those keys and values represent. The same pattern applies to the inline behavioral comments (for example `// create validator need to lock 1 BNB`), which are dropped elsewhere in the same port.
