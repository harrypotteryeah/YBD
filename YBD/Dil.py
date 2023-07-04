
RAKAMLAR = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
ALFABE = list("abcçdefgğhıijklmnoöprsştuüvyzqxwABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZXQW")
Operatorler = ["+", "-", "*", "/", "%","**"]#Sonradan Dict'e çevriliyor {"+" : ARTI, "-" : EKSI, ... }
MANTIKSAL = ["==", "<", ">", "&", "|", "!", " ", "=>", ">=", "<=","=<",
	      "ve", "veya", "ya da", "Dogru", "Doğru", "Yanlis", "Yanlış"]

if __name__=="__main__":
	INPUT_MODE = 1

DEBUG = False
# ====================================================================
def arasinda(num:int|float,liste):
	if not bool(liste):
		return False
	for i,min in [x[0] for x in liste]:
		if num == min or (num>min and num<=liste[i][1]):
			return True
	return False

def icinde(liste:str|list|tuple, karakterler):
	if isinstance(karakterler, (list,str,tuple,type({}.values()))):
		for i in karakterler:
			if i in liste:
				return True
	else:
		raise ValueError

	return False

def ayir(metin:str,ayraclar:str|list=" \t"):
	if not icinde(metin, ayraclar):
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
	
def degistir(liste:list, degistirlecek:list|object, konulacak:list|object):
	if isinstance(degistirlecek, list) and icinde(liste,degistirlecek):
		if liste==degistirlecek:
			if isinstance(konulacak,list):
				liste.clear()
				liste.extend(konulacak)
			else:
				liste.clear()
				liste.append(konulacak)
			return liste
		i=0
		while i<=len(liste):
			if len(liste)==i:
				raise BulunamayanOge
			
			if liste[i]==degistirlecek[0]:
				x = 0
				while i <=len(liste):
					
					if x==len(degistirlecek):
						for _ in range(len(degistirlecek)):
							liste.pop(i-x)
						if isinstance(konulacak,list):
							for oge in konulacak[::-1]:
								liste.insert(i-x,oge)
						else:
							liste.insert(i-x,konulacak)
						
						return liste
					
					if i==len(liste):
						raise BulunamayanOge

					if  liste[i]!=degistirlecek[x]:
						i-=1
						break

					x,i=x+1,i+1
			i+=1
		else:
			raise BulunamayanOge
				
	else:
		if degistirlecek in liste:
			x = liste.index(degistirlecek)
			if not isinstance(konulacak, list):
				liste[x] = konulacak
			else:
				for i, oge in enumerate(konulacak):
					if i == 0:
						liste[x] = oge
					else:
						liste.insert(x+i, oge)
# ====================================================================
#region Hatalar
class Hata(Exception):
	mesaj = "Bir hata oluştu"
	f'''
	{mesaj}
	'''
	def __repr__(cls):
		return cls.mesaj
	def __str__(cls):
		return cls.__repr__()

class GecersizDegiskenİsmi(Hata):
	mesaj = "Yanlış değişken ismi."

class DegiskenAdiHarfleBaslar(Hata):
	mesaj = "Değişken ismi bir harfle başlamalıdır."

class DegiskenAdindaOzelKarakter(Hata):
	mesaj = "Değişken ismi harf, sayı ve alt çizgi(_) dışında karakter içermemelidir."

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

class GecersizIslem(Hata):
	mesaj="Veri tipleri arasında geçersiz işlem."
	def __init__(self,tip1:type,tip2:type,operasyon:str) -> None:
		self.mesaj=f"'{tip1}' ve {tip2} veri tipleri arasında geçersiz {operasyon} işlemi."
#endregion
# ====================================================================
class Islem:
	def __init__(self, ilk_oge,ikinci_oge,operator):
		self.ilk_oge=ilk_oge
		self.ikinci_oge=ikinci_oge
		self.operator=operator
	
	def __repr__(self):
		return f"Islem[{repr(self.ilk_oge)} {repr(self.operator)} {repr(self.ikinci_oge)}]" if DEBUG else f"I[{repr(self.ilk_oge)} {repr(self.operator)} {repr(self.ikinci_oge)}]"

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
		return str(self.deger)
	
	def topla(self,toplanacak):
		if isinstance(toplanacak,Sayi):
			return Sayi(self.deger+toplanacak.deger)
		
		elif isinstance(toplanacak,Metin):
			return Metin(str(self)+toplanacak.deger)
		
		else:
			return GecersizIslem(Sayi,type(toplanacak),"toplama")

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
		return self.deger.strip('"')
	
	def topla(self,toplanacak):
		if isinstance(toplanacak,Metin):
			return Metin(str(self)+str(toplanacak))
		elif isinstance(toplanacak,Sayi):
			return Metin(str(self)+str(toplanacak))
		else:
			return GecersizIslem(Metin,type(toplanacak),"toplama")
		
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
		return f"Degisken({self.isim} : {self.deger})" if DEBUG else f"< {self.isim} : {self.deger} >"

	def __str__(self):
		return self.__repr__()
	
class Kod_Parcasi:
	def __init__(self,kod:list) -> None:
		self.kod=kod

	def __repr__(self) -> str:
		return f"{self.kod}"
	
	def __str__(self) -> str:
		return self.__repr__()
# ====================================================================
#region Tokenler
class Token:
	def __init__(self,rpr:str) -> None:
		self.rpr=rpr

	def __repr__(self):
		return self.rpr
	
	def __str__(self):
		return self.__repr__()

class OPERATOR(Token):
	def __init__(self, rpr: str, islem:str) -> None:
		self.rpr=rpr
		self.islem=islem


BOSLUK =Token('" "')

TAB =Token('"/t"')

SAG_PARANTEZ=Token(")")

SOL_PARANTEZ=Token("(")

ESITTIR=Token("=")

ARTI=OPERATOR('+',"toplama")

EKSI=OPERATOR('-',"çıkarma")

CARPI=OPERATOR('*',"çarpma")

BOLU=OPERATOR('/',"bölme")

KALAN=OPERATOR('%',"kalanını alma")

KUVVET=OPERATOR("**","kuvvetini alma")

Operatorler={"**":KUVVET, "*":CARPI, "/":BOLU, "%":KALAN, "+":ARTI, "-":EKSI}
#endregion
# ====================================================================
def listelestir(girdi:str,Metinler:dict | None =None) -> list:
	if girdi=="":
		raise ValueError("girdi boş")
	
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

		if girdi[i]== "=":

			if i == len(girdi)-1:
				raise GecersizSozDizimi
			
			if len(cikti_liste)==0:
				raise GecersizSozDizimi
			
			if len(cikti_liste)==1 and not isinstance(cikti_liste[0],str):
				raise GecersizSozDizimi
			
			cikti_liste.append(ESITTIR)
			continue
			
			""" x=cikti_liste.copy()[::-1]
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

				if x[i1] in OPERATORLER.values():
					raise DegiskenAdindaOzelKarakter

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
			if not all(map(lambda x:x in RAKAMLAR+ALFABE+["_"],deg_adi)):#ALFABE+RAKAMLAR+"_"
				return DegiskenAdindaOzelKarakter
			deg_deger=listelestir(girdi[i+1:])
			for i1,n in enumerate(deg_deger):
				if n in (BOSLUK,TAB):
					deg_deger.pop(i1)
				else:
					break
			cikti_liste=[Degisken(deg_adi,deg_deger)]
			break """
			
		if girdi[i] =="(":
			cikti_liste.append(SOL_PARANTEZ)

		if girdi[i]==")":
			cikti_liste.append(SAG_PARANTEZ)

		if girdi[i] in Operatorler.keys():
			if len(cikti_liste)==0:
				raise GecersizSozDizimi
			if girdi[i]=="*" and i<len(girdi)-1 and girdi[i+1]=="*":
				cikti_liste.append(KUVVET)
				i+=1
			else:
				cikti_liste.append(Operatorler[girdi[i]])
			continue

		if girdi[i] in RAKAMLAR and girdi[i]!=".":
			sayi=[]
			nokta=0
			while i<len(girdi) and girdi[i] in RAKAMLAR+["."]:
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

# ====================================================================
def cozumle(girdi:list):
	if len(girdi)==0:
		raise ValueError("girdi boş")
	cikti_liste=[]

	if ESITTIR in girdi:
		i=girdi.index(ESITTIR)
		if i==0 or i==len(girdi)-1:
			raise GecersizSozDizimi
			
		n=i-1
		while girdi[n] in (BOSLUK,TAB):
			if n==0:
				raise GecersizSozDizimi
			n-=1
		deg_adi=[]

		while n>=0 and not girdi[n] in (BOSLUK,TAB):
			if isinstance(girdi[n],Sayi):
				if isinstance(girdi[n].deger,float):
					raise DegiskenAdindaOzelKarakter
				deg_adi.append(girdi[n].deger)

				n-=1

			elif isinstance(girdi[n],str):
				deg_adi.append(girdi[n])

				n-=1

			else:
				raise TypeError(f"Değişken ismi için geçersiz type {girdi[n]}")
			
		if n>0:
			if not all(map(lambda x:x in (BOSLUK,TAB),girdi[0:n])):
				raise GecersizSozDizimi
		
		if not isinstance(deg_adi[-1],str):
			raise DegiskenAdiHarfleBaslar
		for i1,x in enumerate(deg_adi):
			if isinstance(x,int):
				deg_adi[i1]=str(x)
		deg_adi="".join(deg_adi[::-1])
		deg_deger=cozumle(girdi[i+1:])

		if any(map(lambda x: isinstance(x,Degisken),deg_deger)) or all(map(lambda x:x in (BOSLUK,TAB),deg_deger)):
			raise GecersizSozDizimi
		cikti_liste.append(Degisken(deg_adi,Kod_Parcasi(deg_deger)))
		return cikti_liste
	
	girdi = list(filter(lambda x:not x in (BOSLUK,TAB),girdi))
	i=0
	while i <len(girdi):
		if  isinstance(girdi[i],(Metin,Sayi)):
			if i>0 and not isinstance(girdi[i-1],OPERATOR):
				raise GecersizSozDizimi
			cikti_liste.append(girdi[i])
			i+=1

		elif girdi[i] == SOL_PARANTEZ:
			if i>0 and not isinstance(girdi[i-1],OPERATOR):
				raise GecersizSozDizimi
			
			parantez_ici=[]
			while i<len(girdi) and girdi[i]!=SAG_PARANTEZ:
				if i==len(girdi)-1:
					raise KapanmayanParantez
				parantez_ici.append(girdi[i])
				i+=1
			x=cozumle(parantez_ici)
			if isinstance(x[0],Islem):
				cikti_liste.append(x)
			else:
				cikti_liste.append(Kod_Parcasi(x))
			i+=1
		
		elif isinstance(girdi[i],OPERATOR):
			if i==0 or i==len(girdi)-1:
				raise GecersizSozDizimi
			
			cikti_liste.append(girdi[i])
			i+=1
		
		elif isinstance(girdi[i],str):
			raise GecersizSozDizimi
		
		else:
			raise ValueError(f"{type(girdi[i])} cozumlenemiyor")
	
	while icinde(cikti_liste,Operatorler.values()):
		i=0
		for operator in Operatorler.values():
			while operator in cikti_liste:
				i=cikti_liste.index(operator)
				if not operator in (ARTI,EKSI):
					if not isinstance(cikti_liste[i-1],(Sayi,Islem)) or not isinstance(cikti_liste[i+1],(Sayi,Islem)):
						raise GecersizIslem(type(cikti_liste[i-1]),type(cikti_liste[i+1]),operator.islem)
				else:
					if operator==ARTI:
						if not isinstance(cikti_liste[i-1],(Sayi,Islem,Metin)) or not isinstance(cikti_liste[i+1],(Sayi,Islem,Metin)):
							raise GecersizIslem(type(cikti_liste[i-1]),type(cikti_liste[i+1]),operator.islem)
					else:
						if not (isinstance(cikti_liste[i-1],(Sayi,Islem)) and isinstance(cikti_liste[i+1],(Sayi,Islem))) or (isinstance(cikti_liste[i-1],Metin) and isinstance(cikti_liste[i+1],Metin)):
							raise GecersizIslem(type(cikti_liste[i-1]),type(cikti_liste[i+1]),operator.islem)
				degistir(cikti_liste,cikti_liste[i-1:i+2],Islem(cikti_liste[i-1],cikti_liste[i+1],cikti_liste[i]))
	
	return cikti_liste

# ====================================================================
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
			cozumle_cikti=cozumle(listelestir_cikti)

		except Exception as exc:
			raise exc
		
		return [cozumle_cikti,listelestir_cikti] if DEBUG else [cozumle_cikti]
	
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
			cozumle_cikti=cozumle(listelestir_cikti)

		except Exception as exc:
			raise exc
		
		cikti_liste.append([sira+1,cozumle_cikti] if not DEBUG else [sira+1,cozumle_cikti,listelestir_cikti])
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