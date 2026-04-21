## DApp-Governed TEE Policies and Network Responsibilities

The Roadmap also includes the ability for DApps to govern custom TEE policies for their own apps by re-using the infrastructure we provided. We have laid the groundwork for this today by building abstractions into our code for TEE Capability Policies, and have made upstream PRs to the Flashtestations project so that it’s open sourced and actively used across multiple projects.

What matters here is not that we are opening an unrestricted path for anyone to add new network capabilities. Today, the network exposes a whitelisted set of capabilities that Ritual governs as public goods, and external parties cannot independently introduce new network-level capabilities. This boundary is the important one: network capabilities remain public goods, while DApps get a mechanism to ship custom behavior on their own cadence.

Over time, network governance could allow new public capabilities to be added, but that should be understood as a slower lane: each new network capability would require broad coordination, strict audits, and ultimately a network vote. The point of DApp-governed TEE policies is to create a faster lane for application-specific behavior without forcing every new use case through network governance.

In practice, a DApp can choose the executor code it wants, deploy its own policy contract, and provision executors through its own contracts. When an executor is launched, the launch flow can check the DApp's deployed policy contract to determine which policy and executor configuration should apply, and user actions can then be routed through that executor accordingly. Payments, incentives, and lifecycle management can flow through the application's own token and contract system, while the contracts enforce that execution stays aligned with the DApp's custom policy.

---

## Public Goods vs. Application Responsibility

There is a strong case that the network should focus on providing **generic, high-leverage primitives**, while leaving **context-heavy logic** to DApps.

For example, delegated secrets are a powerful primitive — but they introduce meaningful risk and coordination overhead. In practice, users are unlikely to delegate secrets unless there is a clear application-level incentive to do so. This suggests that delegated secret usage will often be driven by DApp-specific contexts, even when some baseline support exists in generic network-level executors.

That does not make delegated secret support in default network executors (e.g. HTTP executors) unhelpful. It is still valuable for the set of HTTP-level restrictions we can anticipate and standardize at the network layer. The value of DApp-managed executors is that they can go further than that fixed set of restrictions: a DApp can make secret usage depend on application-specific state, user roles, quotas, workflow steps, or semantic checks on the action being requested. For example, an app might allow a Twitter action but forbid tagging certain accounts, or allow a trading API call only when it stays within app-specific risk limits. Those kinds of constraints are difficult to package as generic network rules, but fit naturally in DApp-managed executor images, where:

- the trust model is explicit,
- incentives are aligned,
- and the application can define its own lifecycle guarantees.

This separation allows the network to offer common protections while still preserving room for DApps to implement richer, application-specific controls.

---

## Application-Level Coordination Benefits

Allowing DApps to govern their own delegated-secret policies also creates useful new functionality at the application layer:

### Custom Liveness Incentives
A DApp can design its own incentive mechanisms to keep the executors it depends on live and healthy. Because delegated secrets are tied to the application's own workflows and users, the DApp is in the best position to define participation rewards, fallback behavior, and lifecycle guarantees that fit its product.

### Better Discovery and Routing
A DApp can also maintain its own registry and discovery flow for which executors hold which delegated secrets, making it easier to route requests, surface the right options to users, and coordinate execution within the app's own environment.

These are not just technical controls; they are product, incentive, and coordination mechanisms. DApp-governed policies make it possible for applications to own those mechanisms directly rather than relying only on network-level defaults.

---

## Where Network-Level Public Goods Make Sense

Network-level capabilities make the most sense when the burden of building, auditing, operating, and incentivizing them can be shared across many applications. In practice, there are a few clear cases where this public-good model is especially valuable.

### Common Reusable Primitives
HTTP executors are a good example of a capability that belongs at the network level because they are an extremely common primitive. Many different applications need the ability to make HTTP requests, so it makes sense to have a network-wide effort behind auditing the implementation, maintaining reliable supply, and reusing that capability across many apps rather than having each DApp rebuild it independently.

### Infrastructure With Strong Liveness Requirements
DKMS is another case where a network-provided public good is useful. It benefits from very strong liveness guarantees, and those guarantees are easier to justify when the network is explicitly supporting and incentivizing the infrastructure. At the same time, DKMS is generic enough to be reused by many different agents and applications, so the cost of providing that reliability can be amortized across the ecosystem.

### End-User-Facing Capabilities
It is also useful to provide a capability as a public good when the goal is to let end users access it quickly and generically, rather than to help a single DApp build internal infrastructure. The key distinction here is end user versus DApp. `AUTONOMOUS_AGENT` fits this pattern: it is valuable as a network-level capability because it gives users a fast path to a broadly useful behavior without requiring each application to stand up its own bespoke stack first.

By contrast, when the behavior depends on application-specific semantics, incentives, or policy logic, it is usually a better fit for DApp-managed executors and contracts.

