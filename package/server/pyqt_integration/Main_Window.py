# add this in your QMainWindow class
self.server_worker = Server_Worker()
self.thread = QtCore.QThread()
self.server_worker.moveToThread(self.thread)
self.thread.started.connect(self.server_worker.run)
self.server_worker.res.connect(self.p)
self.thread.start()


 
def p(self,val):
    # add this in your QMainWindow class and write UI changes here the val varible is what result of the post request
    print(val)