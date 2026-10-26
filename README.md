# A Locução

Site estático da produtora A Locução, publicado pelo GitHub Pages em https://alocucao.com.br.

## Manutenção

- `data/new-voices.json`: perfis, características, e-mails profissionais e caminhos separados de demonstração Off e Produção Completa.
- `data/site-pages.json`: conteúdo editorial e rotas anteriores preservadas após a migração.
- `data/legal-pages.json`: documentos jurídicos personalizados; revisão por advogado não é presumida.
- `scripts/build-nova.py`: gerador único das páginas e sitemap.
- `assets/nova.css` e `assets/nova.js`: identidade visual, navegação, filtros e reprodução de áudio.
- `assets/demos/`: áudios fornecidos para o novo catálogo, hospedados neste domínio.
- `assets/privacy.js` e `assets/tracking.js`: consentimento e medição de cliques pelo WhatsApp.

Execute `npm run build` e `npm test`. O build usa apenas a biblioteca padrão do Python. Os testes dinâmicos usam Node.js.

Não execute os geradores antigos isoladamente: eles pertencem ao modelo comercial anterior. As automações antigas de importação do fornecedor e publicação de artigos foram retiradas do agendamento para evitar a reintrodução de regras antigas. O conteúdo editorial existente foi mantido; novas publicações devem entrar em `data/site-pages.json` e passar pelo gerador atual.

## Especificação comercial vigente em 26/10/2026

Locução Off R$ 12,00 e Produção Completa R$ 25,00 por peça comercial de até 40 segundos. Narrativas longas e projetos especiais sob orçamento. Atendimento de segunda a sexta, 08h–18h, e sábado, 08h–12h, horário de Brasília. Contratação pelo WhatsApp +55 27 99652-9832. Não divulgar outros idiomas.

## Limitações da hospedagem

GitHub Pages não oferece configuração nativa de redirecionamentos HTTP 301 por rota. As rotas equivalentes mantidas como compatibilidade servem conteúdo e indicam a URL principal com canonical e noindex. Não há redirecionamento HTML. Um 301 real exige uma camada de servidor/proxy compatível e deve ser tratado separadamente, sem mudança de DNS automática.

Relatório da migração em `reports/reformulacao-2026-10-26/RELATORIO.md`.

### Últimos trabalhos dos perfis

`data/latest-works.json` organiza os projetos por `voice` (slug existente), cliente/título, data real do trabalho e formato. O gerador mantém as demonstrações fixas e acrescenta a seção `#ultimos-trabalhos` somente nos perfis com projetos disponíveis, ordenados por data decrescente. Os players usam MP3 locais em `assets/trabalhos/`, sem autoplay e com carregamento sob demanda.

A pasta autorizada de importação tem ID `1gX1hUIiTJEbvXC5GAJjIKU3JrFCtBqLY`. Organize como `Locutor / Tipo e cliente — data / áudios`. Os IDs, nomes, datas de modificação e hashes de origem ficam no JSON para evitar duplicações; nenhum link do Drive é incluído nas páginas. Datas e clientes devem vir da identificação fornecida, sem inferir a data do trabalho pelo upload. Arquivos sem identificação segura ficam pendentes. A atualização é executada pela tarefa semanal vinculada à conversa; o site não consulta o Drive no navegador.
