---
title: "AP2 — Agent Payments Protocol"
description: "Agent Payments Protocol do Google: como provar que o usuário aprovou este valor, neste merchant — com constraints criptográficas fail-closed."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# AP2 — Agent Payments Protocol

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camada 3 — autorização
> Prova criptográfica de que o usuário aprovou *este valor, neste checkout*. A camada mais interessante tecnicamente.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

Camada 3. É a peça mais interessante tecnicamente e a mais subestimada.

- Spec: <https://ap2-protocol.org/>
- Repo: <https://github.com/google-agentic-commerce/AP2>
- v0.1.0 em 2025-09-16 (Google, com PayPal, Mastercard, Amex, Cloudflare,
  Coinbase, Stripe). **v0.2.0 em 2026-04-28.**
- **Doado à FIDO Alliance** em 2026-04-28, para padronização nos TWGs de
  Agentic Authentication e Payments.

### A premissa honesta

Do documento de segurança do AP2, e essa é a frase mais importante de todo o
ecossistema:

> "AP2 assumes that preventing prompt injection attacks is infeasible.
> Therefore, all LLMs and Agents MUST be considered potential attackers."

E: *"when either role is agentic, then the Agent itself is a potential
attacker. As such, additional tamper-evident mechanisms are needed."*

A resposta do AP2 **não é tentar impedir injeção** — é limitar
criptograficamente o *blast radius* financeiro. Um agente injetado pode escolher
um produto pior dentro dos limites, mas não ultrapassar os limites.

### Cinco papéis

1. **Shopping Agent (SA)** — discovery, cart, execução
2. **Credential Provider (CP)** — emite credenciais; verifica que o agente pode
   *acessar* a credencial e a escopa
3. **Merchant (M)** — dono do catálogo; verifica o Checkout Mandate
4. **Merchant Payment Processor (MPP)** — processa; verifica que a credencial
   está autorizada para *este* checkout
5. **Trusted Surface (TS)** — a UI de consentimento. **MUST be non-agentic.**

Uma entidade pode plays múltiplos papéis. Toda validação MUST acontecer em
código determinístico, independentemente de o papel ser agentic ou não.

### Mandates: taxonomia evoluiu, cuidado com material antigo

**v0.1** usava `Cart Mandate` (human present) e `Intent Mandate` (human not
present). **v0.2 reestruturou** para **dois tipos × dois estados**:

| | Verificado por | Significa |
|---|---|---|
| **Checkout Mandate** (aberto) | Merchant | agente autorizado a montar o carrinho |
| **Checkout Mandate** (fechado) | Merchant | autorização do *checkout finalizado* |
| **Payment Mandate** (aberto) | CP / Network / MPP | agente autorizado a pagar aquele checkout |
| **Payment Mandate** (fechado) | CP / Network / MPP | valor amarrado ao checkout finalizado |

Praticamente todo material secundário ainda descreve a taxonomia v0.1. Se
alguém na reunião falar "Intent Mandate", está lendo de 2025.

### A cadeia de prova (o mecanismo real)

```
user-signed OPEN mandate  (constraints[] + cnf{RFC7800} com PoP key do agente)
        ↓  kb-sd-jwt  (typ: kb+sd-jwt)
agent-signed CLOSED mandate  (sd_hash → open; checkout_hash → Checkout JWT)
        ↓
Verifier → signed Mandate Receipt { iss, result, reference, error? }
```

Pontos que valem citar tecnicamente:
- **`cnf` (RFC 7800) é obrigatório** no mandato aberto: liga a chave de
  prova de posse do agente.
- O **mandato fechado de pagamento é embutido dentro da credencial de
  pagamento** — é assim que o MPP verifica o escopo.
- **Selective disclosure** é o ponto: o agente só apresenta as divulgações
  necessárias, e constraints desconhecidas **falham** a avaliação (fail-closed).
- Anti-double-spend: um Shopping Agent MUST NOT apresentar mandato aberto
  subsequente sem ter recebido um *rejection receipt* do anterior.
- Modos: **Direct** (human present) e **Autonomous** (human not present, com
  mandates abertos e assinatura posterior do agente). Verificadores **sempre**
  recebem mandato fechado; só o caminho de verificação muda.
- Um fluxo HNP **pode ser rebaixado** para HP via erro
  `unresolved_constraint`.

### Constraints do mandato aberto

Checkout: `allowed_merchants`, `line_items` (com `acceptable_items`
divulgáveis seletivamente). A avaliação é especificada como **problema de
fluxo máximo** — limitação explícita: *"does not support splitting the open
Checkout Mandate across multiple Checkouts."*

Payment: `agent_recurrence` (ON_DEMAND/DAILY/WEEKLY/… + `max_occurrences`),
`allowed_payees`, `allowed_payment_instruments`, `allowed_pisps` (com domínio
eIDAS QWAC), `amount_range`, `budget` (teto cumulativo), `reference`,
`execution_date`.

> [!tip] A contribuição mais subestimada do AP2
> A distinção **mandato aberto vs. fechado** é o mecanismo de
> **atribuição de responsabilidade** mais novo já produzido por qualquer
> desses padrões. Em modo Autonomous, você **difa o comportamento real do
> agente contra as constraints assinadas pelo usuário** e atribui o desvio
> com precisão. O princípio declarado: responsabilidade cai numa entidade
> real (usuário, merchant, issuer) "e só cai no agente se uma decisão
> *load-bearing* do agente for determinada como errada."

### Threat model — cinco, não quatro

| # | Ameaça | Mitigação |
|---|---|---|
| 1 | **Manipulated Checkout** — replay de mandato assinado contra checkout não relacionado | `transaction_id` / `payment.reference`; `sd_hash`; `cnf`; merchant verifica `checkout_hash` == hash do último `checkout_jwt` |
| 2 | **Manipulated Payment** — agente altera pagamento em trânsito | MPP + CP MUST verificar assinatura do usuário; `checkout_hash` dentro de `transaction_id` |
| 3 | **Payment Credential Theft** — token roubado usado em contexto errado | token só liberado **após** receipt + verificação de mandato final |
| 4 | **Manipulated Discovery** — injeção faz o agente escolher produto malicioso | assinatura do merchant garante integridade da oferta; constraints limitam pior caso |
| 5 | **Double Spend** — agente aprova checkouts sobrepostos de um mandato aberto | receipt-gated issuance; CP/Network/MPP MAY rejeitar mandates sobrepostos |

**Hardening de rainbow table** (não óbvio): digests SD-JWT precisam de sal;
`checkout_hash` depende da entropia da assinatura, então o Checkout JWT **MUST**
usar esquema **não-determinístico (ECDSA), não Ed25519**. A Trusted Surface
pode inserir decoy digests.

> [!warning] Inconsistência viva do AP2
> `specification.md` diz "classe de algoritmo (ECDSA)"; o doc de segurança diz
> "regra de entropia, satisfeita por qualquer algoritmo com entropia suficiente
> no payload". Rastreado em AP2 [#268](https://github.com/google-agentic-commerce/AP2/issues/268).
> Sob a leitura de entropia, a mesma chave serviria para AP2 e Web Bot Auth.

### Trusted lists de agentes — ⚠️ em grande parte aspiracional

Este é o ponto mais mal especificado do AP2, e o material secundário exagera.

- O que a spec v0.2 diz, **no total**: uma frase. Em modo Direct, a assinatura
  do mandato fechado "is validated as coming from a User directly, using a User
  Credential or a **trust list of Agent Providers**."
- O doc de Implementação Considerations diz: *"These details are left to the
  Commerce Protocol layer."*
- v0.1 [[seguranca|Segurança]] chamava "Real Time Trust Establishment" de **problema em aberto** e
  "Issuance of Trusted Public Keys" de *"a crucial question… Establishing these
  'roots of trust' is a critical area for innovation."*

**Não existe registro de agentes confiáveis nativo do AP2.** Na prática esse
trabalho foi terceirizado para as **redes de cartão** ([[mastercard|Mastercard]] e [[visa|Visa]]) e para o **Payments
TWG da FIDO** (presidido por Mastercard e Visa).

### UCP ↔ AP2

Flow: business anuncia `dev.ucp.common.payment.ap2_mandate` no
`/.well-known/ucp` → ativação de sessão → business retorna
`ap2.merchant_authorization` (JWS detached content sobre o checkout
canonicalizado em JCS, **assinando header e payload** para impedir
substituição de algoritmo) → sessão fica **"Security Locked"** (não há retorno a
checkout padrão) → plataforma obtém dois credenciais → business e PSP verificam.

Erros: `mandate_required`, `agent_missing_key`, `mandate_invalid_signature`,
`mandate_expired`, `mandate_scope_mismatch`, `merchant_authorization_invalid`,
`merchant_authorization_missing`.

**Estado real:** o FAQ do AP2 diz que **SDK e MCP server ainda estão em
desenvolvimento**. AP2 standalone é, hoje, essencialmente demos +
padronização na FIDO. **UCP+AP2 é o veículo de produção.**

---

## Relacionados
- [[ucp|UCP]] — onde o AP2 roda como extensão (`dev.ucp.common.payment.ap2_mandate`)
- [[mastercard|Mastercard]] · [[visa|Visa]] — implementações de prova de intenção em nível de rede
- [[fido|FIDO]] — para onde o AP2 foi doado
- [[seguranca|Segurança]] — o threat model do AP2 em contexto
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
