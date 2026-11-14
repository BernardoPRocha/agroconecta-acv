# Vídeo de ACV - roteiro pronto para Bernardo

Duração sugerida: 3 a 4 minutos. Gravação pendente. Este roteiro não é um vídeo gravado e não comprova coleta em campo.

## Antes de gravar

Abra o sistema com INICIAR_WINDOWS.bat, acesse localhost:8000, atualize com Ctrl+F5 e prepare as imagens da pasta examples. Abra o relatório na página das métricas. Prepare uma fotografia de folha de tomate em outro dispositivo para o teste da câmera. Grave tela e sua voz; evite mostrar senhas, tokens ou informações pessoais.

| Tempo aproximado | O que mostrar | O que falar |
|---|---|---|
| 0:00-0:25 | Página inicial | “Eu sou Bernardo Rocha, RM99209. Nosso grupo também tem Eric Rodrigues, RM550249, e Renato Izumi, RM99242. Este é o módulo de visão computacional do AgroConecta, voltado ao apoio de pequenos produtores.” |
| 0:25-0:50 | Área de análise e categorias | “O protótipo analisa folhas de tomate e reconhece três categorias: aparência saudável, possível pinta-preta e possível requeima. Ele não reconhece todas as doenças nem foi treinado para outras culturas.” |
| 0:50-1:20 | Enviar 1_pinta_preta_1.jpg e analisar | “Ao enviar a foto, a aplicação chama nossa API e o detector retorna caixas, categorias e confiança. Os números das etiquetas correspondem à lista ao lado. Confiança é a pontuação do modelo, não certeza de diagnóstico.” |
| 1:20-1:55 | Usar câmera e mover a imagem no enquadramento | “Agora a análise usa a câmera física do computador. Estou apontando para uma fotografia exibida em outra tela. Isso demonstra captura e inferência contínua; não é um teste com uma planta real no campo.” |
| 1:55-2:20 | Parar câmera e analisar 2_requeima_1.jpg | “O sistema também pode falhar. Neste exemplo, com o limite inicial de 40%, o resultado é inconclusivo. Ausência de detecção não significa que a planta esteja saudável.” |
| 2:20-2:55 | Relatório: dados e métricas | “Usamos um recorte real do PlantDoc, com 180 imagens de treino, 45 de validação e 27 de teste. Ajustamos um YOLOv8n durante 30 épocas. O mAP a IoU 0,5 foi de 68,6%. Essa métrica avalia detecção e não equivale a 68,6% de diagnósticos corretos.” |
| 2:55-3:25 | Relatório: erros e API | “Ainda existem confusões entre doenças e folhas não detectadas. Os erros estão documentados. A API permite conectar o módulo aos demais componentes do AgroConecta. A próxima validação será com mais imagens externas e folhas reais.” |

O tempo é uma referência. Descreva o resultado que realmente aparecer na sua gravação; não repita valores diferentes dos que estiverem na tela.

## Finalizar

Revise se textos e áudio estão legíveis, publique o vídeo na modalidade solicitada pelo professor e copie o link real. Não foi informado limite específico de duração de ACV no resumo recebido; confira o enunciado original antes da gravação definitiva.

## Demonstração já incluída

`docs/videos/Demonstracao_ACV_Fotos.mp4` registra a interface executando três fotos com o modelo real (aparência saudável, possível pinta-preta e resultado inconclusivo). É uma demonstração automática sem áudio; não contém a câmera física nem substitui a apresentação narrada deste roteiro.
