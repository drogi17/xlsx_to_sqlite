import sqlite3

def outp_correct(data_all):
    x_c = 0
    y_c = 0
    while y_c <= len(data_all)-1:
        while x_c <= len(data_all[y_c])-1:
            if data_all[y_c][x_c] and type(data_all[y_c][x_c]).__name__ == 'str' and ':$"$:' in str(data_all[y_c][x_c]):
                data_all[y_c] = list(data_all[y_c])
                print(data_all[y_c])
                data_all[y_c][x_c] = data_all[y_c][x_c].replace(':$"$:', "'")
            x_c += 1
        x_c = 0
        y_c += 1
    return data_all

class DataBase:
    version = '0.1 Test'
    def __init__(self, data_base_file):
        self.conn = sqlite3.connect(data_base_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def request(self, request, args=None):
        if args:
            request_data = self.cursor.execute(request, args).fetchall()
        else:
            request_data = self.cursor.execute(request).fetchall()
        return outp_correct(request_data)

    def commit(self):
        self.conn.commit()