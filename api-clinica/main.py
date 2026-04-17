from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc

app = FastAPI(title="API Gestão de Clínica")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STRING_CONEXAO = (
    r'DRIVER={SQL Server};'
    r'SERVER=.\SQLEXPRESS;'
    r'DATABASE=ClinicaDB;'
    r'Trusted_Connection=yes;'
)

class NovoAgendamento(BaseModel):
    nome_paciente: str
    cpf: str
    telefone: str
    id_medico: int
    data_hora: str 

class AtualizaStatus(BaseModel):
    status: str

@app.get("/medicos")
def listar_medicos():
    try:
        conexao = pyodbc.connect(STRING_CONEXAO)
        cursor = conexao.cursor()
        cursor.execute("SELECT id_medico, nome, especialidade FROM Medicos")
        
        lista = [{"id": linha.id_medico, "nome": linha.nome, "especialidade": linha.especialidade} for linha in cursor.fetchall()]
        
        conexao.close()
        return lista
    except Exception as erro:
        return {"erro": str(erro)}
    
@app.get("/atendimentos")
def listar_atendimentos():
    try:
        conexao = pyodbc.connect(STRING_CONEXAO)
        cursor = conexao.cursor()
        
        query = """
            SELECT 
                A.id_agendamento, 
                P.nome as paciente, 
                P.cpf, 
                M.nome as medico,
                A.status_atendimento, 
                A.data_hora
            FROM Agendamentos A
            INNER JOIN Pacientes P ON A.id_paciente = P.id_paciente
            INNER JOIN Medicos M ON A.id_medico = M.id_medico
            ORDER BY A.data_hora ASC
        """
        cursor.execute(query)
        
        lista_atendimentos = []
        for linha in cursor.fetchall():
            lista_atendimentos.append({
                "id": linha.id_agendamento,
                "paciente": linha.paciente,
                "medico": linha.medico,
                "status": linha.status_atendimento,
                "cpf": str(linha.cpf).strip(),
                "data": linha.data_hora.strftime("%d/%m/%Y"),
                "hora": linha.data_hora.strftime("%H:%M")
            })
            
        conexao.close()
        return lista_atendimentos
    except Exception as erro:
        return {"erro": str(erro)}

@app.post("/atendimentos")
def criar_agendamento(dados: NovoAgendamento):
    try:
        conexao = pyodbc.connect(STRING_CONEXAO)
        cursor = conexao.cursor()
   
        query_conflito = "SELECT 1 FROM Agendamentos WHERE id_medico = ? AND data_hora = ?"
        cursor.execute(query_conflito, dados.id_medico, dados.data_hora)
        if cursor.fetchone():
            return {"erro": "Horário indisponível! Este médico já possui uma consulta marcada para esta data e hora."}
        
        query_paciente = """
            IF NOT EXISTS (SELECT 1 FROM Pacientes WHERE cpf = ?)
            BEGIN
                INSERT INTO Pacientes (nome, cpf, telefone) VALUES (?, ?, ?)
            END
        """
        cursor.execute(query_paciente, dados.cpf, dados.nome_paciente, dados.cpf, dados.telefone)
        
        cursor.execute("SELECT id_paciente FROM Pacientes WHERE cpf = ?", dados.cpf)
        id_paciente = cursor.fetchone()[0]
        
        query_agendamento = """
            INSERT INTO Agendamentos (id_paciente, id_medico, data_hora, status_atendimento)
            VALUES (?, ?, ?, 'Aguardando')
        """
        cursor.execute(query_agendamento, id_paciente, dados.id_medico, dados.data_hora)

        conexao.commit()
        conexao.close()
        
        return {"mensagem": "Agendamento criado com sucesso!"}
        
    except Exception as erro:
        return {"erro": f"Falha ao salvar: {str(erro)}"}
    
@app.put("/atendimentos/{id_agendamento}")
def atualizar_status(id_agendamento: int, dados: AtualizaStatus):
    try:
        conexao = pyodbc.connect(STRING_CONEXAO)
        cursor = conexao.cursor()
        
        query = """
            UPDATE Agendamentos 
            SET status_atendimento = ? 
            WHERE id_agendamento = ?
        """
        cursor.execute(query, dados.status, id_agendamento)
        
        conexao.commit()
        conexao.close()
        
        return {"mensagem": "Status atualizado com sucesso!"}
        
    except Exception as erro:
        return {"erro": f"Falha ao atualizar: {str(erro)}"}