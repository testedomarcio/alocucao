# Banco de vozes — operação e manutenção

A página /vozes/ utiliza HTML, CSS, JavaScript sem framework e JSON no próprio domínio. Não baixa MP3 antes do clique. Uma única tag audio serve para todas as demos. Favoritos ficam no navegador; a comparação aceita até três vozes. Não há classificações por estrelas inventadas ou agenda presumida.

## Sincronização

O workflow Atualizar banco de vozes consulta a página pública https://painel.audio.net.br/Vozes/alocucao a cada 15 minutos, nos minutos 02, 17, 32 e 47 de cada hora, e também aceita workflow_dispatch. A consulta usa um identificador explícito A-Locucao-Catalog-Sync, sem cookies ou senha. Não é uma API oficial do fornecedor: é um adaptador para a tabela pública. Alterações no HTML podem exigir manutenção.

O parser HTML5 é necessário para reproduzir a correção de estrutura que o navegador aplica à tabela de origem. A primeira tentativa com html.parser não extraiu todas as linhas; essa versão foi substituída antes da troca da interface. A versão validada extraiu 164 locutores e verificou que a quantidade de registros corresponde à de demos.

O resultado fica em assets/voices-catalog.json, com fetchedAt, contentUpdatedAt, hash e lista completa. O script atualiza também o ItemList e a lista noscript. A página contém apenas 24 cartões inicialmente e adiciona mais 24 por ação, para limitar o custo de renderização.

A atualização é periódica, sujeita ao tempo de execução e publicação do GitHub. Não é um webhook nem uma promessa de atualização instantânea. A página consulta novamente seu JSON a cada 15 minutos enquanto está visível e ao voltar de outra aba. O cache do site também pode introduzir atraso.

O workflow tem publicação própria com Jekyll e deploy-pages: commits do GITHUB_TOKEN não devem ser usados como garantia de disparo automático do build padrão. Apenas scripts e artefatos validados são adicionados ao commit, com rebase antes do push.

## Falhas e dados vencidos

403, timeout, tabela ausente, URL inesperada, duplicidade, catálogo vazio, extração incompleta ou redução acima de 35% interrompem a sincronização. O último JSON válido permanece. O GitHub Actions mostra a falha. Verifique Actions → Atualizar banco de vozes e consulte o suporte do fornecedor quando necessário; não contorne restrições de acesso.

Após três horas sem consulta válida, a interface troca os status por Disponibilidade sob consulta. Demos e filtros restantes continuam funcionando. Offline/indisponível são estados do catálogo, não disponibilidade calculada por horário habitual. Nenhum status confirma prazo contratual: isso continua sendo combinado no atendimento.

## Dados externos

Áudios aceitos: HTTPS em storageoffs.offsbrasil.com.br. Perfis: perfillocutor.com.br ou www.perfillocutor.com.br. IDs são slugs do perfil, não IDs oficiais garantidos. Gênero vem dos marcadores da linha; a pasta masculino dos MP3 também contém demos femininas. O marcador paulista é normalizado para São Paulo. Campos de nome e estilo são renderizados com textContent. Não copiar HTML da fonte para o DOM.

O parâmetro nocache é de cache, não uma chave de API. O player usa a data da consulta para renovar o cache de demos com o mesmo caminho. Não renomear os MP3 a partir do nome de exibição.

## Verificação

Foram testados busca sem acento, filtros, favoritos, limite de comparação, carregamento progressivo, player único, nenhum MP3 antes do clique, oito larguras entre 320 e 1440 px, CTAs responsivos, dados vencidos, armazenamento bloqueado, texto externo com marcação e mídia inválida. Os eventos de reprodução e WhatsApp usam os scripts compartilhados e dependem do consentimento; não há promessa de contato recebido ou venda a partir do clique.

Se o fornecedor oferecer API/feed oficial ou webhook, substituir a etapa de coleta preservando o formato JSON e a interface. Se o catálogo crescer ou diminuir legitimamente acima do limite, conferir a fonte e ajustar o limite com evidência, em vez de remover a proteção.

## Lista e fotos

A exibição padrão é lista; o usuário pode alternar para cartões. A preferência é local. Fotos vêm do campo imgPerfil no perfil público, e são importadas como WebP de até 160px, com leitura da imagem limitada a 6MB. A página carrega as miniaturas com loading=lazy e decoding=async. Onde não houver imagem, as iniciais permanecem; nenhuma foto é gerada. Perfis são conferidos no máximo uma vez por dia, com duas consultas concorrentes. Falhas não impedem a sincronização de status e preservam a foto anterior. Não são usadas credenciais; três falhas iniciais interrompem as consultas restantes de fotos.


## Horários de gravação e perfis locais

O importador de fotos também lê a tabela pública #captain de cada perfil. Não realiza requisições extras no navegador: a agenda é texto no mesmo JSON. Os perfis são consultados diariamente; os status continuam no ciclo de 15 minutos. O parser reconhece os sete dias e intervalos HH:MM, remove o marcador Hoje, valida horas e não presume folga nos dias ausentes. Não calcula online/offline a partir da agenda e não presume o fuso horário. Falha na foto preserva os horários que foram lidos; falha na consulta do perfil mantém a última agenda válida.

Cada locutor recebe localProfile e profilePublished. As rotas planejadas ficam em data/voice-profile-routes.json. São geradas do nome sem acentos e com hífens; o identificador resolve nomes duplicados. Uma rota já registrada é mantida quando o nome muda. O link discreto Ver perfil aparece somente quando existe perfil-locutor-<slug>/index.html. O ItemList e a lista HTML de fallback também passam a apontar ao perfil local publicado. O workflow é disparado por publicações nessas pastas e também confere a existência no ciclo periódico.

Consulte PERFIS-LOCUTORES-JULES.md antes de criar os perfis. Não publicar páginas vazias para tornar os links visíveis.
