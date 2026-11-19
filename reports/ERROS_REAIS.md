# Auditoria de erros de detecção no conjunto de teste

Referência: modelo YOLOv8n incluído, confiança mínima 0,4 e IoU 0,5. O pareamento considera a classe e usa as anotações do PlantDoc como referência. As categorias TP, FP e FN são relativas às anotações, que podem conter omissões ou inconsistências.

Os cinco casos abaixo possuem uma revisão visual complementar em [`REVISAO_ERROS.md`](REVISAO_ERROS.md). As imagens de referência e previsão estão em `reports/predictions/`.

## Caso 1 — bugs-and-blight-061.jpg

Arquivo: `cb80ee89467395e798a5.jpg`. **TP=1; FP=13; FN=3.**

O modelo não reproduziu integralmente as caixas e classes anotadas. A cena inclui folhas visíveis sem caixas na referência; parte dos FP pode estar associada a anotação incompleta. O efeito da iluminação ou da escala não foi isolado experimentalmente.

## Caso 2 — Tomato59.JPG.jpg

Arquivo: `ecf6c471a58c9ec1876c.jpg`. **TP=3; FP=0; FN=7.**

Foram omitidas várias folhas anotadas em uma cena com elementos pequenos e sobrepostos.

## Caso 3 — dscn3175.jpg

Arquivo: `4582746506e3d93af1cf.jpg`. **TP=1; FP=0; FN=5.**

Uma das seis caixas anotadas de pinta-preta encontrou correspondência no pareamento.

## Caso 4 — Shoemaker_7068.JPG.jpg

Arquivo: `c85286e8013a50d23839.jpg`. **TP=0; FP=2; FN=1.**

O modelo apresentou previsões de requeima diante de uma referência rotulada como pinta-preta. O caso ilustra confusão entre as classes.

## Caso 5 — tomato_early-blight_01_zoom.jpg

Arquivo: `385b11756b74b532a7bf.jpg`. **TP=1; FP=1; FN=2.**

Houve divergência de localização e contagem: uma das três caixas anotadas foi correspondida com IoU de pelo menos 0,5.

As observações são descritivas. Não há evidência suficiente para afirmar causalidade individual de iluminação, escala, oclusão ou qualidade do rótulo. Qualquer ajuste guiado por imagens do teste exigiria uma nova avaliação independente.
