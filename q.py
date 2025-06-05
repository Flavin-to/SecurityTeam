import customtkinter as ctk
import json
import requests

is_admin_logged_in = False
is_vip_logged_in = False

WEBHOOK_URL = "https://discord.com/api/webhooks/1373416947034750996/fwb1dStvCh06tlCgu4xeSrxpRhFTcMLJ4Axd-eAxpG7Vspv-krNHgm"

def post():
    data = {"content": "Connect At SecurityTeam"}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("LOG: Mensagem enviada via webhook")
    else:
        print(f"LOG: Erro webhook {response.status_code}")

def salvar_dados(user, pwd, tipo="user"):
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados_atuais = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados_atuais = {"usuarios": {}}

    dados_atuais["usuarios"][user] = {"senha": pwd, "tipo": tipo}

    with open("dados.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados_atuais, arquivo, indent=4, ensure_ascii=False)
    print(f"LOG: Usuário '{user}' salvo no JSON")

def abrir_tela_registro():
    registro = ctk.CTk()
    registro.geometry("400x250")
    registro.title("Tela de Registro")

    user_entry = ctk.CTkEntry(registro, placeholder_text="Novo usuário")
    user_entry.pack(pady=10, padx=20)

    pwd_entry = ctk.CTkEntry(registro, placeholder_text="Nova senha", show="*")
    pwd_entry.pack(pady=10, padx=20)

    def registrar():
        user = user_entry.get()
        pwd = pwd_entry.get()
        if user and pwd:
            salvar_dados(user, pwd, tipo="user")  # Sempre user no registro público
            registro.destroy()
        else:
            print("LOG: Preencha todos os campos!")

    btn_registrar = ctk.CTkButton(registro, text="Registrar", command=registrar)
    btn_registrar.pack(pady=20)

    registro.mainloop()

def atualizar_tipo_usuario(nome_usuario, novo_tipo):
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados_atuais = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("LOG: Arquivo de dados não encontrado ou vazio.")
        return

    if nome_usuario in dados_atuais.get("usuarios", {}):
        dados_atuais["usuarios"][nome_usuario]["tipo"] = novo_tipo
        with open("dados.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados_atuais, arquivo, indent=4, ensure_ascii=False)
        print(f"LOG: Tipo do usuário '{nome_usuario}' alterado para '{novo_tipo}'")

def abrir_tela_admin():
    admin_window = ctk.CTk()
    admin_window.geometry("800x600")
    admin_window.title("Página Admin")
    app.withdraw()
    post()

    label = ctk.CTkLabel(admin_window, text="Bem-vindo, Admin!", font=("Arial", 24))
    label.pack(pady=20)

    lista_usuarios = ctk.CTkComboBox(admin_window, width=300)
    lista_usuarios.pack(pady=10)

    tipo_usuario = ctk.CTkComboBox(admin_window, values=["user", "admin", "vip"], width=150)
    tipo_usuario.pack(pady=10)

    def carregar_usuarios():
        try:
            with open("dados.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            dados = {"usuarios": {}}

        usuarios = dados.get("usuarios", {})
        lista_usuarios.configure(values=list(usuarios.keys()))
        if usuarios:
            lista_usuarios.set(list(usuarios.keys())[0])
            tipo_usuario.set(usuarios[list(usuarios.keys())[0]]["tipo"])
        else:
            lista_usuarios.set("")
            tipo_usuario.set("")

    def ao_selecionar_usuario(event):
        user = lista_usuarios.get()
        if not user:
            return
        try:
            with open("dados.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            dados = {"usuarios": {}}

        tipo = dados.get("usuarios", {}).get(user, {}).get("tipo", "user")
        tipo_usuario.set(tipo)

    def salvar_alteracao():
        user = lista_usuarios.get()
        novo_tipo = tipo_usuario.get()
        if user and novo_tipo:
            atualizar_tipo_usuario(user, novo_tipo)

    def logout():
        admin_window.destroy()
        app.deiconify()

    lista_usuarios.bind("<<ComboboxSelected>>", ao_selecionar_usuario)

    btn_salvar = ctk.CTkButton(admin_window, text="Salvar Alteração", command=salvar_alteracao)
    btn_salvar.pack(pady=10)

    btn_logout = ctk.CTkButton(admin_window, text="Logout", fg_color="red", command=logout)
    btn_logout.pack(pady=10)

    carregar_usuarios()

    admin_window.mainloop()

def abrir_tela_usuario(user):
    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"usuarios": {}}

    tipo = dados.get("usuarios", {}).get(user, {}).get("tipo", "user")

    user_window = ctk.CTk()
    user_window.geometry("800x600")
    user_window.title(f"Bem-vindo, {user}")
    app.withdraw()

    label_bemvindo = ctk.CTkLabel(user_window, text=f"Bem-vindo, {user}!", font=("Arial", 24))
    label_bemvindo.pack(pady=20)

    status_vip = "VIP" if tipo == "vip" else "Usuário comum"
    label_vip = ctk.CTkLabel(user_window, text=f"Status: {status_vip}", font=("Arial", 18))
    label_vip.pack(pady=10)

    def logout():
        user_window.destroy()
        app.deiconify()

    btn_logout = ctk.CTkButton(user_window, text="Logout", fg_color="red", command=logout)
    btn_logout.pack(pady=10)

    user_window.mainloop()

def login():
    global is_admin_logged_in
    global is_vip_logged_in

    user = uname.get()
    pwd = passw.get()

    try:
        with open("dados.json", "r", encoding="utf-8") as arquivo:
            dados_atuais = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("LOG: Arquivo de dados não encontrado ou vazio.")
        return

    usuarios = dados_atuais.get("usuarios", {})

    if user in usuarios and usuarios[user]["senha"] == pwd:
        tipo = usuarios[user].get("tipo", "user")
        if tipo == "admin":
            is_admin_logged_in = True
            abrir_tela_admin()
        else:
            is_admin_logged_in = False
            is_vip_logged_in = (tipo == "vip")
            abrir_tela_usuario(user)
    else:
        print("LOG: Denny Access")

app = ctk.CTk()
app.geometry("500x300")
app.eval('tk::PlaceWindow . center')
app.title("Tela de Login")

uname = ctk.CTkEntry(app, placeholder_text="username")
uname.pack(padx=20, pady=10)

passw = ctk.CTkEntry(app, placeholder_text="passworld", show="*")
passw.pack(padx=20, pady=10)

botao_login = ctk.CTkButton(app, text="Login", command=login)
botao_login.pack(pady=10)

botao_registrar = ctk.CTkButton(app, text="Registrar", command=abrir_tela_registro)
botao_registrar.pack(pady=10)

app.mainloop()
