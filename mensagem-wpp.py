from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

# Inicialize o navegador
driver = webdriver.Chrome()  # ou o navegador de sua escolha

# Abra o WhatsApp Web
driver.get('https://web.whatsapp.com/')
input("Faça o login no WhatsApp Web e pressione Enter depois de escanear o código QR...")

# Defina os contatos, mensagens e dias de envio
contacts_messages_and_days = {
    "Gabriela Martinez": {"message": "Eaeee Gabi!! Só passando aqui pra lembrar que o vencimento da mensalidade da Academia de Muay Thai tá chegando! 😊 Não esquece de dar aquela renovada no pagamento antes do dia 07 pra continuar firme e forte nos treinos! \n Qualquer dúvida ou se precisar de uma força, tamo junto! É só chamar! \n Valeu e até breve nos tatames!", "send_day": 05},
    "Luiz Henrique": {"message": "Eaeee Luiz!! Só passando aqui pra lembrar que o vencimento da mensalidade da Academia de Muay Thai tá chegando! 😊 Não esquece de dar aquela renovada no pagamento antes do dia 07 pra continuar firme e forte nos treinos! \n Qualquer dúvida ou se precisar de uma força, tamo junto! É só chamar! \n Valeu e até breve nos tatames!", "send_day": 15},
    "Vinícius Cezar": {"message": "Eaeee Vinícius!! Só passando aqui pra lembrar que o vencimento da mensalidade da Academia de Muay Thai tá chegando! 😊 Não esquece de dar aquela renovada no pagamento antes do dia 07 pra continuar firme e forte nos treinos! \n Qualquer dúvida ou se precisar de uma força, tamo junto! É só chamar! \n Valeu e até breve nos tatames!", "send_day": 15}
}

# Função para enviar mensagens
def send_message(contact_name, message):
    try:
        # Localize o campo de pesquisa
        search_box = driver.find_element_by_xpath('//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.ENTER)
        
        time.sleep(2)  # Espera um pouco para carregar o chat
        
        # Localize o campo de mensagem
        message_box = driver.find_element_by_xpath('//div[@class="_2_1wd copyable-text selectable-text"][@contenteditable="true"][@data-tab="6"]')
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        
        print(f"Mensagem enviada para {contact_name}: {message}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {contact_name}: {str(e)}")

# Função para verificar o dia e enviar mensagens
def check_and_send_messages():
    today = datetime.now().day
    for contact, data in contacts_messages_and_days.items():
        if today == data["send_day"]:
            send_message(contact, data["message"])

# Verifica e envia mensagens diariamente
while True:
    now = datetime.now()
    # Verifica se é meia-noite para enviar mensagens
    if now.hour == 0 and now.minute == 0:
        check_and_send_messages()
        # Espera 24 horas antes de verificar novamente
        time.sleep(86400)
    else:
        # Aguarda um minuto antes de verificar novamente
        time.sleep(60)

# Feche o navegador após a conclusão
driver.quit()
