# SEO técnico e conteúdo

Foram preservadas todas as URLs existentes. O sitemap passa a incluir sete páginas de serviço com canonical próprio e foi deduplicado por caminho. Títulos e descrições completos estão em `inventario.csv`; cada uma das sete novas páginas tem metadados próprios, H1 único, conteúdo de finalidade específica e marcação Service. Não foram criadas avaliações, AggregateRating, resultados garantidos ou schema de produtos com preço fixo para orçamento personalizado.

| Intenção | Página principal sugerida | Diferenciação |
| --- | --- | --- |
| Contratar voz sem edição musical | /locucao-off/ | Somente voz, preço por peça comercial |
| Contratar anúncio finalizado | /spot-comercial/ | Voz, trilha compatível e acabamento |
| Narrar vídeo corporativo | /narracao-para-videos/ | Arquivo de voz, sem edição integral do vídeo |
| Conteúdo contínuo longo | /narracoes/ | Até cinco minutos no escopo inicial |
| Gravar atendimento telefônico | /gravacao-de-ura/ | Mensagem de até 30 s e formatos da central |
| Melhorar gravação existente | /tratamento-de-audio/ | Avaliação técnica e resultado limitado pela fonte |

As URLs /locucao-para-video-institucional/ e /espera-telefonica-ura/ permanecem acessíveis e com seus canonicals anteriores. Há possível sobreposição com as novas páginas. Antes de uma consolidação futura, consultar consultas/páginas no Search Console e no Bing, escolher a URL que preserva o melhor histórico e mapear um 301 real. Não foi presumido qual endereço já possui tráfego ou backlinks. Nenhum redirecionamento artificial foi anunciado como HTTP 301.

GitHub Pages atende rotas estáticas: mudança de canonical não equivale a redirecionamento HTTP. A lista de aliases continua no gerador atual e no inventário. A configuração de robots permite recursos públicos e bloqueia diretórios de manutenção; não foi usada para esconder páginas de conteúdo que precisam mostrar noindex aos buscadores.

Performance: CSS e JS locais, sem nova dependência, fonte do sistema, hero WebP existente com dimensões, imagens secundárias lazy e áudios preload=none. A calculadora não chama APIs nem envia roteiros durante a digitação. HTTPS já estava ativo. Cache e headers são administrados pela hospedagem: não há promessa de controle inexistente. Não foram medidos LCP/INP/CLS de campo nem atribuídas notas Lighthouse sem execução.

Acessibilidade: navegação por botão com aria-expanded, link de pular conteúdo, labels de campos e players, foco visível e respeito a movimento reduzido. Tabelas podem rolar em largura estreita. Não se declara conformidade WCAG integral com base nesses testes.

Conteúdo futuro: publicar demonstrações próprias de URA e narração; guias sobre preparação de roteiro e especificações telefônicas; casos reais com autorização expressa. Evitar multiplicar páginas regionais ou páginas quase idênticas. A oportunidade de reduzir ou consolidar os muitos aliases noindex exige análise de dados reais e camada de 301 antes de qualquer remoção.
