import zlib,base64

data = open('files\demo.txt','r').read() 
data_types = bytes(data,'utf-8')
compressed_data = base64.b64encode(zlib.compress(data_types))
decoded_data = compressed_data.decode('utf-8')
compressed_file = open('compressed.txt','w')
compressed_file.write(decoded_data)

decompressed_data = zlib.decompress(base64.b64decode(compressed_data))
print (decompressed_data)


