def file_read(file_name):
    file_name = open(file_name, 'r')
    print(file_name.read())
    
    file_name.close

file_read(input())