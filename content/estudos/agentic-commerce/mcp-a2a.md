---
title: "MCP e A2A em comércio"
description: "MCP e A2A como transportes: binding, delegação e lifecycle. Nenhum dos dois é protocolo de pagamento."
date: 2026-09-29
tags:
  - "estudo"
  - "agentic-ai"
  - "agentic-commerce"
  - "protocolos"
---

# MCP e A2A em comércio

[[estudos/agentic-commerce/index|← Agentic Commerce]]

> [!info] Camada transporte
> Substratos de transporte e lifecycle. MCP é o binding mais usado; A2A é delegação. Nenhum dos dois é protocolo de pagamento.
> Estado em **2026-09-29**. Para o mapa completo dos protocolos e as decisões de
> negócio, ver [[estudos/agentic-commerce/index|Agentic Commerce]].

---

**MCP** — core protocol version `2026-07-28`. Extensões oficiais: `ext-auth`
(OAuth client credentials, enterprise-managed authz), **`ext-apps` (MCP Apps,
SEP-1865)**, `ext-tasks`, `ext-skills`.

**MCP Apps** é o primitivo natural de **superfície de consentimento** para
agentic payments: iframe sandboxed com `postMessage` bidirecional,
`_meta.ui.csp` allowlist, capacidades host-gated. O iframe
*"prevents your app from accessing the parent window's DOM, reading the host's
cookies or local storage, navigating the parent page, or executing scripts in
the parent context."*

> [!warning] Gap real
> **Não existe extensão de pagamentos no core do MCP.** A proposta de
> ferramentas pagas via x402 ([issue #3393](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3393))
> foi **fechada como "not planned"** em 2026-09-26. Pagamentos chegam ao MCP
> por quatro vias **fora do core**: transporte x402-MCP, transporte UCP-MCP,
> MCP do ACP, transporte MPP-MCP. E mais um comercial: o MCP Server da Visa.
>
> Não encontrei fonte primária descrevendo **AP2-over-MCP** como configuração
> entregue. Trate como gap, não como capacidade.

**A2A** — Apache 2.0, doado à **Linux Foundation** em 2025-06-23; em 2026-08-17
aceito como projeto Growth Stage do **Agentic AI Foundation**, junto com MCP.
150+ organizações. Escopo explícito: *"Not an agent development kit… Not a
replacement for MCP… Not a sub-agent or tool-call protocol."*

Papel em comércio: **substrato de transporte e lifecycle de task**, não
pagamentos. Contribuição: *Agent Cards* para discovery, delegação, streaming, e
`input-required` como máquina de estados de elicitação de pagamento.

> [!note] Regressão a acompanhar
> O `docs/a2a-extension.md` do AP2 existe na tag **v0.1.0** e está **ausente na
> v0.2.0**, enquanto os samples ainda usam A2A. O binding A2A do AP2 parece
> ter sido **removido ou adiado**.

---

## Relacionados
- [[ucp|UCP]] — MCP como um dos transports do UCP
- [[x402|x402]] · [[mpp|MPP]] — pagamentos como binding sobre MCP, fora do core
- [[ap2|AP2]] — Trusted Surface e o gap de AP2-over-MCP
- [[estudos/agentic-commerce/index|← Agentic Commerce]]
