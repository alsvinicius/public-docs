---
title: "MPP — Machine Payments Protocol"
description: "Stripe + Tempo: HTTP 402 com o modelo Challenge–Credential–Receipt e cobertura de rails muito maior que o x402."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# MPP — Machine Payments Protocol

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camada 4 — settlement
> Concorrente direto do x402, co-autorado por Stripe e Tempo. Mesma substrato HTTP 402, cobertura de rails muito maior.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

- <https://mpp.dev/> · lançado **2026-03-18**
- Stripe: <https://stripe.com/blog/machine-payments-protocol>

Mesmo substrato HTTP 402, arquitetura diferente: modelo
**Challenge–Credential–Receipt**, com campo `Credential` separado (vs.
payload/assinatura do x402). Papel de *relay* (o "facilitator" do x402).
Transportes: HTTP, **MCP/JSON-RPC**, WebSocket (streaming in-band).

**Cobertura de método de pagamento muito mais ampla que x402**: Tempo
stablecoins (TIP-20), **Stripe SPT (cartões)**, encrypted network tokens,
**Lightning/BOLT11**, EVM, Solana, XRP Ledger, Stellar SEP-41, Monad
(ERC-20 + ERC-3009), **NEAR Intents**, RedotPay, custom. Intents: charge,
**session** (pay-as-you-go com vouchers off-chain), subscription.

**Compatibilidade explícita com x402**: `x402/express.mpp`, `x402/hono.mpp`,
`x402/mcp.mpp`, `x402/next`, e um método `EVM` rodando "x402 exact flows".

Stripe: *"funds settle into a business's existing balance, in their default
currency, and on their standard payout schedule… tax calculation, fraud
protection, reporting, accounting integrations, and refunds."*

> [!warning] A diferença estrutural que decide a pergunta "quem ganha"
> x402 tem **neutralidade de Linux Foundation**. **MPP é Stripe + Tempo sem
> foundation** — a página de governança existe mas a independência não está
> verificada. Essa é a maior diferença entre os dois padrões HTTP 402, e é
> diferente de uma escolha técnica.
>
> Volume medido (Visa/Artemis, 2026-07-14, dados 2026-04-21): MPP ~**\$25.000
> em ~115.000 transações** nas primeiras semanas após 2026-03-15. x402 ~\$15,0M
> ajustado. *"On both, the average payment is a fraction of a cent."*

---

## Relacionados
- [[x402|x402]] — concorrente direto, mesma substrato HTTP 402
- [[mastercard|Mastercard]] — AP4M federa estes rails
- [[mcp-a2a|MCP-A2A]] — bindings de transporte
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
