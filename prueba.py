import pyodbc

DATA_BASE='WAREHOUSING'
SERVER='sqles.backoffice.com.ar,1480'
UID='powerbi'
PWD='Pb3661'

conn=pyodbc.connect('Driver={SQL Server}; Server='+SERVER+'; Database='+DATA_BASE+'; UID='+UID+'; PWD='+PWD+';')