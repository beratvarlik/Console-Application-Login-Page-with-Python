import sqlite3
import bcrypt
import re


con = sqlite3.connect('../SQL/loginpage.db', timeout=5)
cursor = con.cursor()


def createUserTable():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loginpage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            nickname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')
    con.commit()


def createLogTable():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            userid INTEGER,
            update_subject TEXT
        )
    ''')
    con.commit()


def addLog(userid, update_subject):
    cursor.execute(
        '''
        INSERT INTO logs (userid, update_subject)
        VALUES (?, ?)
        ''',
        (userid, update_subject)
    )
    con.commit()


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


createUserTable()
createLogTable()


class User():
    def __init__(self, email = None, password = None, is_active = 0):

        if is_active == 0:
            self.singin()
            return

        self.email = email  # getUserID için saklandı

        cursor.execute('SELECT is_active FROM loginpage WHERE email = ?', (email,))
        row = cursor.fetchone()

        if row is None:
            print("Bu e-postaya ait bir kayıt bulunamadı. Kayıt olma işlemine yönlendiriliyorsunuz...")
            self.singin()
            return

        db_active = row[0]

        if db_active != is_active:
            print("Kullanıcı aktif değil")
            return

        if self.login(email, password):
            print("Giriş Başarılı")
            addLog(self.getUserID(), "Logged in")
        else:
            print("Şifre veya e-posta hatalı.")


    def getUserID(self):
        cursor.execute('SELECT id FROM loginpage WHERE email = ?', (self.email,))
        return cursor.fetchone()[0]


    def enterData(self):
        name = input('Enter your name: ').capitalize()
        surname = input('Enter your surname: ').capitalize()
        nickname = input('Enter your nickname: ').lower()
        email = input('Enter your email: ').lower()
        if is_valid_email(email):
            self.email = email
            password = input('Enter your password: ')
            password2 = input('Enter your password again: ')
        else:
            print("Bu uzantıda bir e-posta adresi olamaz!")
            return None

        if password == password2:
            self.password = password
            password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            return (name, surname, nickname, email, password_hashed)
        else:
            return None


    def singin(self):
        datas = self.enterData()
        if datas is not None:
            cursor.execute(
                '''
                INSERT INTO loginpage
                (name, surname, nickname, email, password_hash, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
                ''',
                datas
            )
            con.commit()
            addLog(self.getUserID(), "Registered")
            print(f"Kaydınız başarıyla oluşturuldu! Hoş geldin {datas[2]}.")
        else:
            print("ERROR 404")


    def login(self, email, password):
        cursor.execute('SELECT password_hash FROM loginpage WHERE email = ?', (email,))
        row = cursor.fetchone()

        if row is None:
            return False

        return bcrypt.checkpw(password.encode(), row[0].encode())

print("Login Page Uygulamasına Hoş Geldiniz!")
value = input("Bir hesabınız var mı E/H").lower()

if value == "e":
    email = input("E-posta:")
    password = input("Şifreniz:")
    user = User(email, password, 1)

elif value == "h":
    user = User()

else:
    print("E/H dışında bir değer girmeyin.")
