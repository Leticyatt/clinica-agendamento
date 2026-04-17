<img width="1615" height="905" alt="image" src="https://github.com/user-attachments/assets/70ecfbc8-5802-4b8b-8eee-4c555ef9522e" />
# Gestão de Agendamentos - Clínica

Este é um projeto **Full Stack** desenvolvido para gerenciar filas e consultas em clínicas de pequeno e médio porte. O sistema permite o controle total de pacientes, médicos e status de atendimento em tempo real.

## Diferenciais do Projeto
- **Busca Global:** Filtro inteligente por Nome ou CPF que vasculha tanto a fila ativa quanto o histórico.
- **Arquitetura Full Stack:** Comunicação fluida entre Front-end (React), Back-end (FastAPI) e Banco de Dados (SQL Server).
- **Interface Intuitiva:** Organização por abas ("Em Andamento" e "Finalizados") para facilitar a rotina da recepção.
- **Filtro de Histórico:** Dados finalizados não são excluídos, permitindo auditoria e consulta posterior.

## Tecnologias Utilizadas

### Front-end
- **React.js** + **Vite**
- **CSS3** (Componentização e Responsividade)
- **Fetch API** (Integração com o Back-end)

### Back-end
- **Python** com **FastAPI**
- **PyODBC** (Conector SQL Server)
- **CORS Middleware** (Segurança na comunicação)

### Banco de Dados
- **SQL Server** (Transact-SQL)

## Estrutura das Pastas

clinica/
api-clinica/      # Servidor Python e lógica de negócio
front-clinica/    # Interface do usuário em React
db/               # Scripts de criação das tabelas SQL

- Como rodar o projeto:

1. Banco de Dados
Execute o script SQL (disponível na pasta /db ou api-clinica) no seu SQL Server para criar as tabelas Pacientes, Médicos e Agendamentos.

2. Back-end (API)
Entre na pasta: cd api-clinica

Inicie o servidor: uvicorn main:app --reload
A API estará rodando em https://www.google.com/search?q=http://127.0.0.1:8000

3. Front-end
Entre na pasta: cd front-clinica

Instale as dependências: npm install

Inicie o projeto: npm run dev
Acesse o painel pelo link gerado no terminal (geralmente http://localhost:5173)

## Próximos Passos:
- Implementar autenticação de usuários (Login para recepcionistas).
- Adicionar geração de relatórios de atendimento em PDF.
- Criar um Dashboard com estatísticas de consultas mensais.


