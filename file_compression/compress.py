import zlib,base64

data = open('files\demo.txt','r').read() 
data_types = bytes(data,'utf-8')
compressed_data = base64.b64encode(zlib.compress(data_types))


