# RISE

O projeto foi desenvolvido durante férias, feriados e finais de semana para gerir um reino do jogo Rise of Kingdoms.

As demandas vinham a pedido dos jogadores que lideravam o
reino 1032, e engloblam desde acompanhamento dos embates
entre reinos, conhecido como KvK, quanto o controle de
eventos recorrentes, como o MGE.

Os dados eram alimentados a partir de arquivos CSV extraídos
via OCR do jogo sendo executado em emulador.

## Primeiros passos

Crie um arquivo _.env_ para exportar, no mínimo a variável
SECRET_KEY, como no exemplo:

```bash
SECRET_KEY=1234
```

Os pré-requisitos para execução do projeto são:

- pipx
- poetry

Instale o pipx segundo sua documentação oficial e,
a partir dele, instale o poetry.

Na raiz do projeto, execute:

```shell
$ poetry install
$ eval $(poetry env activate)
```

Você terá o comando _task_ disponível, e pode ver
as opções com a flag --help.

Aplique as migrações, crie um super usuário e execute
o servidor em modo desenvolvimento, com:

```shell
$ task migrations
$ python manage.py createsuperuser
$ task dev
```

O sistema não foi estruturado para gerir múltiplos reinos,
Mas é possível que no futuro saia algo do gênero a título
de demonstração.

Visto que o desenvolvimento era nos horários livres,
em muitos casos não houve planejamento, por isso,
nem sempre as melhores decisões e estruturas foram
utilizadas.

Se você é entusiastas de coisas diferentes, dê uma olhada
no app _tasks_, em que utilizei importlib para subir
scripts cuja execução seria corriqueira, com retorno
via interface web.
