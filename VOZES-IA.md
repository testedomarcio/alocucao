# Catálogo de Vozes IA

Página pública: https://alocucao.com.br/vozes-ia/

Acesso direto: https://alocucao.com.br/vozes-ia/#banco-de-vozes

## Atualizar

1. Edite `data/vozes-ia.json`: nome, descrição, gênero, estilo e etiquetas. Não atribua características sem confirmação. `drive_id` documenta a origem do áudio; não é usado como player público.
2. Baixe o original da pasta Drive indicada pelo proprietário, sem o modificar. Coloque uma cópia otimizada em `assets/vozes-ia/audio/<id>.mp3`. Exemplo: `ffmpeg -i original.mp3 -map_metadata -1 -ac 1 -ar 44100 -codec:a libmp3lame -b:a 96k <id>.mp3`.
3. Adicione `"audio": "<id>.mp3"` e `"duration": 40` (duração real em segundos) ao perfil. Na ausência do campo de áudio, a página exibe “Demonstração em breve”. Kaique corresponde ao arquivo Kaike.mp3 fornecido no Drive.
4. Use retratos fictícios em `assets/vozes-ia/images/<id>.webp`. Eles representam perfis sintéticos, sem afirmar a identidade de pessoas reais.
5. Execute `npm run build` para regenerar a página IA e todas as listas compartilhadas, verifique os arquivos e publique pelo fluxo GitHub Pages existente. O HTML é pré-renderizado; não depende de JS para exibir o catálogo.

Não há sincronização automática com o Drive. Novos arquivos exigem atualização e publicação. O script não baixa áudios nem altera os originais.

## Medição

O catálogo reutiliza `alocucaoTrackEvent` e o consentimento existentes. Eventos GA4: `ia_demo_play`, `ia_voice_select`, `ia_filter_select`. Cliques WhatsApp usam o evento global `whatsapp_click`, com `service_name=vozes_ia`, origem, campanha e `cta_id`; o evento global também alimenta UET. Nenhuma meta de conversão nova foi configurada nas plataformas de anúncios.

## Pendentes no momento da implementação

Will, Aida, Thiago e Ana Alice sem áudio na pasta lida. David, Eduardo S, Roberta, Fernanda, Amanda Kelly, Cassio Cruz e Marcio usam descrição neutra até confirmação do perfil vocal.
