# AgroConecta — Applied Computer Vision

Projeto de visão computacional da **Global Solution 2026.2 — FIAP**, desenvolvido como parte da plataforma AgroConecta, voltada ao apoio de pequenos produtores rurais.

O módulo realiza **triagem visual experimental de folhas de tomate** por fotografias ou câmera, usando um detector YOLOv8n treinado para três categorias. O sistema apresenta caixas delimitadoras, classificação e confiança da detecção. Não constitui diagnóstico agronômico definitivo.

## Integrantes do grupo

| Integrante | RM |
|---|---|
| Bernardo Rocha | 99209 |
| Eric Rodrigues | 550249 |
| Renato Izumi | 99242 |

## Demonstração e entrega

- **Vídeo final narrado:** [AgroConecta — demonstração de ACV no YouTube](https://www.youtube.com/watch?v=KIRmYhAmrdI)
- **Relatório final:** [`reports/Relatorio_Tecnico_ACV_AgroConecta.pdf`](reports/Relatorio_Tecnico_ACV_AgroConecta.pdf)
- **Repositório:** https://github.com/BernardoPRocha/agroconecta-acv
- **Contrato de integração:** [`docs/API.md`](docs/API.md)
- **Estado do módulo e limitações:** [`docs/STATUS.md`](docs/STATUS.md)

A demonstração apresenta o fluxo de análise por foto e câmera. O teste com câmera física utiliza uma fotografia exibida em outra tela; não representa validação em campo.

## Funcionalidades

- Carregamento de fotos JPEG, PNG ou WEBP, até 8 MB.
- Captura de quadros pela câmera do navegador (em `localhost` ou HTTPS).
- Detecção de regiões correspondentes a folhas e apresentação de caixas delimitadoras.
- Classificação em `tomate_saudavel`, `pinta_preta` e `requeima`.
- Ajuste de confiança mínima na interface (padrão: 40%).
- Resultado inconclusivo quando não há detecções acima do limite escolhido.
- API FastAPI com documentação OpenAPI em `/docs`.

As classes indicam **aparência saudável**, **possível pinta-preta** ou **possível requeima** no recorte de dados escolhido. O modelo não detecta todas as doenças ou pragas, e a pontuação de confiança não representa probabilidade calibrada de diagnóstico.

## Execução local — Windows

Pré-requisitos: Python 3.12 e conexão com a internet para a instalação inicial.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Aplicação: http://localhost:8000  
Documentação da API: http://localhost:8000/docs

O arquivo `INICIAR_WINDOWS.bat` também inicia o servidor após a criação do ambiente virtual. A execução fornecida utiliza **CPU**, sem depender de GPU NVIDIA.

### Linux

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

No macOS, PyTorch deve ser instalado conforme as instruções apropriadas para a plataforma.

## Dados e treinamento

Fonte: [PlantDoc Object Detection Dataset](https://github.com/pratikkayal/PlantDoc-Object-Detection-Dataset), revisão `4730a233a555b30ee98e0879c63ad25d82407455`.

A preparação inclui seleção das três categorias, conversão de caixas CSV para YOLO, validação de coordenadas, remoção de seis duplicatas exatas/aproximadas e exclusão de imagens com rótulos fora do escopo ou anotações incompatíveis. Os critérios e ocorrências estão em `reports/dataset_audit.json`.

| Conjunto | Imagens |
|---|---:|
| Treinamento | 180 |
| Validação | 45 |
| Teste | 27 |

O modelo incluído em `models/best.pt` foi ajustado por **30 épocas**, com imagens de **320 pixels**, **batch 8**, **CPU** e semente **42**. O teste reservado foi utilizado para avaliação final, não para selecionar os pesos.

| Métrica no conjunto de teste | Valor |
|---|---:|
| Precisão | 60,2% |
| Recall | 66,3% |
| mAP@50 | 68,6% |
| mAP@50:95 | 43,7% |

Essas são métricas de **detecção de objetos**, não uma taxa de diagnósticos agronômicos corretos. O conjunto de teste possui apenas 27 imagens. A avaliação completa está em `reports/test_metrics.json`, e a análise dos erros em `reports/REVISAO_ERROS.md`.

O repositório contém os scripts `prepare_data.py`, `train.py` e `evaluate.py` para reproduzir o processo. **O modelo fornecido já está treinado; não é necessário executar novo treinamento para utilizar o aplicativo.** O notebook em `notebooks/` oferece uma alternativa opcional de treinamento no Google Colab; não corresponde à execução de 30 épocas documentada acima.

## Geração de relatório técnico complementar

O arquivo `scripts/build_report.py` gera `reports/Relatorio_Tecnico_ACV_GERADO.pdf` a partir dos JSONs de avaliação e das imagens disponíveis. Ele **não sobrescreve** `reports/Relatorio_Tecnico_ACV_AgroConecta.pdf`, que é o documento final revisado para a entrega.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-report.txt
.\.venv\Scripts\python.exe scripts/build_report.py
```

## Testes automatizados

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Os sete testes registrados cobrem integridade dos dados, contrato da API, entradas inválidas, arquivo muito grande, orientação EXIF e ausência do modelo. Os testes da API utilizam um substituto de inferência para validar o contrato: **não medem a precisão do YOLO**. A qualidade do detector foi avaliada separadamente com imagens reais do PlantDoc.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| `app/` | FastAPI, interface web, desenho das detecções e câmera |
| `models/` | Pesos do detector treinado e metadados |
| `scripts/` | Preparação de dados, treinamento, avaliação e evidências |
| `reports/` | Métricas, auditorias, previsões e PDF acadêmico |
| `examples/` | Imagens de demonstração com atribuição de origem |
| `docs/` | API, status, versões e documentação do vídeo |
| `tests/` | Testes automatizados |
| `notebooks/` | Alternativa opcional de treinamento no Colab |

O `Dockerfile` e `compose.yaml` fornecem uma opção de empacotamento. O desenvolvimento de infraestrutura pública, CI/CD e observabilidade é documentado separadamente em [agroconecta-secure](https://github.com/BernardoPRocha/agroconecta-secure). A existência da API não significa que a versão HTML estática do portal principal esteja conectada ao detector.

## Licenças, referências e limitações

O PlantDoc é apresentado pelo repositório de origem sob CC BY 4.0. A atribuição está em `docs/PLANTDOC_LICENSE.txt` e `examples/SOURCES.json`; o caráter público da base não elimina possíveis direitos de terceiros sobre imagens originalmente coletadas na internet.

Singh et al. (2020). *PlantDoc: A Dataset for Visual Plant Disease Detection*. DOI: https://doi.org/10.1145/3371158.3371196.

Ultralytics YOLOv8: https://docs.ultralytics.com/models/yolov8/ — verificar as condições AGPL-3.0 ou comerciais antes de qualquer uso fora do contexto acadêmico.

O protótipo não foi validado agronomicamente ou com plantas reais em campo. Resultados inconclusivos não devem ser interpretados como folhas saudáveis. O sistema não prescreve defensivos agrícolas.
