# coding:utf-8

import struct

ftype = {'picture' : ['FFD8FF', '89504E47', '47494638', '424D', '49492A00']}
   
def bytes2hex(bytes):  
    num = len(bytes)  
    hexstr = u""  
    for i in range(num):  
        t = u"%x" % bytes[i]  
        if len(t) % 2:  
            hexstr += u"0"  
        hexstr += t  
    return hexstr.upper()  
  
def check_filetype(file, type): 
    for hcode in ftype[type]:
        numOfBytes = len(hcode) / 2 
        file.seek(0) 
        hbytes = struct.unpack_from("B"*numOfBytes, file.read(numOfBytes)) 
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:  
            return True
    return False