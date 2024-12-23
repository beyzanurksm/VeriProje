import heapq
import bisect
from datetime import datetime

# 1. Müşteri Verilerinin Yönetimini Sağlama(Linked List ile yapıldı)
class Gonderi:
    def __init__(self, gonderi_id, tarih, teslim_durumu, teslim_suresi):
        self.gonderi_id = gonderi_id
        self.tarih = datetime.strptime(tarih, "%Y-%m-%d")
        self.teslim_durumu = teslim_durumu
        self.teslim_suresi = teslim_suresi
        self.sonraki = None

class GonderiYigini:
    def __init__(self):
        self.yigin = []

    def gonderi_ekle(self, gonderi):
        self.yigin.append(gonderi)

    def son_gonderileri_al(self, adet=5):
        if not self.yigin:
            return "Gonderim yigini bos."
        return self.yigin[-adet:]

class Musteri:
    def __init__(self, musteri_id, isim, soyisim):
        self.musteri_id = musteri_id
        self.isim = isim
        self.soyisim = soyisim
        self.gonderim_gecmisi = GonderiYigini()  # Her musteri icin bir yigin olusturduk.

class MusteriYoneticisi:
    def __init__(self):
        self.musteriler = {}

    def musteri_ekle(self, musteri):
        if musteri.musteri_id in self.musteriler:
            return "Bu musteri ID zaten mevcut."
        self.musteriler[musteri.musteri_id] = musteri
        return f"Musteri {musteri.isim} {musteri.soyisim} eklendi."

    def gonderim_gecmisi(self, musteri_id):
        musteri = self.musteriler.get(musteri_id)
        if musteri:
            gecmis = []
            for gonderi in reversed(musteri.gonderim_gecmisi.yigin):
                gecmis.append({
                    "Gonderi ID": gonderi.gonderi_id,
                    "Tarih": gonderi.tarih.strftime("%Y-%m-%d"),
                    "Teslim Durumu": gonderi.teslim_durumu,
                    "Teslim Suresi": gonderi.teslim_suresi
                })
            return gecmis if gecmis else "Gonderim gecmisi bos."
        return "Musteri bulunamadi."

# 2. Kargo Onceliklendirme (Priority Queue ile yapıldı.)
class OncelikliGonderi:
    def __init__(self):
        self.oncelik_sirasi = []  # Gonderiler heap olarak saklanacak

    def gonderi_ekle(self, gonderi_id, teslim_suresi, durum):
        heapq.heappush(self.oncelik_sirasi, (teslim_suresi, gonderi_id, durum))

    def gonderi_isle(self):
        if self.oncelik_sirasi:
            return heapq.heappop(self.oncelik_sirasi)
        return "Islenecek gonderi yok"

# 3. Kargo Rotalama (Ağaç yapısını kullanma)
class SehirDugumu:
    def __init__(self, sehir_adi, sehir_id, teslimat_suresi):
        self.sehir_adi = sehir_adi
        self.sehir_id = sehir_id
        self.teslimat_suresi = teslimat_suresi 
        self.alt_sehirler = []

    def alt_sehir_ekle(self, sehir_dugumu):
        self.alt_sehirler.append(sehir_dugumu)

class TeslimatAgaci:
    def __init__(self):
        self.kok = None

    def kok_ayarla(self, sehir_dugumu):
        self.kok = sehir_dugumu

    def agacin_gorunumu(self, dugum=None, seviye=0):
        if dugum is None:
            dugum = self.kok
        if dugum:
            print(" " * seviye * 4 + f"{dugum.sehir_adi} (ID: {dugum.sehir_id}, Teslimat Suresi: {dugum.teslimat_suresi} saat)")
            for alt_sehir in dugum.alt_sehirler:
                self.agacin_gorunumu(alt_sehir, seviye + 1)
        else:
            print("Agacta goruntulenecek veri yok.")

    def alt_sehir_ekle(self, ust_sehir_id, alt_sehir_adi, alt_sehir_id, teslimat_suresi):
        def dugum_bul(dugum, sehir_id):
            if dugum.sehir_id == sehir_id:
                return dugum
            for alt_sehir in dugum.alt_sehirler:
                bulunan = dugum_bul(alt_sehir, sehir_id)
                if bulunan:
                    return bulunan
            return None

        ust_sehir = dugum_bul(self.kok, ust_sehir_id)
        if ust_sehir:
            yeni_sehir = SehirDugumu(alt_sehir_adi, alt_sehir_id, teslimat_suresi)
            ust_sehir.alt_sehir_ekle(yeni_sehir)
            print(f"{alt_sehir_adi} sehri, {ust_sehir.sehir_adi} sehrine alt sehir olarak eklendi.")
        else:
            print("Hata: Ust sehir bulunamadi.")

# 4. Kargo Durum Sorgulama 
class TeslimEdilenGonderiler:
    def __init__(self):
        self.teslim_edilenler = []

    def teslim_edilen_ekle(self, gonderi_id):
        if gonderi_id not in self.teslim_edilenler:
            bisect.insort(self.teslim_edilenler, gonderi_id)

    def gonderi_bul(self, gonderi_id):
        indeks = bisect.bisect_left(self.teslim_edilenler, gonderi_id)
        if indeks < len(self.teslim_edilenler) and self.teslim_edilenler[indeks] == gonderi_id:
            return f"Gonderi {gonderi_id} bulundu. Durum: Teslim Edildi."
        return f"Gonderi {gonderi_id} Teslim Edilmedi."

class TeslimEdilmeyenGonderiler:
    def __init__(self):
        self.teslim_edilmeyenler = []

    def teslim_edilmeyen_ekle(self, gonderi):
        self.teslim_edilmeyenler.append(gonderi)

    def merge_sort(self, liste):
        if len(liste) <= 1:
            return liste

        orta = len(liste) // 2
        sol = self.merge_sort(liste[:orta])
        sag = self.merge_sort(liste[orta:])

        return self.merge(sol, sag)

    def merge(self, sol, sag):
        sonuc = []
        i = j = 0

        while i < len(sol) and j < len(sag):
            if sol[i].teslim_suresi <= sag[j].teslim_suresi:
                sonuc.append(sol[i])
                i += 1
            else:
                sonuc.append(sag[j])
                j += 1

        sonuc.extend(sol[i:])
        sonuc.extend(sag[j:])
        return sonuc

    def siralama(self):
        self.teslim_edilmeyenler = self.merge_sort(self.teslim_edilmeyenler)

    def teslim_edilmeyenleri_goster(self):
        if not self.teslim_edilmeyenler:
            print("Teslim edilmemis gonderi bulunmuyor.")
        for gonderi in self.teslim_edilmeyenler:
            print(vars(gonderi))

# Ornek veri ile agacin baslatilmasi
def ornek_teslimat_agaci_olustur():
    kok = SehirDugumu("Merkez", 1, 0)
    teslimat_agaci = TeslimatAgaci()
    teslimat_agaci.kok_ayarla(kok)

    teslimat_agaci.alt_sehir_ekle(1, "Sehir A", 2, 3)
    teslimat_agaci.alt_sehir_ekle(1, "Sehir B", 3, 5)
    teslimat_agaci.alt_sehir_ekle(2, "Sehir C", 4, 2)
    teslimat_agaci.alt_sehir_ekle(2, "Sehir D", 5, 4)
    teslimat_agaci.alt_sehir_ekle(3, "Sehir E", 6, 1)

    return teslimat_agaci

# Test Senaryolarini uygulama (Ayrı bir şekilde atmak yerine koda ekledik)
def test_senaryolari():
    print("\n--- Test Senaryolari ---")

    # 1. Musteri Ekleme Testi
    musteri_yoneticisi = MusteriYoneticisi()
    musteri1 = Musteri(1, "Beyza", "Kara")
    musteri2 = Musteri(2, "Ramiz", "Gok")
    print(musteri_yoneticisi.musteri_ekle(musteri1))
    print(musteri_yoneticisi.musteri_ekle(musteri2))

    # 2. Gonderi Ekleme ve Durum Testi
    gonderi1 = Gonderi(101, "2024-01-11", "Teslim Edildi", 3)
    musteri1.gonderim_gecmisi.gonderi_ekle(gonderi1)
    print(musteri_yoneticisi.gonderim_gecmisi(1))

    # 3. Oncelikli Gonderi Islemleri
    oncelikli_gonderi = OncelikliGonderi()
    oncelikli_gonderi.gonderi_ekle(101, 3, "Teslim Edildi")
    print(oncelikli_gonderi.gonderi_isle())

    # 4. Teslimat Agaci Testi
    teslimat_agaci = ornek_teslimat_agaci_olustur()
    teslimat_agaci.agacin_gorunumu()

    # 5. Teslim Durumu Sorgulama
    teslim_edilenler = TeslimEdilenGonderiler()
    teslim_edilenler.teslim_edilen_ekle(101)
    print(teslim_edilenler.gonderi_bul(101))
    print(teslim_edilenler.gonderi_bul(102))

# Kullanici Menu Arayuzu
def ana_menu():
    musteri_yoneticisi = MusteriYoneticisi()
    oncelikli_gonderi = OncelikliGonderi()
    teslimat_agaci = ornek_teslimat_agaci_olustur()
    teslim_edilenler = TeslimEdilenGonderiler()
    teslim_edilmeyenler = TeslimEdilmeyenGonderiler()

    while True:
        print("\n--- Kargo Yonetim Sistemi ---")
        print("1. Yeni musteri ekle.")
        print("2. Kargo gonderimi ekle.")
        print("3. Kargo durumu sorgula.")
        print("4. Gonderim gecmisini goruntule.")
        print("5. Tum kargolari listele (siramali).")
        print("6. Teslimat rotalarini goster.")
        print("7. Test senaryolarini goster.")
        print("0. Cikis.")

        secim = input("Seciminizi yapin: ")

        if secim == "0":
            print("Programdan cikiliyor...")
            break

        elif secim == "1":
            musteri_id = int(input("Musteri ID: "))
            isim = input("Isim: ")
            soyisim = input("Soyisim: ")
            musteri = Musteri(musteri_id, isim, soyisim)
            print(musteri_yoneticisi.musteri_ekle(musteri))

        elif secim == "2":
            musteri_id = int(input("Gonderim yapmak istediginiz musteri ID'si: "))
            gonderi_id = int(input("Gonderi ID: "))
            tarih = input("Tarih (YYYY-MM-DD): ")
            teslim_durumu = input("Teslim Durumu (Teslim Edildi/Teslim Edilmedi): ")
            teslim_suresi = int(input("Teslim Suresi (gun): "))

            gonderi = Gonderi(gonderi_id, tarih, teslim_durumu, teslim_suresi)
            musteri = musteri_yoneticisi.musteriler.get(musteri_id)
            if musteri:
                musteri.gonderim_gecmisi.gonderi_ekle(gonderi)
                oncelikli_gonderi.gonderi_ekle(gonderi_id, teslim_suresi, teslim_durumu)
                if teslim_durumu == "Teslim Edildi":
                    teslim_edilenler.teslim_edilen_ekle(gonderi_id)
                else:
                    teslim_edilmeyenler.teslim_edilmeyen_ekle(gonderi)
                print("Gonderim basariyla eklendi.")
            else:
                print("Hata: Musteri bulunamadi.")

        elif secim == "3":
            gonderi_id = int(input("Kargo ID'sini girin: "))
            print(teslim_edilenler.gonderi_bul(gonderi_id))

        elif secim == "4":
            musteri_id = int(input("Musteri ID'sini girin: "))
            gecmis = musteri_yoneticisi.gonderim_gecmisi(musteri_id)
            if isinstance(gecmis, list):
                print("Gonderim Gecmisi:")
                for kayit in gecmis:
                    print(kayit)
            else:
                print(gecmis)

        elif secim == "5":
            print("Teslim Edilmis Kargolar:")
            print(teslim_edilenler.teslim_edilenler)

            print("Teslim Edilmemis Kargolar (Teslim Suresine Gore):")
            teslim_edilmeyenler.siralama()
            teslim_edilmeyenler.teslim_edilmeyenleri_goster()

        elif secim == "6":
            print("\n--- Teslimat Rotasi ---")
            teslimat_agaci.agacin_gorunumu()

        elif secim == "7":
            test_senaryolari()

if __name__ == "__main__":
    ana_menu()

