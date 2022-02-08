import smtplib
import email.message

def sendEmail(nomeUser, emailUser, numUser, msgUser): 
    mensagem = f"""
    <h1>{nomeUser} deseja entrar em contato!</h1>
    <hr>
    <ul>
        <li>Seu e-mail é: {emailUser}</li>
        <li>Seu número de celular: {numUser}</li>
    </ul>
    <hr>
    <h2>Mensagem:</h2>
    <p>{msgUser}</p>
    """

    msg = email.message.Message()
    msg["Subject"] = "Contato"                          # Assunto do mensagem.
    msg["From"] = "enviadordeemailsteste@gmail.com"     # E-mail do remetente.
    msg["To"] = "enricogregorio5@gmail.com"             # E-mail do destinatário.
    password = "Show123casa"                            # Senha do remetente.
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(mensagem)

    s = smtplib.SMTP("smtp.gmail.com: 587")
    s.starttls()
    # Credenciais de login para enviar o email.
    s.login(msg["From"], password)
    s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
    print("Email enviado")
