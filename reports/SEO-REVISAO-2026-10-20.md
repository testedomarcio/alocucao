# Auditoria técnica de SEO — A Locução

Data: 20/10/2026. Execução e commits pela interface do navegador.

## Escopo e resultado

Foram inspecionadas as 59 URLs do sitemap publicado. A conferência final no navegador não encontrou títulos duplicados, canônicas divergentes da URL final, H1 ausente ou múltiplo, descrição ausente, imagem sem atributo ALT, endereço antigo no texto visível ou links internos antigos dos termos. A validação no GitHub Actions passou. Isso não equivale a garantia de indexação ou posicionamento, nem a uma varredura HTTP de todas as rotas históricas.

O comparativo desde f730b0bf4fac4ff890a23e8b9ac78c07ee269ae0 mostra 67 arquivos desta revisão e dois JSONs do catálogo alterados pela sincronização de vozes no mesmo intervalo. Os JSONs do catálogo não são apresentados como correções desta auditoria. Este relatório é um arquivo adicional e fica fora da publicação do site por estar em reports/.

## Desempenho da página inicial

PageSpeed Insights, 20/10/2026 às 06:43 BRT, teste de laboratório:

| Métrica | Celular | Computador |
|---|---:|---:|
| Desempenho | 98 | 100 |
| Acessibilidade | 100 | 100 |
| Boas práticas | 100 | 100 |
| SEO | 100 | 100 |
| LCP | 1,8 s | 0,4 s |
| CLS | 0 | 0 |

Acessibilidade no celular era 91 na medição anterior. A variação de desempenho entre execuções é normal; a comparação não isola causalidade. Não há dados de campo suficientes no relatório para concluir aprovação dos Core Web Vitals de visitantes reais. Áudios já usam preload=none e imagens abaixo da dobra usam carregamento adiado. Permanecem oportunidades indicadas pelo PageSpeed para imagens e cache; headers da hospedagem e conteúdo do subdomínio exigem administração fora deste repositório.

## Bugs corrigidos

- Dez tutoriais repetiam o mesmo conteúdo genérico de WhatsApp. Cada um recebeu orientação própria; o índice passou a ligar todas as etapas.
- A canônica dos termos apontava para a URL sem barra, que redireciona. Canonical, og:url, sitemap e links revisados agora usam /termos/.
- A página de Natal declarava um Product incompleto além de Service. O serviço agora é representado sem o Product redundante.
- O endereço antigo aparecia em rodapés e no JSON-LD regional. Foi alinhado à identificação atual da página Sobre e do template comercial.
- O gerador regional reintroduziria o endereço antigo; sua fonte foi corrigida.
- Relatórios internos poderiam ser publicados pelo Pages; a pasta foi excluída da publicação.
- Contraste e controles pequenos no rodapé foram ajustados.

## Log de arquivos

| Arquivo | Alteração |
|---|---|
| `.github/workflows/seo-audit.yml` | Executa validação em push e manualmente com contents: read; não faz commits. |
| `_config.yml` | Exclui reports da publicação pelo GitHub Pages. |
| `assets/site-layout.css` | Melhora contraste da microcópia, área de toque e foco dos controles do rodapé. |
| `avaliacoes/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/agencia-de-vozes-locucao-comercial/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/audio-para-campanha-eleitoral/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/como-fazer-roteiro-para-carro-de-som/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/locucao-comercial-publicitaria/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/locucao-off-o-que-e/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/locucao-para-supermercado/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/locucao-profissional-como-contratar-locutor/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/propaganda-dia-das-criancas/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/quanto-custa-um-spot-comercial/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/roteiro-spot-black-friday/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/spot-black-friday/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `blog/voz-ia-ou-locucao-humana/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `calculadora/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `espera-telefonica-ura/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `gravacao-off-e-producao/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `indique-e-ganhe/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `locucao-campanha-politica/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `locucao-off/index.html` | Título e descrição concisos, H1 descritivo, Service/WebPage e links dos termos. |
| `locucao-para-video-institucional/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `locucao-voz-infantil/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `planos-para-agencias-revenda/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `politica-de-privacidade/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `portfolio/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `precos/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `producao-para-igrejas/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `producao-para-supermercados/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-bahia/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-distrito-federal/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-espirito-santo/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-goias/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-minas-gerais/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-parana/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-rio-de-janeiro/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-rio-grande-do-sul/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-santa-catarina/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `produtora-de-audio-sao-paulo/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `robots.txt` | Restringe /scripts/, /templates/ e /reports/; preserva rastreamento de recursos públicos e declaração do sitemap. |
| `scripts/generate-seo-pages.js` | Corrige endereço da Organization na geração regional. |
| `scripts/seo-consistency.py` | Auditoria de sitemap, canônicas, títulos/H1, descrições, ALT e sintaxe JSON-LD. Modo --fix é opcional e local. |
| `servicos/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `sitemap.xml` | Normaliza URL final dos termos e lastmod das páginas com alterações de conteúdo. |
| `sobre/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `spot-black-friday/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `spot-comercial-natal/index.html` | Remove Product incompleto e redundante; mantém Service, adiciona WebPage, revê título, descrição e H1. |
| `spot-comercial/index.html` | Título e descrição concisos, Service/WebPage, URL da oferta e links dos termos. |
| `spot-para-carro-de-som/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `templates/site-footer.html` | Usa /termos/ no fragmento compartilhado. |
| `termos/index.html` | Canonical e og:url com barra final; link interno e identificação consistentes. |
| `tutoriais/como-acompanhar-pedido/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-adquirir-creditos/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-baixar-pedido/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-completar-cadastro/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-escolher-locutor/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-pedir-locucao-off/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-pedir-spot-comercial/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-preparar-texto/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-se-cadastrar/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/como-solicitar-correcao/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `tutoriais/index.html` | Conteúdo específico, título, descrição, H1, links por etapa e JSON-LD WebPage/BreadcrumbList; remoção de identificação antiga. |
| `vinhetas-para-podcast-e-radio/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |
| `vozes/index.html` | Padroniza identificação comercial e/ou destino dos links para /termos/. |

## Limites de acesso e indexação

A sessão do Google foi desconectada e a autenticação precisa ser concluída para atualizar Search Console e Analytics. Bing Webmaster Tools também depende de acesso autenticado. Não foram atribuídas quedas de tráfego a páginas sem dados comparáveis. A validação de dados estruturados iniciada no Search Console em 19/10 ainda precisa de acompanhamento.

As versões sem barra de Natal e do artigo de Black Friday chegaram às páginas finais corretas no navegador. O domínio Comerciais Top também chega ao site atual, mas seu index.html usa meta refresh e location.replace. Isso não substitui um redirecionamento HTTP 301 configurado na hospedagem. A conferência de status, cadeia e caminhos antigos permanece pendente no provedor.

O robots.txt deste domínio não controla vozes.alocucao.com.br. Rotas de login, cadastro e pedidos do painel precisam de proteção e política de indexação próprias no subdomínio. Perfis históricos com noindex precisam ser avaliados conforme sua função atual; não foi removido noindex em massa.

## Plano de ação externo

### Primeiros 7 dias

1. Concluir acesso ao Google e ao Bing. No Search Console, comparar 28 dias com os 28 anteriores por página e consulta; acompanhar as duas ocorrências antigas de redirecionamento e a validação de dados estruturados. Conferir também as URLs descobertas ainda não indexadas.
2. No GA4, confirmar o fluxo G-TBHF64CH1R, testar page_view e eventos de contato em tempo real após consentimento e conferir se filtros ou configuração impedem a coleta. Medir cliques de WhatsApp e pedido online separadamente de vendas concluídas; integrar cadastros e compras do painel com o provedor quando possível.
3. Configurar 301 de http/https e www/sem-www do domínio antigo diretamente para a URL correspondente em alocucao.com.br. Mapear serviços antigos para equivalentes; evitar enviar indiscriminadamente todas as páginas para a inicial. Testar caminhos e parâmetros antes de concluir a migração.
4. Conferir sitemap, inspeção de URLs prioritárias e rastreamento no Bing. O workflow IndexNow já está ativo; aceitação do envio não garante indexação.

### Conteúdo e conversão — próximas 4 semanas

- Priorizar os grupos banco de vozes, locução off, spot comercial, carro de som, supermercados e igrejas. Cada página comercial deve responder preço, entrega, escolha da voz, exemplo de áudio e próximo passo.
- Atualizar as páginas de Black Friday e Natal com exemplos reais, roteiro comentado e condições vigentes. Manter oferta e datas coerentes entre página, schema e atendimento. Evitar novas páginas quase iguais para a mesma intenção de busca.
- Produzir um estudo de caso por quinzena com autorização do cliente: objetivo, roteiro, escolha da voz, áudio entregue e contexto de uso. Acrescentar transcrição curta para tornar o conteúdo de áudio compreensível também em texto.
- Transformar dúvidas recorrentes do atendimento em guias úteis, ligados à página do serviço correspondente. Usar os tutoriais revisados para reduzir dificuldade no cadastro, pagamento e download.
- Conferir descrições e trechos exibidos no Google depois de haver impressões suficientes. Priorizar ajustes onde há boa posição e baixo CTR, preservando intenção e conteúdo.

### Autoridade e backlinks — 30 a 60 dias

- Buscar referências editoriais em sites de rádios, agências, produtoras de vídeo e clientes que realmente utilizem o serviço. Preparar amostras ou cases úteis e solicitar menção com link quando houver relação real.
- Atualizar menções legítimas a Comerciais Top para A Locução, começando por parceiros e perfis controlados pela empresa. Manter nome, contato e endereço consistentes.
- Criar materiais que mereçam ser citados: calculadora de duração, exemplos de roteiro por canal e checklist de briefing. Monitorar quais páginas recebem links e quais geram contatos qualificados.
- Evitar compra de pacotes de links, cadastros massivos e avaliações fictícias. Nenhum contato externo foi enviado nesta execução.

### Acompanhamento

Revisar semanalmente: páginas indexáveis, erros de rastreamento, cliques/impressões orgânicas por página, contatos qualificados, cadastros e compras. Separar marca de buscas genéricas e tráfego pago de orgânico. Avaliar o resultado em janelas comparáveis, sem atribuir variações diárias automaticamente a estas alterações.
  
