# Histórico de versões — AgroConecta ACV

## Versão 1.1 — interface de detecção

A versão 1.1 aprimorou a apresentação das detecções sem modificar os pesos treinados, o número de classes ou as métricas de avaliação.

Principais alterações:

- Etiquetas numeradas, com identificação e confiança, associadas à lista de resultados.
- Posicionamento das etiquetas para reduzir sobreposição e corte, inclusive em imagens pequenas.
- Área adicional para etiquetas em cenas muito densas, com linhas de ligação às caixas.
- Redesenho automático das detecções quando a área de visualização muda de tamanho.
- Registro complementar do funcionamento da câmera física com fotografia exibida em outra tela.

Os testes de apresentação da versão 1.1 estão em `reports/ui_update_checks.json`. O treinamento e os resultados quantitativos permanecem registrados em `models/metadata.json` e `reports/test_metrics.json`.

## Execução

Os procedimentos de instalação e inicialização estão consolidados no [README principal](../README.md). Não há necessidade de aplicar manualmente um pacote incremental para obter a versão mantida no repositório.
