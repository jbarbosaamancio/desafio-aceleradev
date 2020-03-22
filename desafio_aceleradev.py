#Bibliotecas
import hashlib,json,requests

#Constantes
CHAVE = 8
TMH_MAX_CHAR = 26

def receber():

    token = "ac65191a3298ea43e7dafa7a65d76caa69c8c2a4"
    url = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={0}".format(token)
    
    response = requests.get(url)

    with open("answer.json", "wb") as file:
        file.write(response.content)

def enviar():
    # Envia o desafio para a API via POST
    token = "ac65191a3298ea43e7dafa7a65d76caa69c8c2a4"
    url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={0}".format(token)
    
    with open("answer.json", "rb") as file:
        files = {"answer": file.read()}

    response = requests.post(url, files=files)

    print(response.content.decode("utf-8"))

def carregar_json(file):
    with open(file,"r") as fl:
        dados = json.load(fl)
    return dados

def escrever_json(dados):
     with open("answer.json", "w") as file:
        json.dump(dados,file)

def cifrar(msg, chave):
    
    msg = msg.lower()
    traduzido = ""

    for simb in msg:

        if simb.isalpha():
            num = ord(simb)
            num += chave
            
            if simb.islower():
                if  num > ord('z'):
                    num -= TMH_MAX_CHAR

                elif num < ord('a'):
                    num += TMH_MAX_CHAR

            traduzido += chr(num)

        else:
            traduzido += simb 

    return traduzido

def decifrar(msg, chave):
    
    msg = msg.lower()
    traduzido = ""
    chave *= -1
    
    for simb in msg:

        if simb.isalpha():
            num = ord(simb)
            num += chave
            
            if simb.islower():
                if  num > ord('z'):
                    num -= TMH_MAX_CHAR
                elif num < ord('a'):
                    num += TMH_MAX_CHAR
            traduzido += chr(num)
        else:
            traduzido += simb  
    return traduzido

receber()

data = carregar_json("answer.json")

msg_cifrada =  data["cifrado"]

msg_decifrada = decifrar(msg_cifrada,CHAVE)

data["decifrado"] = msg_decifrada

resumo_criptografado = hashlib.sha1(msg_decifrada.encode('utf-8')).hexdigest()
data["resumo_criptografico"] = resumo_criptografado

escrever_json(data)
escrever_json(data)

enviar()

