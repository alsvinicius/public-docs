---
title: "Segurança e economia de fraude"
description: "Os papers peer-reviewed, o vetor do merchant falsificado, o gap de responsabilidade e um registro consolidado de riscos."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# Segurança e economia de fraude

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Transversal
> O quadro de segurança é severo, e os papers peer-reviewed são melhores que os blogs de vendors. Leia antes de dimensionar risco.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

O quadro de segurança é, no meio de software, ** genuinamente severo**. E os
papers peer-reviewed são substancialmente melhores que os blogs de vendors —
Use-os.

### USENIX Security 2026 — [arXiv:2607.19545](https://arxiv.org/abs/2607.19545)

*"When HTTP 402 Meets the Blockchain: Risks on Emerging x402 Payments"* (ETH
Zurich + Zhejiang). Primeiro estudo sistemático de corretude de autorização e
segurança de execução em deploys reais de facilitator.

- **8 security rules** para facilitators como infraestrutura crítica.
- **4 vetores de ataque**: **Free Shopping**, **Asset Theft**, **Service
  Denial**, **Gas Abuse**.
- Black-box em **15 facilitators maiores** (60K+ sellers, 360K+ buyers) →
  **violações encontradas em todos os 15**. **31 vulnerabilidades
  desconhecidas**, 49 instâncias.
- **>93% dos servidores** do estudo estavam associados a **exclusivamente um
  facilitator** — o achado de centralização.
- Escala: 119M transações, ~\$202.000 em taxas 2025-10-01→12-26, dos quais
  **~\$5.800 eram reverts**.

> [!important] As 4 recomendações — a takeaway prática
> 1. **Vincular verificação a settlement.**
> 2. Reservar nonces.
> 3. Rechecar tempo e estado da conta.
> 4. **Allowlistar estritamente as formas de transação ERC-1271 e ERC-6492.**
>
> E: *release service only after settlement succeeds, or implement explicit
> rollback.*

### Segundo estudo — [arXiv:2605.11781](https://arxiv.org/abs/2605.11781)

*"Five Attacks on x402 Agentic Payment Protocol"*. 4 propriedades
(soundness de autorização, **payment-service correspondence**, resistência a
replay, atomicidade do facilitator); 5 ataques. Enquadramento-chave: x402
*"introduces a cross-layer attack surface absent from conventional web and
on-chain payments"* ao combinar autorização HTTP síncrona com settlement
blockchain assíncrono. Classe de resultado: *"either unpaid service or
paid-but-denied."*

### A análise de ameaça da Visa (2025-11-20)

O vetor mais importante, e é contraintuitivo:

> *"AI shopping agents, which by design find the best deals and make purchases
> on behalf of consumers, can be deceived by sophisticated **counterfeit
> merchants** engineered specifically to exploit them. A fraudulent storefront
> may look entirely legitimate, pass automated security checks, and offer
> prices far below market rate. Then, once the AI agent completes the purchase
> using stored credentials, the malicious merchant can harvest payment data and
> instantly use it for unauthorized transactions."*

Ou seja: **loja falsificada é o vetor**, e o agente é o proxy de credencial
involuntário. Os dois lados automatizados.

Outros achados: +450% em posts de dark web mencionando "AI Agent" (6 meses);
+25% em transações maliciosas iniciadas por bot (+40% nos EUA). E uma rede de
sites fraudulentos rodando **agente de IA conversacional de duplo propósito**:
fachada de legitimidade *e* **desencorajar vítimas de contatar o banco**,
atrasando a denúncia por dias.

> [!warning] Dados de vendor
> O "+4.700% de tráfego de IA em sites de varejo" e o "+450% no dark web" são
> **dados do próprio vendor, com motivação comercial**. Directional, não
> citable como fato neutro.

### Responsabilidade — o gap que ninguém resolveu

Da Visa/Artemis:

> *"If an agent buys the wrong thing, or a malicious prompt redirects its
> spending, it isn't obvious who should be responsible. Is it the person who
> handed over the task, the platform that ran the agent, the company that built
> the model, or the merchant? **Existing legal and regulatory frameworks
> weren't written with this kind of delegation in mind.**"*

E: *"Chargeback windows and evidence rules were designed for human-speed
commerce… Once agents are transacting thousands of times an hour, with money
moving through chains of agents paying other agents, there's no settled way to
unwind a payment that went wrong."*

A única resposta séria é a do AP2 ([[ap2|AP2]]): diffing mandato aberto vs. fechado.

### Registro consolidado de riscos

| # | Risco | Onde morde | Mitigação disponível |
|---|---|---|---|
| 1 | **Free shopping** — serviço liberado no verify, antes do settle | fluxo `authorization` do x402; MPP; qualquer facilitator | bind verify→settle; fluxos `upfront`/`escrow`; idempotência |
| 2 | **Centralização de facilitator** | >93% servidores single-facilitator; Nakamoto 1 | self-facilitation; multi-facilitator; permissionless |
| 3 | **Abuso de gas sponsorship** | \$202K/trimestre, \$5,8K reverts | cap de fees; rejeitar pagamentos não-econômicos; batch |
| 4 | **Prompt injection → dano financeiro** | Shopping Agent; tool results MCP; feeds | constraints de mandato aberto (fail-closed); **política de gasto em código, não em prompt**; default de \$1 do x402 |
| 5 | **Merchant falsificado / credential harvesting** | agente como proxy involuntário | TAP: assinaturas merchant-scoped, purpose-scoped, time-bound, non-relayable; agentic tokens |
| 6 | **Engenharia social conversacional + supressão de denúncia** | agente de IA consistente em dissuadir contato com banco | challenges baseados em tempo |
| 7 | **Replay de token/mandato** | AP2, x402, MPP, UCP | `checkout_hash`+`sd_hash`+`cnf`; EIP-3009 nonce; UCP `Binding`; SIWX nonce + origin binding a config (nunca headers) |
| 8 | **Rainbow table / hash de baixa entropia** | `checkout_hash` do AP2 | digests com sal; **ECDSA, não Ed25519** ⚠️ spec se contradiz |
| 9 | **Double spend via mandato aberto** | AP2 Autonomous | receipt-gated issuance; rejeição de mandates sobrepostos |
| 10 | **Confusão de forma ERC-1271/6492** | validação do facilitator | **allowlist estrito de formas de transação** |
| 11 | **Ambiguidade de responsabilidade** | legal/regulatório, cross-border | diffing de constraints do AP2; FIDO Payments TWG |
| 12 | **Métricas de Goodhart** | investment e reporting | disciplina de identificação do arXiv:2607.12575 |
| 13 | **SSRF/LFI via metadata de discovery** | Bazaar `$ref`/`$id` do x402 | JSON Pointer same-document apenas; rejeição de IP-literal/loopback (CWE-918) |
| 14 | **Comprometimento de chave do agente** | AP2 Autonomous; chaves EOA do SIWX | key binding; o Agent Provider MUST NOT expor a chave de assinatura ao Agente |
| 15 | **Captura de standards body / governança** | x402 Foundation 40 membros; MPP Stripe-controlado; UCP Google+Shopify+Stripe | neutralidade LF (x402); processo multi-vendor da FIDO (AP2); **independência do MPP é a questão aberta** |

---

---

## Relacionados
- [[x402|x402]] · [[mpp|MPP]] — onde os ataques foram medidos
- [[ap2|AP2]] — threat model e limites criptográficos
- [[visa|Visa]] — o vetor do merchant falsificado
- [[mastercard|Mastercard]] — biometria on-device e Verifiable Intent
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
