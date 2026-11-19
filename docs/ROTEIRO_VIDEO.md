# Demonstração em vídeo — AgroConecta ACV

**Vídeo final:** https://www.youtube.com/watch?v=KIRmYhAmrdI

## Conteúdo apresentado

A demonstração audiovisual do módulo de visão computacional cobre:

1. Objetivo do AgroConecta e o uso da visão computacional na triagem de folhas de tomate.
2. Arquitetura do detector YOLOv8n, treinamento e integração com Python/FastAPI.
3. Metadados do modelo treinado e métricas da avaliação no conjunto de teste.
4. Execução do aplicativo com fotografias de folhas e visualização das caixas, categorias e confiança.
5. Captura pela câmera do dispositivo e análise de quadros sucessivos.
6. Limitações do protótipo e caráter experimental das classificações.

## Escopo da evidência

O aplicativo identifica aparência saudável, possíveis sinais de pinta-preta e possíveis sinais de requeima no recorte de folhas de tomate. As caixas correspondem a **folhas**, não a lesões individuais. A câmera foi demonstrada apontando para imagens em uma tela, sem teste de campo com plantas reais.

A avaliação do detector está em `reports/test_metrics.json` e o relatório acadêmico em `reports/Relatorio_Tecnico_ACV_AgroConecta.pdf`.

O arquivo `docs/videos/Demonstracao_ACV_Fotos.mp4` permanece como registro complementar de uma execução automática com fotografias, sem narração. O vídeo final narrado é o publicado no YouTube.
