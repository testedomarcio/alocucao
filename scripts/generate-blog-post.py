#!/usr/bin/env python3
"""
Generator script for A Locução blog articles.
Selects the next unpublished topic from data/blog-topics.json,
generates a structured HTML article, updates blog/index.html,
updates sitemap.xml, and marks the topic as published.
"""

import os
import sys
import json
import urllib.parse
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOPICS_PATH = os.path.join(ROOT_DIR, "data", "blog-topics.json")
BLOG_INDEX_PATH = os.path.join(ROOT_DIR, "blog", "index.html")
SITEMAP_PATH = os.path.join(ROOT_DIR, "sitemap.xml")

PHONE_NUMBER = "5527996529832"
BASE_URL = "https://alocucao.com.br"


def load_topics():
    if not os.path.exists(TOPICS_PATH):
        print(f"Error: Topics file not found at {TOPICS_PATH}")
        sys.exit(1)
    with open(TOPICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_topics(topics):
    with open(TOPICS_PATH, "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)


def generate_whatsapp_url(title, slug, custom_msg=None):
    if custom_msg:
        msg = custom_msg
    else:
        msg = f"Olá! Estava lendo o artigo '{title}' no blog da A Locução e gostaria de mais informações sobre locução comercial."
    encoded = urllib.parse.quote(msg)
    return f"https://wa.me/{PHONE_NUMBER}?text={encoded}"


def build_article_html(topic, today_str):
    title = topic["title"]
    slug = topic["slug"]
    eyebrow = topic.get("eyebrow", "Blog • A Locução")
    excerpt = topic.get("excerpt", "")
    reading_time = topic.get("reading_time", "7 min de leitura")
    main_keyword = topic.get("main_keyword", "locução comercial")
    commercial_url = topic.get("commercial_url", "https://alocucao.com.br/locucao-off/")
    commercial_focus = topic.get("commercial_focus", "locução off")
    sections = topic.get("sections", [])
    faq_items = topic.get("faq", [])

    article_url = f"{BASE_URL}/blog/{slug}/"
    wa_primary_url = generate_whatsapp_url(title, slug)
    wa_mid_url = generate_whatsapp_url(title, slug, f"Olá! Li o artigo sobre {main_keyword} e gostaria de orçar uma gravação para minha empresa.")

    # TOC items
    toc_html_list = []
    for i, sec in enumerate(sections, 1):
        sec_id = f"secao-{i}"
        toc_html_list.append(f'<li><a href="#{sec_id}">{sec["h2"]}</a></li>')
    if faq_items:
        toc_html_list.append('<li><a href="#perguntas-frequentes">Perguntas Frequentes (FAQ)</a></li>')
    toc_html = "\n".join(toc_html_list)

    # Sections HTML
    sections_html_list = []
    for i, sec in enumerate(sections, 1):
        sec_id = f"secao-{i}"
        sec_block = f'<h2 id="{sec_id}">{sec["h2"]}</h2>\n{sec["content"]}'
        sections_html_list.append(sec_block)

        # Insert intermediate conversion box after 2nd section
        if i == 2:
            mid_box = f'''
        <div class="conversion-box">
          <h2>Precisa de uma locução profissional para sua empresa?</h2>
          <p>A Locução oferece gravação rápida de offs comerciais e spots produzidos em poucas horas.</p>
          <div class="conversion-actions">
            <a class="btn btn-primary" href="{wa_mid_url}" target="_blank" rel="noopener" data-cta="blog_mid_whatsapp">Falar com A Locução pelo WhatsApp</a>
            <a class="btn btn-light" href="{commercial_url}">Conhecer {commercial_focus}</a>
          </div>
        </div>
'''
            sections_html_list.append(mid_box)

    sections_html = "\n\n".join(sections_html_list)

    # FAQ HTML & Schema
    faq_html_list = []
    faq_schema_graph = []
    for item in faq_items:
        q = item["question"]
        a = item["answer"]
        faq_html_list.append(f'<details><summary>{q}</summary><p>{a}</p></details>')
        faq_schema_graph.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    faq_html = "\n".join(faq_html_list)

    ld_json_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": f"{article_url}#artigo",
                "mainEntityOfPage": {"@type": "WebPage", "@id": article_url},
                "headline": title,
                "description": excerpt,
                "datePublished": today_str,
                "dateModified": today_str,
                "inLanguage": "pt-BR",
                "author": {"@type": "Organization", "name": "A Locução", "url": f"{BASE_URL}/sobre/"},
                "publisher": {"@type": "Organization", "name": "A Locução", "url": f"{BASE_URL}/"},
                "articleSection": topic.get("category", "Locução comercial"),
                "keywords": [main_keyword, commercial_focus, "locução profissional", "A Locução"]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Início", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE_URL}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": article_url}
                ]
            }
        ]
    }

    if faq_schema_graph:
        ld_json_data["@graph"].append({
            "@type": "FAQPage",
            "mainEntity": faq_schema_graph
        })

    schema_script = json.dumps(ld_json_data, ensure_ascii=False, indent=2).replace("<", "\\u003c")

    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
  <meta name="google-site-verification" content="WcO6J5Y4iflQpSpdu-w0tIuax-aBDPbO9-UM0hgKUFM">
  <script src="/assets/privacy.js" defer></script>
  <script src="/assets/tracking.js?v=20261016-hybrid" defer></script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} | A Locução</title>
  <meta name="description" content="{excerpt}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{article_url}">
  <meta name="theme-color" content="#0d1b2a">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{excerpt}">
  <meta property="og:url" content="{article_url}">
  <meta property="og:site_name" content="A Locução">
  <meta property="article:published_time" content="{today_str}">
  <meta property="article:modified_time" content="{today_str}">
  <meta name="twitter:card" content="summary">
  <link rel="stylesheet" href="/assets/blog.css">
  <script type="application/ld+json">
{schema_script}
  </script>
  <meta property="og:image" content="{BASE_URL}/assets/brand/icon-192.png">
  <link rel="stylesheet" href="/assets/contextual-cta.css">
  <link rel="stylesheet" href="/assets/site-layout.css?v=20261005-brand">
  <link rel="stylesheet" href="/assets/panel-commerce.css?v=20261005-retail-visual">
  <link rel="icon" href="/assets/brand/favicon-64.png?v=20261005" type="image/png" sizes="64x64">
  <link rel="icon" href="/favicon.ico?v=20261005" sizes="any">
  <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
  <link rel="stylesheet" href="/assets/hybrid-commerce.css?v=20261016">
</head>
<body data-order-channels="dual">
  <a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
  <div class="topbar">
    <div class="container">
      <span>✓ Vozes humanas e IA</span>
      <span>✓ Gravações rápidas</span>
      <span>✓ Atendimento em todo o Brasil</span>
    </div>
  </div>
  <!-- site-header:start -->
  <!-- site-header:end -->

  <main id="conteudo">
    <div class="container">
      <div class="breadcrumb" aria-label="Caminho da página">
        <a href="/">Início</a><span>›</span><a href="/blog/">Blog</a><span>›</span>{title}
      </div>
    </div>

    <section class="hero">
      <div class="container hero-grid">
        <div>
          <span class="eyebrow">{eyebrow}</span>
          <h1>{title}</h1>
          <p class="lead">{excerpt}</p>
          <div class="meta">
            <span>Por A Locução</span><span>•</span>
            <time datetime="{today_str}">{today_str}</time><span>•</span>
            <span>{reading_time}</span>
          </div>
        </div>
        <aside class="hero-proof" aria-label="Resumo do artigo">
          <strong>Atendimento rápido A Locução</strong>
          <p>Solicite a gravação do seu anúncio com entregas rápidas para rádio, TV e redes sociais.</p>
          <ul class="proof-list">
            <li>Locução Off a partir de R$ 11,90</li>
            <li>Spot comercial por R$ 29,90</li>
            <li>Atendimento direto pelo WhatsApp</li>
          </ul>
        </aside>
      </div>
    </section>

    <div class="container article-shell">
      <article class="article">
        <div class="answer-box">
          <p><strong>Resumo prático:</strong> {excerpt} Para solicitar o áudio da sua empresa com vozes profissionais, entre em contato direto com A Locução pelo WhatsApp.</p>
        </div>

        <nav class="toc" aria-label="Sumário do artigo">
          <strong>Neste artigo</strong>
          <ol>
            {toc_html}
          </ol>
        </nav>

        {sections_html}

        {f'<section class="faq" id="perguntas-frequentes" aria-labelledby="faq-title"><h2 id="faq-title">Perguntas frequentes</h2>{faq_html}</section>' if faq_items else ''}

        <div class="conversion-box">
          <h2>Solicitar minha locução pelo WhatsApp</h2>
          <p>Fale diretamente com nossa equipe, tire dúvidas sobre vozes humanas e IA, e faça seu pedido com rapidez.</p>
          <div class="conversion-actions">
            <a class="btn btn-primary" href="{wa_primary_url}" target="_blank" rel="noopener" data-cta="blog_final_whatsapp">Solicitar minha locução pelo WhatsApp</a>
            <a class="btn btn-light" href="{commercial_url}">Ver opções de {commercial_focus}</a>
          </div>
        </div>

        <div class="author">
          <div class="author-mark">AL</div>
          <div>
            <h2>A Locução</h2>
            <p>Produtora de áudio, locução off e spots comerciais com atendimento online para todo o Brasil. Vozes humanas e inteligência artificial.</p>
            <p><a href="{wa_primary_url}" target="_blank" rel="noopener">Falar com A Locução pelo WhatsApp</a> | <a href="/vozes/">Banco de Vozes Humana</a> | <a href="/vozes-ia/">Catálogo de Vozes IA</a></p>
          </div>
        </div>
      </article>

      <aside class="sidebar" aria-label="Atalhos e contratação">
        <div class="side-card">
          <h2>Solicite sua gravação</h2>
          <p>Envie seu roteiro pelo WhatsApp e receba suporte para escolher a voz ideal.</p>
          <a class="btn btn-primary" href="{wa_primary_url}" target="_blank" rel="noopener" data-cta="blog_sidebar_whatsapp">Falar pelo WhatsApp</a>
        </div>
        <div class="side-card">
          <h2>Serviços relacionados</h2>
          <a href="/locucao-off/">Locução Off Profissional</a>
          <a href="/spot-comercial/">Produção de Spot Comercial</a>
          <a href="/vozes/">Banco de Vozes Humana</a>
          <a href="/vozes-ia/">Banco de Vozes IA</a>
          <a href="/calculadora/">Calculadora de Duração</a>
        </div>
      </aside>
    </div>

    <section class="related">
      <div class="container">
        <h2>Próximos passos</h2>
        <div class="related-grid">
          <a class="related-card" href="/locucao-off/">
            <strong>Locução Off Profissional</strong>
            <span>Voz seca em alta qualidade por R$ 11,90 por crédito.</span>
          </a>
          <a class="related-card" href="/spot-comercial/">
            <strong>Spot Comercial Produzido</strong>
            <span>Anúncio finalizado com trilha e efeitos por R$ 29,90.</span>
          </a>
          <a class="related-card" href="/vozes/">
            <strong>Ouvir Demonstrações</strong>
            <span>Mais de 100 vozes humanas para comerciais e vinhetas.</span>
          </a>
        </div>
      </div>
    </section>
  </main>

  <!-- site-footer:start -->
  <!-- site-footer:end -->

  <div class="mobile-conversion-bar">
    <a class="btn btn-primary" style="background-color:#25D366;color:#fff;" href="{wa_primary_url}" target="_blank" rel="noopener" data-cta="blog_mobile_whatsapp">Solicitar minha locução pelo WhatsApp</a>
  </div>

  <script src="/assets/site.js?v=20261014"></script>
  <a class="panel-help-link" data-panel-support data-cta="whatsapp_flutuante" href="https://wa.me/{PHONE_NUMBER}" target="_blank" rel="noopener" aria-label="Faça seu pedido pelo WhatsApp">
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>
    </svg>
    <span>Faça seu pedido pelo WhatsApp</span>
  </a>
  <script src="/assets/site-layout.js?v=20261002" defer></script>
</body>
</html>
'''
    return html


def update_blog_index(topic, today_str):
    if not os.path.exists(BLOG_INDEX_PATH):
        print("Warning: blog/index.html not found.")
        return

    with open(BLOG_INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    slug = topic["slug"]
    title = topic["title"]
    eyebrow = topic.get("eyebrow", "Blog • A Locução")
    excerpt = topic.get("excerpt", "")
    article_url = f"/blog/{slug}/"

    card_html = f'''<a class="post-card" href="{article_url}" data-cta="blog_artigo_{slug.replace('-', '_')}"><div class="post-art" aria-hidden="true"><div class="sound-mark"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div></div><div class="post-copy"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{excerpt}</p><div class="meta"><time datetime="{today_str}">{today_str}</time></div><span class="post-link">Ler artigo completo →</span></div></a>'''

    # Insert card after <div class="container post-list">
    target = '<div class="container post-list">'
    if target in content and article_url not in content:
        content = content.replace(target, f'{target}{card_html}')
        with open(BLOG_INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated blog/index.html with card for {slug}")


def update_sitemap(slug, today_str):
    if not os.path.exists(SITEMAP_PATH):
        print("Warning: sitemap.xml not found.")
        return

    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    loc_url = f"{BASE_URL}/blog/{slug}/"
    if loc_url not in content:
        entry = f"  <url><loc>{loc_url}</loc><lastmod>{today_str}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n"
        content = content.replace("</urlset>", f"{entry}</urlset>")
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated sitemap.xml with {loc_url}")


def apply_layout_standardization():
    standardize_script = os.path.join(ROOT_DIR, "scripts", "standardize-layout.py")
    if os.path.exists(standardize_script):
        import subprocess
        subprocess.run(["python3", standardize_script], check=True)


def publish_next_topic(dry_run=False):
    topics = load_topics()
    next_topic = None

    for topic in topics:
        if not topic.get("published", False):
            next_topic = topic
            break

    if not next_topic:
        print("No unpublished topics found in database.")
        return False

    title = next_topic["title"]
    slug = next_topic["slug"]
    today_str = datetime.now().strftime("%Y-%m-%d")

    print(f"Selected topic for publishing: '{title}' (slug: {slug})")

    if dry_run:
        print("[DRY-RUN] Article HTML generation simulated successfully.")
        return True

    article_dir = os.path.join(ROOT_DIR, "blog", slug)
    os.makedirs(article_dir, exist_ok=True)
    article_filepath = os.path.join(article_dir, "index.html")

    html_content = build_article_html(next_topic, today_str)
    with open(article_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Article HTML written to: {article_filepath}")

    update_blog_index(next_topic, today_str)
    update_sitemap(slug, today_str)

    next_topic["published"] = True
    next_topic["published_at"] = today_str
    save_topics(topics)

    apply_layout_standardization()
    print(f"Publication complete for article: {slug}")
    return True


if __name__ == "__main__":
    dry_run_arg = "--dry-run" in sys.argv
    publish_next_topic(dry_run=dry_run_arg)
