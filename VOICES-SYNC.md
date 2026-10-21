# Catálogo humano oficial e vitrine compartilhada

Fonte única: https://vozes.alocucao.com.br/. O sincronizador lê o catálogo público `locutoresData`, valida IDs, nomes e URLs e preserva o último JSON válido quando há falha. Conexões transitórias recebem até três tentativas; erros de autorização e conteúdo inválido não são contornados.

O workflow `sync-voices.yml` roda a cada 15 minutos, sujeito a atrasos do GitHub Actions. Atualiza `assets/voices-catalog.json` e executa `scripts/unified-catalog.py` para regenerar as listas indexáveis em todas as páginas. Não usa login nem altera a fonte. O navegador atualiza perfis pelo JSON público a cada cinco minutos e ao voltar à aba.

A disponibilidade é consultada diretamente na API pública `https://vozes.alocucao.com.br/check_status.php`, com o escopo da loja 382, conforme o código da própria vitrine. A API permite CORS. A primeira consulta usa `last_check=0`; as seguintes usam o timestamp retornado, para receber mudanças incrementais. O polling ocorre a cada 30 segundos, só com a página visível, sem cookies ou credenciais. O HTML de status da fonte é ignorado; somente texto e campos validados são exibidos.

Não há status humano forçado para Online. Falhas na consulta direta mostram sob consulta, mantendo perfis e áudios. O cache com mais de 45 minutos também não é apresentado como disponibilidade atual sem uma consulta direta válida. O usuário sempre confirma o prazo do pedido.

Componente: `scripts/unified-catalog.py`; interface: `assets/unified-voices.js` e `assets/unified-voices.css`. O catálogo mostra duas colunas em computadores e abas em celulares. Busca e filtros são independentes; cada painel começa com 12 vozes. Ordem inicial aleatória, estável ao filtrar e atualizar os status. Os áudios são carregados por ação do usuário e apenas uma demonstração toca por vez.

Rotas: `/vozes/` para as duas modalidades; `/locutores/` somente humanos; `/vozes-ia/` somente IA. As listas também são reutilizadas nas páginas de conversão. Os componentes antigos `featured-voices` e `landing-voices` não são mais usados pelas páginas.

Dados IA: `data/vozes-ia.json`. A integração de novos MP3 do Drive é manual; depois de atualizar os dados/arquivos, execute `npm run build` para regenerar todas as listas e publique pelo fluxo GitHub Pages.
