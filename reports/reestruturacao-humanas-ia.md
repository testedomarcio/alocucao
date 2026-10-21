# A Locução — vozes humanas e inteligência artificial

## Resultado

- 414 arquivos HTML inventariados, incluindo redirecionamentos históricos.
- 64 páginas existentes atualizadas e uma nova página específica para locutores humanos.
- 20 páginas com o novo catálogo compartilhado em lista.
- 116 locutores humanos consultados na fonte oficial.
- 22 perfis IA, com 18 demonstrações e quatro perfis aguardando áudio.
- Nova leitura da pasta Drive: 18 MP3, todos já integrados; nenhum arquivo adicional encontrado nessa leitura.

Catálogos: `/vozes/` apresenta ambas as modalidades; `/locutores/` apresenta humanos; `/vozes-ia/` apresenta IA. A âncora `/vozes-ia/#banco-de-vozes` permanece. Não havia uma rota de catálogo humano própria apropriada: as antigas páginas individuais são redirecionamentos para `/vozes/`; por isso foi criada `/locutores/`, com conteúdo e finalidade distintos.

## Atualização humana automática

A fonte continua sendo `https://vozes.alocucao.com.br/`. O catálogo público `locutoresData` é consultado e validado pelo sincronizador já existente, sem login, dados privados ou alteração na origem. Também foi identificada e testada a API pública `check_status.php` da própria vitrine, com CORS habilitado e escopo da loja 382, conforme o código público da fonte.

O workflow `sync-voices.yml` consulta a fonte a cada 15 minutos, sujeito a atrasos do GitHub Actions, atualiza o JSON público e regenera as listas indexáveis das páginas. O navegador consulta esse JSON ao abrir, ao retornar à aba e a cada cinco minutos para atualizar perfis e totais. A disponibilidade é consultada diretamente na API pública a cada 30 segundos, somente com a página visível, por atualizações incrementais e sem credenciais. A resposta é validada e usada como texto, ignorando o HTML enviado pela origem. Os status não mudam a ordem da lista nem interrompem áudios.

O total é calculado pelos dados. Estados humanos seguem a fonte: não são convertidos em Online. O cache periódico com mais de 45 minutos aparece sob consulta quando não há status direto válido; uma falha na consulta direta também mostra disponibilidade sob consulta até a próxima tentativa. Os áudios e perfis continuam disponíveis mesmo quando o status não pode ser consultado.

Não se trata de disponibilidade instantânea. A interface mostra a data da atualização e orienta a confirmação do prazo. A sincronização de IA com o Drive continua manual: novas demonstrações precisam ser integradas e publicadas.

A primeira execução do workflow após a publicação encontrou timeout de conexão ao servidor de origem. Foram adicionadas até três tentativas para falhas transitórias de rede (sem repetir erros de autorização nem aceitar dados inválidos). A execução seguinte passou, atualizando o catálogo automaticamente. O catálogo publicado preserva os últimos dados válidos e o tratamento de falhas.

## Interface e conteúdo

Dois painéis em computadores e abas em celulares, com busca e filtros independentes. Listas horizontais compactas, fotos/avatares, nome, características, disponibilidade, reprodução e seleção pelo WhatsApp. São mostradas inicialmente 12 vozes por painel, com botão para carregar mais. Os perfis permanecem no HTML para indexação e uso sem JavaScript.

Ordem inicial aleatória e estável durante busca, filtros, carregamento adicional e atualização de status. O áudio é carregado quando solicitado. Ao iniciar outra reprodução, o áudio anterior é pausado, inclusive nos portfólios da página. Há estados de carregamento, falha e disponibilidade sob consulta. Os filtros possuem rótulos; as abas possuem navegação por teclado.

Zozo está classificado como Masculina. Perfis IA possuem Online com explicação de disponibilidade para pedido, retratos ilustrativos e avisos junto à lista e no rodapé.

Os botões identificam nome, modalidade e página de origem na mensagem do WhatsApp oficial. Os eventos existentes de clique e consentimento foram preservados. Eventos adicionais: `voice_select`, `voice_demo_play` e `voice_filter_select`, por meio de `alocucaoTrackEvent`.

## Preços e posicionamento

Home, serviços, Off, Spot, preços, sobre, regionais e landing pages passaram a apresentar as duas modalidades. O artigo `/blog/voz-ia-ou-locucao-humana/` foi reescrito porque ainda dizia que a empresa oferecia apenas locução humana. Foram preservados os conteúdos especificamente humanos, os exemplos entregues e as respectivas identificações.

Avulsos por até 40 segundos: Off humano R$ 11,90; Off IA R$ 8,50; Produzida humana R$ 29,90; Produzida IA R$ 19,00. Comparativo explícito e economia aproximada de 29% e 36%. Pacotes humanos não foram recalculados e não foram criados pacotes IA.

Black Friday: condição humana publicada de Off R$ 8,90 e Produção R$ 16,90 até 10/11/2026, com tratamento de encerramento já existente preservado. A página de boas-vindas mantém o primeiro pedido humano elegível, sujeito à validação pelo WhatsApp. Essas promoções são identificadas separadamente dos valores IA.

## Páginas com catálogo

Home; `/vozes/`; `/locutores/`; `/vozes-ia/`; `/locucao-off/`; `/spot-comercial/`; `/spot-black-friday/`; `/producao-para-supermercados/`; `/producao-para-igrejas/`; `/gravacao-off-e-producao/`; `/locucao-para-video-institucional/`; `/espera-telefonica-ura/`; `/vinhetas-para-podcast-e-radio/`; `/calculadora/`; `/portfolio/`; `/spot-para-carro-de-som/`; e os artigos `/blog/voz-ia-ou-locucao-humana/`, `/blog/locucao-off-o-que-e/`, `/blog/locucao-comercial-publicitaria/`, `/blog/agencia-de-vozes-locucao-comercial/`.

## Landing pages

URLs existentes mantidas: Off, Spot, supermercados, igrejas, boas-vindas/concorrentes, Black Friday, carro de som, vídeos, URA, vinhetas, agências e Natal. As páginas regionais receberam o posicionamento e a comparação de preços. Nenhuma configuração ou anúncio do Microsoft Advertising foi alterado. Não foi feita leitura da conta de anúncios nesta execução; a correspondência dos textos dos anúncios ativos com os novos preços não foi verificada no painel.

## SEO e testes

Titles, descriptions, H1, Open Graph e descrições estruturadas das páginas comerciais revisados. Ofertas estruturadas identificam modalidade, serviço, preço e duração. Novo catálogo humano no sitemap; canonicals preservados. Nomes e descrições dos perfis estão no HTML, sem depender de iframe. Cabeçalhos e rodapés mantêm a identidade da empresa e os links entre modalidades.

Verificações concluídas: build; sintaxe JavaScript; auditoria de 61 URLs canônicas sem erros; links e arquivos locais das páginas alteradas; IDs únicos; contagem dos perfis; URLs dos áudios entregues preservadas; testes funcionais com DOM do HTML real (filtros, busca sem acentos, abas, progressão, ordem estável, visitas aleatórias, reprodução, eventos, status humanos e estado desatualizado); testes de consentimento e tracking existentes; 116 URLs de áudio humano respondendo HTTP 200 e tipo de áudio.

Não foram medidos Core Web Vitals nem feita avaliação visual em navegador real neste ambiente. As regras responsivas e de acessibilidade foram verificadas no código e no DOM. Search Console e Bing Webmaster Tools não foram acessados para verificar indexação real. Nenhuma posição nos resultados é prometida.

## Pendências de áudio IA

Will, Aida, Thiago e Ana Alice continuam com “Demonstração em breve”, sem player quebrado. Os demais 18 arquivos estão associados aos respectivos perfis. Não foram usados áudios de outras vozes para preencher essas lacunas.

## Manutenção

Dados IA em `data/vozes-ia.json`; componente em `scripts/unified-catalog.py`; interface em `assets/unified-voices.js` e `.css`. Ao adicionar áudio IA, atualizar nome do arquivo/duração, executar o build e publicar. O build regenera a página IA e todos os componentes compartilhados. O workflow humano também regenera os componentes quando os profissionais mudam.
