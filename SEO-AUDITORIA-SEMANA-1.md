# Auditoria SEO — Semana 1

Data: 10 de setembro de 2026

## Resumo executivo

O site já possui uma boa base: HTTPS, domínio canônico sem `www`, páginas comerciais separadas, títulos e descrições próprios, um único H1 por página indexável, `robots.txt`, sitemap, dados estruturados, conteúdo editorial e links internos sem destinos quebrados.

Os principais problemas encontrados foram uma divergência de preços na página de serviços, uma página nova ausente do sitemap, versões antigas sem `noindex` e pouca ligação entre as páginas de venda e os conteúdos que deveriam apoiá-las.

## Corrigir agora

- [x] Alinhar a página `/servicos/` com os preços publicados nas páginas de venda: Locução Off a partir de R$ 12 e Spot Comercial a partir de R$ 25.
- [x] Incluir `/blog/audio-para-campanha-eleitoral/` no sitemap.
- [x] Marcar as versões antigas `/locucao_off.html`, `/locucaooff/`, `/spot_comercial.html` e `/spotcomercial/` como `noindex,follow`, preservando seus redirecionamentos e canônicas.
- [x] Reduzir a descrição da Home para evitar corte excessivo no resultado de busca.
- [x] Adicionar metadados sociais básicos à Home e às páginas principais de venda.
- [x] Reforçar os dados estruturados de Locução Off e Spot Comercial com `Service`, `BreadcrumbList` e perguntas frequentes visíveis na página.
- [x] Criar blocos de conteúdos relacionados nas páginas de Locução Off e Spot Comercial.
- [x] Criar ligações contextuais do conteúdo eleitoral para a página de Spot Comercial.
- [x] Adicionar links internos da página de serviços para as páginas comerciais detalhadas.

## Melhorar depois

- Validar no Search Console a indexação das páginas canônicas, o processamento do sitemap e a remoção gradual das URLs antigas.
- Medir Core Web Vitals com dados de campo quando houver volume suficiente e acompanhar as páginas separadamente no PageSpeed Insights.
- Criar versões leves e curtas das demonstrações de áudio, mantendo os arquivos originais preservados.
- Mover estilos repetidos que hoje estão embutidos nas páginas para arquivos compartilhados e cacheáveis, sem alterar o visual.
- Padronizar metadados sociais nas páginas institucionais e criar uma imagem social somente quando houver uma arte oficial da marca.
- Publicar avaliações reais e autorizadas; não adicionar marcação de avaliações enquanto a página ainda não tiver depoimentos publicados.
- Confirmar eventos de clique no WhatsApp, origem da página e envio de avaliação no GA4.

## Criar

Prioridade para o cluster de Spot Comercial:

1. Quanto custa um spot comercial?
2. Como fazer um roteiro de spot de 30 segundos?
3. Spot de 15, 30 ou 60 segundos: qual escolher?
4. Spot comercial para rádio.
5. Spot para carro de som.
6. Spot promocional para loja e supermercado.
7. Exemplos de spot comercial.

Prioridade seguinte para Locução Off:

1. Quanto custa uma locução off?
2. Locução off para vídeo.
3. Locução para rádio e produtoras.
4. Como escolher voz masculina ou feminina.
5. Como preparar o texto antes da gravação.

Cada artigo deve responder a uma intenção específica e apontar para uma única página comercial principal, evitando duas páginas disputando a mesma busca.

## Remover ou consolidar

- Não apagar agora as páginas antigas. Elas ainda protegem acessos e links históricos, redirecionando para as URLs atuais.
- Manter fora do sitemap todas as versões antigas e páginas de redirecionamento.
- Quando o Search Console confirmar que as substituições foram processadas, avaliar redirecionamentos HTTP permanentes. No GitHub Pages, os redirecionamentos atuais acontecem dentro do HTML e não equivalem a um `301` de servidor.

## Arquitetura recomendada

- Home: apresenta a marca e distribui autoridade para Locução Off, Spot Comercial, Serviços, Vozes e Blog.
- Locução Off: página transacional principal apoiada por guias sobre conceito, preço, escolha de voz, vídeo, rádio e preparação de texto.
- Spot Comercial: página transacional principal apoiada por conteúdos sobre preço, roteiro, duração, rádio, carro de som, varejo e exemplos.
- Serviços específicos: páginas de intenção comercial própria, como campanha política, URA, vinheta e narração.
- Blog: responde dúvidas informacionais e conduz o visitante à página de serviço correspondente.

## Validação técnica realizada

- 26 arquivos HTML inventariados.
- Nenhum link ou recurso local quebrado.
- Nenhum erro de sintaxe nos dados estruturados JSON-LD.
- Sitemap válido, com 15 URLs canônicas e todos os destinos presentes.
- Scripts JavaScript compartilhados sem erro de sintaxe.
- Nenhuma ocorrência restante dos preços antigos de R$ 15/R$ 40 nas páginas de serviço.

