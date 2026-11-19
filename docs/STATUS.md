# Estado técnico do AgroConecta ACV

Global Solution 2026.2 — FIAP  
Revisão documental: 19/11/2026

## Implementação

- Detector YOLOv8n com classes `tomate_saudavel`, `pinta_preta` e `requeima`.
- Modelo treinado incluído em `models/best.pt` e identificado por SHA-256 em `models/metadata.json`.
- Aplicação web FastAPI com upload de fotos, câmera e apresentação de detecções em caixas.
- API `POST /api/predict`, além das rotas `/health`, `/ready` e `/docs`.
- Repositório público: https://github.com/BernardoPRocha/agroconecta-acv.
- Vídeo final de demonstração: https://www.youtube.com/watch?v=KIRmYhAmrdI.
- Relatório acadêmico em `reports/Relatorio_Tecnico_ACV_AgroConecta.pdf`.

## Dados e avaliação registrados

| Indicador | Resultado |
|---|---:|
| Treino | 180 imagens |
| Validação | 45 imagens |
| Teste | 27 imagens |
| Épocas de treinamento | 30 |
| Resolução | 320 px |
| Batch | 8 |
| Precisão (teste) | 0,6022 |
| Recall (teste) | 0,6628 |
| mAP@50 (teste) | 0,6858 |
| mAP@50:95 (teste) | 0,4367 |

Treinamento registrado em CPU, semente 42. A auditoria do conjunto de dados documentou seis duplicatas removidas, seis imagens fora do escopo excluídas e uma rejeição por incompatibilidade de anotação. Detalhes em `reports/dataset_audit.json`.

A auditoria operacional de detecções, com confiança 0,4 e IoU 0,5, registrou 35 TP, 29 FP e 25 FN relativos às anotações. Esses valores não representam uma taxa de diagnóstico agronômico correto nem substituem o cálculo de mAP.

## Verificações da interface e da API

- Sete testes automatizados registrados como aprovados.
- Seis fotografias analisadas com o modelo real pela interface.
- Verificações de layout em telas de tamanhos diferentes, sem erro JavaScript registrado.
- Fluxo da câmera exercitado com dispositivo virtual durante os testes de navegador.
- Demonstração adicional da câmera física, apontada para uma fotografia exibida em outra tela; não houve validação em campo.

Os resultados encontram-se em `reports/tests.txt`, `reports/browser_checks.json` e `reports/ui_update_checks.json`.

## Limitações

O modelo pode confundir classes, omitir folhas e apresentar previsões que não coincidem com as anotações. A base de teste contém apenas 27 imagens e não representa toda a variabilidade de ambientes agrícolas.

Não houve calibração probabilística da confiança, validação agronômica ou estudo de impacto sobre a produção agrícola. Uma imagem sem detecção é **inconclusiva**, não necessariamente saudável.

O Dockerfile e o Compose fazem parte do pacote, mas esta documentação não inclui evidência de sua execução independente. A infraestrutura e as verificações de segurança do MVP são tratadas separadamente em [agroconecta-secure](https://github.com/BernardoPRocha/agroconecta-secure).

## Integração com o AgroConecta

O módulo ACV expõe uma API que pode ser consumida pelos outros componentes da plataforma. O código do MVP em Secure possui uma aplicação com visão computacional; isso é distinto do HTML estático de apresentação do grupo, que pode exibir uma demonstração sem executar inferência diretamente.
