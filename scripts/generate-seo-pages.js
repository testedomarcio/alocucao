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
    const folderName = `produtora-de-audio-${cleanSlug}`;
    const outputDir = path.join(ROOT_DIR, folderName);

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const canonicalUrl = `https://alocucao.com.br/${folderName}/`;
    generatedUrls.push(canonicalUrl);

    // Dynamic WhatsApp Link
    const waText = `Olá! Acessei a página de ${region.stateName} e quero um orçamento.`;
    const whatsappUrl = `https://api.whatsapp.com/send?phone=5527996529832&text=${encodeURIComponent(waText)}`;

    // Cities formatting
    const citiesListFormatted = Array.isArray(region.cities)
      ? region.cities.join(', ')
      : region.cities || region.stateName;

    // Area Served JSON
    const areaServedArray = Array.isArray(region.cities)
      ? [region.stateName, ...region.cities]
      : [region.stateName];
    const areaServedSchemaJson = JSON.stringify(areaServedArray, null, 2);

    const safeReplace = (str, pattern, replacement) => {
      const val = typeof replacement === 'string' ? sanitizeReplacement(replacement) : replacement;
      return str.replaceAll(pattern, val);
    };

    let pageHtml = templateHtml;
    pageHtml = safeReplace(pageHtml, '<meta name="robots" content="noindex">', '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">');
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
    pageHtml = safeReplace(pageHtml, '{{citiesListFormatted}}', citiesListFormatted);
    pageHtml = safeReplace(pageHtml, '{{areaServedSchemaJson}}', areaServedSchemaJson);
    pageHtml = safeReplace(pageHtml, '{{whatsappUrl}}', whatsappUrl);

    const outputPath = path.join(outputDir, 'index.html');
    fs.writeFileSync(outputPath, pageHtml, 'utf8');
    console.log(`Generated: ${folderName}/index.html`);
  });

  updateSitemap(generatedUrls, today);
}

function sanitizeReplacement(str) {
  if (typeof str !== 'string') return str;
  return str.replace(/\$/g, '$$$$');
}

function updateSitemap(urls, todayDate) {
  if (!fs.existsSync(SITEMAP_PATH)) {
    console.warn(`Sitemap not found at ${SITEMAP_PATH}, skipping sitemap update.`);
    return;
  }

  let sitemapContent = fs.readFileSync(SITEMAP_PATH, 'utf8');

  urls.forEach((url) => {
    const locTag = `<loc>${url}</loc>`;
    if (!sitemapContent.includes(locTag)) {
      // Insert new URL before </urlset>
      const newEntry = `  <url><loc>${url}</loc><lastmod>${todayDate}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n`;
      sitemapContent = sitemapContent.replace('</urlset>', `${newEntry}</urlset>`);
    }
  });

  fs.writeFileSync(SITEMAP_PATH, sitemapContent, 'utf8');
  console.log(`Verified sitemap.xml for ${urls.length} regional URLs.`);
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

generatePages();
