import wx
import hospital
import mysql.connector

class DataManager:
    def __init__(self):
        self.conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="rumah_sakit")
        self.cursor = self.conn.cursor()

    def Jalankan(self, query, returnData = False):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.conn.commit()
        if returnData :
            return result

class Login (DataManager, hospital.MyFrame1):
    def __init__(self, parent):
        hospital.MyFrame1.__init__(self, parent)
        self.DM = DataManager()
    
    def btn_login( self, event ):
        username = self.m_textCtrl8.GetValue()
        password = self.m_textCtrl9.GetValue()

        self.query = "select * from admin where username = '{}' and password = '{}'".format(username, password)
        hasil = self.DM.Jalankan(self.query, returnData = True)
        
        if hasil is not None and len(hasil) > 0:
            event = Tabel(None)
            event.Show()
            self.Destroy()
            self.DM.conn.close()
        else:
            wx.MessageBox('Username atau Password yang anda masukkan salah', 'Terjadi Kesalahan')


run = wx.App()
frame = Login(parent=None)
frame.Show()
run.MainLoop()