def p2p_even_recive(self):
    # add this in your QMainWindow class and connect it the btn that is going to start the server for the peer2peer conection
    if self.server_worker.Stat == False:
        self.server_worker.moveToThread(self.thread)
        self.thread.started.connect(self.server_worker.run)
        self.server_worker.res.connect(self.p)
        self.thread.start()

 
def p(self,val):
    # add this in your QMainWindow class and write UI changes here the val varible is what result of the post request
    print(val)

# add this in your QMainWindow init function
# self.server_worker = Server_Worker()
# self.thread = QtCore.QThread()