from ldap3 import Server, Connection, ALL, NTLM, Tls
import logging

try:
    server=Server('ldap://127.0.0.1:389', get_info=ALL)
    connection=Connection(server, auto_bind=True, receive_timeout=1)
    print("ldap server listening on port 389.")
    connection.serve_forever()

except KeyboardInterrupt:
    print("\nldap server shutting down...")

except Exception as e:
    print(f"an error occurred: {e}")

finally:
    if 'connection' in locals() and connection.listening:
        connection.stop_listening() 
    print("ldap server stop")