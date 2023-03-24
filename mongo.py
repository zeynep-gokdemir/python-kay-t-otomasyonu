
                                                          #çalışan kayıt otomasyonu

import pymongo
from pymongo import MongoClient
import pyinputplus as pyip

connect = MongoClient(
    "mongodb+srv://zeynepgokdemir:b6FcuE3zT7ES5rjJ@cluster1.j6vwxqq.mongodb.net/?retryWrites=true&w=majority")

dbase = connect["calisanlar_db"]
coll = dbase["calisanlar"]


def validate_date(prompt=""):                                                       #girilen tarihi(doğum/işe alım) kontrol etmek için bir fonk tanımlayalım
    while True:
        entered_date = input(prompt)
        date_list = entered_date.split("/")
        date_str_w_out_slashes = "".join(date_list)
        a = 0
        for i in date_str_w_out_slashes:
            if i not in "0123456789":                                                     #tarihte sadece rakamlar olabilir
                if a == 1:                                                                #birden çok rakam olmayan varsa da print birden çok kere
                    continue                                                                                    # çalışmasın diye a yı kullandım
                else:
                    a += 1
                print("gg/aa/yy ; gg,aa ve yy rakamlardan oluşacak şekilde girdiğinizden emin olunuz")
        if entered_date.count("/") != 2:                                                   #iki tane / olmalı
            print("gün ay ve yıl olarak / ile ayrılmış üç alan girdiğinizden emin olunuz")
            continue
        elif a == 1:                                                                      #full rakamsa aşağıdaki kodlardan devam
            continue
        elif len(date_list[0]) != 2 or len(date_list[1]) != 2 or len(date_list[2]) != 2:   #gün,ay ve yıl kısımları ikişer basamaktan oluşmalı
            print("gün, ay ve yıl ifadelerinin hepsi iki basamaklı olmalıdır")
            continue
        elif int(date_list[0]) > 31 or int(date_list[0]) <= 0:                             #0<bir aydaki gün sayısı<32
            print("gün kısmını yanlış girdiniz")
            continue
        elif int(date_list[1]) > 12 or int(date_list[1]) <= 0:                              #0<yıldaki ay sayısı<13
            print("ay kısmını yanlış girdiniz")
            continue
        elif int(date_list[2]) <= 0:                                                        #0<yıl sayısı
            print("yıl kısmını yanlış girdiniz")
            continue
        else:                                                                               #hiçbir sıkıntı yoksa girilen tarihi döndür
            return entered_date
            break

def validate_phone_number(prompt=""):                                                      #girilen tel numarasını kontrol eden bir fonk tanımlayalım
    while True:
        phone_number = input(prompt)
        a = 0
        for l in phone_number:
            if l not in "0123456789":                                                       #tel no rakamlardan oluşmalı
                if a == 1:
                    continue
                else:
                    a += 1
                print("sadece rakamlar girdiğinizden emin olunuz")
        if a == 1:
            continue
        elif " " in phone_number:                                                          #boşluk olmamalı
            print("rakamları boşluk bırakmadan, bitişik girmeniz gerek")
            continue
        elif phone_number[0] == "0":                                                        #başında 0 olmamalı
            print("başına sıfır koymayınız")
            continue
        elif len(phone_number) < 10:                                                         #tam olarak 10 hane olmalı
            print("eksik hane sayısı")
            continue
        elif len(phone_number) > 10:
            print("fazla hane sayısı")
            continue
        else:
            return phone_number                                                               #hiçbir sıkıntı yoksa girilen telefon numarasını döndür
            break

def actions(prompt=""):                                                                       #asıl uygulama bu fonksiyonun çalışmasından ibaret
    while True:
        operation = input(prompt)                                                             #yapılacak işlemin bağdaştırıldığı sayı alınıyor

        if operation == "1":                                                                  #op 1 = çalışan ekleme
            name = pyip.inputStr("çalışanın adını giriniz: ")                                 #çalışana ait girilecek 3 bilginin kontrolünde pyinputplus
            surname = pyip.inputStr("çalışanın soyadını giriniz: ")                                    # lib, diğer 3'ünde tanımladığım fonkları kullandım
            birth_date = validate_date(prompt="çalışanın doğum tarihini gg/aa/yy şeklinde giriniz: ")
            hire_date = validate_date(prompt="işe alınma tarihini gir: ")
            mail = pyip.inputEmail("çalışanın emailini girin: ")
            phone_no = validate_phone_number(
                prompt="çalışanın telefon numarasını başına  sıfır koymadan 10 haneli,bitişik şekilde girin: ")

            new_employee = {"name": name, "surname": surname, "birth date (dd/mm/yy)": birth_date, "mail": mail,
                            "hire date": hire_date, "phone number": phone_no}

            coll.insert_one(new_employee)                                                    #yeni çalışanı db'e kaydedelim


        elif operation == "2":                                                               #op 2 = çalışan sorgulama:( w/id or w/out id ) \
                                                                                                    # (only w/specified name or all employees)
            y = list(coll.find())                                                            #db boşsa
            if len(y) == 0:
                print("hiç çalışan yok")
            else:
                id = pyip.inputMenu(choices=["evet","hayır"] ,prompt="sonuçlarda ID'leri görmek ister misiniz?\n")
                if id == "evet":
                    while True:
                        result = input("ada göre arama yapmak istiyorsanız 1 \nkayıtlı tüm çalışanları görmek istiyorsanız 2 \nyazın ")
                        if result == "1":
                            while True:
                                name = input("bilgilerini görmek istediğiniz çalışanın adını girin: ")
                                myquery = {"name": name}
                                y = list(coll.find(myquery))                                 #böyle isimli biri db de yoksa
                                if len(y) == 0:
                                    print("yanlış ad girdiniz")
                                else:
                                    mydoc= coll.find(myquery)
                                    for x in mydoc:
                                        print(x)
                                    break
                            break
                        elif result == "2":                                                 #kayıtlı tüm çalışanları görmek için
                            for x in coll.find():
                                print(x)
                            break

                        else:
                            print("lütfen 1 ya da 2 girin")

                if id == "hayır":                                                          #id görüntülenmek istenmiyorsa
                    while True:
                        result = input("ada göre arama yapmak istiyorsanız 1 \nkayıtlı tüm çalışanları görmek istiyorsanız 2 \nyazın ")
                        if result == "1":
                            while True:
                                name = input("bilgilerini görmek istediğiniz çalışanın adını girin: ")
                                myquery = {"name": name}
                                y = list(coll.find(myquery))
                                if len(y) == 0:
                                    print("yanlış ad girdiniz")
                                else:
                                    for x in coll.find(myquery,{"_id":0}):
                                        print(x)
                                    break
                            break
                        elif result == "2":                                                   #kayıtlı tümçalışanları görmek için
                            for x in coll.find({},{"_id":0}):
                                print(x)
                            break

                        else:
                            print("lütfen 1 ya da 2 girin")


        elif operation == "3":                                                  #op 3 = çalışan silme: belirli ada sahip herkes / belirli ada sahip \
                                                                                                  # ilk eklenmiş çalışan or belirli ID'ye sahip olanı
            y = list(coll.find())                                               #db boşsa
            if len(y) == 0:
                print("hiç çalışan yok")
            else:
                while True:
                    result = input("     belirli ada sahip tüm çalışanları silmek için 1 \n \
                    belirli ada sahip ilk eklenmiş çalışanı silmek için 2 \n \
                         yazın: ")
                    if result == "1":
                        while True:
                            name = input("silmek istediğiniz çalışanın adını girin: ")
                            myquery = {"name": name}
                            y = list(coll.find(myquery))                             #db de bu adlı biri yoksa
                            if len(y) == 0:
                                print("hatalı ad girdiniz")

                            else:
                                x = coll.delete_many(myquery)
                                print(x.deleted_count,"kişi silindi")
                                break
                        break
                    elif result == "2":                                            #belirli ada sahip ilk eklenmiş çalışanı silmek için
                        while True:
                            name = input("silmek istediğiniz çalışanın adını girin: ")
                            myquery = {"name": name}
                            y = list(coll.find(myquery))                           #bu adlı biri db de yoksa
                            if len(y) == 0:
                                print("hatalı ad girdiniz")

                            else:
                                coll.delete_one(myquery)
                                print("silme işlemi başarılı")
                                break
                        break
                    else:
                        print("lütfen 1 ya da 2 giriniz")


        elif operation == "4":                                                      #çalışan sıraladıktan sonra tüm çalışanları gösterme: ID / ada göre
            y = list(coll.find())                                                   #db boşsa
            if len(y) == 0:
                print("hiç çalışan yok")
            else:
                id = pyip.inputMenu(choices=["ID", "ad"], prompt="sıralama işlemi neye göre yapılsın?\n")
                if id == "ID":
                    mydoc = coll.find().sort("_id")                                #çalışanlar idleri küçükten büyüğe olacak şekilde sıralanır
                    print("çalışanlar :")
                    for x in mydoc:
                        print(x)

                elif id == "ad":                                                   #çalışanlar adları alfabetik sırada olacak şekilde sıralanır
                    mydoc = coll.find().sort("name")
                    print("çalışanlar :")
                    for x in mydoc:
                        print(x)


        elif operation == "5":                                                     #uygulamadan çıkmak için
            print("uygulama kapatılıyor")
            break


        else:
            print("lütfen 1,2,3,4 ve 5 rakamlarından birini girin")



                                                                                   #uygulama fonkunmuzu çağıralım
actions(prompt="\n     Çalışan eklemek için 1 \n \
    Çalışanların bilgilerini sorgulamak için 2 \n \
    Çalışan silmek için 3 \n \
    Çalışanları sıralayıp tüm çalışanları görmek için 4 \n \
    Uygulamayı kapatmak için 5 \n     yazın")

