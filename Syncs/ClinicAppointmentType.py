from DatabaseSyncs import DBFunctions as dbf

ListofList = []
HostFail = []
sqlquery = 'SELECT type_id, description, amount, appt_minutes FROM appt_types'

for i in range(1,len(dbf.ClinicDict)+1): #Loop while in range of max clinic #len(dbf.ClinicDict)+1
    hostip = dbf.ClinicDict[i] #Set IP Variable
    QueryResults = dbf.ESGrab(hostip,sqlquery)
    if not QueryResults:
        HostFail.append(hostip)
        pass
    else:
        for idx, row in enumerate(QueryResults): #For each row of data
            ListofList.append([i]) #add list for each row with clinic ID
            for value in row: #For each value in the row's Tuple
                ListofList[len(ListofList)-1].append(value) #Append to last list added

dataText = ''
for item in ListofList:
    dataText+=str(tuple(item))+','
dataText = dataText[:-1]
insertString = 'INSERT INTO "Clinic"."AppointmentType" VALUES {0} ON CONFLICT (clinicid, typeid) DO NOTHING'.format(dataText) #Create row insert string
try:
    dbf.PGInsert(insertString) #Execute query
except:
    print("Couldn't INSERT row: ") #Error
    print(insertString) #Error
print(HostFail or "No failures")
