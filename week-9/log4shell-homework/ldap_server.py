from ldap3 import Server, Connection, ALL
import socket, time

HOST="0.0.0.0"
PORT=389
print("ldap server listening on port 389.")
listener=socket.Socket()
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
listener.bind((HOST, PORT))
listener.listen()

try:

    sock, _=listener.accept()
    conn=Connection(Server(None, get_info=ALL), client_socket=sock)
    time.sleep(2)
    conn.unbind()
    sock.close()

except KeyboardInterrupt:
    print("\nldap server shutting down...")

except Exception as e:
    print(f"an error occurred: {e}")

finally:
    listener.close
    print("ldap server stop")