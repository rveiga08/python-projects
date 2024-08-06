import pygame
import base64
from io import BytesIO
import pycurl

# Função para decodificar Base64
def base64_decode(encoded):
    try:
        decoded_bytes = base64.b64decode(encoded)
        decoded_string = decoded_bytes.decode('utf-8')  # ou outra codificação apropriada
        return decoded_string
    except Exception as e:
        print(f"Erro ao decodificar Base64: {e}")
        return ""

# Função para carregar uma imagem da memória
def load_image_from_memory(binary_data):
    image = pygame.image.load(BytesIO(binary_data))
    return image

# Função para realizar uma consulta HTTP usando cURL
def perform_http_request(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    response = BytesIO()
    c.setopt(c.WRITEDATA, response)
    c.perform()
    c.close()
    return response.getvalue().decode('utf-8')

# Inicializar o Pygame
pygame.init()

# Configurações da janela
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Base64 to Image Converter")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# Carregar fonte
font = pygame.font.SysFont("arial", 16)

# Inicializar variáveis
equipamento_ip = ""
acionador_id = ""
base64_string = ""

# Loop principal
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.unicode < 128:
                if input_text.get_text() == "Cole a string Base64 aqui":
                    input_text.set_text("")
                if event.key == pygame.K_BACKSPACE:
                    # Backspace para remover caracteres
                    current_string = input_text.get_text()
                    if current_string:
                        current_string = current_string[:-1]
                        input_text.set_text(current_string)
                elif event.key == pygame.K_RETURN:
                    # Enter para processar a string Base64
                    base64_string = input_text.get_text()
                    binary_data = base64.b64decode(base64_string)
                    image = load_image_from_memory(binary_data)

                    if image.get_width() == 0 or image.get_height() == 0:
                        error_text.set_text("Erro: String Base64 inválida.")
                    else:
                        error_text.set_text("")

                    # Exibir imagem na janela
                    window.blit(image, (0, 0))
                    input_text.draw(window)
                    error_text.draw(window)
                    pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Botão Consultar
            if button_rect.collidepoint(mouse_pos):
                # Consultar a URL com IP e ID inseridos
                equipamento_ip = input_text.get_text()
                acionador_id = response_text.get_text()
                url = f"http://{equipamento_ip}/cgi-bin/AccessFace.cgi?action=list&UserIDList[0]={acionador_id}"

                # Realizar a consulta HTTP
                http_response = perform_http_request(url)

                # Exibir a resposta na tela
                response_text.set_text(f"Resposta do servidor:\n{http_response}")

            # Botão Visualizar
            elif view_button_rect.collidepoint(mouse_pos):
                # Atualizar o campo de texto com a nova string
                input_text.set_text(base64_string)

                # Exibir imagem na janela
                image = load_image_from_memory(base64.b64decode(base64_string))
                window.blit(image, (0, 0))
                input_text.draw(window)
                error_text.draw(window)
                pygame.display.update()

    window.fill(white)
    pygame.draw.rect(window, white, input_rect)
    input_text.draw(window)
    window.blit(ip_label.get_surface(), ip_label.get_rect())
    window.blit(id_label.get_surface(), id_label.get_rect())
    error_text.draw(window)

    pygame.draw.rect(window, white, button_rect)
    window.blit(button_text.get_surface(), button_text.get_rect())

    pygame.draw.rect(window, white, view_button_rect)
    window.blit(view_button_text.get_surface(), view_button_text.get_rect())

    response_text.draw(window)

    pygame.display.update()
    clock.tick(30)
