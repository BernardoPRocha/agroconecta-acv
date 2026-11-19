# API de análise de folhas — AgroConecta ACV

**Base local:** `http://localhost:8000`

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Estado do processo e disponibilidade do modelo (`model_ready`) |
| GET | `/ready` | HTTP 200 quando o modelo está carregado; HTTP 503 caso contrário |
| POST | `/api/predict?confidence=0.4` | Análise de imagem enviada em `multipart/form-data`, campo `file` |
| GET | `/docs` | Documentação interativa OpenAPI |

Exemplo de requisição:

```bash
curl -X POST "http://localhost:8000/api/predict?confidence=0.4" -F "file=@folha.jpg"
```

Exemplo **ilustrativo** de estrutura da resposta, sem correspondência com uma inferência específica:

```json
{
  "width": 640,
  "height": 480,
  "detections": [
    {
      "class_id": 1,
      "label": "Possível pinta-preta",
      "confidence": 0.72,
      "bbox": [12, 20, 500, 400]
    }
  ],
  "status": "detections",
  "latency_ms": 180,
  "notice": "Triagem visual experimental"
}
```

Os campos `bbox` representam `x1, y1, x2, y2` em pixels na imagem com orientação EXIF corrigida. `status=inconclusive` indica ausência de detecções acima do limite escolhido, e não comprova aparência saudável.

## Classes

| Identificador | Categoria |
|---|---|
| 0 | Aparência saudável |
| 1 | Possível pinta-preta |
| 2 | Possível requeima |

A confiança de entrada varia de 0,05 a 0,95, com valor padrão 0,4. Não equivale à probabilidade calibrada de diagnóstico.

## Validações e erros

- **413:** imagem acima de 8 MB.
- **415:** imagem inválida, formato incompatível ou dimensões excessivas.
- **422:** parâmetros inválidos.
- **503:** modelo treinado indisponível.
- **500:** falha interna durante a inferência.

São aceitas imagens JPEG, PNG e WEBP com até 16 milhões de pixels. O módulo processa as imagens em memória e não implementa armazenamento de uploads.

## Integração

A resposta JSON pode ser consumida por serviços de visualização, histórico de dados e explicação de hipóteses agrícolas. O aplicativo de visão computacional não depende dos módulos de RPA, Big Data ou IA generativa para executar a detecção.

Integrações com outros domínios exigem configuração explícita de CORS e HTTPS. Antes de qualquer implantação pública devem ser avaliados limites de requisição, proteção contra abuso, capacidade de processamento e privacidade. A API serializa inferências e não foi dimensionada para alta concorrência.
