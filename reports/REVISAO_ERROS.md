# Revisão visual de cinco erros reais

Referência: modelo incluído, teste PlantDoc, confiança 0,4, IoU 0,5, correspondência por classe. Os números são relativos à anotação, não à verdade agronômica. As imagens foram inspecionadas lado a lado (referência e previsão).

1. **bugs-and-blight-061.jpg**: quatro caixas de pinta-preta na referência; o modelo produz 13 caixas da classe saudável e uma de pinta-preta. Há diversas folhas verdes sem anotação no quadro. Assim, parte dos 13 FP pode envolver anotação incompleta; não é possível atribuir tudo ao modelo. Também deixa de corresponder a três caixas anotadas. Próximo passo: revisar a completude das anotações e incluir cenas semelhantes no treino, sem reutilizar esta imagem de teste.
2. **Tomato59.JPG.jpg**: referência com dez folhas saudáveis e apenas três correspondências detectadas. A cena tem muitas folhas pequenas e sobrepostas. Isso sugere dificuldade com escala/oclusão, sem demonstrar causalidade. Próximo passo: comparar resolução maior no conjunto de validação e ampliar exemplos de folhas pequenas.
3. **dscn3175.jpg**: seis caixas de pinta-preta na referência, uma correspondência. Folhas se sobrepõem e apresentam diferentes orientações. Próximo passo: ampliar variedade de cenas e revisar exemplos omitidos na validação.
4. **Shoemaker_7068.JPG.jpg**: uma caixa de pinta-preta na referência, duas previsões de requeima. É um caso explícito de confusão de classe, além de divergência de localização/contagem. Próximo passo: revisar rótulos com orientação especializada e coletar exemplos contrastantes das duas doenças.
5. **tomato_early-blight_01_zoom.jpg**: três caixas na referência, duas previsões de pinta-preta, mas apenas uma coincide com IoU >=0,5. Ocorre uma caixa extra/incompatível e duas omissões no pareamento. Próximo passo: revisar o padrão de caixas e avaliar resolução maior na validação.

Não ajustar o modelo repetidamente para acertar estas imagens e continuar chamando-as de teste independente. Se elas forem usadas no desenvolvimento, reservar um novo conjunto externo para a próxima avaliação final.
