from waitress import serve
import ws

serve(ws.app, host='0.0.0.0', port=8080)