# Auditoria SEO — Semana 1

Data: 10 de setembro de 2026

## Status da fundação

A fundação técnica e estrutural do site está concluída no repositório. As páginas principais de venda foram reforçadas, as versões antigas foram consolidadas, o sitemap foi revisado e a arquitetura interna passou a apontar com mais clareza para os dois serviços centrais: Locução Off e Spot Comercial.

A única frente estrutural que permanece fora do repositório é a validação de indexação dentro do Google Search Console. Como o GSC Wizard não será utilizado, essa checagem deverá ser feita manualmente no Search Console quando necessário.

## Concluído

- [x] Home revisada para SEO, arquitetura e conversão.
- [x] Página `/spot-comercial/` fortalecida como página comercial principal de Spot Comercial.
- [x] Página `/locucao-off/` fortalecida como página comercial principal de Locução Off.
- [x] Página `/servicos/` alinhada aos preços e serviços atuais e enriquecida com dados estruturados.
- [x] Página `/sobre/` alinhada ao posicionamento atual e enriquecida com dados da organização.
- [x] Sitemap atualizado com as URLs canônicas e datas relevantes.
- [x] `robots.txt` validado com rastreamento liberado e referência ao sitemap.
- [x] Versões antigas de URLs mantidas fora do sitemap, com `noindex,follow`, canonical e redirecionamento em HTML.
- [x] Preços antigos de R$ 15/R$ 40 removidos das páginas de serviço revisadas.
- [x] Links internos reforçados entre Home, Locução Off, Spot Comercial, Serviços, Vozes, Blog e páginas específicas.
- [x] Dados estruturados adicionados ou reforçados em Home, Locução Off, Spot Comercial, Serviços e Sobre.
- [x] Players principais configurados para não pré-carregar arquivos de áudio desnecessariamente.
- [x] Textos comerciais priorizam o WhatsApp como principal caminho de conversão para novos clientes.

## Validação pública e publicação

O GitHub Pages está configurado para publicar no domínio `https://alocucao.com.br/`. Os workflows de build e deploy executados durante a revisão concluíram com sucesso; após alterações em sequência, o último workflow pode permanecer temporariamente na fila enquanto os anteriores finalizam.

Ferramentas externas de rastreamento podem exibir versões em cache por algum tempo. A fonte de verdade para o conteúdo atual é o branch `main` do repositório e o último deploy bem-sucedido do GitHub Pages.

## Pendente fora do repositório

- Validar manualmente no Google Search Console a indexação das URLs canônicas.
- Conferir o processamento do sitemap no Search Console.
- Acompanhar a saída gradual das URLs antigas do índice.
- Solicitar indexação manual das páginas estratégicas quando necessário.
- Incorporar os dois exemplos reais de Locução Off quando os MP3 puderem ser publicados em `assets/audio/`.

## Desempenho

Os players da Home e do banco de vozes usam `preload="none"`, evitando que dezenas de demonstrações sejam baixadas automaticamente ao abrir a página. A página de Locução Off também foi ajustada para esse comportamento.

Existem arquivos grandes no repositório, mas eles não prejudicam diretamente a abertura da página quando não são requisitados pelo navegador. O ponto que deve continuar sendo monitorado é o peso dos arquivos efetivamente reproduzidos e recursos carregados no primeiro acesso.

## Próxima fase: clusters de conteúdo

A partir daqui, a prioridade deixa de ser reformular continuamente Home, Spot Comercial e Locução Off. O foco passa para conteúdos que ampliem cobertura de busca e transmitam autoridade às páginas comerciais.

### Cluster de Spot Comercial

1. Quanto custa um spot comercial?
2. Como fazer um roteiro de spot de 30 segundos?
3. Spot de 15, 30 ou 60 segundos: qual escolher?
4. Spot comercial para rádio.
5. Spot promocional para loja e supermercado.
6. Exemplos de spot comercial.

### Cluster de Locução Off

1. Quanto custa uma locução off?
2. Locução off para vídeo.
3. Locução para rádio e produtoras.
4. Como escolher voz masculina ou feminina.
5. Como preparar o texto antes da gravação.

Cada artigo deve responder a uma intenção específica e apontar para uma única página comercial principal, reduzindo risco de canibalização.

## Regra de arquitetura

- Home: apresenta a marca e distribui autoridade.
- Locução Off: página transacional principal do serviço de voz sem produção.
- Spot Comercial: página transacional principal da produção completa.
- Serviços: hub para formatos complementares.
- Vozes: catálogo e prova de variedade.
- Blog: conteúdo informacional que apoia as páginas comerciais.
- Páginas específicas: atendem intenções próprias, como carro de som e campanha política.

## Encerramento da Semana 1

A fase de auditoria, correção estrutural e organização das páginas principais pode ser considerada concluída no código. As próximas mudanças devem ser orientadas por conteúdo, autoridade, conversão e dados de desempenho, evitando retrabalho desnecessário nas páginas que já foram estruturadas.
