import socket, sys
try:

    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8085 # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'Socket created'
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
         
    print 'Socket bind complete'
     
    #Start listening on socket
    s.listen(10)
    print 'Socket now listening'

    conn, addr = s.accept()
    print "Connected to {}".format(addr)

    file = open(str(sys.argv[1])+".csv", "w")
    file.write("time;x;y;z;rx;ry;rz\n")
    print "Opened outputfile: " + str(sys.argv[1]) + ".csv"
    sys.stdout.write("Receiving data")
    totalTime = 0
    while 1:
        rawdata = conn.recv(100*7*16)
        while rawdata == "":
            conn, addr = s.accept()
            print "reconnected to {}".format(addr)
            rawdata = conn.recv(100*7*16)
        data2 = []
        for i in range(0, len(rawdata)/2):
            num = ((ord(rawdata[(i*2)+1])*2**8)+ord(rawdata[(i*2)]))
            if num > 2**15:
                data2.append(num-2**16)
            else:
                data2.append(num)
        for i in range(0, len(data2)/7):
            j = i*7
            totalTime += data2[j]
            file.write("{};{};{};{};{};{};{}\n".format(totalTime, data2[j+(0+1)], data2[j+(1+1)], data2[j+(2+1)], data2[j+(3+1)], data2[j+(4+1)], data2[j+(5+1)]))
        sys.stdout.write('.')
        sys.stdout.flush()

finally:
    print "\nClosing"
    s.close()