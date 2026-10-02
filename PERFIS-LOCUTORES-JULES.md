# Atualização: perfis agora gerados automaticamente

O usuário solicitou a criação dos perfis pela IA. As páginas são geradas por scripts/generate-voice-profiles.py e atualizadas pelo workflow. Consulte VOICES-SYNC.md para manutenção; não recriar os arquivos ou as rotas abaixo. As instruções originais permanecem como referência de qualidade.

# Perfis de locutores — instruções para o Jules

## Objetivo e rotas

Criar páginas úteis e individuais no site existente, preservando o banco de vozes, player, filtros, fotos, favoritos, âncoras e sincronização.

Use data/voice-profile-routes.json como relação oficial de IDs, nomes e caminhos. Para cada path, crie a pasta correspondente e index.html. Exemplo: /perfil-locutor-elissandra/ corresponde a perfil-locutor-elissandra/index.html. O nome completo é normalizado sem acentos e com hífens. Não gerar uma segunda regra de slugs nem alterar rotas existentes.

O banco adiciona automaticamente o link discreto Ver perfil quando o arquivo existe. Até lá o link não é exibido, evitando 404. Publicar essas pastas dispara a sincronização; conferir Actions → Atualizar banco de vozes e o resultado do deploy.

## Conteúdo de cada perfil

- H1 com o nome real e a profissão. Title e description específicos, canonical para a rota local e breadcrumb com link para /vozes/.
- Foto local real, quando houver, de assets/voices-catalog.json; fallback com iniciais.
- Demonstração de áudio com preload=none; MP3 apenas ao clicar, sem autoplay.
- Estilos, região e idiomas somente conforme o catálogo. Campos ausentes não devem ser inventados.
- Horários semanais do campo schedule. Os dias ausentes não significam folga. Não assumir fuso, disponibilidade imediata ou prazo; mostrar a data da consulta e orientar a confirmação.
- Orientação específica útil sobre seleção e aplicação da voz, baseada nas demos e dados confirmados. Não repetir um texto genérico apenas trocando nomes. Não inventar biografia, experiência, clientes, avaliações ou especialidades.
- CTA para verificar orçamento/disponibilidade pelo WhatsApp já utilizado pelo site. Voltar ao banco com /vozes/#voice-grid.
- Schema Person e WebPage coerentes com o conteúdo visível. Usar dados reais, sem avaliações ou estrelas fabricadas.
- Inserir os perfis publicados no sitemap, preservar sua configuração atual e conferir as URLs finais com barra.

## Atualizações e desempenho

A página pode consultar o JSON local para atualizar status, horários e fotos, mas o conteúdo principal deve existir no HTML. Reutilizar assets do projeto; sem bibliotecas, iframes externos ou busca individual de perfil do fornecedor no navegador. Preservar privacy.js e tracking.js e as escolhas de consentimento.

Começar pelos perfis com conteúdo completo e revisar a qualidade antes de ampliar. A existência do arquivo ativa o link; publicar só páginas prontas.

## Validação

Testar a página em 320px, celular e desktop, links e canonical, carregamento de uma demo real, navegação de volta ao catálogo, nenhuma requisição de MP3 antes do clique e ausência de erros no console. Confirmar deploy concluído e resposta HTTP 200, sem placeholders ou redirecionamentos para o catálogo.
