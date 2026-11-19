# Revisão visual de cinco casos com divergências

A avaliação considera as detecções do modelo incluído no projeto, com confiança mínima de 0,4, IoU de 0,5 e pareamento por classe. Os valores TP, FP e FN são calculados em relação às anotações do conjunto de teste PlantDoc, não a uma verificação agronômica independente.

As imagens de referência e predição foram comparadas lado a lado. Os registros correspondentes estão em `reports/predictions/`.

## 1. bugs-and-blight-061.jpg

- **Resultado:** TP=1, FP=13, FN=3.
- **Observação:** a referência contém quatro caixas de pinta-preta. O detector prevê treze regiões como aparência saudável e uma como pinta-preta. Existem folhas visíveis sem anotação; portanto, parte dos FP pode refletir incompletude da referência.
- **Melhoria proposta:** revisar anotações e ampliar exemplos semelhantes no treinamento, preservando a independência das imagens de teste.

## 2. Tomato59.JPG.jpg

- **Resultado:** TP=3, FP=0, FN=7.
- **Observação:** o conjunto de referência inclui dez folhas saudáveis, das quais somente três foram correspondidas. A cena contém folhas pequenas e sobrepostas.
- **Melhoria proposta:** ampliar exemplos de folhas pequenas e comparar resoluções usando o conjunto de validação.

## 3. dscn3175.jpg

- **Resultado:** TP=1, FP=0, FN=5.
- **Observação:** uma das seis caixas anotadas de pinta-preta foi correspondida. A imagem apresenta folhas sobrepostas e em diferentes orientações.
- **Melhoria proposta:** ampliar a diversidade de cenas e avaliar o efeito da orientação e da oclusão na validação.

## 4. Shoemaker_7068.JPG.jpg

- **Resultado:** TP=0, FP=2, FN=1.
- **Observação:** uma referência rotulada como pinta-preta corresponde a uma cena na qual o detector prevê duas regiões de requeima. Há divergências de classe e localização.
- **Melhoria proposta:** revisar rótulos com conhecimento especializado e incluir exemplos contrastantes das duas doenças.

## 5. tomato_early-blight_01_zoom.jpg

- **Resultado:** TP=1, FP=1, FN=2.
- **Observação:** há três caixas na referência e duas previsões de pinta-preta, mas apenas uma previsão coincide com IoU de pelo menos 0,5.
- **Melhoria proposta:** revisar o padrão das anotações e estudar o efeito da resolução na validação.

## Interpretação

Sobreposição, escala, iluminação e incompletude de anotações são hipóteses plausíveis, não causas confirmadas por experimentos controlados. O conjunto de teste não deve ser utilizado para ajustar repetidamente o modelo. Caso suas imagens orientem mudanças no treinamento, uma nova avaliação final independente será necessária.
