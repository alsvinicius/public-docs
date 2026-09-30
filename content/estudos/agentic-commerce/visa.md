---
title: "Visa — Intelligent Commerce e Trusted Agent Protocol"
description: "Intelligent Commerce e Trusted Agent Protocol: enforcement em nível de rede e assinaturas merchant-scoped."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# Visa — Intelligent Commerce e Trusted Agent Protocol

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camadas 3 e 1
> A oferta da Visa: enforcement em nível de rede e assinaturas merchant-scoped. A peça de discovery/anti-bot que o AP2 deixou de fora.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

### Visa Intelligent Commerce (VIC) — 2025-04-30

Lançado no Visa Global Product Drop, SF. Parceiros: Anthropic, IBM, Microsoft,
Mistral, OpenAI, Perplexity, Samsung, Stripe.

Quatro serviços integrados (docs do developer):

- **Tokenization** — *"A new pass-through payment token, specific to agents,
  that is intended for use at Visa-accepting merchant locations."*
- **Authentication** — step-up verification do titular + **Passkey** que
  autentica as Payment Instructions.
- **Payment Instructions** — *"new controls to ensure that payment credential
  requests match the user's authenticated instructions and to **validate that
  authorizations received by VisaNet match the original instruction**."*
- **Signals** — commerce signals para resolução rápida de disputas.

Fluxo (7 passos, docs): agent onboarding → agent-specific tokens (com step-up +
Passkey) → manage payment instructions → autenticar instruction via Passkey →
retrieve payment credentials (validados contra a instruction) → pay at merchant
(inicialmente guest checkout / key entry) → **implement transaction controls at
VisaNet** → share commerce signals.

> [!important] A diferenciação da Visa é a **enforcement em nível de rede**
> A cláusula *"authorizations received by VisaNet match the original
> instruction"* e o *"controls will be enforced to ensure that the request
> originates from the intended merchant for the correct amount"* não são
> asserções do lado do agente — são **controles da rede**. Isso é
> estruturalmente mais forte que uma declaração criptográfica que ninguém
> fora da rede verifica. É o argumento mais forte que existe em favor da Visa
> em agentic commerce, e vale citar exatamente assim.

**Visa MCP Server**: *"a ready-made integration layer for AI agents to securely
access Visa's capabilities… Starting with Visa Intelligent Commerce APIs."*
Faz bridge para VIC APIs, Visa Token Service (VTS) e Visa Developer Platform.
Reference agent público: <https://github.com/visa/vic-reference-agent>.

> [!note] A Visa konstruiu a peça de **discovery/anti-bot** que o AP2 deixou de fora
> Merchant sites historically classificam tráfego automatizado como bot e
> bloqueiam. A Visa resolve isso com o **Trusted Agent Protocol (TAP)**,
> co-desenvolvido com Cloudflare, com **reference implementation pública**
> (<https://github.com/visa/trusted-agent-protocol>).

### Visa Trusted Agent Protocol

- Announced 2025-10-17. <https://developer.visa.com/capabilities/trusted-agent-protocol/overview>

Mecanismo: **assinaturas merchant-specific, purpose-specific e time-bound**,
*"cannot be replayed or relayed."* Três categorias:

**Verifiable Information**
- *Agent Intent* — que este é um agente Visa confiável com intenção de buscar
  detalhes ou comprar um produto específico daquele merchant.
- *Consumer Recognition* — token ID de conta/loyalty do merchant, device
  identifiers de interação prévia, country/postal para restrições, endereço
  de wallet.

**Payment Information** — três modos:
- **Key Entry** — passa **credencial VIC hasheada** + metadata de cartão (card
  art). **O agente nunca envia PAN.**
- **API/protocol-based** — token + endereço de entrega/faturamento.
- **IOUs** — *"Information needed to manage balances and settlements between
  agents and merchants, **bringing merchants supplemental content revenue
  beyond traditional models like ads and upsells**."*

> [!tip] A propriedade criptográfica que importa
> **Merchant-scoped + purpose-scoped + time-bound + non-replayable +
> non-relayable.** Isso é estritamente mais forte que identidade genérica de
> agente, e é a resposta de facto ao "trusted list" que o AP2 declaradamente
> não resolveu. Se você está avaliando um "quem é este agente?", esta é a
> resposta mais concreta disponível hoje.

### Visa × OpenAI (2026-06-10)

Anunciado no Visa Payments Forum, SF — **o mesmo dia** do AP4M da Mastercard.
A Visa "will provide its global network, credentialing capabilities and
security infrastructure to support agentic commerce experiences." Detalhes
específicos (integração em ChatGPT/Codex, spending limits) vêm de fontes
secundárias, não do release da Visa.

---

## Relacionados
- [[mastercard|Mastercard]] — o contrapeso mais próximo
- [[fido|FIDO]] — Mastercard e Visa presidem o Payments TWG
- [[ap2|AP2]] — a camada de prova de intenção que a Visa implementa de outro jeito
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
