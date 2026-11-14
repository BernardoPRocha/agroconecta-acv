# Atualizar para a versão 1.1

Esta atualização muda a apresentação das detecções e a documentação. O modelo, as classes, as métricas e as dependências permanecem os mesmos.

## Se você já instalou a versão anterior

1. Pare a aplicação com Ctrl+C no terminal.
2. Extraia o pacote `AgroConecta_ACV_Atualizacao_1_1.zip` em uma pasta temporária.
3. Abra a pasta `agroconecta-acv` que veio na atualização.
4. Copie o conteúdo dela para dentro da sua pasta `agroconecta-acv` existente. Aceite substituir os arquivos de mesmo nome. Evite criar uma pasta agroconecta-acv dentro de outra.
5. Execute `INICIAR_WINDOWS.bat`.
6. Abra http://localhost:8000 e pressione Ctrl+F5 para atualizar os arquivos do navegador.
7. Teste uma foto pequena (pinta-preta 1) e uma foto com várias folhas (saudável 1). Cada caixa deve ter uma etiqueta curta, como #1 · 71%, com o mesmo número na lista de resultados.

Não apague a pasta .venv, não reinstale dependências e não treine o modelo novamente para esta atualização.

## Se baixar o projeto completo atualizado

Ele já contém as alterações. Para preservar sua instalação, copie apenas os arquivos da atualização ou siga o README em uma pasta nova.

## Mudanças

- Texto calculado pelo tamanho de exibição, sem amplificação em fotos pequenas.
- Etiquetas curtas, numeradas e separadas; a descrição completa aparece na lista.
- Reposicionamento das etiquetas para evitar sobreposição e corte. Em cenas muito cheias, etiquetas excedentes vão para uma faixa abaixo da foto, com linhas de ligação.
- Redesenho ao redimensionar a janela.
- Relatório e situação da entrega atualizados com o teste de câmera informado por Bernardo.
