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
        
 class Tabel (DataManager, hospital.MyFrame3):
    def __init__(self, parent):
        hospital.MyFrame3.__init__(self, parent)
        self.DM = DataManager()
        self.tampilData()

    def tampilData(self):
        self.query = 'SELECT jenis_pasien, no_rm, nama_pasien, jenis_kelamin, nik, tanggal_lahir, no_hp, alamat, keluhan FROM pasien'
        hasil = self.DM.Jalankan(self.query, returnData=True)
        for a in range (9) :
            b = 0
            for row in hasil:
                self.m_grid2.SetCellValue(b, a, str(row[a]))
                b = b+1

    def btn_logout( self, event ):
        self.DM.conn.close()
        event = Login(None)
        event.Show()
        self.Destroy()
    
    def btn_tambah(self, event):
        event = Registrasi(None)
        event.Show()
        self.Destroy()
        self.DM.conn.close()

class Registrasi (DataManager, hospital.MyFrame2):
    def __init__(self, parent):
        hospital.MyFrame2.__init__(self, parent)
        self.DM = DataManager()
        self.parent = parent

    def btn_simpan( self, event ):
        jenis_pasien = self.m_choice1.GetString(self.m_choice2.GetSelection())
        no_rm = self.m_textCtrl11.GetValue()
        nama_pasien = self.m_textCtrl12.GetValue()
        jenis_kelamin = self.m_choice2.GetString(self.m_choice2.GetSelection())
        nik = self.m_textCtrl14.GetValue()
        tanggal_lahir = self.m_textCtrl4.GetValue()
        no_hp = self.m_textCtrl5.GetValue()
        alamat = self.m_textCtrl6.GetValue()
        keluhan = self.m_textCtrl7.GetValue()

        if jenis_pasien != "" and no_rm != "" and nama_pasien != "" and jenis_kelamin != "" and nik != "" and tanggal_lahir != "" and no_hp != "" and alamat != "" and keluhan != "":
            self.query = "INSERT INTO pasien (jenis_pasien, no_rm, nama_pasien, jenis_kelamin, nik, tanggal_lahir, no_hp, alamat, keluhan) VALUES (%s , %s, %s , %s, %s , %s, %s , %s, %s )"
            self.value = (jenis_pasien, no_rm, nama_pasien, jenis_kelamin, nik, tanggal_lahir, no_hp, alamat, keluhan)
            self.DM.cursor.execute(self.query, self.value)
            self.DM.conn.commit()
            wx.MessageBox('Data Berhasil', 'Selamat data anda berhasil disimpan', wx.OK | wx.ICON_INFORMATION)
            event = Tabel(None)
            event.Show()
            self.Destroy()
            self.DM.conn.close()
        else:
            wx.MessageBox('Data tidak boleh kosong', 'Terjadi Kesalahan')

run = wx.App()
frame = Login(parent=None)
frame.Show()
run.MainLoop()
