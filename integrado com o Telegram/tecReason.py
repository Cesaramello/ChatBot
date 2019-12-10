# Código integrado com o telegram

# César Augusto Sampaio de Mello
# Mariana Narita Masunaga Nara Mendes Benitez 

# -*- coding: utf-8 -*-
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing

intencao = []
frases = []
f = open("intencoes.txt", "r") 
for x in f:
 
  classe, texto = x.split(">>") #separa intenções das frases usando split
  intencao.append(classe) #salva as intenções no vetor intencao
  frases.append(texto.rstrip()) #salva o resto das frases no vetor frase... rstrip remove o\n
 
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,strip_accents='unicode')
x = vectorizer.fit_transform(frases)
 
##### KNN 
y = np.array(intencao)
loo = LeaveOneOut()
loo.get_n_splits(x)
array = []
#print(loo)
 
for train_index, test_index in loo.split(x):
  X_train, X_test = x[train_index], x[test_index]
  y_train, y_test = y[train_index], y[test_index]
  
  #KNN
  model = KNeighborsClassifier(n_neighbors=1)
  model.fit(X_train,y_train)
  
  resultado = model.predict(X_test)[0]
  array.append(resultado) 
   
import random
#print("Nick>> Olá, como posso ajudar?")
entradaUsuario = ' '
 
#Criação de vetores respostas para intenções
vet_respostas = {
    "agradecimento": ["Por nada!","Eu que agradeço!"],
    "ajuda": ["Em que posso ajudar?","Como posso ajudar?"],
    "aulaexperimento": ["Você pode agendar sua aula através do número (67)3211-2199","Ligue para o número (67)3211-2199 e agende sua aula experimental com um de nossos atendentes"],
    "bolsadeestudo": ["Não trabalhamos com bolsa de estudo","No momento não temos bolsa de estudo","Por enquanto não oferecemos bolsa de estudo"],
    "cancelamento": ["Para realizar qualquer tipo de cancelamento, você deve entrar em contato com a empresa","Ligue para o número (67)3211-2199 e faça seu cancelamento com uma de nossas atendentes","O cancelamento é feito apenas com nossas atendentes"],
    "certificado": ["Ao final de cada curso, o aluno recebe uma certificação","O certificado é gerado no final do curso","O certificado será gerado ao final do curso"],
    "contato": ["Telefone: (67) 3211-2199 \nSite: http://www.tecreason.com.br/ \nEmail: tecreason@hotmail.com"],
    "coloniadeferias": ["A colônia de férias são cursos destinados à crianças no período de férias. Confira nossos cursos em https://www.codigokid.com.br/","Nossa colônia de férias é incrível para as crianças passarem o período de férias. Veja nossos cursos em https://www.codigokid.com.br/"],
    "cursoaula": ["Confira os detalhes nos sites: \nhttp://www.tecreason.com.br/ \nhttps://www.codigokid.com.br/","Em nossos sites você saberá mais sobre nossos cursos: \nhttp://www.tecreason.com.br/ \nhttps://www.codigokid.com.br/"],
    "despedida": ["Até mais","tchau o/","Até mais, estarei aqui se precisar"],
    "endereco": ["Rua Espírito Santo, número 1503 - Vila Gomes - Campo Grande, Mato Grosso do Sul"],
    "empresa": ["Consulte informações no nosso site: www.tecreason.com.br","Saiba mais sobre nossa empresa em nosso site: www.tecreason.com.br"],
    "estado" : ["Estou bem! Como posso te ajudar?"],
    "facom" : ["Faculdade de computação está localizada em UFMS-Campo Grande"],
    "horariofuncionamento": ["Seg à Sex das 8:00h às 17:00h e Sábado das 8:00h ao 12:00h"],
    "idade": ["Aqui na TecReason oferecemos cursos para todas as idades. \nOpções de cursos para crianças: https://www.codigokid.com.br/ Mais informações em: \nhttp://www.tecreason.com.br/"],
    "infocurso": ["Você pode conferir melhor os detalhes nos sites: \nhttp://www.tecreason.com.br/ \nhttps://www.codigokid.com.br/","Para mais detalhes entre em nossos sites: \nhttp://www.tecreason.com.br/ \nhttps://www.codigokid.com.br/"],
    "matricula": ["As matrículas são feitas presencialmente no local da empresa","A matrícula é feita apenas em nossa escola","Venha até nossa escola para realizar sua matrícula","Realizamos a matrícula apenas em nossa escola"],
    "nick": ["Sou o chatbot da tecReason! Estou aqui para tirar dúvidas.","sou eu :D","it's me, Nick o/"],
    "normas": ["Você pode consultar nossas normas no site http://www.tecreason.com.br/","Nossas normas estão no nosso site http://www.tecreason.com.br/"],
    "naoentendimento": ["Não entendi. Poderia me explicar melhor?","Não entendi o que você quis dizer"],
    "pagamento": ["O pagamento pode ser realizado à vista ou no cartão de crédito. Pode ser parcelado em até 3x sem juros!"],
    "preco": ["Os valores são especificados somente na empresa","Venha até nossa escola ou fale com uma de nossas atendentes para saber mais sobre os preços","Entre em contato com uma de nossas atendentes para saber sobre nossos valores"],
    "presencial": ["Os cursos são feitos via Ensino à Distância(EAD), mas o aluno pode frequentar a escola"],
    "respostadefault": ["Que?","Não entendi, explique de novo"],
    "saudacao": ["Olá","Oi!","Oie"],
    "trocadilho": ["No céu da frança tem pão francês kkkkkk"],
    "reserva": ["Reservas podem ser feitas somente por telefone ou diretamente na empresa","Não posso realizar reserva por aqui, tente entrar em contato com uma de nossas atendentes"],
    "tecreason": ["Conheça nossa empresa: \nSite:http://www.tecreason.com.br/ \nInstagram: tecreason"],
    "respostanegativa": ["ok!","tudo bem!"]
}

def criador_de_resposta(intencao):
  return random.choice(vet_respostas.get(intencao))

import telepot
api = "952574925:AAGxBqk4hKaSeiX1ixXt6QTdy0mzXrCCGS8"

def receber(msg):
  text = msg['text']
  _id = msg['from']['id']

  inst = vectorizer.transform([text])
  intencao = model.predict(inst)#[0]
                
  if intencao =='agradecimento':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("agradecimento"))
    #print("Nick>> "+criador_de_resposta("agradecimento"))

  elif intencao =='ajuda':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("ajuda"))
    #print("Nick>> "+criador_de_resposta("ajuda"))
 
  elif intencao =='aulaexperimental':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("aulaexperimental"))
    #print("Nick>> "+criador_de_resposta("aulaexperimental"))
  
  elif intencao =='bolsadeestudo':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("bolsadeestudo"))
    #print("Nick>> "+criador_de_resposta("bolsadeestudo"))
  
  elif intencao =='cancelamento':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("cancelamento"))
    #print("Nick>> "+criador_de_resposta("cancelamento"))
  
  elif intencao =='certificado':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("certificado"))
    #print("Nick>> "+criador_de_resposta("certificado"))
  
  elif intencao =='contato':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("contato"))
    #print("Nick>> "+criador_de_resposta("contato"))
  
  elif intencao =='coloniadeferias':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("coloniadeferias"))
    #print("Nick>> "+criador_de_resposta("coloniadeferias"))
  
  elif intencao =='cursoaula':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("cursoaula"))
    #print("Nick>> "+criador_de_resposta("cursoaula"))
  
  elif intencao == 'despedida':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("despedida"))
    #print("Nick>> "+criador_de_resposta("despedida"))

  elif intencao =='endereco':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("endereco"))
    #print("Nick>> "+criador_de_resposta("endereco"))
  
  elif intencao =='empresa':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("empresa"))
    #print("Nick>> "+criador_de_resposta("empresa"))
  
  elif intencao == 'estado':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("estado"))
    #print("Nick>> "+criador_de_resposta("estado"))

  elif intencao =='horariofuncionamento':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("horariofuncionamento"))
    #print("Nick>> "+criador_de_resposta("horariofuncionamento"))
  
  elif intencao =='idade':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("idade"))
    #print("Nick>> "+criador_de_resposta("idade"))
  
  elif intencao =='infocurso':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("infocurso"))
    #print("Nick>> "+criador_de_resposta("infocurso"))
  
  elif intencao =='matricula':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("matricula"))
    #print("Nick>> "+criador_de_resposta("matricula"))
  
  elif intencao == 'nick':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("nick"))
    #print("Nick>> "+criador_de_resposta("nick"))
 
  elif intencao =='normas':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("normas"))
    #print("Nick>> "+criador_de_resposta("normas"))
  
  elif intencao =='naoentendimento':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("naoentendimento"))
    #print("Nick>> "+criador_de_resposta("naoen"))
  
  elif intencao =='pagamento':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("pagamento"))
    #print("Nick>> "+criador_de_resposta("pagamento"))
  
  elif intencao =='preco':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("preco"))
    #print("Nick>> "+criador_de_resposta("preco"))
  
  elif intencao =='presencial':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("presencial"))
    #print("Nick>> "+criador_de_resposta("presencial"))
  
  elif intencao =='respostadefault':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("respostadefault"))
    #print("Nick>> "+criador_de_resposta("respostadefault"))
  
  elif intencao =='saudacao':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("saudacao"))
    #print("Nick>> "+criador_de_resposta("saudacao"))
  
  elif intencao == 'trocadilho':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("trocadilho"))
    #print("Nick>> "+criador_de_resposta("trocadilho"))
  
  elif intencao == 'reserva':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("reserva"))
    #print("Kick>> "+criador_de_resposta("reserva"))
  
  elif intencao =='tecreason':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("tecreason"))
    #print("Nick>> "+criador_de_resposta("tecreason"))
  
  elif intencao =='respostanegativa':
    tele.sendMessage(_id, "Nick>> "+criador_de_resposta("respostanegativa"))
    #print("Nick>> "+criador_de_resposta("respostanegativa"))

tele = telepot.Bot(api)
tele.message_loop(receber)

while True:
  pass
