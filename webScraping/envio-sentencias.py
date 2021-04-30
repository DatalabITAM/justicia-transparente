# %%
import pickle
import os
import smtplib
import mimetypes
import keyring
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


def mime_init(from_addr, recipients_addr, subject, body):
    """
    :param str from_addr:           The email address you want to send mail from
    :param list recipients_addr:    The list of email addresses of recipients
    :param str subject:             Mail subject
    :param str body:                Mail body
    :return:                        MIMEMultipart object
    """

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = ','.join(recipients_addr)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg

def send_email(user, password, from_addr, recipients_addr, subject, body, files_path=None, server='smtp.office365.com'):
    """
    :param str user:                Sender's email userID
    :param str password:            sender's email password
    :param str from_addr:           The email address you want to send mail from
    :param list recipients_addr:    List of (or space separated string) email addresses of recipients
    :param str subject:             Mail subject
    :param str body:                Mail body
    :param list files_path:         List of paths of files you want to attach
    :param str server:              SMTP server (port is choosen 587)
    :return:                        None
    """

    #   assert isinstance(recipents_addr, list)
    FROM = from_addr
    TO = recipients_addr if isinstance(recipients_addr, list) else recipients_addr.split(' ')
    PASS = password
    SERVER = server
    SUBJECT = subject
    BODY = body
    msg = mime_init(FROM, TO, SUBJECT, BODY)

    for file_path in files_path or []:
        with open(file_path, "rb") as fp:
            part = MIMEBase('application', "octet-stream")
            part.set_payload((fp).read())
            # Encoding payload is necessary if encoded (compressed) file has to be attached.
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment", filename= "%s" % os.path.basename(file_path))
            msg.attach(part)

    if SERVER == 'localhost':   # send mail from local server
        # Start local SMTP server
        server = smtplib.SMTP(SERVER)
        text = msg.as_string()
        server.send_message(msg)
    else:
        # Start SMTP server at port 587
        server = smtplib.SMTP(SERVER, 587)
        server.starttls()
        # Enter login credentials for the email you want to sent mail from
        server.login(user, PASS)
        text = msg.as_string()
        # Send mail
        server.sendmail(FROM, TO, text)

    server.quit()

# %%

with open('asignacion-sentencias.p', 'rb') as inp:
    team_info = pickle.load(inp)


# team_info = {
#     'Fede': [[0, 10, 20, 30, 40, 50, 60, 70, 80, 90], 'fd.molina@outlook.com'],
#     'Arturo': [[1, 11, 21, 31, 41, 51, 61, 71, 81, 91], 'lierarturo@gmail.com'],
#     'Fernando': [[2, 12, 22, 32, 42, 52, 62, 72, 82, 92],'fernandogomez210398@gmail.com'],
#     'Ricardo': [[3, 13, 23, 33, 43, 53, 63, 73, 83, 93],'ricardobenacres@gmail.com'],
#     'David': [[4, 14, 24, 34, 44, 54, 64, 74, 84, 94], 'dvdveloz12@gmail.com'],
#     'Victor': [[5, 15, 25, 35, 45, 55, 65, 75, 85, 95], 'amayalvictor@hotmail.com'],
#     'Les': [[6, 16, 26, 36, 46, 56, 66, 76, 86, 96], 'lesliepbv@gmail.com'],
#     'Raquel': [[7, 17, 27, 37, 47, 57, 67, 77, 87, 97], 'raquel.aguayo25@gmail.com'],
#     'Vale': [[8, 18, 28, 38, 48, 58, 68, 78, 88, 98], 'valentina@mancera.org.mx'],
#     'Yosshua': [[9, 19, 29, 39, 49, 59, 69, 79, 89, 99], 'cisne.villasana1im3@gmail.com']
#     }

data_columns = ['id_sentencia','edad_imputado','genero_imputado','estado civil_imputado','oficio_imputado','es_extranjero_imputado','estado de residencia_imputado','es_indigena_imputado','adicciones_imputado','nivel_socioecon_imputado','edad_victima','genero_victima','estado civil_victima','oficio_victima','es_extranjero_victima','estado de residencia_victima','es_indigena_victima','adicciones_victima','nivel_socioecon_victima']


user = 'david.velozs@outlook.com'         # Email userID
password = keyring.get_password('email', user) 
from_addr = 'david.velozs@outlook.com'
add_sample = False

for person in team_info:
    to_do = team_info[person][0]
    address = team_info[person][1]
    recipients_addr = [address]
    if address != '':
        subject = '[Datalab] - Sentencias a etiquetar.'
        body = 'Hola {}\nAdjunto se encuentran las sentencias a etiquetar de esta semana. \nSaludos\nDavid.'.format(person)
        file_paths = []
        pdf_path  = r'C:\Users\dvdve\OneDrive - INSTITUTO TECNOLOGICO AUTONOMO DE MEXICO\DataLab' + '\\' +person
        for i in range(2):
            file_paths.append(pdf_path + '\\sentencia_{}.pdf'.format(to_do.pop(0)))
        if add_sample:
            import pandas as pd
            body = 'Hola {}\nAdjunto se encuentran las sentencias a etiquetar de esta semana y unos archivos tipo excel.\nGuarda el archivo "etiquetas-{}.xlsx" y registra ahí mismo tus observaciones de las sentencias. Para facilitar la recolección de información, no le cambies el nombre al archivo y agrega las etiquetas de las próximas semanas al mismo archivo. \nFinalmente, en el archivo "muestra de etiquetado.xlsx" puedes ver un ejemplo de como se etiquetan las sentencias.\nSaludos\nDavid.'.format(person, person)
            data = pd.DataFrame(columns = data_columns)
            data.to_excel('etiquetas-{}.xlsx'.format(person))
            file_paths.append('etiquetas-{}.xlsx'.format(person))
            aux_path = r'C:\Users\dvdve\OneDrive - INSTITUTO TECNOLOGICO AUTONOMO DE MEXICO\DataLab'
            file_paths.append(aux_path + '\\-aa-muestra de etiquetado\\muestra de etiquetado.xlsx')
        team_info[person][0] = to_do        
        try:
            send_email(user, password, from_addr, recipients_addr, subject, body, file_paths)
            print('data sent succesfully to {}'.format(person))
        except:
            print(user, password, from_addr, recipients_addr, subject, body, file_paths)
            print("Error sending data to {}".format(person))
    else: print('{} has no email on record'.format(person))


with open('asignacion-sentencias.p', 'wb') as out:
    pickle.dump(team_info, out)


# %%
# %%



