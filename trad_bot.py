import telebot
import requests
import json
import base64
CHAVE_API = "5117408298:AAEaU6BtnS0vApdp1-vTHFpfvCmg1Bias1I"

bot = telebot.TeleBot(CHAVE_API)

idiomas = ["Português", "Inglês", "Chinês", "Alemão"]

#Conecta-se à api de tradução e retorna a resposta ao usuário com as devidas traduções ou exceções.
def traduz(mensagem , lingua_atual_id = 0 , lingua_destino_id = 1 ):
    url = "https://api.gotit.ai/Translation/v1.1/Translate"
    
    linguas = ["PtBr", "EnUs", "ZhCh","DeAl"]
    
    payload = json.dumps({
    "T": str(mensagem.text),
    "SL": linguas[lingua_atual_id - 1],
    "TL": linguas[lingua_destino_id - 1]
    })
    userAndPass = base64.b64encode(b"2294-ZHlbHcfB:zyMmarlm6Hb4QziNfF6/xxcK7F52z7q/C5NyQXO8aeuF").decode("ascii")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {userAndPass}'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        bot.send_message(mensagem.chat.id, f'Tradução do {idiomas[lingua_atual_id-1]} para o {idiomas[lingua_destino_id-1]}:  {response.text[11:-2]}.')
        bot.send_message(mensagem.chat.id, "Clique em /restart para voltar ao menu de comandos. =)")
        
    except :
        bot.send_message(mensagem.chat.id, "Algo de errado não está certo. Por favor /restart")

#Passa o idioma1 para repassa_idioma1
@bot.message_handler(commands = ["traduzir"])
def traduzir(mensagem):
    idioma1 = bot.send_message(mensagem.chat.id, "Digite o número do idioma origem: [1 - Português | 2 - Inglês | 3 - Chinês | 4 - Alemão]")
    bot.register_next_step_handler(idioma1, lambda b: repassa_idioma1(b))

#Pega o idioma1 contido em "mensagem", lê o idioma2 e repassa-os para repassa_idiomas_1e2
def repassa_idioma1(mensagem):
    idioma1 = int(mensagem.text)
    idioma2 = bot.send_message(mensagem.chat.id, "Digite o número do idioma destino: [1 - Português | 2 - Inglês | 3 - Chinês | 4 - Alemão]")
    bot.register_next_step_handler(idioma2, lambda c: repassa_idiomas_1e2(c, idioma1))

#Repassa frase e idiomas de origem e destino para a tradução
def repassa_idiomas_1e2(mensagem,id1):
    idioma2 = int(mensagem.text)
    send = bot.send_message(mensagem.chat.id, f"Digite a frase que deseja traduzir do {idiomas[id1-1]} para o {idiomas[idioma2-1]}")
    bot.register_next_step_handler(send, lambda m: traduz(m, id1, idioma2))
    
def verificar(mensagem):
    return True

@bot.message_handler(func = verificar)
def comandos(mensagem):
    texto = """ 
    Escolha uma opção:
    /traduzir Traduz um texto digitado pelo usuário
    Qualquer comando além desses não vai funcionar.
    """
    bot.reply_to(mensagem, texto)
    

bot.polling()