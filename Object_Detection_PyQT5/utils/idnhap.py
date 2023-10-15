import csv

# Save username and password to file .csv
def saveId(user, pwd):
    headers = ['name', 'key']
    values = [{'name':user, 'key':pwd}]
    with open('userInfo.csv', 'a', encoding='utf-8', newline='') as fp:
        writer = csv.DictWriter(fp, headers)
        writer.writerows(values)

# Read file .csv to get information account
def getId():
    USER_PWD = {}
    with open('userInfo.csv', 'r') as csvfile:
        spamReader = csv.reader(csvfile)
        # Duyệt qua từng dòng tệp csv, lưu trữ tên người dùng và mật khẩu theo từ điển
        for row in spamReader:
            USER_PWD[row[0]] = row[1]
    return USER_PWD