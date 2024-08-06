import sys
import logging
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurar logging
logging.basicConfig(filename='erros.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Consulta de Log de Erros')
        
        self.vpn_label = QLabel('Lembre-se de habilitar a VPN!', self)
        
        self.condo_id_label = QLabel('ID do Condomínio:', self)
        self.condo_id_input = QLineEdit(self)
        
        self.consult_button = QPushButton('Consultar', self)
        self.consult_button.clicked.connect(self.on_consult)
        
        self.id_consulta_label = QLabel('ID da Consulta (opcional):', self)
        self.id_consulta_input = QLineEdit(self)
        self.id_consulta_input.setVisible(False)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Table Name', 'Sentido', 'Operation', 'Error'])

        layout = QVBoxLayout()
        layout.addWidget(self.vpn_label)
        layout.addWidget(self.condo_id_label)
        layout.addWidget(self.condo_id_input)
        layout.addWidget(self.consult_button)
        layout.addWidget(self.id_consulta_label)
        layout.addWidget(self.id_consulta_input)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.show()

    def on_consult(self):
        condo_id = self.condo_id_input.text().strip()
        id_consulta = self.id_consulta_input.text().strip()

        if not condo_id:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira o ID do condomínio.')
            return

        query = self.build_query(id_consulta)
        result, error = self.run_query(condo_id, query)

        if error:
            QMessageBox.critical(self, 'Erro', error)
        else:
            self.update_table(result)
            self.id_consulta_input.setVisible(True)

    def build_query(self, id_consulta):
        if not id_consulta:
            return "SELECT id, table_name, sentido, operation, error FROM log_sync_err ORDER BY id DESC;"
        else:
            return f"SELECT id, table_name, sentido, operation, error FROM log_sync_err WHERE id > {id_consulta} ORDER BY id DESC;"

    def run_query(self, condo_id, query):
        db_url = f'mysql+pymysql://rodrigo.veiga:1687555059@193.122.203.251:21286/{condo_id}'
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            result = session.execute(query).fetchall()
            session.commit()
            return result, None
        except Exception as e:
            session.rollback()
            error_message = f'Erro ao executar a consulta: {e}'
            logging.error(error_message)
            return None, error_message
        finally:
            session.close()

    def update_table(self, result):
        self.table.setRowCount(len(result))
        for row_idx, row_data in enumerate(result):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DatabaseApp()
    sys.exit(app.exec_())
