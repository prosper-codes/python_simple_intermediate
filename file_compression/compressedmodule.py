import zlib, base64


def compress (input_file ,outputfile):
    data = open(input_file,'r').read() 
    data_types = bytes(data,'utf-8')
    compressed_data = base64.b64encode(zlib.compress(data_types))
    decoded_data = compressed_data.decode('utf-8')
    compressed_file = open(outputfile,'w')
    compressed_file.write(decoded_data)

compress('files\demo.txt','comp.txt')
 
def decompress(inputfile ,outputfile):
    file_content = open (inputfile ,'r').read()
    encoded_data= file_content.encode('utf-8')
    decompressed_data=zlib.decompress(base64.b64decode(encoded_data))
    decoded_data=decompressed_data.decode('utf-8')
    file=open(outputfile,'w')
    file.write(decoded_data)
    file.close()


decompress('comp.txt','decomp.txt')