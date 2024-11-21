from typing import Annotated

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel import select

from domain import *

usuario_bd="getfit"
senha_bd="getfit"
host_bd="localhost"
banco_bd="getfit"
url_bd = f"mariadb+pymysql://{usuario_bd}:{senha_bd}@{host_bd}:3306/{banco_bd}?charset=utf8mb4"
engine = create_engine(url_bd, echo=True)

#injecao dependencia
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# app
app = FastAPI(debug=True)

@app.get("/")
async def root():
    return {"message": "root"}

#get_all
@app.get("/usuario/all")
async def get_all(se: SessionDep) -> list[Usuario]:
    return se.exec(select(Usuario)).all()

@app.get("/notificacao/all")
async def get_all(se: SessionDep) -> list[Notificacao]:
    return se.exec(select(Notificacao)).all()

@app.get("/mensagem/all")
async def get_all(se: SessionDep) -> list[Mensagem]:
    return se.exec(select(Mensagem)).all()

@app.get("/avaliacao/all")
async def get_all(se: SessionDep) -> list[Avaliacao]:
    return se.exec(select(Avaliacao)).all()

@app.get("/consulta/all")
async def get_all(se: SessionDep) -> list[Consulta]:
    return se.exec(select(Consulta)).all()

@app.get("/curriculo/all")
async def get_all(se: SessionDep) -> list[Curriculo]:
    return se.exec(select(Curriculo)).all()

@app.get("/formulario/all")
async def get_all(se: SessionDep) -> list[Formulario]:
    return se.exec(select(Formulario)).all()

#post_objeto
@app.post("/usuario")
async def postUsuario(usuario: Usuario, se: SessionDep) -> Usuario:
    se.add(usuario)
    se.commit()
    se.refresh(usuario)
    return usuario

@app.post("/notificacao")
async def postNotificacao(notificacao: Notificacao, se: SessionDep) -> Notificacao:
    se.add(notificacao)
    se.commit()
    se.refresh(notificacao)
    return notificacao

@app.post("/mensagem")
async def postMensagem(msg: Mensagem, se: SessionDep) -> Mensagem:
    se.add(msg)
    se.commit()
    se.refresh(msg)
    return msg

@app.post("/avaliacao")
async def postAvaliacao(avaliacao: Avaliacao, se: SessionDep) -> Avaliacao:
    se.add(avaliacao)
    se.commit()
    se.refresh(avaliacao)
    return avaliacao

@app.post("/consulta")
async def postConsulta(consulta: Consulta, se: SessionDep) -> Consulta:
    se.add(consulta)
    se.commit()
    se.refresh(consulta)
    return consulta

@app.post("/curriculo")
async def postCurriculo(curriculo: Curriculo, se: SessionDep) -> Curriculo:
    se.add(curriculo)
    se.commit()
    se.refresh(curriculo)
    return curriculo

@app.post("/formulario")
async def postFormulario(formulario: Formulario, se: SessionDep) -> Formulario:
    se.add(formulario)
    se.commit()
    se.refresh(formulario)
    return formulario

#delete_id
@app.delete("/usuario/{string}")
async def deleteUsuario(id: str, se: SessionDep):
    usuario = se.get(Usuario, id)

    curriculos_nutricionista = se.exec(select(Curriculo).where(Curriculo.id_nutricionista == id)).all()
    curriculos_avaliador = se.exec(select(Curriculo).where(Curriculo.id_avaliador == id)).all()
    for curriculo in curriculos_nutricionista + curriculos_avaliador:
        se.delete(curriculo)
    
    consultas_paciente = se.exec(select(Consulta).where(Consulta.id_paciente == id)).all()
    consultas_nutricionista = se.exec(select(Consulta).where(Consulta.id_nutricionista == id)).all()
    for consulta in consultas_paciente + consultas_nutricionista:
        se.delete(consulta)
    
    formularios = se.exec(select(Formulario).where(Formulario.id_paciente == id)).all()
    for formulario in formularios:
        se.delete(formulario)
    
    avaliacoes_paciente = se.exec(select(Avaliacao).where(Avaliacao.id_paciente == id)).all()
    avaliacoes_nutricionista = se.exec(select(Avaliacao).where(Avaliacao.id_nutricionista == id)).all()
    for avaliacao in avaliacoes_paciente + avaliacoes_nutricionista:
        se.delete(avaliacao)
    
    notificacoes = se.exec(select(Notificacao).where(Notificacao.id_usuario == id)).all()
    for notificacao in notificacoes:
        se.delete(notificacao)
    
    mensagens_receptor = se.exec(select(Mensagem).where(Mensagem.id_receptor == id)).all()
    mensagens_remetente = se.exec(select(Mensagem).where(Mensagem.id_remetente == id)).all()
    for mensagem in mensagens_receptor + mensagens_remetente:
        se.delete(mensagem)

    if usuario != None:
        se.delete(usuario)
        
    se.commit()
    return {"ok": True}

@app.delete("/notificacao/{string}")
async def deleteNotificacao(id: str, se: SessionDep):
    notificacao = se.get(Notificacao, id)
    if notificacao != None:
        se.delete(notificacao)
        se.commit()
    return {"ok": True}

@app.delete("/mensagem/{string}")
async def deleteMensagem(id: str, se: SessionDep):
    mensagem = se.get(Mensagem, id)
    if mensagem != None:
        se.delete(mensagem)
        se.commit()
    return {"ok": True}

@app.delete("/avaliacao/{string}")
async def deleteAvaliacao(id: str, se: SessionDep):
    avaliacao = se.get(Avaliacao, id)
    if avaliacao != None:
        se.delete(avaliacao)
        se.commit()
    return {"ok": True}

@app.delete("/consulta/{string}")
async def deleteConsulta(id: str, se: SessionDep):
    consulta = se.get(Consulta, id)
    if consulta != None:
        se.delete(consulta)
        se.commit()
    return {"ok": True}

@app.delete("/curriculo/{string}")
async def deleteCurriculo(id: str, se: SessionDep):
    curriculo = se.get(Curriculo, id)
    if curriculo != None:
        se.delete(curriculo)
        se.commit()
    return {"ok": True}

@app.delete("/formulario/{string}")
async def deleteFormulario(id_paciente: str, se: SessionDep):
    formulario = se.get(Formulario, id_paciente)
    if formulario != None:
        se.delete(formulario)
        se.commit()
    return {"ok": True}

#get_id
@app.get("/usuario/{string}")
async def get_idUsuario(id: str, se: SessionDep) -> Usuario:
    s = se.exec(select(Usuario).where(Usuario.id == id)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

@app.get("/notificacao/{string}")
async def get_idNotificacao(id: str, se: SessionDep) -> Notificacao:
    s = se.exec(select(Notificacao).where(Notificacao.id == id)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

@app.get("/mensagem/{string}")
async def get_idMensagem(id: str, se: SessionDep) -> Mensagem:
    s = se.exec(select(Mensagem).where(Mensagem.id == id)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

@app.get("/avaliacao/{string}")
async def get_idAvaliacao(id: str, se: SessionDep) -> Avaliacao:
    s = se.exec(select(Avaliacao).where(Avaliacao.id == id)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

@app.get("/consulta/{string}")
async def get_idConsulta(id: str, se: SessionDep) -> Consulta:
    s = se.exec(select(Consulta).where(Consulta.id == id)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

@app.get("/curriculo/{string}")
async def get_idCurriculo(id: str, se: SessionDep) -> Curriculo:
    s = se.exec(select(Curriculo).where(Curriculo.id == id)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

@app.get("/formulario/{string}")
async def get_idFormulario(id_paciente: str, se: SessionDep) -> Formulario:
    s = se.exec(select(Formulario).where(Formulario.id_paciente == id_paciente)).first()
    if not s:
        raise HTTPException(status_code=404)
    return s

#put_id ???