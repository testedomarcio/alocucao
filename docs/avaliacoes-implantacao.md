# Avaliações verificadas — implantação

## Estado entregue em 27/10/2026

A interface pública está preparada para todos os 27 locutores atuais e futuros: estrelas SVG cinza, “0 avaliações”, resumo no perfil e nos cards, seção `#avalie` e política de moderação. Os recursos comerciais anteriores são preservados. A ordem aleatória não é modificada.

O recebimento permanece **desativado** em `assets/reviews-config.js`. Não há formulário de envio enquanto o serviço não estiver configurado. A área administrativa também informa a pendência de configuração. As migrações e funções são código preparado; não constituem um serviço provisionado.

Nenhuma conta externa foi criada, nenhum plano pago foi contratado e nenhuma avaliação fictícia foi publicada. Não há custo recorrente contratado por esta alteração. O custo de operação dependerá dos planos escolhidos e do uso de Supabase/Cloudflare; conferir as condições vigentes antes de ativar, sem upgrade automático autorizado.

## Configuração necessária

1. Criar/selecionar um projeto Supabase sob controle do proprietário. Conferir região, capacidade, backup, condições de transferência internacional e limites de custo antes de ativar.
2. Instalar a CLI Supabase e autenticar localmente. Executar `supabase link --project-ref SEU_PROJECT_REF`. Não armazenar credenciais no Git.
3. Aplicar as duas migrações em `supabase/migrations/` com `supabase db push` após revisar o diff. Elas criam tabelas com RLS e sem permissões de navegador, funções exclusivas do servidor e um bucket **privado** `review-images`.
4. Executar `python3 scripts/prepare-reviews.py` e aplicar `supabase/seed-review-voices.sql` pelo SQL Editor do projeto. Repetir esse passo ao cadastrar novas vozes; a interface é gerada automaticamente pelo catálogo.
5. Pelo Supabase Auth, criar um usuário administrativo com senha forte e **desabilitar cadastro público**. Não há envio de convite de e-mail por este código. Aplicar no SQL Editor: `insert into public.review_admins(user_id) values ('UUID_DO_USUARIO');`. Apenas o dono do projeto pode conceder esse acesso. Testar também com um usuário comum, que deverá receber acesso negado.
6. Criar um widget Cloudflare Turnstile autorizado para `alocucao.com.br`. A ação esperada é `review`; hostname e ação são conferidos no servidor.
7. Configurar o segredo `TURNSTILE_SECRET_KEY` no gerenciador de segredos da Edge Function. `SUPABASE_URL` e `SUPABASE_SERVICE_ROLE_KEY` ficam exclusivamente no ambiente Supabase; nunca em `assets/`. `REVIEWS_ORIGIN` deve ser `https://alocucao.com.br`.
8. Preparar a dependência de imagens: `npm install --no-save @imagemagick/magick-wasm@0.0.30` e `node scripts/prepare-review-images.mjs`. Isso gera um WASM local ignorado pelo Git e incluído pela CLI via `static_files` em `supabase/config.toml`. O código de processamento usa a mesma versão fixada. Rodar `deno check` e testar no runtime local da CLI antes do deploy.
9. Publicar a função: `supabase functions deploy reviews`. O gateway tem `verify_jwt=false` porque clientes não precisam de conta. Todas as ações administrativas fazem verificação real de usuário em `/auth/v1/user` e na lista privada `review_admins`. Não basta possuir qualquer JWT.
10. Preencher `url`, `anonKey` (chave pública/anon) e `turnstileSiteKey` em `assets/reviews-config.js` de um ambiente de homologação. O frontend aceita projetos padrão `https://PROJECT.supabase.co`. Nunca colocar service role ou segredo Turnstile nesse arquivo.
11. Concluir os testes de ativação abaixo em um projeto de homologação. Só depois alterar `enabled:true` e publicar a configuração de produção. Não transferir avaliações de teste.
12. Atualizar o parágrafo da Política de Privacidade que diz que o sistema está em preparação quando o recebimento for efetivamente ativado. Ajustar o versionamento de cache dos arquivos de configuração a cada ativação/alteração.

## Operação

- Painel: `https://alocucao.com.br/administracao/avaliacoes/` (shell público; dados e operações privados).
- Link simples: `https://alocucao.com.br/locutores/aline-mota/#avalie`.
- O painel gera links `?convite=TOKEN#avalie` para um locutor e pedido. Validade de 1 a 90 dias; padrão de 30. Reemitir um convite não utilizado invalida o anterior. Pedido já avaliado não pode gerar outro convite.
- O token tem 256 bits de aleatoriedade; o banco armazena somente SHA-256. O consumo é transacional e bloqueia a linha do convite; há unicidade de avaliação por convite e convite por locutor/pedido. A identificação do pedido deve ser estável e consistente; não inserir dados pessoais nesse campo.
- A página remove o token da barra de endereço antes dos scripts de medição e usa política de referência `no-referrer`. O token permanece somente na memória da página. Reabrir o link original se for necessário atualizar a página antes do envio.
- Sessões administrativas são mantidas na memória; ao expirar, entrar novamente. Não há senhas administrativas ou tokens em localStorage. Encerrar o acesso com “Sair”.
- A moderação registra responsável, data, decisão e justificativa. A interface não oferece alteração de nota. Avaliações negativas legítimas devem ser publicadas pelos mesmos critérios das positivas.
- As médias públicas incluem somente aprovadas e são consultadas novamente a cada visita. Recarregar páginas já abertas para ver decisões recentes. Não foi criado canal Realtime nem há promessa de push em abas abertas.
- O bucket é privado, sem políticas de acesso direto. Imagens pendentes exigem administrador. Mesmo imagens aprovadas são entregues pela função, que confere o status a cada acesso; ocultar uma avaliação impede novas consultas à sua imagem. Dados de pedidos e convites nunca são retornados por endpoints públicos.
- JPG, PNG e WebP estáticos de até 2 MB, 4000 × 4000 e 12 megapixels são validados pelo conteúdo e pelas dimensões antes de decodificar. A função recodifica para WebP com até 512 pixels no maior lado e remove metadados. O nome original não é armazenado. SVG/GIF/executáveis são recusados.
- A proteção inclui Turnstile no servidor e limite persistente de 30 tentativas/hora por convite; administradores têm 500 operações/hora. Os endpoints públicos de leitura devem receber também limites de tráfego no gateway/WAF caso haja abuso; não se deve inventar IP a partir de cabeçalhos controlados pelo cliente.
- A exclusão solicitada pelo titular é realizada no painel, após verificação de identidade pelo atendimento. Remove o depoimento e histórico e enfileira a eliminação da imagem. A referência privada do pedido/convite consumido é conservada pelo prazo operacional máximo de 24 meses para impedir reutilização e atender registros do pedido.

## Retenção e manutenção (configurar antes de ativar)

O painel possui “Executar retenção e excluir imagens pendentes”. A função `review_cleanup` remove avaliações pendentes/rejeitadas/ocultadas com mais de 90 dias e todas as avaliações com mais de 24 meses, a partir do envio; também apaga limites vencidos e convites antigos. Imagens entram em fila transacional e são excluídas pelo comando `cleanup` da Edge Function; falhas são retomadas na próxima execução (lotes de 100).

Configurar uma rotina diária de operação ou um agendador seguro sob controle do proprietário para chamar a limpeza. Nenhum agendamento externo foi criado nesta entrega. Registrar a execução e repetir enquanto houver imagens na fila. Reconciliar também objetos privados órfãos após falhas de rede/interrupção de upload, removendo somente os que não estiverem referenciados por nenhuma avaliação; nunca tornar o bucket público. Incluir os backups e sua expiração no procedimento de atendimento a exclusões.

## Validação reproduzível

- `npm run build && npm test`: validação geral e das 27 interfaces, estado zero, bloqueio de rede enquanto desativado, limites de campos e cabeçalhos de imagem.
- `npm install --no-save @electric-sql/pglite@0.5.12 && npm run test:reviews:db`: executa PostgreSQL WASM com as migrações reais. Verifica permissões anon/authenticated, validade, locutor correto, consumo, substituição de convite, moderação, média real, ocultação, exclusão, retenção e limites.
- `deno check supabase/functions/reviews/index.ts`: checagem TypeScript das funções, com dependências instaladas conforme o runtime Deno/CLI.

### Obrigatórios em homologação antes de receber clientes

1. Envio completo com Turnstile real, sem cadastro, com e sem imagem; testar os três formatos, arquivo falsificado, oversized e dimensões excedidas.
2. Disparar simultaneamente dois envios com o mesmo convite: somente um deve persistir. Conferir remoção segura de uploads excedentes.
3. Verificar convite expirado, usado, de outro locutor e token malformado. Simular falha de rede após commit.
4. Confirmar acesso negado às tabelas, RPCs, bucket e ações administrativas com chave pública, sem login e com usuário comum.
5. Aprovar uma avaliação e conferir perfil/card após nova consulta; rejeitar/ocultar/excluir e confirmar média e imagem recalculadas/indisponíveis. Nenhuma pendente deve aparecer na lista pública.
6. Testar filtros, histórico, cópia de convite, login expirado e exclusão. Verificar backup e rotina de retenção.
7. Validar teclado, leitor de tela, erros, campos e CAPTCHA em celular e desktop.
8. Testar falha do Supabase: demos, filtros e WhatsApp continuam funcionando; avaliações exibem indisponibilidade em vez de inventar zero.
9. Nenhuma avaliação ou imagem de teste em produção. Nenhum segredo no repositório. Confirmar política e consentimento da versão ativada.

Referências técnicas: https://supabase.com/docs/guides/database/postgres/row-level-security e https://supabase.com/docs/guides/functions/examples/image-manipulation.
