from ldap3 import Connection, Server, ANONYMOUS, SIMPLE, SYNC, ASYNC, ALL, \
    SUBTREE, ALL_ATTRIBUTES


class LdapServer:
    def __init__(self, ip, binddn, bindpw):
        self.ip = ip
        self.binddn = binddn
        self.bindpw = bindpw


class LdapPool:
    _connections = []

    def bind(self, ldapServer):
        server = Server(ldapServer.ip, port=1389, get_info=ALL)
        c = Connection(server, user=ldapServer.binddn,
                                password=ldapServer.bindpw)
        # perform the Bind operation
        if not c.bind():
            print('error in bind', c.result)
            return
        print('bind OK', c.result)

    def addServer(self, ldapServer):
        server = Server(ldapServer.ip, port=1389, get_info=ALL)
        connection = Connection(server, user=ldapServer.binddn,
                                password=ldapServer.bindpw, auto_bind=True)
        self._connections.append(connection);

    def getUser(self, username):
        for connection in self._connections:
            search_base = 'dc=example,dc=com'
            # search_filter = '(&(objectClass=user)(sAMAccountName=' + username + '))'
            search_filter = '(objectClass=top)';

            connection.search(search_base=search_base,
                              search_filter=search_filter,
                              search_scope=SUBTREE,
                              attributes=ALL_ATTRIBUTES)

            print(connection.response)
