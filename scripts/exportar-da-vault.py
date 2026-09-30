#!/usr/bin/env python3
"""Exporta notas da vault Obsidian para o site Quartz público.

    python3 scripts/exportar-da-vault.py [caminho-da-vault]

O destino é `content/estudos/agentic-commerce/`, e o resultado é sempre
sobrescrito a partir da vault — nunca edite os arquivos gerados à mão.

Regras:
  - slug de arquivo (sem acento/espaço), porque o Quartz resolve wikilink por slug
  - wikilinks para notas publicadas viram o slug
  - wikilinks para notas privadas perdem o link mas preservam o texto
  - remove marcadores %% ai-session %% (vazam caminho interno da vault)
"""

import json
import os
import re
import sys

VAULT = sys.argv[1] if len(sys.argv) > 1 else "/home/vinicius/Documents/vini"
SRC = os.path.join(VAULT, "estudos")
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")

# slug de arquivo no site, por nome original
SLUGS = {
    # o hub é o index.md da pasta: se fosse agentic-commerce.md colidiria com o
    # slug da própria pasta e a página sairia 404
    "Agentic Commerce — Índice": "estudos/agentic-commerce/index",
    "overview": "overview",
    "UCP": "ucp",
    "AP2": "ap2",
    "ACP": "acp",
    "Mastercard": "mastercard",
    "Visa": "visa",
    "FIDO": "fido",
    "x402": "x402",
    "MPP": "mpp",
    "MCP-A2A": "mcp-a2a",
    "Segurança": "seguranca",
}

# índice de estudos: landing page da pasta estudos/
ESTUDOS_LINK = "estudos/index"
ESTUDOS_FILE = "index"

# o hub precisa de nome de arquivo diferente do slug usado nos wikilinks
HUB_FILE = "index"

# alvos que só aparecem em wikilink, nunca como arquivo de origem
EXTRA_LINKS = {"Estudos — Índice": ESTUDOS_LINK}

def wikilink_target(slug):
    """Slug cru: o registry do Quartz usa `pasta/index`, não `pasta`.

    Apontar para `pasta` resolve o href certo mas marca o link como quebrado,
    porque nenhum slug é exatamente `pasta`.
    """
    return slug

TITLES = {
    # "Índice" no título vira ruído fora da vault, onde a nota aparece na busca
    "estudos/agentic-commerce/index": "Agentic Commerce",
}

DESCRICOES = {
    "agentic-commerce": "Mapa de referência dos protocolos de comércio por agentes de IA: quatro camadas ortogonais, uma nota por protocolo e uma matriz de decisão por papel.",
    "overview": "As quatro camadas, o mapa dos protocolos, a matriz de decisão por papel, 20 perguntas para discussão técnica e a timeline consolidada.",
    "ucp": "Universal Commerce Protocol (Google + Shopify): catálogo, carrinho, checkout e order em produção, com merchant-of-record preservado.",
    "ap2": "Agent Payments Protocol do Google: como provar que o usuário aprovou este valor, neste merchant — com constraints criptográficas fail-closed.",
    "acp": "Agentic Commerce Protocol (OpenAI + Stripe): checkout agentic com Shared Payment Token e discovery gateado por plataforma.",
    "mastercard": "Agent Pay, Verifiable Intent e AP4M: Agentic Tokens, registro de agente e settlement multi-rail.",
    "visa": "Intelligent Commerce e Trusted Agent Protocol: enforcement em nível de rede e assinaturas merchant-scoped.",
    "fido": "Agentic Authentication TWG e Payments TWG: onde identidade de agente e prova de intenção estão consolidando.",
    "x402": "HTTP 402, stablecoins e facilitators permissionless — e por que os números brutos de adoção não significam o que parecem.",
    "mpp": "Stripe + Tempo: HTTP 402 com o modelo Challenge–Credential–Receipt e cobertura de rails muito maior que o x402.",
    "mcp-a2a": "MCP e A2A como transportes: binding, delegação e lifecycle. Nenhum dos dois é protocolo de pagamento.",
    "seguranca": "Os papers peer-reviewed, o vetor do merchant falsificado, o gap de responsabilidade e um registro consolidado de riscos.",
}

# notas que NÃO vão para o site: o wikilink é desfeito, o texto permanece
PRIVADAS = {
    "TDC São Paulo 2026 — conceitos",
    "OmniRoute",
    "Índice",
    "BERT — Índice",
    "Perspective-Based Reading",
    "Três Dívidas",
}

WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]*))?\]\]")
AI_SESSION = re.compile(r"^\s*%%\s*ai-session:.*?%%\s*$", re.M)

# nomes de nota não fazem sentido como texto de link fora da vault
DISPLAY = [
    ("Agentic Commerce — Índice", "Agentic Commerce"),
    ("Índice de Agentic Commerce", "Agentic Commerce"),
    ("Estudos — Índice", "Estudos"),
    ("Índice de Estudos", "Estudos"),
]


def escape_currency(text):
    r"""Escapa `$` de moeda fora de code spans.

    Sem isso o remark-katex abre math mode em `$188 mil e $20,3 milhões` e
    renderiza aquilo como fórmula. Dentro de crases não se mexe: `$ref` e
    `$id` do JSON Schema são literais.
    """
    parts = re.split(r"(`[^`]*`)", text)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"\$(?=\d)", r"\\$", parts[i])
    return "".join(parts)


def sync_h1(body, title):
    """Mantém o H1 do corpo igual ao title do frontmatter.

    Sem isso o site mostra dois títulos: um vindo do frontmatter (usado pelo
    cabeçalho da página) e outro do H1 no corpo.
    """
    def sub(m):
        return f"{m.group(1)} {title}"

    return re.sub(r"^(#+) .+$", sub, body, count=1, flags=re.M)


def yaml_scalar(value):
    """Aspas sempre: títulos e descrições contêm ': ' e quebram o YAML."""
    return json.dumps(value, ensure_ascii=False)


def clean_display(label):
    for original, public in DISPLAY:
        label = label.replace(original, public)
    return label


def resolve(target):
    """Devolve (novo_target, ainda_e_link)."""
    target = target.strip()
    if target in PRIVADAS:
        return None, False
    slug = SLUGS.get(target) or EXTRA_LINKS.get(target)
    if slug:
        return wikilink_target(slug), True
    # alvo dentro do próprio site mas com nome diferente do slug mapeado
    for original, s in SLUGS.items():
        if original.lower() == target.lower():
            return s, True
    return target, True


def rewrite_links(text):
    def sub(m):
        target, display = m.group(1), m.group(2)
        new, keep = resolve(target)
        label = clean_display(display if display else target)
        return f"[[{new}|{label}]]" if keep else label

    return WIKILINK.sub(sub, text)


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return {}, text
    end = text.index("\n---\n", 3)
    raw, body = text[4:end], text[end + 5 :]
    data, key = {}, None
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            data[key] = m.group(2)
        elif line.strip().startswith("- ") and key:
            data.setdefault("_list_" + key, []).append(line.strip()[2:])
        elif not line.strip() and key:
            continue
    return data, body


def build_frontmatter(slug, data):
    title = TITLES.get(slug) or data.get("title") or slug
    out = ["---", f"title: {yaml_scalar(title)}"]
    if slug in DESCRICOES:
        out.append(f"description: {yaml_scalar(DESCRICOES[slug])}")
    date = data.get("date")
    if date and re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        out.append(f"date: {date}")
    tags = data.get("_list_tags") or []
    if tags:
        out.append("tags:")
        out.extend(f"  - {yaml_scalar(t)}" for t in tags)
    # aliases só existem para cross-link dentro da vault; no site público viram
    # páginas de redirect na raiz e poluem o explorer
    out.append("---")
    return "\n".join(out) + "\n"


def convert(name, slug, dest_dir, filename=None, src_dir=None):
    src = os.path.join(src_dir or SRC, name + ".md")
    with open(src, encoding="utf-8") as fh:
        raw = fh.read()

    data, body = split_frontmatter(raw)
    body = AI_SESSION.sub("", body)
    body = rewrite_links(body)
    body = body.lstrip("\n")

    # remove linhas que sobraram apontando só para a vault privada
    kept = []
    for line in body.splitlines():
        s = line.strip()
        if s in {"← Índice de Projetos", "- ← Índice de Projetos"}:
            continue
        kept.append(line)
    body = "\n".join(kept)

    # corta separadores/code-fence vazios que a remoção das linhas deixou para trás
    body = re.sub(r"\n{4,}", "\n\n\n", body).rstrip() + "\n"
    body = escape_currency(body)

    fm = build_frontmatter(slug, data)
    if slug in TITLES:
        body = sync_h1(body, TITLES[slug])

    os.makedirs(dest_dir, exist_ok=True)
    out = os.path.join(dest_dir, (filename or slug) + ".md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(fm + "\n" + body)
    return out


def main():
    ac_dir = os.path.join(DST, "estudos", "agentic-commerce")
    ac_src = os.path.join(SRC, "agentic-commerce")
    written = [
        convert(
            original,
            slug,
            ac_dir,
            filename=HUB_FILE if original.startswith("Agentic Commerce") else None,
            src_dir=ac_src,
        )
        for original, slug in SLUGS.items()
    ]

    for path in written:
        print(os.path.relpath(path, DST))


if __name__ == "__main__":
    main()