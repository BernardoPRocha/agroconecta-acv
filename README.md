# AgroConecta - Applied Computer Vision

**Versão 1.1 - 10/11/2026.** Legendas das caixas corrigidas e teste da câmera física documentado. Para atualizar uma instalação existente, veja `docs/ATUALIZAR_VERSAO.md`. Para publicar o código, veja `docs/PUBLICAR_GITHUB.md`.

Projeto acadêmico de detecção de folhas de tomate para a Global Solution 2026.2, FIAP.

| Integrante | RM | Responsabilidade no grupo |
|---|---|---|
| Bernardo Rocha | 99209 | ACV e Secure DevOps |
| Eric Rodrigues | 550249 | RPA e Big Data |
| Renato Izumi | 99242 | Startup e IA generativa |

Maker Lab é compartilhado. Este pacote implementa **ACV**, com um Dockerfile inicial para integração futura em Secure.

## Comece aqui (Windows)

1. Instale Python 3.12 e extraia o ZIP em uma pasta de trabalho.
2. Abra o terminal **dentro de `agroconecta-acv`**, onde está este README.
3. Execute:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Abra http://localhost:8000. Documentação da API: http://localhost:8000/docs.
A instalação inicial requer internet. O modelo e a aplicação, depois de instalados, operam localmente.
O pacote pode ser usado em CPU; essa instalação não utiliza a RTX 5070.
Para treinamento acelerado, use o notebook Colab fornecido, com GPU disponível.

**Status da execução e limitações: leia `docs/STATUS.md`.** Um modelo treinado só é carregado quando `models/best.pt` existe e tem as três classes esperadas. O servidor nunca substitui a ausência do modelo por previsões fictícias.

## Linux/macOS

```bash
python3.12 -m venv .venv
# Linux CPU:
.venv/bin/python -m pip install torch==2.7.1 torchvision==0.22.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

No macOS, instale torch/torchvision pelo índice padrão (sem `--index-url` CPU).

## O que o modelo faz

- Detecta caixas ao redor de folhas, não de cada lesão.
- Classes: `tomate_saudavel`, `pinta_preta`, `requeima`.
- Foto ou câmera do navegador; a câmera envia um quadro por vez para a API local.
- Sem detecção: resultado **inconclusivo**; nunca significa automaticamente que a planta está saudável.
- Pontuação de confiança não é probabilidade calibrada de diagnóstico.
- Apenas triagem experimental. Não identifica todas as doenças, não prescreve defensivos e não substitui avaliação agronômica.
- A classe saudável corresponde ao rótulo `Tomato leaf` do PlantDoc. O resultado é descrito como aparência saudável dentro desse recorte limitado.

## Dados e reprodutibilidade

Fonte: https://github.com/pratikkayal/PlantDoc-Object-Detection-Dataset
Commit: `4730a233a555b30ee98e0879c63ad25d82407455`.

O script baixa somente o recorte de interesse a partir do commit fixado. Converte as caixas CSV para YOLO, valida coordenadas e proporção da imagem, exclui imagens com classes fora do escopo, registra falhas e remove duplicatas exatas e aproximadas por hash médio (distância <= 4 em 256 bits). A deduplicação aproximada é uma heurística: pode remover imagens diferentes ou deixar passar versões transformadas; não substitui auditoria visual.

O teste original tem prioridade sobre duplicatas. O restante é dividido em treino/validação com semente 42 e estratificação por combinação de classes. A validação recebe aproximadamente 20% das imagens de treino elegíveis. O teste é reservado para avaliação final, não para escolher hiperparâmetros.

```powershell
.venv\Scripts\python scripts\prepare_data.py
.venv\Scripts\python scripts\train.py --epochs 60 --imgsz 640 --batch 8 --device cpu --name tomato_final
.venv\Scripts\python scripts\evaluate.py --device cpu
```

Se o dataset já estiver incluído, a preparação não o baixa novamente. O script de treino/avaliação atualiza o caminho absoluto de `data.yaml` para a sua máquina.
O treinamento baixa `yolov8n.pt`, ajusta os pesos, seleciona o melhor checkpoint pela validação e copia para `models/best.pt`. Reinicie a API depois de mudar os pesos.
Cada treino cria uma nova pasta em `runs/`; copie o modelo anterior se quiser preservá-lo antes de treinar novamente.
Métricas reais: `reports/test_metrics.json`; contagens/exclusões: `reports/dataset_audit.json`; procedência por imagem: `data/tomato/manifest.json`.

## Testes

```powershell
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\python -m pytest -q
```

Testes automatizados usam imagens de teste artificiais e um substituto de inferência exclusivamente para validar o contrato e os erros da API. Isso **não mede a qualidade do modelo**. A qualidade é medida separadamente no conjunto real de teste pelo script de avaliação.

## Estrutura

- `app/`: API, página, estilos, captura da câmera e desenho das detecções.
- `scripts/`: preparação, treino, avaliação e geração das evidências.
- `models/`: detector treinado e metadados (quando disponíveis).
- `data/tomato/`: imagens, rótulos, separação dos conjuntos e manifesto.
- `reports/`: resultados reais de execução e relatório técnico.
- `notebooks/`: treinamento no Colab.
- `docs/`: integração, roteiro do vídeo e situação das entregas.
- `tests/`: testes de API e integridade dos dados.

## Integração e publicação

Consulte `docs/API.md`. Eric e Renato podem consumir `POST /api/predict` independentemente de suas outras matérias.
O Dockerfile roda a aplicação sem root. O Compose expõe apenas localhost. Após instalar Docker, use `docker compose up --build` e abra localhost:8000.
A câmera requer localhost ou HTTPS. Hospedagem pública, Terraform, CI/CD e monitoramento completo pertencem à etapa de Secure e não são considerados entregues por este pacote.

## Licenças e referências

PlantDoc: CC BY 4.0 conforme repositório; cópia da licença em `docs/PLANTDOC_LICENSE.txt`. Preservar atribuição. Imagens foram coletadas originalmente da internet; a licença declarada da base não elimina possíveis direitos de terceiros sobre cada imagem.

Singh et al. (2020). *PlantDoc: A Dataset for Visual Plant Disease Detection*. DOI: https://doi.org/10.1145/3371158.3371196.

Ultralytics YOLOv8: https://docs.ultralytics.com/models/yolov8/
Treinamento: https://docs.ultralytics.com/modes/train/
Avaliação: https://docs.ultralytics.com/modes/val/
Ultralytics: AGPL-3.0 ou licença comercial conforme termos do fornecedor. Verifique obrigações antes de distribuir/usar comercialmente. Este projeto depende do pacote e de pesos derivados dele.

## Relatório técnico

O PDF pronto está em `reports/Relatorio_Tecnico_ACV_AgroConecta.pdf`. Para regenerá-lo com as mesmas evidências, instale `requirements-report.txt` e execute `python scripts/build_report.py`. O gerador descreve esta execução de referência; após novo treinamento, revise também os textos e parâmetros fixos antes de gerar uma nova entrega.

## Publicar o código

O peso `models/best.pt` está liberado no .gitignore para inclusão no repositório. Dados completos e execuções ficam fora do Git; a preparação usa a fonte pública fixada e os manifestos preservam a procedência. Não publique o ambiente virtual. Inclua os links reais de repositório e vídeo antes da submissão.

## Materiais da versão 1.1

- `docs/videos/Demonstracao_ACV_Fotos.mp4`: demonstração automática com fotos, sem áudio.
- `docs/ROTEIRO_VIDEO.md`: falas e cenas para Bernardo gravar a apresentação com câmera.
- `docs/PUBLICAR_GITHUB.md`: passos para publicar o repositório.
- `reports/ui_update_checks.json`: verificações da interface atualizada.
