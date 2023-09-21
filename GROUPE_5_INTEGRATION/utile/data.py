import sqlite3

# valeurs de simulation
fake_victims = [
    [1,
     '7F8450550806FDD46F70E307A016CFEE9EC7CF8768E5F0C20EA0382FF3D0324FA38B96691405BEC2624CC2CE75216604A2DC6E590B99C719'
     '5EABDA6FDFE0CD1DD87C58832011FCFA0EA5F58B004F69B4ACC36740975BE22A06BD8C21323899524398FF835575F6636572DE0D55AD49E2'
     '34C0B7E7E2443E895EF60AB3DC7F6FA3',
     'WORKSTATION', 'c:,e:,f:', 'PENDING', 108],
    [2,
     '61AA1B2E9331A6AA453E3CA5C6648573C025F12C57B66D4152BA033096DBA834122BFB300CB61A60411EB9545436CEF23B25C3596208C613'
     'C3457B8BAE26A93999E71F5858D8D55984F16937C48F705FE2A3E985AE091352F0C8A612C548F68F77BDD3B2474BC6591B181516CCD8626C'
     'C4C80A47B3292EBE47B48A3E790330D9',
     'SERVEUR', 'c:,e:', 'PROTECTED', 23],
    [3,
     '8873B1F65C614B63CC60381CC0FBFB62E37D8E53462A5B5F56FFD8D1C1936B7DF2092BAB6A404FFE505A9E77CF691B9EF9B1203BC907A2E4'
     'AA34F7829693D5F9F9D2918CE46D223F14B1B204DE7BFA3EB6E6C7BB011D28666B21BFD0C77BA2A1970AF51E16365485815B204154426960'
     '543ADD142E45DAE9AF74D6260343C670',
     'WORKSTATION', 'c:,f:', 'INITIALIZE', 0],
    [4,
     '589F8453D6AC610ABD40CC94DD7FA0FCFACD1801D46C57C89F9FD039F56B52B9FC090A4C702A9E10A1A3355409A017961F8D4EBD8FFFB53D'
     'D893B4B60D97E1492FAB313A4FD6050F016C173596CC0D4D9899267BD7DA147BC9B86A2C2250FC855C651FA34C4457F8BEC66E7D92135802'
     '26876B24DB25CE1C2C08ECEE96BD64EF',
     'WORKSTATION', 'c:,f:,y:,z:', 'PROTECTED', 108]
]

fake_histories = [
    [1614356410, 'INITIALIZE', 0],
    [1614356420, 'CRYPT', 0],
    [1614356430, 'PENDING', 20],
    [1614356760, 'DECRYPT', 23],
    [1614356990, 'DECRYPT', 23]
]


dataBase = sqlite3.connect('../serveur_cles/data/victims.sqlite',  check_same_thread=False)
cursor = dataBase.cursor()


"""
################## INSERT INTO FUNCTION ################## 
"""


def addVictims(id_victims, os, hash, disks, key):
    i = 0
    while i < 4:
        queryAddVictims = f'INSERT INTO victims (id_victim, os, hash, disks, key) VALUES ' \
                          f'("{fake_victims[i][0]}", "{fake_victims[i][1]}", "{fake_victims[i][2]}", "{fake_victims[i][3]}", "{fake_victims[i][4]}");'
        cursor.executescript(queryAddVictims)
        i += 1


def addStates(id_states, id_victims, datetime, state):
    queryAddStates = f'INSERT INTO states (id_states, id_victims, datetime, state)' \
                     f'VALUES ({id_states}, {id_victims}, {datetime}, {state});'
    cursor.executescript(queryAddStates)


def addEncrypted(id_encrypted, id_victims, datetime, nb_files):
    queryEcrypted = f'INSERT INTO victims (id_encrypted, id_victims, datetime, nb_files)' \
                    f'VALUES ({id_encrypted}, {id_victims}, {datetime}, {nb_files});'
    cursor.executescript(queryEcrypted)


def addDecrypted(id_decrypted, id_victims, datetime, nb_files):
    queryDecrypted = f'INSERT INTO victims (id_decrypted, id_victims, datetime, nb_files)' \
                     f'VALUES ({id_decrypted}, {id_victims}, {datetime}, {nb_files});'
    cursor.executescript(queryDecrypted)


"""
################## SELECT FUNCTIONS ################## 
"""


def readVictims(id=False):
    if not id:
        cursor.execute('SELECT * FROM victims;')
        rows = cursor.fetchall()
        return rows
    else:
        cursor.execute(f'SELECT * FROM victims WHERE id_victim = {id};')
        rows = cursor.fetchone()
        return rows


def main():
    addVictims(fake_victims)
    data = readVictims(2)
    print(data[0])


if __name__ == '__main__':
    main()
