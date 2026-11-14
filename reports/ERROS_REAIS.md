# Análise automática de até cinco erros reais

Confiança 0,4 e IoU 0,5; pareamento por classe. Falsos positivos/negativos são relativos às anotações da base, que também podem conter erros. Revisão humana ainda necessária.

## Caso 1: bugs-and-blight-061.jpg

Arquivo: `cb80ee89467395e798a5.jpg`. TP=1; FP=13; FN=3.

Observação: o modelo não reproduziu integralmente as caixas e classes anotadas. As imagens de referência e previsão estão em `reports/predictions`. Iluminação, escala, confusão entre classes e anotações inconsistentes são hipóteses a verificar, não causas comprovadas.

## Caso 2: Tomato59.JPG.jpg

Arquivo: `ecf6c471a58c9ec1876c.jpg`. TP=3; FP=0; FN=7.

Observação: o modelo não reproduziu integralmente as caixas e classes anotadas. As imagens de referência e previsão estão em `reports/predictions`. Iluminação, escala, confusão entre classes e anotações inconsistentes são hipóteses a verificar, não causas comprovadas.

## Caso 3: dscn3175.jpg

Arquivo: `4582746506e3d93af1cf.jpg`. TP=1; FP=0; FN=5.

Observação: o modelo não reproduziu integralmente as caixas e classes anotadas. As imagens de referência e previsão estão em `reports/predictions`. Iluminação, escala, confusão entre classes e anotações inconsistentes são hipóteses a verificar, não causas comprovadas.

## Caso 4: Shoemaker_7068.JPG.jpg

Arquivo: `c85286e8013a50d23839.jpg`. TP=0; FP=2; FN=1.

Observação: o modelo não reproduziu integralmente as caixas e classes anotadas. As imagens de referência e previsão estão em `reports/predictions`. Iluminação, escala, confusão entre classes e anotações inconsistentes são hipóteses a verificar, não causas comprovadas.

## Caso 5: tomato_early-blight_01_zoom.jpg

Arquivo: `385b11756b74b532a7bf.jpg`. TP=1; FP=1; FN=2.

Observação: o modelo não reproduziu integralmente as caixas e classes anotadas. As imagens de referência e previsão estão em `reports/predictions`. Iluminação, escala, confusão entre classes e anotações inconsistentes são hipóteses a verificar, não causas comprovadas.

