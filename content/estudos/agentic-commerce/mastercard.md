---
title: "Mastercard — Agent Pay, Verifiable Intent e AP4M"
description: "Agent Pay, Verifiable Intent e AP4M: Agentic Tokens, registro de agente e settlement multi-rail."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# Mastercard — Agent Pay, Verifiable Intent e AP4M

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camadas 3 e 4
> A oferta da Mastercard: tokens agentic, registro de agente, prova de intenção e settlement multi-rail.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

### Agent Pay (2025-04-29)

Lançado com parceiros Microsoft, IBM, Braintree, Checkout.com. Quatro pilares:

1. **Registrar e autenticar agentes confiáveis** — agentes devem ser
   *registered and verified* antes de transacionar.
2. **Transações seguras** — tokenização estendida; *"Every player in the value
   chain, from consumers to issuers and merchants, will be able to recognize
   the transactions that are facilitated by intelligent agents."*
3. **Regras claras de controle do consumidor** — o consumidor controla o que o
   agente pode comprar.
4. **Proteção a fraude** — biometria on-device + processo para transações
   agentic desconhecidas.

Primitiva central: **Mastercard Agentic Tokens**, evolução da tokenização que já
opera contactless e card-on-file. P positioning: *"Only registered agents can
transact — governed and traceable with Mastercard network tokens."*

> [!warning] Cuidado com o que o release de 2025 diz e o que não diz
> O release **não** especifica mecanismo criptográfico — nenhum esquema de
> assinatura, nenhum mandate, nenhum VC. "Network token ligado
> criptograficamente a agente verificado" é **caracterização razoável, não
>_statement literal_.** A história crypto explícita da Mastercard é a camada
> posterior, separada, chamada **Verifiable Intent**.

Também: o CPO Jorn Lambert disse que a Mastercard quer *"advance the standards
for agentic payments, such as applying the Model Context Protocol to Secure
Remote Commerce"* — ou seja, a contribuição da Mastercard é uma **extensão de
MCP sobre o SRC existente**, não um protocolo novo.

### Verifiable Intent

Camada de autorização: *"Purpose-built for agentic commerce, ensuring every
transaction is verified by authenticated user intent and explicit consent
before an action is taken."* Descrita como **AP2-compatible**, e doada à FIDO.

Três pilares: *Know your agent*, *Verifiable Intent*, *interface standards*
("a universal data exchange protocol enabling seamless, scalable
personalization").

> [!note] Convergência de vocabulário
> A Mastercard usa a **mesma expressão** que o AP2 — "Verifiable Intent". A
> Mastercard converge para o enquadramento do AP2 sem reclamar autoria. É a
> evidência mais forte de que o AP2 é o framework vencedor na camada 3.

### Agent Pay for Machines — AP4M (2026-06-10)

Serviço separado, para micropagamentos agente-a-agente e machine-to-machine.
Quatro capacidades: **Credentialing** (todo agente é credentialed, e com
Verifiable Intent é reconhecível cross-ecosystem), **Permissioning** (regras
de autorização e spending limits **programmaticamente enforced**),
**Transacting**, **Settling** — *"reliable, guaranteed **multi-rail settlement
across cards, accounts and stablecoins**"*.

Posicionamento: *"Where Agent Pay defines how trusted AI agents participate in
payments, Agent Pay for Machines is designed for a complementary opportunity:
automated, micro- and machine-driven transactions."*

**30+ parceiros**, incluindo Adyen, Ant International, BVNK, Checkout.com,
Cloudflare, Coinbase, Global Payments, **Stripe**, **Tempo**, Solana
Foundation, Polygon, OKX, Aave Labs, Anchorage, Crossmint, MoonPay, Rain,
RippleX, t54 Labs, Turnkey, Utila, Nevermined, Sapiom, Skyfire, Catena, Basis
Theory, Coinflow, PayOS, Getnet/Santander, Alchemy, Lovable Labs,
Mastercard Merchant Cloud.

> [!tip] Duas leituras de negócio
> 1. A Mastercard está atacando o **outro lado** do mercado do UCP: o
>    "agent buying agent for compute/API", que o UCP (orientado a merchant
>    of record) não endereça.
> 2. Ela está explicitamente **abrindosettlement multi-rail** — isso é a
>    convergência com x402/MPP assumida em público, e é o sinal mais forte de
>    que "cart rail vs stablecoin" virou falsa oposição.

---

## Relacionados
- [[visa|Visa]] — o contrapeso mais próximo
- [[ap2|AP2]] — convergência de vocabulário em "Verifiable Intent"
- [[fido|FIDO]] — Mastercard e Visa presidem o Payments TWG
- [[x402|x402]] · [[mpp|MPP]] — os rails que a Mastercard quer federar
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
