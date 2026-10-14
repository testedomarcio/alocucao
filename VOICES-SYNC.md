# Banco oficial de vozes

Fonte única: https://vozes.alocucao.com.br/. O sincronizador lê o catálogo público `locutoresData`, valida IDs, nomes e URLs de mídia e preserva a última versão se a fonte estiver incompleta ou indisponível.

O workflow consulta o catálogo a cada 15 minutos (a execução pode atrasar no GitHub Actions), publica no GitHub Pages e pode ser iniciado manualmente. Não usa login nem altera dados na origem. Fotos e áudios vêm do domínio oficial. O banco completo verifica a versão publicada a cada 5 minutos e ao voltar à aba, sem interromper uma demo em reprodução. Status com mais de 45 minutos são apresentados como sob consulta.

`/vozes/#demo` abre o catálogo próprio. Ordem aleatória a cada abertura, estável ao pesquisar. Filtros de nome, gênero e estilo, áudios carregados só quando solicitados e botões de WhatsApp com nome do profissional.

As páginas de conversão usam 8 vozes: Celso Ricardo, Lindy, Gabriel Zamboni, Elissandra Lima, Sunshine, Absamira Santos, Charles Helfer e Tito Maciel. Seleção editorial pela variedade de estilos e vozes, sem alegar desempenho de conversão medido. Nome, foto, estilos e áudio; sem status nem cadastro. Fonte e IDs em scripts/generate-featured-voices.py.
