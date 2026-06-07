from app import create_app
import socket

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

app = create_app()

if __name__ == '__main__':
    port = 5000
    try:
        # Tenta usar a 5000, se falhar, pega uma livre
        app.run(host='0.0.0.0', port=port, debug=False)
    except OSError:
        port = get_free_port()
        print(f'Porta 5000 ocupada, subindo em: {port}')
        app.run(host='0.0.0.0', port=port, debug=False)