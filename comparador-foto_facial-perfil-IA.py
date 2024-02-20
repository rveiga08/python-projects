import csv
import numpy as np
import cv2
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from tkinter import Tk, Label, Button

Base = declarative_base()

class FotosMorador(Base):
    __tablename__ = 'fotos_morador'
    id = Column(Integer, primary_key=True)
    foto = Column(String)
    IdMorador = Column(Integer)

class ImagensImagemBiometria(Base):
    __tablename__ = 'imagens_imagensBiometria'
    id = Column(Integer, primary_key=True)
    imagem = Column(String)
    idAcio = Column(Integer)

def comparar_fotos(foto1, foto2):
    # Implementação da comparação de fotos utilizando inteligência artificial (OpenCV)
    # Convertendo as fotos para tons de cinza
    foto1_gray = cv2.cvtColor(foto1, cv2.COLOR_BGR2GRAY)
    foto2_gray = cv2.cvtColor(foto2, cv2.COLOR_BGR2GRAY)

    # Criando o detector de faces
    detector_faces = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detectando faces nas fotos
    faces1 = detector_faces.detectMultiScale(foto1_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    faces2 = detector_faces.detectMultiScale(foto2_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Se não houver faces em ambas as fotos, considere que as fotos não correspondem
    if len(faces1) == 0 or len(faces2) == 0:
        return False

    # Extração das regiões de interesse (faces) das fotos
    x1, y1, w1, h1 = faces1[0]
    face1 = foto1_gray[y1:y1+h1, x1:x1+w1]

    x2, y2, w2, h2 = faces2[0]
    face2 = foto2_gray[y2:y2+h2, x2:x2+w2]

    # Redimensionamento das faces para o mesmo tamanho para a comparação
    face1 = cv2.resize(face1, (100, 100))
    face2 = cv2.resize(face2, (100, 100))

    # Comparação das faces utilizando o método de comparação de similaridade de histograma
    score = cv2.compareHist(cv2.calcHist([face1], [0], None, [256], [0,256]), 
                            cv2.calcHist([face2], [0], None, [256], [0,256]), 
                            cv2.HISTCMP_CORREL)

    # Se o score for alto (próximo de 1), consideramos as faces como correspondentes
    return score > 0.8

def gerar_relatorio(ids_errados):
    with open('relatorio.csv', 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Tabela']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for id_errado in ids_errados:
            writer.writerow({'ID': id_errado[0], 'Tabela': id_errado[1]})

class SistemaComparacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Comparação de Fotos")
        self.labels = [Label(root), Label(root)]
        self.btn_proximo = Button(root, text="Próximo", command=self.carregar_proxima)
        self.btn_auto = Button(root, text="Automático", command=self.modo_automatico)
        self.ids_errados = []

        self.carregar_proxima()

    def carregar_proxima(self):
        # Lógica para carregar a próxima foto do banco de dados
        # (substitua isso pela sua lógica real de consulta ao banco de dados)
        # Consulta ao banco de dados para obter as fotos do mesmo morador
        try:
            connection = psycopg2.connect(user="seu_usuario",
                                          password="sua_senha",
                                          host="localhost",
                                          port="5432",
                                          database="nome_do_banco")
            cursor = connection.cursor()

            cursor.execute("SELECT fotos_morador.foto, imagens_imagensBiometria.imagem "
                           "FROM fotos_morador "
                           "INNER JOIN imagens_imagensBiometria "
                           "ON fotos_morador.IdMorador = imagens_imagensBiometria.idAcio")
            records = cursor.fetchall()

            for record in records:
                # Substituir pelo carregamento real da foto
                foto1 = np.random.rand(100, 100, 3) * 255  
                foto2 = np.random.rand(100, 100, 3) * 255  

                if comparar_fotos(foto1, foto2):
                    self.labels[0].config(image=foto1)
                    self.labels[1].config(image=foto2)
                else:
                    self.ids_errados.append((1, "fotos_morador"))  

            connection.close()
        except (Exception, psycopg2.Error) as error:
            print("Erro ao buscar dados do banco de dados:", error)

    def modo_automatico(self):
        # Lógica para alternar para o modo automático
        # (substitua isso pela sua lógica real de iteração automática)
        for _ in range(10):  
            self.carregar_proxima()

        # Após a iteração automática, gerar relatório
        gerar_relatorio(self.ids_errados)

root = Tk()
sistema = SistemaComparacao(root)
root.mainloop()
