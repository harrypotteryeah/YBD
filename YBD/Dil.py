
RAKAMLAR = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
ALFABE = list("abcçdefgğhıijklmnoöprsştuüvyzqxwABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZXQW")
MATEMATIKSEL = ["\t", " ", "+", "-", "*", "/", ".", "(", ")"]+RAKAMLAR
MANTIKSAL = ["==", "<", ">", "&", "|", "!", " ", "=>", ">=", "<=","=<",
	      "ve", "veya", "ya da", "Dogru", "Doğru", "Yanlis", "Yanlış"]
if __name__=="__main__":
	INPUT_MODE = 1

DEBUG = True
# ====================================================================
def arasinda(num:int|float,liste):
	if not bool(liste):
		return False
	for i,min in [x[0] for x in liste]:
		if num == min or (num>min and num<=liste[i][1]):
			return True
	return False

def icinde(list1:str|list, list2:str|list):
	if isinstance(list1, list) and isinstance(list2, list):
		for i in list1:
			if i in list2:
				return True

	elif isinstance(list1, str) and isinstance(list2, list):
		for i in list2:
			if i in list1:
				return True

	elif isinstance(list2, str) and isinstance(list1, list):
		for i in list1:
			if i in list2:
				return True
	elif isinstance(list2, str) and isinstance(list1, str):
		for i in list1:
			if i in list2:
				return True
	else:
		return -1

	return False

def ayir(metin:str,ayraclar:str|list=" \t"):
	if not icinde(ayraclar, metin):
		liste=[metin]
		return liste
	else:
		metin=metin.strip(ayraclar).split(ayraclar[0])
		for ayrac in ayraclar[1:]:
			k_metin=metin.copy()
			for bolum in k_metin:
				if ayrac in bolum and bolum!="" and bolum!=ayrac:
					degistir(metin, bolum, bolum.strip(ayrac).split(ayrac))
				elif bolum=="" or bolum==ayrac:
					metin.remove(bolum)
		return metin
	
def degistir(liste:list, gidecek, gelecek):
	if isinstance(gidecek, list) and icinde(gidecek,liste):
		i=0
		while i<=len(liste):
			if len(liste)==i:
				raise BulunamayanOge
			
			if liste[i]==gidecek[0]:
				x = 0
				while i <=len(liste):
					if i==len(liste):
						raise BulunamayanOge
					
					if x==len(gidecek):
						for _ in range(len(gidecek)):
							liste.pop(i-x)
						if isinstance(gelecek,list):
							for oge in gelecek[::-1]:
								liste.insert(i-x,oge)
						else:
							liste.insert(i-x,gelecek)
						
						return liste

					if  liste[i]!=gidecek[x]:
						i-=1
						break

					x,i=x+1,i+1
			i+=1
		else:
			raise BulunamayanOge
				
	else:
		if gidecek in liste:
			x = liste.index(gidecek)
			if not isinstance(gelecek, list):
				liste[x] = gelecek
			else:
				for i, oge in enumerate(gelecek):
					if i == 0:
						liste[x] = oge
					else:
						liste.insert(x+i, oge)
# ====================================================================

class Hata(Exception):
	mesaj = "Bir hata oluştu"
	def __repr__(cls):
		return cls.mesaj
	def __str__(cls):
		return cls.__repr__()

class GecersizDegiskenİsmi(Hata):
	mesaj = "Yanlış değişken ismi."

class DegiskenHarfleBaslar(Hata):
	mesaj = "Değişken ismi bir harfle başlamalıdır."

class DegiskenAdindaOzelKarakter(Hata):
	mesaj = "Değişken ismi alfabedeki harfler ve alt çizgi(_) dışında karakter içermemelidir."

class BilinmeyenDegisken(Hata):
	mesaj = "Bilinmeyen değişken ismi"

class SifiraBolmeHatasi(Hata):
	mesaj="Sıfırla bölünemez"

class GecersizSozDizimi(Hata):
	mesaj="Geçersiz söz dizimi"

class KapanmayanTirnak(Hata):
	mesaj="Tırnak işareti kapanmamış" 

class KapanmayanParantez(Hata):
	mesaj="Parantez işareti kapanmamış"

class BulunamayanOge(Hata):
	mesaj="Bulunamayan öge"
# ====================================================================
class Islem:
	def __init__(self, islem_liste:list):
		self.liste=islem_liste
		self.duzenlenmis=False
	
	def duzenle(self):
		#TODO duzenle fonksyonu ekle
		pass
	
	def __repr__(self):
		return f"I|({self.duzenlenmis}){self.liste}|" if DEBUG else f"I|{self.liste}|"

	def __str__(self):
		return self.__repr__()

class Sayi:
	def __init__(self, deger):
		if isinstance(deger, int):
			self.deger = deger
		elif isinstance(deger, str):
			if int(float(deger)) == float(deger):
				self.deger = int(deger)
			else:
				self.deger = float(deger)
		elif isinstance(deger, float):
			self.deger = float(deger)

	def __repr__(self):
		return f"Sayi({self.deger})" if DEBUG else f"S_{self.deger}"

	def __str__(self):
		return self.__repr__()

class Metin:
	def __init__(self, deger):
		self.deger = deger
		if self.deger[0]=='"' and self.deger[-1] == '"':
			self.uzunluk=len(self.deger)-2
		else:
			self.uzunluk = len(deger)
			self.deger=f'"{self.deger}"'

	def __repr__(self):
		return f"Metin({self.deger})" if DEBUG else f"M_{self.deger}"

	def __str__(self):
		return self.__repr__()
	
	@classmethod
	def Metin_Bul(cls,girdi:str) ->dict:
		if not '"' in girdi:
			return {}
		Metinler={}
		x2=0
		while x2 < len(girdi):
			x2=girdi.find('"',x2)+1 if girdi.find('"',x2)+1!=len(girdi) else KapanmayanTirnak# " işaretinin olduğu yere gidiyor
			if x2==KapanmayanTirnak :raise KapanmayanTirnak
			if x2==0:break
			metin=[]
			while x2<len(girdi) and girdi[x2]!='"':
				metin.append(girdi[x2])
				x2+=1

			if x2==len(girdi):
				raise KapanmayanTirnak
			metin=Metin("".join(metin))
			Metinler.update({metin:[x2-(metin.uzunluk+1),x2]})
			x2+=1
		return Metinler

class Degisken:
	degiskenler = {}

	def __init__(self, isim, deger):
		self.isim = isim
		self.deger = deger
		self.halledildi=False
		if isinstance(self.deger, Metin):
			self.deger = self.deger.deger
		Degisken.degiskenler.update({self.isim: self})

	def __repr__(self):
		return f"Degisken({self.isim}: {self.deger} )" if DEBUG else f"<{self.isim}:{self.deger}>"

	def __str__(self):
		return self.__repr__()
# ====================================================================
class Enum(type):
	rpr=""
	def __repr__(cls):
		return cls.rpr
	def __str__(cls):
		return cls.__repr__()

class BOSLUK(metaclass=Enum):rpr="BOŞLUK" if DEBUG else '" "'

class TAB(metaclass=Enum):rpr="TAB" if DEBUG else '"/t"'

# ====================================================================
def listelestir(girdi:str,Metinler:dict | None =None) -> list:
	if girdi=="":
		raise ValueError
	
	if not Metinler:
		Metinler=Metin.Metin_Bul(girdi)
	
	if "#" in girdi and not arasinda(girdi.find("#"),Metinler.values):
		girdi=girdi[:girdi.find("#")]
	
	cikti_liste=[]
	i=-1
	while i<=len(girdi):
		i+=1
		if i==len(girdi):
			break

		if girdi[i]=='"':
			if not i in [x[0] for x in Metinler.values()]:
				raise UserWarning
			
			for i1,index in enumerate(Metinler.values()):#Metinler={Metin:[baştaki ", sondaki "]}
				if i==index[0]:
					cikti_liste.append(list(Metinler.keys())[i1])
					i=index[1]+1
					break
			else:
				continue

		if i==len(girdi):
			break

		if girdi[i]== "=" and i!=len(girdi)-1:
			if len(cikti_liste)==0:
				raise GecersizSozDizimi
			
			if len(cikti_liste)==1 and not isinstance(cikti_liste[0],str):
				raise GecersizSozDizimi
			
			x=cikti_liste.copy()[::-1]
			deg_adi=[]
			i1=0
			while x[i1] in(BOSLUK,TAB) and i1<len(cikti_liste):
					i1+=1

			if i1==len(cikti_liste):
				raise GecersizSozDizimi
			i1-=1
			while i1<len(cikti_liste):
				i1+=1
				if i1==len(cikti_liste) or x[i1] in (BOSLUK,TAB):
					break
				
				if isinstance(x[i1],str):
					deg_adi.append(x[i1])

				elif isinstance(x[i1],Sayi):
					if i1 ==len(x)-1:
						raise DegiskenHarfleBaslar
					
					if x[i1+1] in (BOSLUK,TAB):
						raise GecersizSozDizimi
					
					if isinstance(x[i1].deger,float):
						raise DegiskenAdindaOzelKarakter
					deg_adi.append(x[i1])
				else:
					raise TypeError("Değişken adı için geçersiz type")
			deg_adi.reverse()
			for i1,x in enumerate(deg_adi):
				if isinstance(x,Sayi):
					deg_adi[i1]=str(x.deger)
			deg_adi="".join(deg_adi)
			if not all(map(lambda x:x in [i1 for i1 in RAKAMLAR if i1!="."]+ALFABE+["_"],deg_adi)):#ALFABE+RAKAMLAR+"_" - "."
				return DegiskenAdindaOzelKarakter
			deg_deger=listelestir(girdi[i+1:])
			for i1,n in enumerate(deg_deger):
				if n in (BOSLUK,TAB):
					deg_deger.pop(i1)
				else:
					break
			cikti_liste=[Degisken(deg_adi,deg_deger)]
			break
			
			
			
		if girdi[i] in RAKAMLAR and girdi[i]!=".":
			sayi=[]
			nokta=0
			while i<len(girdi) and girdi[i] in RAKAMLAR:
				if girdi[i]==".": 
					nokta+=1
				if nokta>1: break
				sayi.append(girdi[i])
				i+=1
			if sayi[-1]==".":sayi.pop(-1);i-=1

			sayi=Sayi("".join(sayi))
			cikti_liste.append(sayi)
			if i==len(girdi):
				break
			i-=1
			continue

		if girdi[i]==" ":
			cikti_liste.append(BOSLUK)
			continue

		if girdi[i]=="\t":
			cikti_liste.append(TAB)
			continue
		
		if i==0 or not isinstance(cikti_liste[-1],str):
			cikti_liste.append(girdi[i])
		else:
			cikti_liste[-1]=cikti_liste[-1]+girdi[i]


	return cikti_liste


def cozumle(girdi:list):
	pass

def calistir(girdi:list | str):
	if isinstance(girdi,str):
		if girdi == "" or girdi.strip(" \t")[0] == "#":
			raise ValueError
		Metinler=Metin.Metin_Bul(girdi)
		if "#" in girdi and not arasinda(girdi.find("#"),Metinler.values):
			girdi=girdi[:girdi.find("#")]
		
		try:
			listelestir_cikti=listelestir(girdi)

		except Exception as exc:
			raise exc
		
		try:
			calistir_cikti=cozumle(listelestir_cikti)

		except Exception as exc:
			raise exc
		
		return [calistir_cikti,listelestir_cikti] if DEBUG else [calistir_cikti]
	
	cikti_liste=[]
	for sira, satir in enumerate(girdi):
		if satir == "" or satir.strip(" \t")[0] == "#":
			continue

		Metinler=Metin.Metin_Bul(satir)

		if "#" in satir and not arasinda(satir.find("#"),Metinler.values):
			satir=satir[:satir.find("#")]

		if ("eger" in satir and not arasinda(satir.find("eger"),Metinler.values)) or ("eğer" in satir and not arasinda(satir.find("eğer"),Metinler.values)):
			pass

		try:
			listelestir_cikti=listelestir(girdi)

		except Exception as exc:
			raise exc
		
		try:
			calistir_cikti=cozumle(listelestir_cikti)

		except Exception as exc:
			raise exc
		
		cikti_liste.append([sira+1,calistir_cikti] if not DEBUG else [sira+1,calistir_cikti,listelestir_cikti])
# =====================================
if __name__ == "__main__":
	if INPUT_MODE == 1:
		while True:
			girdi = input("kod_gir >>")
			cikti = calistir(girdi)
			print(cikti)
			

	elif INPUT_MODE == 0:
		try:
			with open("dosya.txt", "r") as f:
				liste = list(map(lambda x: x.strip("\n \t"), f.readlines()))
			cikti = calistir(liste)

		except FileNotFoundError:
			print("Belirtilen dosya bulunamadı")

		except Exception as e:
			print(e)

	print(cikti)
	print("\nProgram sona erdi.")