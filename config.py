# import pypyodbc
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'sicklesight.database.windows.net'
DATABASE_NAME = 'sickelSight01'
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TRUST = 'yes'
VID = 'SickleSightAdmin'
PWD = 'sicklesight@23'
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