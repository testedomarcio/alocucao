const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const REGIONS_JSON_PATH = path.join(ROOT_DIR, 'data', 'regions.json');
const TEMPLATE_PATH = path.join(ROOT_DIR, 'templates', 'region-template.html');
const SITEMAP_PATH = path.join(ROOT_DIR, 'sitemap.xml');

function generatePages() {
  if (!fs.existsSync(REGIONS_JSON_PATH)) {
    console.error(`Regions file not found at ${REGIONS_JSON_PATH}`);
    process.exit(1);
  }

  if (!fs.existsSync(TEMPLATE_PATH)) {
    console.error(`Template file not found at ${TEMPLATE_PATH}`);
    process.exit(1);
  }

  const regions = JSON.parse(fs.readFileSync(REGIONS_JSON_PATH, 'utf8'));
  const templateHtml = fs.readFileSync(TEMPLATE_PATH, 'utf8');

  const today = new Date().toISOString().split('T')[0];
  const generatedUrls = [];

  regions.forEach((region) => {
    const rawSlug = region.slug.trim().toLowerCase();
    const cleanSlug = rawSlug.replace(/^produtora-de-audio-/, '');
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(cleanSlug)) {
      throw new Error(`Invalid regional slug: ${region.slug}`);
    }
    const folderName = `produtora-de-audio-${cleanSlug}`;
    const outputDir = path.join(ROOT_DIR, folderName);

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const canonicalUrl = `https://alocucao.com.br/${folderName}/`;
    generatedUrls.push(canonicalUrl);

    const panelUrl = 'https://vozlocutor.com.br/painel/alocucao/';

    // Cities formatting
    const citiesListFormatted = Array.isArray(region.cities)
      ? region.cities.join(', ')
      : region.cities || region.stateName;

    // Remote service coverage; this does not represent a physical office.
    const areaServedArray = [{ "@type": "AdministrativeArea", name: region.stateName }];

    // HTML values and JSON-LD have different escaping rules.
    const safeReplace = (str, pattern, replacement) =>
      str.replaceAll(pattern, () => escapeHtml(String(replacement ?? "")));

    let pageHtml = templateHtml;
    pageHtml = pageHtml.replace('<meta name="robots" content="noindex">', '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">');
    pageHtml = safeReplace(pageHtml, '{{stateName}}', region.stateName);
    pageHtml = safeReplace(pageHtml, '{{stateAbbr}}', region.stateAbbr);
    pageHtml = safeReplace(pageHtml, '{{stateIn}}', region.stateIn || `em ${region.stateName}`);
    pageHtml = safeReplace(pageHtml, '{{stateOf}}', region.stateOf || `de ${region.stateName}`);
    pageHtml = safeReplace(pageHtml, '{{stateFor}}', region.stateFor || `para ${region.stateName}`);
    pageHtml = safeReplace(pageHtml, '{{slug}}', cleanSlug);
    pageHtml = safeReplace(pageHtml, '{{pagePath}}', folderName);
    pageHtml = safeReplace(pageHtml, '{{canonicalUrl}}', canonicalUrl);
    pageHtml = safeReplace(pageHtml, '{{pageTitle}}', region.pageTitle);
    pageHtml = safeReplace(pageHtml, '{{metaDescription}}', region.metaDescription);
    pageHtml = safeReplace(pageHtml, '{{eyebrow}}', region.eyebrow);
    pageHtml = safeReplace(pageHtml, '{{h1Title}}', region.h1Title);
    pageHtml = safeReplace(pageHtml, '{{nicheEmphasis}}', region.nicheEmphasis);
    pageHtml = safeReplace(pageHtml, '{{heroParagraph}}', region.heroParagraph);
    pageHtml = safeReplace(pageHtml, '{{regionalFocus}}', region.regionalFocus);
    pageHtml = safeReplace(pageHtml, '{{exampleTitle}}', region.exampleTitle);
    pageHtml = safeReplace(pageHtml, '{{exampleScript}}', region.exampleScript);
    pageHtml = safeReplace(pageHtml, '{{briefingTip}}', region.briefingTip);
    pageHtml = safeReplace(pageHtml, '{{citiesListFormatted}}', citiesListFormatted);
    pageHtml = safeReplace(pageHtml, '{{panelUrl}}', panelUrl);

    const structuredData = {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Organization", "@id": "https://alocucao.com.br/#organization",
          name: "A Locução", url: "https://alocucao.com.br/", logo: "https://alocucao.com.br/assets/brand/a-locucao-logo.png",
          telephone: "+5527996529832",
          contactPoint: { "@type": "ContactPoint", telephone: "+5527996529832",
            contactType: "customer service", areaServed: "BR", availableLanguage: "pt-BR" }
        },
        {
          "@type": "Service", "@id": canonicalUrl + "#service",
          name: `Locução e produção de áudio online ${region.stateFor || `para ${region.stateName}`}`,
          url: canonicalUrl, description: region.metaDescription,
          provider: { "@id": "https://alocucao.com.br/#organization" },
          areaServed: areaServedArray,
          availableChannel: { "@type": "ServiceChannel", serviceUrl: canonicalUrl, availableLanguage: "pt-BR" },
          serviceType: ["Spot Comercial", "Locução Profissional", "Gravação para Carro de Som",
            "Vídeos Institucionais", "Espera Telefônica e URA"]
        },
        { "@type": "WebPage", "@id": canonicalUrl + "#webpage", url: canonicalUrl,
          name: region.pageTitle, description: region.metaDescription },
        { "@type": "BreadcrumbList", itemListElement: [
          { "@type": "ListItem", position: 1, name: "A Locução", item: "https://alocucao.com.br/" },
          { "@type": "ListItem", position: 2, name: "Atendimento online", item: "https://alocucao.com.br/servicos/" },
          { "@type": "ListItem", position: 3, name: region.stateName, item: canonicalUrl }
        ] }
      ]
    };
    const schemaJson = JSON.stringify(structuredData, null, 2).replace(/</g, "\\u003c");
    pageHtml = pageHtml.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/,
      () => `<script type="application/ld+json">\n${schemaJson}\n  </script>`);

    // Read the same shared fragments used by every static page.
    for (const part of ['header', 'footer']) {
      const fragment = fs.readFileSync(path.join(ROOT_DIR, 'templates', `site-${part}.html`), 'utf8').trim();
      pageHtml = pageHtml.replace(new RegExp(`<!-- site-${part}:start -->[\\s\\S]*?<!-- site-${part}:end -->`), () => fragment);
    }

    const outputPath = path.join(outputDir, 'index.html');

    let isModified = true;
    if (fs.existsSync(outputPath)) {
      const existingContent = fs.readFileSync(outputPath, 'utf8');
      if (existingContent === pageHtml) {
        isModified = false;
      }
    }

    fs.writeFileSync(outputPath, pageHtml, 'utf8');
    console.log(`Generated: ${folderName}/index.html ${isModified ? '(updated)' : '(unchanged)'}`);

    updateSitemapForUrl(canonicalUrl, today, isModified);
  });
}

function escapeHtml(value) {
  return value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function updateSitemapForUrl(url, todayDate, isModified) {
  if (!fs.existsSync(SITEMAP_PATH)) {
    console.warn(`Sitemap not found at ${SITEMAP_PATH}, skipping sitemap update.`);
    return;
  }

  let sitemapContent = fs.readFileSync(SITEMAP_PATH, 'utf8');
  const locTag = `<loc>${url}</loc>`;

  if (!sitemapContent.includes(locTag)) {
    // Insert new URL before </urlset>
    const newEntry = `  <url><loc>${url}</loc><lastmod>${todayDate}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n`;
    sitemapContent = sitemapContent.replace('</urlset>', `${newEntry}</urlset>`);
    fs.writeFileSync(SITEMAP_PATH, sitemapContent, 'utf8');
  } else if (isModified) {
    // Update existing <lastmod> for this url if content was actually modified
    const urlBlockRegex = new RegExp(`(<url>\\s*<loc>${escapeRegExp(url)}</loc>\\s*<lastmod>)[^<]+(</lastmod>)`);
    if (urlBlockRegex.test(sitemapContent)) {
      sitemapContent = sitemapContent.replace(urlBlockRegex, `$1${todayDate}$2`);
      fs.writeFileSync(SITEMAP_PATH, sitemapContent, 'utf8');
    }
  }
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

generatePages();

// Preserve shared navigation and panel purchase links in regenerated regional pages.
require("child_process").execFileSync("python3", [path.join(__dirname, "standardize-layout.py")], {stdio: "inherit"});
