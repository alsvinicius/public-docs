---
title: "Agentic Commerce — overview"
description: "As quatro camadas, o mapa dos protocolos, a matriz de decisão por papel, 20 perguntas para discussão técnica e a timeline consolidada."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# Agentic Commerce — overview

[[estudos/agentic-commerce/index|← Agentic Commerce]]

Mapa, decisões e framing. **Não é** a especificação — para o mecanismo de cada
protocolo, veja as notas individuais.

> [!info] Como esta pasta está organizada
> - **Esta nota** — as quatro camadas, mapa dos protocolos, matriz de decisão por
>   papel, perguntas para discussão, timeline consolidada e o que **não** está
>   verificado.
> - **Uma nota por protocolo** — a spec a fundo. Ver
>   [[estudos/agentic-commerce/index|Agentic Commerce]] para a lista.
>
> Estado em **2026-09-29**.

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

## 1. As quatro camadas

| Camada | Pergunta que responde | Protocolos |
|---|---|---|
| **1. Identidade e descoberta** | Quem é este agente? Confio nele? | [[visa|Visa]] Trusted Agent Protocol, Agentic Tokens (MC), WBA, [[mcp-a2a|MCP-A2A]] Agent Cards |
| **2. Comércio / orquestração** | Como eu acho produtos, monto carrinho, faço checkout? | **[[ucp|UCP]]**, **[[acp|ACP]]** |
| **3. Autorização / prova de intenção** | Como provo que o *usuário* aprovou este valor, neste merchant? | **[[ap2|AP2]]** (SD-JWT mandates), [[mastercard|Mastercard]] Verifiable Intent, [[visa|Visa]] Payment Instructions |
| **4. Settlement / rail** | Como os bytes de valor andam? | **[[x402|x402]]**, **[[mpp|MPP]]**, tokens de rede, rails de cartão |

Composição canônica: **AP2 (ou UCP+AP2) dá consentimento, escopo e evidência de
disputa; x402 ou MPP move o dinheiro.** O agente ganha um mandato limitado e
comprovável, e então gasta sobre HTTP 402.

> [!tip] Como usar isso numa reunião
> Quando alguém diz "nós vamos usar X", pergunte: **em qual camada?** 90% dos
> debates improdutivos de agentic commerce são disputes de camada 2 fingindo
> ser disputes de camada 4.

---

---

## 2. Mapa dos protocolos (uma tela cada)

| Protocolo | Camada | Quem mantém | Estado | Para que serve |
|---|---|---|---|---|
| **[[ucp|UCP]]** | 2 — commerce | Google + Shopify (Stripe no council) | **Produção**, v2026-08-25, verticals em expansão | Catálogo → cart → checkout → order, merchant-of-record preservado, discovery permissivo |
| **[[ap2|AP2]]** | 3 — autorização | Google; **doado à [[fido|FIDO]]** (2026-04-28) | v0.2; **SDK ainda em dev** | Prova criptográfica de que o usuário aprovou *este valor, neste checkout* |
| **[[acp|ACP]]** | 2 — commerce | OpenAI + Stripe (TSC: +Meta) | Beta, `2026-04-17` | Checkout agentic com **Shared Payment Token**; discovery **gateado por plataforma** |
| **[[mastercard|Mastercard]] Agent Pay / AP4M** | 3 + 4 | Mastercard | Produção (2025-04-29 / 2026-06-10) | Agentic Tokens, registro de agente, Verifiable Intent, **settlement multi-rail** |
| **[[visa|Visa]] VIC / TAP** | 3 + 1 | Visa (TAP com Cloudflare) | Deploying; ref. impl. pública | Payment Instructions com **enforcement na VisaNet**; assinaturas merchant-scoped |
| **[[x402|x402]]** | 4 — settlement | x402 Foundation (**Linux Foundation**), 40 membros | Spec v2, volume fino | HTTP 402, stablecoins, permissionless facilitators |
| **[[mpp|MPP]]** | 4 — settlement | Stripe + Tempo (**sem foundation**) | 2026-03-18, volume mínimo | HTTP 402 com Challenge–Credential–Receipt, **cobertura de rails muito maior** |
| **[[fido|FIDO]] TWGs** | 1 + 3 | FIDO Alliance | Criado 2026-04-28 | Onde a identidade de agente e a prova de intenção estão **realmente** consolidando |

> [!tip] Como escolher por camada
> - Compra de produto físico por um shopper agent → **UCP** (+ AP2 se quiser
>   prova de consentimento) + Visa/MC tokens.
> - Compra de API/dados/compute entre agentes → **x402** ou **MPP** (+ AP2 para
>   escopo).
> - "Quem é este agente?" → **Visa TAP** ou as trust lists da FIDO. Não o AP2.

> [!warning] O número que vai te enganar
> Todo mundo vai te mostrar "100M+ de transações agentic" no x402. O paper
> peer-reviewed mediu **136,7M settlements** e decomposição, e a demanda
> genuína fica entre **\$188 mil e \$20,3 milhões** — duas ordens de grandeza de
> intervalo. Contadores medem *manufacturability*, não adoption. Ver
> [[x402|x402]] — detalhe §7.2.

---

---

## 3. Matriz de decisão

### 3.1 Se você é merchant / varejista

| Pergunta | Resposta 2026 |
|---|---|
| Qual implementar primeiro? | **UCP.** É o único com escopo de comércio completo (catalog→cart→checkout→order), discovery permissivo, merchant-of-record preservado, e MCP + A2A + REST. |
| Preciso implementar AP2 separado? | Não — vem como **extensão** do UCP (`dev.ucp.common.payment.ap2_mandate`). AP2 standalone ainda não tem SDK. |
| Preciso implementar ACP? | Só se um cliente específico (ChatGPT) exigir. Compete pelo *seu* tempo de engenharia; o ACP é merchant-of-record via SPT/delegate payment. |
| Devo me worries com x402/MPP? | Só se você vende API/dados/compute. Não se você vende produto físico. |
| Merchant of Record? | Preserve. Se um parceiro de plataforma propuser ser *merchant of record* em nome seu, isso é uma migração de risco, não um detalhe de onboarding. |

### 3.2 Se você é plataforma de IA / agent builder

| Decisão | Recomendação |
|---|---|
| Protocolo de commerce | **UCP** (multi-vertical, múltiplos transports, mais recente, mais PMPs) **e** ACP se ChatGPT for o canal material. Suporte a ambos é o custo deinsurance. |
| Consentimento | **MCP Apps** (SEP-1865) para a Trusted Surface. Não deixe o agente desenhar a tela de consentimento. |
| Pagamento | Handler UCP + AP2 mandates para prova; x402 ou MPP se micro/machine payments. |
| Política de gasto | **Em código, junto ao cliente de pagamento.** Nunca em prompt. Default de \$1. |
| Merchant onboarding | Prefira UCP (permissivo) a ACP (gateado por plataforma). |

### 3.3 Se você é PSP / acquirer / provider de credencial

- O ponto de inserção no UCP é o **Payment Handler** — você publica a spec,
  o merchant configura, a platform executa. É literalmente o seu trabalho
  empacotado num JSON Schema versionado.
- A **Trust Triangle** do UCP existe para que você não precise tocar o merchant.
  Aproveite.
- Este é o layer onde PayPal e Ant International estãovos mais ativos
  (Payments TC do UCP).

### 3.4 Se você é investidor / decide alocação

| Bet | Status |
|---|---|
| Infra de autenticação de agente (FIDO) | **Melhor posicionado.** Presido por Mastercard+Visa+Google+OpenAI+PayPal. |
| UCP adoption | Forte, porque a governança é Google+Shopify+Stripe+Amazon. |
| x402 como economia | **Cuidado.** Contadores são Goodhart. Demanda real é 2-3 ordens abaixo do número bruto. |
| MPP vs x402 | MPP tem cobertura de método de pagamento e compliance stack; x402 tem neutralidade. Nenhum dos dois tem economia ainda. |
| Agentic identity / reputation | **Espaço em aberto** — cf. IOU do Visa TAP, `extension-offer-and-receipt` do x402. |

---

---

## 4. Perguntas para uma discussão técnica de referência

**Sobre UCP:**
1. Onde exatamente a **versioning de capabilities** diverge da versioning de
   protocolo, e o que acontece quando um vendor extension exige uma versão de
   capability que você não suporta?
2. Como você implementa o **Algorithm de interseção** quando o array de versões
   do seu peer tem formatos diferentes do seu?
3. Seu `/.well-known/ucp` é servível? `Cache-Control: public, max-age>=60`,
   sem 3xx, com ETag. Você auditou isso?
4. Seus webhooks estão assinados? (MUST)
5. Como você lida com `Actions` de terceiros — seu `id` é estável no
   throughout o lifecycle do recurso?
6. Você implementa `Request Constraints` como preflight, ou deixa o round-trip?
7. O que você faz quando um `schema` URL de uma capability viola o
   Authority Binding? (MUST NOT fetch, MUST reject.)

**Sobre AP2:**
1. `cnf` no mandato aberto: como é a rotação de chave PoP do agente?
2. E o conflito ECDSA-vs-Ed25519 (#268)? Qual leitura você implementa?
3. Em Autonomous mode, você **tem** um receipt de rejeição do mandato anterior
   antes de emitir o próximo?
4. Qual é o seu plano se o seu provedor de identidade de agente não está em
   nenhuma trust list — porque **não existe trust list no AP2**.
5. O seu Delegate SD-JWT é *RFC* ou você está na dependência de individual
   draft? (AP2 depende de um draft individual para o chaining — risco de
   maturidade real.)

**Sobre segurança:**
1. Em que momento do seu fluxo o serviço é liberado — **antes** ou **depois**
   do settlement? Se antes, você tem um "free shopping".
2. Seus nonces são reservados atomicamente? (E em Solana, você tem um
   `SettlementCache`? RPC Solana retorna "success" para duplicatas.)
3. Você allowlista as formas de transação ERC-1271/6492, ou aceita o que vier?
4. Sua política de gasto está em código ou no prompt do sistema?
5. Você tem canal de denúncia de fraude que **não** passa pelo agente?

**Sobre negócio:**
1. Se a plataforma de IA que é seu maior canal de agentic commerce amanhã
   mudar de estratégia (como a OpenAI fez em 2026-03), o que quebra? Sua
   business logic está em qual superfície?
2. Você aceita que um *counterfeit merchant* use seu agente como proxy de
   credencial? O que muda se o seu merchant endpoint **não** é verifiable?
3. Quem é o merchant of record no seu fluxo agentic, e quem tem o first-party
   data?
4. Se sua única caminho de descoberta for UCP, o que acontece se o Google
   decide mudar a política de ordenação ou de fees?
5. Seu Merchant Center feed já está limpo? O UCP usa os feeds existentes do
   Merchant Center para discovery — o seu já está? (É o menor lift de
   integração possível.)

---

---

## 5. Linha do tempo

| Data | Evento |
|---|---|
| 2025-04-29 | **Mastercard Agent Pay** (Agentic Tokens) |
| 2025-04-30 | **Visa Intelligent Commerce** (VIC) no Global Product Drop |
| 2025-09-04 | Visa MCP Server + Acceptance Agent Toolkit (ambos pilot) |
| 2025-09-16 | **Google anuncia AP2** |
| 2025-09-29 | **ACP spec inicial** (OpenAI + Stripe), open source |
| 2025-10-17 | **Visa Trusted Agent Protocol** (com Cloudflare) |
| 2025-10-28 | PayPal anuncia adoção de ACP para ChatGPT + "PayPal's ACP server" |
| 2025-11-21 | CLA de ACP assinada por Stripe + OpenAI |
| 2025-12-12 | ACP v2 (fulfillment) |
| 2026-01-11 / 01-23 | **UCP v2026-01-11**, **v2026-01-23** |
| 2026-01-16 / 01-30 | ACP — capability negotiation; extensions/discounts/payment handlers |
| 2026-01-20 | **Mastercard entra no UCP**; Agent Pay → Copilot Checkout |
| 2026-03-06 | **OpenAI move Instant Checkout para Apps**; pivô para discovery |
| 2026-03-15 | Stripe + Tempo lançam **MPP** |
| 2026-03-19 | Meta assina CLA de ACP (assento 3 do TSC) |
| 2026-04-16 | **PayPal assina CLA de ACP** |
| 2026-04-17 | ACP — cart, feed, orders, auth, **MCP** |
| 2026-04-24 | UCP Tech Council → 16 assentos (Amazon, Meta, Microsoft, Stripe, Salesforce) |
| 2026-04-28 | **Stripe entra no Governing Council do UCP**; **AP2 doado à FIDO**; AP2 v0.2.0 |
| 2026-06-10 | **Mastercard AP4M** — e, **no mesmo dia**, **Visa × OpenAI** |
| 2026-07-14 | x402 Foundation operacional na Linux Foundation (40 membros) |
| 2026-07-16 | UCP **Food TC** formado |
| 2026-08-11 | UCP **Lodging TC** formado |
| 2026-08-17 | A2A entra no Agentic AI Foundation (AAIF) |
| 2026-08-25 | **UCP v2026-08-25** (3DS2, multi-vertical, grocery, versioning independente) |
| 2026-09-02 | UCP **Payments TC** formado (PayPal sim; Mastercard/Visa não) |

> [!note] O padrão nas datas
> As duas maiores Jogadas de 2026 — AP4M da Mastercard e o deal Visa×OpenAI —
> caíram no **mesmo dia**. Isso é rivalidade de mindshare, não de
> arquitetura. E o movimento de 2026-06 já é Explicit multi-rail.

---

---

## 6. ⚠️ Não verificado / não citar sem checar

1. **Anúncio OpenAI+PayPal de abril/2025** ("Instant Checkout"): não
   recuperável em fonte primária. Fontes secundárias datam de "late April
   2025". O primeiro primário verificável é **2025-10-28** (adoção).
2. **"Mastercard MCP server"** — confirmado que a Mastercard *defende* MCP; um
   **artefato MCP publicado da Mastercard** não foi confirmado. (A Visa tem,
   desde 2025-09.)
3. **"Visa Tokenized Agentic Commerce"** — nenhum produto com esse nome. O
   produto real da Visa é "AI-ready cards" / agent-specific payment tokens
   dentro do VIC. Provável confusão.
4. **Detalhes do deal Visa×OpenAI** (integração em ChatGPT/Codex, spending
   limits) vêm de fontes secundárias, não do release da Visa.
5. **Data exata** em que a Mastercard entrou no UCP: o texto diz "last week"
   numa nota de 2026-01-20. Tratar como ~2026-01-13 a 2026-01-20.
6. **"Binding criptográfico" em Agent Pay** é inferência. O release de 2025
   fala em registro/verificação, network tokens e biometria on-device — nunca
   em esquema de assinatura ou VC.
7. **Números de adoção do x402** além de arXiv / Visa-Artemis / x402stats.
   Os sites de comparação discordam entre si por ordens de grandeza.
8. **Independência da governança do MPP** — não verificada; aparenta ser
   Stripe+Tempo sem foundation.
9. **Delegate SD-JWT** é individual draft (Gareth Oliver, 2026), não RFC — e o
   chaining de mandates do AP2 depende dele.
10. **AP2 A2A extension na v0.2** — `docs/a2a-extension.md` existe na v0.1.0
    e está ausente na v0.2.0.
11. **SDK / MCP server do AP2** — o FAQ do AP2 diz que ainda estão em
    desenvolvimento. Nenhum SDK AP2 production-grade confirmado.
12. **Trusted-agent list do AP2** — uma frase normativa; o resto é aspiracional
    delegado à camada de commerce ou à FIDO.
13. **Meta como co-autor do ACP** — os docs da Stripe dizem Stripe+OpenAI+Meta;
    o badge de maintainer no GitHub diz "OpenAI & Stripe". O `governance.md`
    confirma Meta no TSC seat 3, mas como *membro*, não Founding Maintainer.
14. **AP2-over-MCP** — nenhuma configuração entregue encontrada.
15. **OWASP Top 10 for Agentic Applications 2026** (2025-12-09) — os itens
    individuais estão atrás de form; **não atribuir rankings específicos**.
16. **Surveys comerciais gated** (Darwinium, Ravelin, Ballerine, Maximus
    Labs) — inacessíveis; as figuras circulando online não são verificáveis.
17. **Long tail de protocolos** (ACK-Pay, FADP, Swarmwage, L402, AEP2, OSL
    AgentPay) — sem fontes primárias; conteúdo SEO de comparação. **Excluído.**

---

---

---

## Relacionados
- [[estudos/agentic-commerce/index|Agentic Commerce]] — mapa, camadas e matriz de decisão
- [[ucp|UCP]] — o protocolo mais maduro em escopo
- [[ap2|AP2]] — a camada de prova de intenção
- [[seguranca|Segurança]] — leia antes de dimensionar risco
