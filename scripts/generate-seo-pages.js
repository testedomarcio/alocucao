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

    let pageHtml = templateHtml
      .replaceAll('{{stateName}}', region.stateName)
      .replaceAll('{{stateAbbr}}', region.stateAbbr)
      .replaceAll('{{slug}}', cleanSlug)
      .replaceAll('{{pagePath}}', folderName)
      .replaceAll('{{canonicalUrl}}', canonicalUrl)
      .replaceAll('{{pageTitle}}', region.pageTitle)
      .replaceAll('{{metaDescription}}', region.metaDescription)
      .replaceAll('{{eyebrow}}', region.eyebrow)
      .replaceAll('{{h1Title}}', region.h1Title)
      .replaceAll('{{nicheEmphasis}}', region.nicheEmphasis)
      .replaceAll('{{heroParagraph}}', region.heroParagraph)
      .replaceAll('{{regionalFocus}}', region.regionalFocus)
      .replaceAll('{{citiesListFormatted}}', citiesListFormatted)
      .replaceAll('{{areaServedSchemaJson}}', areaServedSchemaJson)
      .replaceAll('{{whatsappUrl}}', whatsappUrl);

    const outputPath = path.join(outputDir, 'index.html');
    fs.writeFileSync(outputPath, pageHtml, 'utf8');
    console.log(`Generated: ${folderName}/index.html`);
  });

  updateSitemap(generatedUrls, today);
}

function updateSitemap(urls, todayDate) {
  if (!fs.existsSync(SITEMAP_PATH)) {
    console.warn(`Sitemap not found at ${SITEMAP_PATH}, skipping sitemap update.`);
    return;
  }

  let sitemapContent = fs.readFileSync(SITEMAP_PATH, 'utf8');

  urls.forEach((url) => {
    const locTag = `<loc>${url}</loc>`;
    if (sitemapContent.includes(locTag)) {
      // Update existing lastmod
      const urlRegex = new RegExp(
        `(<url>\\s*<loc>${escapeRegExp(url)}<\/loc>(?:(?!<\/url>)[\\s\\S])*?<lastmod>)([^<]+)(<\/lastmod>)`,
        'g'
      );
      if (urlRegex.test(sitemapContent)) {
        sitemapContent = sitemapContent.replace(
          urlRegex,
          `$1${todayDate}$3`
        );
      } else {
        // If lastmod tag is missing in this <url> block
        sitemapContent = sitemapContent.replace(
          locTag,
          `${locTag}<lastmod>${todayDate}</lastmod>`
        );
      }
    } else {
      // Insert new URL before </urlset>
      const newEntry = `  <url><loc>${url}</loc><lastmod>${todayDate}</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>\n`;
      sitemapContent = sitemapContent.replace('</urlset>', `${newEntry}</urlset>`);
    }
  });

  fs.writeFileSync(SITEMAP_PATH, sitemapContent, 'utf8');
  console.log(`Updated sitemap.xml with ${urls.length} regional URLs.`);
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

generatePages();
