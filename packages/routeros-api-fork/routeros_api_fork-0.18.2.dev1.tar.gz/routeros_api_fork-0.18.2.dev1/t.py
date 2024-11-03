import routeros_api_fork

host = '192.168.88.1'
username = 'python'
password = 'YwQuGoFGLCi5g4p'

connection = routeros_api_fork.RouterOsApiPool(host, username=username, password=password, port=8728, plaintext_login=True)

api = connection.get_api()
address_list_resource = api.get_resource('/ip/firewall/address-list')
for entry in address_list_resource.get(address='31.13.72.9'):
    print(entry)