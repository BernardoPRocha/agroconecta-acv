# Publicar o ACV no GitHub

Nome sugerido: `agroconecta-acv`. Visibilidade exigida pelo resumo do enunciado: pública.

Nenhum repositório foi publicado nesta atualização. A conexão disponível não retornou repositórios acessíveis. Não foram inventados links de GitHub ou de vídeo.

## Criar e enviar

1. Entre no GitHub e crie um repositório público vazio chamado agroconecta-acv. Não adicione README, licença nem .gitignore pelo site: esses arquivos já pertencem ao projeto.
2. Copie a URL HTTPS real do novo repositório.
3. Abra o terminal dentro da pasta agroconecta-acv e execute:

```bat
git init
git add .
git status
```

Confira os arquivos que serão incluídos. A pasta .venv, dados completos e runs devem ficar excluídos pelo .gitignore. O modelo models/best.pt está incluído explicitamente.

```bat
git commit -m "Entrega inicial do modulo ACV AgroConecta"
git branch -M main
```

Se o Git solicitar identidade, configure seu nome e seu e-mail do GitHub localmente nesse repositório e repita o commit:

```bat
git config user.name "Bernardo Rocha"
git config user.email "SEU_EMAIL_DO_GITHUB"
```

Adicione a URL real (substitua o texto entre aspas, sem usar literalmente o exemplo):

```bat
git remote add origin "URL_HTTPS_REAL_DO_REPOSITORIO"
git push -u origin main
```

Se o repositório já tiver histórico ou o remoto origin já existir, não use force e não apague o histórico. Confira `git remote -v` e adapte o envio ao repositório existente.

## Conferir antes de entregar

- Abra o repositório em janela anônima para conferir que está público.
- Verifique app/, scripts/, models/best.pt, README.md, requirements.txt e o PDF em reports/.
- Verifique os créditos da base e as condições das dependências.
- Adicione os links reais do repositório e do vídeo ao README e ao portal da faculdade.
- A publicação do código não coloca o site no ar. A URL pública do MVP será tratada em Secure.
