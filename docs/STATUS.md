# Situação da entrega - 10/11/2026

## Concluído e verificado

- Recorte PlantDoc real: 180 imagens de treino, 45 de validação, 27 de teste.
- Seis duplicatas removidas; seis imagens com classes fora do escopo excluídas; uma imagem rejeitada por incompatibilidade de proporção com a anotação.
- YOLOv8n ajustado por 30 épocas, imagens de 320 px, batch 8, CPU, semente 42. Peso `models/best.pt` incluído.
- Avaliação independente no conjunto de teste: precisão 0,6022; recall 0,6628; mAP@50 0,6858; mAP@50:95 0,4367. Não são métricas de diagnóstico clínico nem acurácia.
- API e interface executadas com o modelo real. Seis fotos testadas de ponta a ponta no navegador, incluindo erro e resultado inconclusivo.
- Fluxo da câmera testado com dispositivo simulado pelo Chromium, incluindo início, análise e parada. Nessa verificação inicial não foi usada câmera física; posteriormente Bernardo confirmou o uso físico, conforme registro abaixo.
- Layout inspecionado em 1365 px e 390 px, sem erro JavaScript e sem rolagem horizontal indevida no celular.
- Sete testes automatizados passaram, incluindo integridade dos conjuntos, entrada inválida, limite de tamanho, orientação EXIF e ausência de modelo.
- PDF técnico, análise de erros, notebook Colab, contrato da API e roteiro de vídeo incluídos.

## Limitações reais

O modelo ainda confunde doenças e perde folhas. Com confiança fixa 0,4 e IoU 0,5, a auditoria do teste encontrou 35 verdadeiros positivos, 29 falsos positivos e 25 falsos negativos, relativamente às anotações. As métricas agregadas de precisão/recall do Ultralytics usam seu próprio limiar escolhido na curva e não devem ser confundidas com esse ponto operacional fixo.

A base de teste tem somente 27 imagens e não representa todos os ambientes rurais. A anotação de folhas do PlantDoc pode ser incompleta. Não houve calibração da confiança, teste com outras culturas, validação agronômica nem estudo de impacto em produtores. O desempenho medido nesta máquina não garante o mesmo FPS em outro equipamento ou na nuvem.

## Pendente para finalizar a entrega acadêmica

1. Repetir rapidamente o teste com a interface atualizada antes de gravar; a câmera física já foi confirmada por Bernardo, apontada para uma imagem em outra tela.
2. Gravar a apresentação narrada com câmera e inserir o link. A demonstração automática de fotos, sem áudio, já está em `docs/videos/Demonstracao_ACV_Fotos.mp4`.
3. Publicar o repositório no GitHub e inserir o link da entrega.
4. Integrar o módulo ao MVP central e publicar a URL na etapa de Secure.
5. Conferir o enunciado original completo de ACV, além do resumo fornecido, antes de enviar à faculdade.

Dockerfile e Compose foram preparados, mas não executados: Docker não estava instalado neste ambiente. Não há deploy público realizado nem repositório remoto criado. Esses itens não devem ser apresentados como concluídos.

## Conteúdo do ZIP

Inclui dados preparados, rótulos, manifesto, scripts, modelo, resultados, documentação e exemplos. O cache bruto duplicado e ambientes virtuais foram excluídos. O dataset pode ser regenerado a partir do commit fixado. Leia README.md para instalar e abrir a aplicação; não é necessário treinar novamente para usar o modelo incluído.

## Atualização 1.1 - evidência fornecida pelo usuário

Bernardo informou que a câmera está funcionando e forneceu uma captura da câmera apontada para uma fotografia de folhas em uma tela. A captura mostra caixas e pontuações do detector. Isso registra uma demonstração de captura e inferência por câmera física; não é validação com folhas reais nem estudo em campo. Não há medição de FPS extraída dessa captura.

As etiquetas foram reduzidas para identificador e confiança, com correspondência numérica na lista completa. O modelo não foi retreinado e as métricas anteriores não foram alteradas.

Verificação da versão 1.1: seis fotos com inferência real, telas de 1280 px e 390 px, cenário sintético de 30 caixas apenas para testar o layout, sem sobreposição de etiquetas, cortes ou erros JavaScript. Resultado em `reports/ui_update_checks.json`. Os sete testes automatizados passaram novamente. Demonstração automática com fotos reais executada e gravada, sem áudio e sem câmera.
