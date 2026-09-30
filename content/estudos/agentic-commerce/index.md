---
title: "Agentic Commerce"
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
  - "indice"
---

# Agentic Commerce

[[estudos/index|← Estudos]]

Trilha de estudo sobre os **protocolos de comércio por agentes de IA**. Estado em
**2026-09-29**. Uma nota por protocolo, mais os overviews.

> [!important] A tese em uma frase
> Não existe "o protocolo de agentic commerce". Existem **quatro camadas
> ortogonais** que cada fornecedor combina de um jeito. Errar de protocolo é
> quase sempre erro de camada. E o jogo em 2026 **não é guerra de padrões**:
> Visa, Mastercard, Stripe, Google, PayPal, Coinbase e Amex estão todos nos
> mesmos consórcios ao mesmo tempo.

> [!warning] Correção factual importante
> A premissa comum ("ACP = Mastercard + Visa + PayPal; a Mastercard tem
> protocolo próprio rival") está **errada**:
> - ACP (*Agentic Commerce Protocol*, agenticcommerce.dev) é mantido por
>   **OpenAI e Stripe** (Founding Maintainers). TSC: OpenAI, Stripe, Meta.
>   PayPal assinou a CLA em 2026-04-16 e é adopter, não founder.
>   ([governance.md](https://raw.githubusercontent.com/agentic-commerce-protocol/agentic-commerce-protocol/main/docs/governance.md))
> - **Nem Mastercard nem Visa são mantenedores, membros do TSC ou signatários da
>   CLA do ACP.**
> - A Mastercard se define como *colaboradora*: o texto dela diz "**OpenAI's**
>   Agentic Commerce Protocol". E **entrou no UCP como endossadora** em
>   jan/2026.
>
> Consequência prática: as redes escolheram **cooptar, não construir rival**.

---

## Como percorrer esta trilha

A ordem cronológica dos anúncios é enganosa — as redes anunciaram em 2025-04, o
Google e a OpenAI em 2025-09, e a maior jogada de 2026 (AP4M) aconteceu **no
mesmo dia** do deal Visa×OpenAI. A ordem abaixo é a ordem em que cada nota
**renderiza** a anterior.

```
As 4 camadas  (o mapa mental — sem isso, todo o resto é decoreba)
   ↓  "ok, o UCP é o mais maduro. Por quê?"
UCP
   ↓  "e como ele prova que o usuário aprovou?"
AP2  ──────────────┐
   ↓               │  "e as redes de cartão, então?"
Mastercard ── Visa ┘
   ↓  "as duas Decoder-only? — não: o ACP"
ACP
   ↓  "e quem é a gente? Não é o AP2."
FIDO
   ↓  "e para agente pagando API?"
x402 ── MPP
   ↓  "e os transportes?"
MCP-A2A
   ↓
Segurança   (leia antes de dimensionar risco)
```

### Trilha A — entender a paisagem (leitura histórica)

1. [[overview|overview]] — as quatro camadas, mapa, matriz de decisão, timeline
2. [[ucp|UCP]] — o protocolo mais maduro; **a nota mais longa da trilha**
3. [[ap2|AP2]] — a camada de prova de intenção (a peça mais interessante
   tecnicamente)
4. [[acp|ACP]] — o outro caminho de camada 2, e a reversão da OpenAI
5. [[mastercard|Mastercard]] · [[visa|Visa]] — as ofertas das redes
6. [[fido|FIDO]] — onde isso realmente consolidou
7. [[x402|x402]] · [[mpp|MPP]] · [[mcp-a2a|MCP-A2A]] — settlement e transportes
8. [[seguranca|Segurança]] — leia por último, mas **não pule**

### Trilha B — decidir o que implementar (prática)

| Você é… | Leia nesta ordem |
|---|---|
| **Merchant / varejista** | [[overview|overview]] (matriz §3.1) → [[ucp|UCP]] (§1.4 modelo de pagamento) → [[seguranca|Segurança]] |
| **Plataforma de IA / agent builder** | [[overview|overview]] (§1 camadas) → [[ucp|UCP]] → [[ap2|AP2]] → [[mcp-a2a|MCP-A2A]] (consent surface) → [[seguranca|Segurança]] |
| **PSP / acquirer** | [[overview|overview]] → [[ucp|UCP]] (§1.4) → [[x402|x402]] → [[mpp|MPP]] |
| **Investidor** | [[overview|overview]] (§2 mapa) → [[fido|FIDO]] → [[seguranca|Segurança]] → [[x402|x402]] (§7.2 adopters) |

> [!tip] O atalho de 3 minutos
> [[overview|overview]] §1 (as quatro camadas) + §2 (mapa) + §3 (matriz de decisão). Isso
> cobre 80% das conversas de decisão de negócio. O resto é para quando alguém
> challenger um número.

---

## As notas

### 0. Orientação

- [[overview|overview]] — as quatro camadas, mapa dos protocolos, matriz de decisão por
  papel (merchant, plataforma, PSP, investidor), 20 perguntas para discussão
  técnica, timeline consolidada e **17 itens não verificados**.

### 1. Camada 2 — comércio

- [[ucp|UCP]] — Universal Commerce Protocol (Google + Shopify). **Produção**,
  v2026-08-25. O mais maduro em escopo: catálogo → cart → checkout → order.
  Discovery permissivo, merchant-of-record preservado, Trust Triangle, payment
  handlers, `Binding`/`Actions`/`Request Constraints`.
- [[acp|ACP]] — Agentic Commerce Protocol (OpenAI + Stripe, TSC + Meta). Beta.
  Shared Payment Token, discovery **gateado por plataforma**, e a reversão
  estratégica da OpenAI em 2026-03.

### 2. Camada 3 — autorização e prova de intenção

- [[ap2|AP2]] — Agent Payments Protocol (Google, doado à [[fido|FIDO]]). v0.2. A premissa
  é que **prompt injection é inevitável**; a resposta é limitar o blast radius
  por constraints criptográficas fail-closed. O **diffing mandato aberto vs.
  fechado** é a única contribuição real de atribuição de responsabilidade já
  produzida por qualquer um desses padrões.
- [[mastercard|Mastercard]] — Agent Pay, Verifiable Intent, AP4M. Agentic Tokens, registro
  de agente, settlement multi-rail.
- [[visa|Visa]] — Intelligent Commerce e Trusted Agent Protocol. **Enforcement em
  nível de rede** (autorizações na VisaNet casam com a Payment Instruction
  autenticada por Passkey) e assinaturas merchant-scoped, purpose-scoped,
  time-bound, non-replayable.

### 3. Camada 4 — settlement e machine payments

- [[x402|x402]] — HTTP 402, stablecoins, permissionless facilitators. Linux
  Foundation, 40 membros. Spec v2. **Atenção:** adoption economicamente fina,
  apesar dos números brutos.
- [[mpp|MPP]] — Stripe + Tempo. Mesmo HTTP 402, modelo Challenge–Credential–Receipt,
  cobertura de rails muito maior. **Sem foundation** — a questão de governança
  aberta.

### 4. Camada 1 + 3 — onde está consolidando

- [[fido|FIDO]] — Agentic Authentication TWG e **Payments TWG (presidido por
  Mastercard e Visa)**. Criado 2026-04-28, semeado com AP2 e Verifiable Intent.
  O desenvolvimento de governança mais importante do setor.

### 5. Transporte

- [[mcp-a2a|MCP-A2A]] — MCP é o binding mais usado; A2A é delegação e lifecycle.
  **Nenhum dos dois é protocolo de pagamento** — pagamentos chegam por
  transports, fora do core do MCP.

### 6. Transversal

- [[seguranca|Segurança]] — os papers peer-reviewed, o vetor do merchant falsificado, o
  gap de responsabilidade e um registro consolidado de 15 riscos.

---

## As quatro camadas

| Camada | Pergunta que responde | Notas |
|---|---|---|
| **1. Identidade e descoberta** | Quem é este agente? Confio nele? | [[visa|Visa]] (TAP), [[mastercard|Mastercard]] (Agentic Tokens), [[fido|FIDO]] |
| **2. Comércio / orquestração** | Como eu acho produtos, monto carrinho, faço checkout? | [[ucp|UCP]], [[acp|ACP]] |
| **3. Autorização / prova de intenção** | Como provo que o *usuário* aprovou este valor, neste merchant? | [[ap2|AP2]], [[mastercard|Mastercard]], [[visa|Visa]] |
| **4. Settlement / rail** | Como os bytes de valor andam? | [[x402|x402]], [[mpp|MPP]] |

Composição canônica: **AP2 (ou UCP+AP2) dá consentimento, escopo e evidência de
disputa; x402 ou MPP move o dinheiro.** O agente ganha um mandato limitado e
comprovável, e então gasta sobre HTTP 402.

> [!tip] Como usar isso numa reunião
> Quando alguém diz "nós vamos usar X", pergunte: **em qual camada?** A maior
> parte dos debates improdutivos de agentic commerce são disputes de camada 2
> fingindo ser disputes de camada 4.

---

## Mapa rápido

| Protocolo | Camada | Quem mantém | Estado | Para que serve |
|---|---|---|---|---|
| [[ucp|UCP]] | 2 | Google + Shopify (Stripe no council) | Produção, v2026-08-25 | Comércio end-to-end, merchant-of-record preservado |
| [[ap2|AP2]] | 3 | Google; doado à FIDO | v0.2; SDK ainda em dev | Prova de que o usuário aprovou este valor, neste checkout |
| [[acp|ACP]] | 2 | OpenAI + Stripe (TSC: +Meta) | Beta, `2026-04-17` | Checkout agentic com Shared Payment Token |
| [[mastercard|Mastercard]] | 3 + 4 | Mastercard | Produção (2025-04-29 / 2026-06-10) | Tokens agentic, registro, Verifiable Intent, multi-rail |
| [[visa|Visa]] | 3 + 1 | Visa (TAP com Cloudflare) | Deploying; ref. impl. pública | Enforcement na VisaNet; assinaturas merchant-scoped |
| [[x402|x402]] | 4 | x402 Foundation (Linux Foundation) | Spec v2, volume fino | HTTP 402, stablecoins, facilitators permissionless |
| [[mpp|MPP]] | 4 | Stripe + Tempo (sem foundation) | 2026-03-18, volume mínimo | HTTP 402 com Challenge–Credential–Receipt |
| [[fido|FIDO]] | 1 + 3 | FIDO Alliance | Criado 2026-04-28 | Onde identidade de agente e prova de intenção consolidam |

> [!warning] O número que vai te enganar
> Todo mundo vai te mostrar "100M+ de transações agentic" no x402. O paper
> peer-reviewed mediu **136,7M settlements** com decomposição, e a demanda
> genuína fica entre **\$188 mil e \$20,3 milhões** — duas ordens de grandeza de
> intervalo. Contadores medem *manufacturability*, não adoption. Ver [[x402|x402]].

---

## Referências primárias

**Specs e repos**
- UCP: <https://ucp.dev/latest/specification/overview/> ·
  <https://github.com/Universal-Commerce-Protocol/ucp> ·
  Google: <https://developers.google.com/merchant/ucp/>
- AP2: <https://ap2-protocol.org/> · <https://github.com/google-agentic-commerce/AP2>
- ACP: <https://www.agenticcommerce.dev/> ·
  <https://github.com/agentic-commerce-protocol/agentic-commerce-protocol> ·
  Stripe: <https://docs.stripe.com/agentic-commerce/acp>
- x402: <https://docs.x402.org/> · MPP: <https://mpp.dev/>
- MCP: <https://modelcontextprotocol.io/extensions/overview> ·
  A2A: <https://a2a-protocol.org/latest/>

**Vendor**
- Mastercard Agent Pay e AP4M (investor.mastercard.com) · Visa VIC e TAP
  (developer.visa.com, corporate.visa.com) · FIDO (fidoalliance.org)

**Papers**
- <https://arxiv.org/abs/2607.19545> — USENIX Sec 2026, segurança em x402
- <https://arxiv.org/abs/2605.11781> — Five Attacks on x402
- <https://arxiv.org/abs/2607.12575> — medição de adoption do x402 (Goodhart)

---

## Relacionados
- BERT — Índice — outro estudo com estrutura de índice-guia (duas trilhas)
- TDC São Paulo 2026 — conceitos — origem: talk "Agentic Commerce" (Edson
  Yanaga, Google), TDC SP 2026
- OmniRoute — AI Gateway; interação com padrões de tool-calling
- [[estudos/index|← Estudos]]
