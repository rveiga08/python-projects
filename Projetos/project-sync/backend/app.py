from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

def connect_to_db():
    return pymysql.connect(
        host='193.122.203.251',
        user='rodrigo.veiga',
        password='1687555059',
        port='21286',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/consulta', methods=['POST'])
def consulta():
    data = request.json
    id_condominio = data.get('id_condominio')
    id_consulta = data.get('id_consulta')

    query = f"SELECT * FROM `{id_condominio}.log_sync_err`"
    if id_consulta:
        query += f" WHERE id > {id_consulta}"
    query += " ORDER BY id DESC"

    connection = connect_to_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    connection.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
