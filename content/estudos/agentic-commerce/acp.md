---
title: "ACP — Agentic Commerce Protocol"
description: "Agentic Commerce Protocol (OpenAI + Stripe): checkout agentic com Shared Payment Token e discovery gateado por plataforma."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# ACP — Agentic Commerce Protocol

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camada 2 — commerce
> Protocolo de checkout agentic mantido por OpenAI e Stripe, com Shared Payment Token e discovery gateado por plataforma.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

- Site: <https://www.agenticcommerce.dev/>
- Repo: <https://github.com/agentic-commerce-protocol/agentic-commerce-protocol>
- Docs Stripe: <https://docs.stripe.com/agentic-commerce/acp>
- Apache 2.0, **status beta**, exige CLA.
- **Founding Maintainers: OpenAI e Stripe.** TSC (7 assentos): OpenAI, Stripe,
  Meta.

### Linha do tempo de releases

`2025-09-29` (inicial) → `2025-12-12` (fulfillment) → `2026-01-16` (capability
negotiation) → `2026-01-30` (extensions, discounts, payment handlers) →
**`2026-04-17`** (cart, feed, orders, authentication, **MCP**) — estável atual.

CLA corporate assinada: Stripe + OpenAI em 2025-11-21; Meta em 2026-03-19;
**PayPal em 2026-04-16**.

### Building blocks

Agentic checkout (create/update/complete sessions), cart & feed, **delegate
payment** (payment handlers passam tokens), **delegate authentication**
(OAuth 2.0), orders + webhooks. **Shared Payment Token (SPT)**: "Securely pass
payment credentials from your buyers to AI agents, without exposing underlying
payment credentials." Stripe é o primeiro PSP compatível, mas o desenho é
PSP-agnostic.

Transporte: REST **ou MCP**. *"Publish your checkout configuration with a
traditional API or MCP. ACP works with any integration pattern."*

### A fraqueza estrutural: discovery

Do próprio site: *"We're working to create discovery mechanisms for AI
platforms to identify businesses that have implemented ACP."* E a participação
é **gateada por plataforma**: "each AI platform will manage their own process
for how businesses can participate. If your business wants to participate in
ChatGPT, you'll need to apply."

Isso é uma diferença real frente ao UCP, onde discovery é permissivo e
autodescritivo.

### O movimento do PayPal é strategicamente importante

PayPal anunciou (2025-10-28) que adotaria ACP para ChatGPT, trazendo catálogos
de pequenos negócios *e* marcas, via **"PayPal's ACP server"** — *"a trusted,
scalable, and compliant access layer to a global network of merchants that will
not require individual merchant integrations."* PayPal gerencia merchant
routing, payment validation e orchestration.

> [!important] Isso é uma assimetria de postura frente ao UCP
> **PayPal construiu um proxy/intermediário em vez de pedir que merchants
> implementem ACP.** No UCP, o merchant implementa o protocolo. São dois
> modelos de fundamentally diferentes: *merchant-implements* vs.
> *platform-intermediates*. Se você é merchant, isso é uma decisão de negócio
> central, não um detalhe.

### A reversão estratégica da OpenAI

Lançado 2025-09-29 para o Instant Checkout no ChatGPT (vendedores Etsy nos
EUA). Em **2026-03-06** a OpenAI moveu o Instant Checkout para dentro de Apps
e pivoteou para **product discovery**, com transações via apps
próprios dos varejistas. (CNBC 2026-03-20; DigitalCommerce360;
análise da Checkout.com.)

> [!tip] Como ler isso
> O **ACP sobreviveu**; a UX de checkout hostil ao merchant não sobreviveu. A
> lição para decisões: em agentic commerce, **quem tem o poder de CHANGEAR o
> fluxo de checkout é a plataforma, e ela pode mudar de ideia**. Construa
> business logic que não dependa de uma única superfície.

---

## Relacionados
- [[ucp|UCP]] — o concorrente de camada 2, com discovery permissivo
- [[mastercard|Mastercard]] · [[visa|Visa]] — Credenciais que processam os tokens do ACP
- [[x402|x402]] · [[mpp|MPP]] — settlement para agentes pagando agentes
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
