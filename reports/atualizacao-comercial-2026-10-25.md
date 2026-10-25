# Atualização comercial — 25/10/2026

Status: implementada e verificada localmente; publicação bloqueada pela revisão automática. A versão pública permanece no commit eae72a66d778ef037bc17799c6b38dbe8aeb0185. Alterações locais no commit a9474bd2f384b700ea4694294b4c9dca088219d3.

## Alterações preparadas

- Locução Off avulsa: R$ 15,00. Produção Completa avulsa: R$ 30,00. Um crédito corresponde a até 40 segundos.
- Pacotes Off: 3 por R$ 36,00; 10 por R$ 100,00; 20 por R$ 120,00.
- Pacotes Produção: 3 por R$ 75,00; 10 por R$ 200,00; 20 por R$ 300,00.
- Cartões com preço unitário, total, economia e destaque discreto para 20 créditos. Páginas gerais exibem os dois serviços; páginas específicas priorizam o respectivo serviço.
- Cadastro e login do painel em destaque; WhatsApp para atendimento, orientação e contratação dos pacotes.
- Preços vigentes em títulos que mencionam valores, textos, FAQs e dados estruturados.
- Política incorporada ao gerador final para evitar restauração dos preços antigos.
- Corrigido o preço estruturado da calculadora gratuita para zero; testes de duração preservados.

## Verificação realizada

- Build completo executado duas vezes. Testes de jornadas comerciais, matemática e links dos pacotes, geração repetida, schema, ativos locais, âncoras, catálogo e amostras aprovados.
- Testes existentes de Black Friday, tracking e consentimento, atribuição comercial, migração de vozes, calculadora e integração do catálogo aprovados.
- Auditoria SEO: 65 URLs do sitemap, sem erros reportados. Isso não comprova posições ou indexação futura nos buscadores.
- Inspeção visual da página Locução Off e dos cartões no navegador em tamanho de computador.
- CSS responsivo com quatro, duas e uma coluna. Não foi feita inspeção visual em dispositivo móvel.
- Catálogo e aviso IA com link para Termos preservados. O iframe externo não exibiu suas vozes neste navegador, inclusive na versão pública original; funcionamento interno dos filtros e áudios do fornecedor não pôde ser confirmado.
- Nenhuma alteração nas campanhas Microsoft Advertising, nas tags de medição ou no código e nas configurações do painel externo.

## Dependências e pendências

- Publicar após autorização explícita para atualizar a branch main do repositório público testedomarcio/alocucao, que alimenta o site principal.
- Confirmar as condições comerciais dentro do painel externo. Os botões de pacotes direcionam ao WhatsApp, sem anunciar compra automática.
- Após publicação, confirmar a implantação e conferir todas as landing pages ao vivo, inclusive /off-comercial/, com histórico de indisponibilidade. A página existe no código e foi atualizada; a disponibilidade pública após implantação ainda deve ser verificada.
- Cadastro e login: destinos conferidos, sem criação de conta ou autenticação de cliente.

## Páginas alteradas no código

- `/404.html`
- `/blog/agencia-de-vozes-locucao-comercial/`
- `/blog/como-escrever-texto-comercial-para-radio-e-carro-de-som/`
- `/blog/como-fazer-roteiro-para-carro-de-som/`
- `/blog/`
- `/blog/locucao-off-o-que-e/`
- `/blog/locucao-para-igrejas-e-eventos-evangelicos/`
- `/blog/locucao-para-supermercado/`
- `/blog/quanto-custa-um-spot-comercial/`
- `/blog/spot-black-friday/`
- `/blog/vinhetas-comerciais-para-radio-e-podcasts/`
- `/blog/voz-ia-ou-locucao-humana/`
- `/calculadora/`
- `/espera-telefonica-ura/`
- `/gravacao-off-e-producao/`
- `/`
- `/indique-e-ganhe/`
- `/locucao-campanha-politica/`
- `/locucao-ia/`
- `/locucao-off/`
- `/locucao-para-video-institucional/`
- `/locucao-voz-infantil/`
- `/locutores/`
- `/off-comercial/`
- `/planos-para-agencias-revenda/`
- `/precos/`
- `/producao-para-igrejas/`
- `/producao-para-supermercados/`
- `/produtora-de-audio-bahia/`
- `/produtora-de-audio-distrito-federal/`
- `/produtora-de-audio-espirito-santo/`
- `/produtora-de-audio-goias/`
- `/produtora-de-audio-minas-gerais/`
- `/produtora-de-audio-parana/`
- `/produtora-de-audio-rio-de-janeiro/`
- `/produtora-de-audio-rio-grande-do-sul/`
- `/produtora-de-audio-santa-catarina/`
- `/produtora-de-audio-sao-paulo/`
- `/servicos/`
- `/spot-black-friday/`
- `/spot-comercial-natal/`
- `/spot-comercial/`
- `/spot-para-carro-de-som/`
- `/tutoriais/como-adquirir-creditos/`
- `/vinhetas-para-podcast-e-radio/`
- `/vozes/`
