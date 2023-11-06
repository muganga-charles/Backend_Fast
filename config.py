# import pypyodbc
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'DESKTOP-SOLD483\SQLEXPRESS'
DATABASE_NAME = 'SickleSight'
TRUST = 'yes'
VID = 'sa'
PWD = 'user'
# uid = 'vid';
# pwd = 'vid';
connection_string = '''
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER_NAME}}};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
    '''
# .format(
#     driver_name=DRIVER_NAME,
#     server_name=SERVER_NAME,
#     database_name=DATABASE_NAME
#)

# connection = pypyodbc.connect(connection_string)
# print(connection)