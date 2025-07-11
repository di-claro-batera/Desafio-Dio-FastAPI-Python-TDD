## 🚀 Desafio DIO – FastAPI, Python e TDD

- Este projeto foi desenvolvido como parte do desafio final do Bootcamp da Digital Innovation One (DIO), com o objetivo de aplicar na prática os conceitos de **APIs RESTful**, **Clean Architecture**, **MongoDB assíncrono**, **FastAPI**, **TDD com pytest**, além de ferramentas modernas como `pre-commit`, `poetry` e linters automáticos.  
  
- A aplicação consiste em um sistema de gerenciamento de produtos com CRUD completo e filtro por faixa de preço, oferecendo uma base sólida e escalável para projetos reais.


## 🚀 API em execução

Abaixo, uma prévia da documentação interativa gerada automaticamente pelo FastAPI:

![Swagger UI](API.png)


## ✨ Funcionalidades

- CRUD de produtos completo com validação
- Filtro de produtos por faixa de preço (`GET /products/filter`)
- Modelos Pydantic com timezone-aware
- Armazenamento no MongoDB (via `motor`)
- Validações e exceções personalizadas
- Hooks com `pre-commit` automatizados
- Testes automatizados com `pytest`



## 📦 Stack utilizada

- [FastAPI](https://fastapi.tiangolo.com/)
- [Poetry](https://python-poetry.org/)
- [MongoDB + Motor (async)](https://motor.readthedocs.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [Pre-commit + Ruff + Pyupgrade](https://pre-commit.com/)
- [Pytest](https://docs.pytest.org/en/latest/)



## 🔧 Como rodar o projeto

1. Clone o repositório:

git clone https://github.com/di-claro-batera/Desafio-Dio-FastAPI-Python-TDD.git
cd Desafio-Dio-FastAPI-Python-TDD


2.  Instale as dependências:

poetry install


3.  Configure o .env (baseie-se no .env.example, se houver)

   
4.  Execute a aplicação:

make run


5.  Acesse a documentação automática:

http://localhost:8000/docs


## ✅ Testes

Execute todos os testes com:

make test

Ou apenas testes que contenham parte do nome:

make test-matching K=filter

## 🧹 Pre-commit

Instale e rode os hooks:make pre-commit-install

make lint


Para manter tudo atualizado:

pre-commit autoupdate

## 📂 Estrutura de pastas

store/

├── main.py

├── models/

├── schemas/

├── controllers/

├── usecases/

└── db/

tests/

Makefile

pyproject.toml



## 👨‍💻 Autor

Desenvolvido por Diego Claro

🔗 LinkedIn https://www.linkedin.com/in/diego-claro-9719b128b/

🎸 Bata forte no código e nos tambores!
