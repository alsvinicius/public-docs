---
title: "UCP — Universal Commerce Protocol"
description: "Universal Commerce Protocol (Google + Shopify): catálogo, carrinho, checkout e order em produção, com merchant-of-record preservado."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# UCP — Universal Commerce Protocol

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camada 2 — commerce
> Protocolo de comércio end-to-end para agentes: catálogo, cart, checkout, order. O mais maduro em escopo.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

O mais maduro em escopo de comércio. Apache 2.0, open source, spec versionada
por data (`YYYY-MM-DD`).

- Spec: <https://ucp.dev/latest/specification/overview/>
- Repo: <https://github.com/Universal-Commerce-Protocol/ucp>
- Versão atual: **v2026-08-25**. Releases: `2026-01-11`, `2026-01-23`,
  `2026-04-08`, `2026-08-25`.
- Adoção no Google: AI Mode no Search, Gemini. Integração **Native** (default)
  ou **Embedded** (iframe, opcional, para merchants aprovados).
  <https://developers.google.com/merchant/ucp/>

### Princípios de design (os que importam em decisão)

1. **Merchant of Record preservado.** O merchant continua sendo o merchant of
   record, dono dos dados e da relação. Isso é a principal arma comercial do UCP
   frente ao ACP — que também promete merchant-of-record, mas via *delegate
   payment* / Shared Payment Token, o que é um arranjo diferente.
2. **Permissive discovery + controls.** Um merchant pode aceitar qualquer
   plataforma que cumpra o protocolo. Não há whitelist obrigatória
   (diferente de "apply to participate" no ACP).
3. **Business logic preservado.** Primitivas 1:1 com operações de varejo
   existentes, para reduzir lift de integração.
4. **Vendor-neutral extensions.** Qualquer um publica capability própria sob
   reverse-domain próprio.

### Modelo de discovery e negociação

- Business publica perfil em **`/.well-known/ucp`**.
- Platform anuncia o URI do perfil via header **`UCP-Agent`**.
- O perfil serve **duas funções ao mesmo tempo**: (a) declarar capabilities e
  (b) publicar chaves de assinatura. É também um JWK Set (RFC 7517) — o
  `keys[]` de topo é o campo canônico de chaves.

**Authority Binding** — o detalhe de segurança mais importante do discovery:
o *host* da URL `schema` de uma capability **deve** casar, reversed, com o
namespace reverso do nome. Ex.: `dev.ucp.shopping.checkout` precisa de schema
servido de `ucp.dev`. Rejeita `com.example.pay` com schema em `evil.example`.
Isso é **proveniência, não confiança** — prova que quem publica o namespace
controla o domínio, não que a entity é confiável. E o check é sobre hostname,
**não** sobre o endereço resolvido: a proteção contra SSRF/DNS rebinding é um
controle separado e independente, sobre o endereço resolvido.

**Intersection Algorithm** (negociação capabilities):
1. Interseção por nome de capability.
2. Versão: interseção dos arrays de versão; escolhe a **maior**; se vazia,
   exclui a capability.
3. Poda extension órfãs: `extends` definido mas nenhum pai na interseção →
   remove. Multi-parent: basta um pai presente.
4. Repete a poda até convergir (cobre cadeias transitivas).

**Versioning** é data-based, e a **versionação de capabilities é independente**
da versão do protocolo (introduzido em `2026-08-25`).

### Capabilities e extensões

Capabilities (raiz): `dev.ucp.shopping.checkout`, `dev.ucp.shopping.cart`,
`dev.ucp.shopping.catalog`, `dev.ucp.shopping.order`,
`dev.ucp.common.identity_linking`, `dev.ucp.common.location`, e
`dev.ucp.shopping.permalink`.

Extensions: `discount`, `fulfillment`, `buyer-consent`, `loyalty`,
**`dev.ucp.common.payment.ap2_mandate`**, `payment.authentication`,
`payment.terms` (pagamento diferido — crucial para lodging), `split-payments`.

**Schema composition** com `allOf`: schemas de extensão **devem** declarar
`$defs["dev.ucp.shopping.checkout"]` etc. e **não podem** definir campos
inline nos transports. Transports referenciam só schemas base.

Namespaces: `dev.ucp.*` reservado ao governance do UCP. `com.{vendor}.*` e
`org.{org}.*` para terceiros. Payload de namespace do protocolo é o
`ucp:` wrapper em toda resposta.

### Modelo de pagamento (o coração técnico do UCP)

O problema resolvido é o **N-para-N** entre platforms, businesses e credential
providers. Solução: separar **Payment Instruments** (o que é aceito) de
**Payment Handlers** (como processado).

**Trust Triangle** — a platform não deve tocar credencial crua:
1. Business ↔ Credential Provider: relação legal/técnica pré-existente.
2. Platform ↔ Credential Provider: a platform tokeniza, mas não é dona do fundo.
3. Platform ↔ Business: a platform entrega token ou mandato.

**Divisão de trabalho:**
| Papel | Ação |
|---|---|
| **Credential Provider** | **Define a spec** — publica o "blueprint" (JSON Schema) do handler |
| **Business** | **Configura o handler** — escolhe e publica `config` (chaves públicas, merchant IDs) |
| **Platform** | **Executa o protocolo** — lê config, executa a spec, adquire o token |

Distinção crítica que todo mundo erra: **provider = entidade** (Google Pay,
Shop Pay); **handler = especificação** (`com.google.pay`, `dev.shopify.shop_pay`).

**Ciclo de vida em 3 passos:**
1. **Negotiation** — business anuncia `payment_handlers` no perfil.
2. **Acquisition** — platform ↔ credential provider, client-side/agent-side.
   O business **não** participa; dado cru nunca toca o frontend do business.
3. **Completion** — platform envia a credencial opaca ao business, que captura
   via backend.

**PCI scope:** fluxo **unidirecional** Platform → Business (business MUST NOT
ecoar credenciais), credenciais opacas (não PAN), e `handler_id` no payload
para evitar key confusion.

**Cenários concretos na spec:** A) Digital Wallet; B) Direct Tokenization com
challenge SCA/3DS (`requires_escalation` + `continue_url`); C) Autonomous Agent
via AP2.

**`Binding`** — conceito que é a defesa real contra replay no UCP: associação
lógica de um instrumento a um recurso de capability específico, por `type`+`id`.
"A credential que era para o recurso X não pode ser interceptada e usada no Y."

**`Actions`** — unidade de trabalho pendente definida por extensão, que **gata**
um efeito. Aberto apenas em respostas. Um exemplo da spec: verificação
estudantil que postpone o desconto ao completion. Cada tipo de Action é um
reverse-domain próprio, e `id` **não pode** ser reusado durante a vida do
recurso. `Messages` explicam; `Actions` travam. Orthogonal ao status do lifecycle.

**`Request Constraints`** — o business sinaliza, em resposta autoritativa, quais
regras vai aplicar no *próximo* request (ex.: "billing_address obrigatório",
"quantidade em passos exatos de 100"). Grammar JSON Schema Draft 2020-12
**restrito** a `required`/`properties`/`anyOf` no nível objeto e `enum`/`const`
no nível valor. Nada mais é admitido. Plataforma pode usar como preflight, mas
o veredito é do business.

**`Signals`** — dados de ambiente para fraud/rate limit. **MUST NOT** ser
claims do comprador: ou observação direta (IP, UA), ou atestação de terceiro
verificável criptograficamente com JWKS. Chaves reverse-domain.

**`Attribution`** — canal/campanha/click-id passando de platform para business.
UCP **não** prescreve modelo, janela ou lógica de atribuição. E o campo é
informacional: sua presença/ausência MUST NOT afetar resposta ou negociação.
(Consequência de negócio real: **você ainda precisa construir sua própria
atribuição**; o UCP só te dá o transporte do dado.)

**Identidade e auth:** HTTP Message Signatures (RFC 9421) é o mecanismo que
habilita onboarding permissionless. API key / OAuth / mTLS implicam
pré-acordo. **Identity binding:** com API key/OAuth/mTLS o verificador MUST
confirmar que o principal autenticado está autorizado a agir em nome do perfil
do `UCP-Agent`. Webhooks **MUST** ser assinados.

**Transports:** REST (OpenAPI 3.x), **MCP** (OpenRPC), **A2A** (Agent Card),
**Embedded** (OpenRPC). Múltiplos bindings, um por transport, com `version`
obrigatória. UCP *define* MCP como transport próprio — não é um MCP extension.
(Consequência: **AP2 mandates over MCP é combinação não suportada** — a
extensão AP2 é de UCP, não de MCP.)

### Governança do UCP (leitura de poder, não de marketing)

- **Governing Council**: Google + Shopify (permanentes) + **Stripe (2026-04-28)**,
  mais 2 assentos eletivos abertos.
- **Tech Council**: 16 assentos. Em 2026-04-24 entraram **Amazon, Meta,
  Microsoft, Stripe, Salesforce**.
- **Technical Councils por vertical:**
  - **Food TC** (2026-07-16): Block/Square, DoorDash, Google, Toast, Uber Eats
  - **Lodging TC** (2026-08-11): Amadeus, Booking.com, Expedia, Google, Hilton,
    Marriott, Trip.com
  - **Payments TC** (2026-09-02): **Adyen, Ant International, Coinbase, Global
    Payments, Google, PayPal, Shopify, Stripe**

> [!note] A assimetria que importa
> **Mastercard e Visa são *endossadoras* do UCP, não governantes.** PayPal é
> mais fundo: tem assento no **Payments TC** *e* é signatário da CLA do ACP
> *e*, via Stripe, tem assento no Governing Council do UCP. As redes
> endossam; não dirigem. Se sua estratégia depende de influenciar a direção do
> protocolo, UCP não é o fórum onde as redes te ouvem.

Participantes (site do UCP): *co-developed* em Shopping = Google, **Shopify**,
Etsy, Wayfair, Target, Walmart, **Amazon**, **Microsoft**, **Meta**,
**Salesforce**, **Stripe**. *Endorsed* inclui **Mastercard, Visa, PayPal,
Stripe**, Adyen, Affirm, Amex, Block, Fiserv, Klarna, SAP, Worldpay, VTEX,
Carrefour, Flipkart, Shopee, Zalando, entre outros.

### Roadmap declarado

- **Loyalty & member benefits** (via account linking)
- **Native cross-sell/upsell** por contexto do usuário
- **Local & omnichannel**: BOPIS, store locators, grocery
- **Global markets**: rollout em India, APAC, LatAm
- **Novas verticales**: Food (spec em breve), Lodging (draft — booking com
  schedules de pagamento `immediate`/`deferred`, política de cancellation
  como objeto, termos de lodging)

> [!tip] O que usar para falar de decisão de negócio
> - "O UCP é merchant-of-record-first." Contra o argumento de que agentic
>   commerce necessariamente significa perder o cliente.
> - "O discovery é permissivo." Ninguém precisa de whitelist sua loja.
> - "O custo é sua superfície de API." Catalog + Cart + Checkout + Order + perfil
>   em `/.well-known/ucp` com schemas correctos e assinatura de webhook.

---

## Relacionados
- [[ap2|AP2]] — camada de prova de intenção que o UCP consome como extensão
- [[visa|Visa]] · [[mastercard|Mastercard]] — tokens agentic que o merchant pode aceitar
- [[acp|ACP]] — o concorrente de camada 2
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
