# Contrato de integração - ACV

Base local: `http://localhost:8000`.

## Rotas

| Método | Rota | Uso |
|---|---|---|
| GET | `/health` | Processo ativo e campo `model_ready` |
| GET | `/ready` | 200 quando detector está carregado; 503 caso contrário |
| POST | `/api/predict?confidence=0.4` | Imagem em multipart, campo `file` |
| GET | `/docs` | Swagger/OpenAPI |

```bash
curl -X POST "http://localhost:8000/api/predict?confidence=0.4" -F "file=@folha.jpg"
```

Resposta (exemplo de estrutura, valores ilustrativos, não evidência):

```json
{"width":640,"height":480,"detections":[{"class_id":1,"label":"Possível pinta-preta","confidence":0.72,"bbox":[12,20,500,400]}],"status":"detections","latency_ms":180,"notice":"..."}
```

`bbox`: x1,y1,x2,y2 em pixels da imagem orientada pela informação EXIF. Não são coordenadas normalizadas. A interface envia um quadro já redimensionado e desenha na mesma resolução. `status=inconclusive` significa lista vazia; não interpretar como saudável.

Classes estáveis: 0 aparência saudável, 1 possível pinta-preta, 2 possível requeima.
`confidence` de entrada: 0.05 a 0.95, padrão 0.4; valor inicial não calibrado.
Erros: 413 arquivo >8 MB, 415 arquivo inválido/formato não aceito/dimensões excessivas, 422 parâmetros inválidos, 503 modelo não disponível, 500 falha de inferência.

Não são persistidas fotos nem dados pessoais. A imagem fica em memória durante a inferência. Não enviar segredos na URL. Somente pesos de origem confiável devem ser carregados.

## Para os colegas

- Renato: consumir o JSON de detecção e fornecer explicação com fontes, preservando o caráter de hipótese. Não converter confiança em diagnóstico confirmado.
- Eric: se houver interesse em histórico, armazenar categorias, horário e pontuação no backend central. A versão ACV não necessita de Big Data ou RPA para funcionar.
- Frontend central: chamar essa API a partir do mesmo domínio/proxy. Não habilitamos CORS irrestrito. Se usarem domínios diferentes, definir uma lista explícita de origens.

## Antes da exposição pública

Configurar HTTPS, limite de corpo no proxy, limitação de requisições e capacidade de CPU. A API serializa inferências porque o preditor compartilha estado; não foi dimensionada para muitas pessoas simultâneas. Não declarar capacidade de produção a partir deste protótipo.
