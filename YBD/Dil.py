
Rakamlar = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")
Alfabe = tuple(
"abcçdefgğhıijklmnoöprsştuüvyzqxwABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZXQW")
Matematiksel = ("\t", " ", "+", "-", "*", "/", ".", "(", ")")+Rakamlar
Mantiksal = ("==", "<", ">", "&", "|", "!", " ", "=>", ">=", "<=",
"=<", "ve", "veya", "ya da", "Dogru", "Doğru", "Yanlis", "Yanlış")
Dil_Alfabesi = Alfabe+Matematiksel+Mantiksal
mod = 0
debug = False
high_debug = False
# ====================================================================

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
		liste=[].append(metin)
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
	
def degistir(liste, oge1, oge2):
	if oge1 in liste:
		x = liste.index(oge1)
		if not isinstance(oge2, list):
			liste[x] = oge2
		else:
			for i, oge in enumerate(oge2):
				if i == 0:
					liste[x] = oge
				else:
					liste.insert(x+i, oge)
# ====================================================================

class Hata(Exception):
	mesaj = "Bir hata oluştu"
	def __init__(self):
		pass
	def __repr__(self):
		return f"HATA:{self.mesaj}"

class GecersizDegiskenİsmi(Hata):
	mesaj = "Yanlış değişken ismi."
	def __init__(self):
		super().__init__()

class DegiskenHarfleBaslar(GecersizDegiskenİsmi):
	mesaj = "Değişken ismi bir harfle başlamalıdır."

class DegiskenAdindaOzelKarakter(GecersizDegiskenİsmi):
	mesaj = "Değişken ismi ozel karakter içermemelidir."

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
# ====================================================================
class Islem:
	def __init__(self, islem_liste:list):
		self.liste=islem_liste
		self.duzenlenmis=False

	def __repr__(self):
		return f"I|({self.duzenlenmis}){self.liste}|" if high_debug else f"I|{self.liste}|"

	def __str__(self):
		return self.__repr__()

class Sayi:
	def __init__(self, deger):
		if isinstance(deger, int):
			self.deger = deger
			self.cins="Tam sayı"
		elif isinstance(deger, str):
			if int(float(deger)) == float(deger):
				self.deger = int(deger)
				self.cins="Tam sayı"
			else:
				self.deger = float(deger)
				self.cins="Ondalıklı sayı"
		elif isinstance(deger, float):
			self.deger = float(deger)
			self.cins="Ondalıklı sayı"

	def __repr__(self):
		return f"S({self.cins}){self.deger}" if high_debug else f"S[{self.deger}]"

	def __str__(self):
		return self.__repr__()

class Metin:
	def __init__(self, deger):
		self.deger = deger
		self.uzunluk = len(deger)

	def __repr__(self):
		if self.deger[0] == '"' and self.deger[-1] == '"':
			return f"M:{self.deger}"

		else:
			return f'M:"{self.deger}"'

	def __str__(self):
		return self.__repr__()

class Degisken:
	degiskenler = {}

	def __init__(self, isim, deger, cins=None):
		self.isim = isim
		self.deger = deger
		self.cins=cins
		if isinstance(self.deger, Metin):
			self.deger = self.deger.deger
			self.cins = "Yazısal"
		elif isinstance(self.deger, int):
			self.cins = "Sayısal"

		if self.cins:
			self.cins = cins

		Degisken.degiskenler.update({self.isim: self})

	def __repr__(self):
		if not self.cins:
			return f"Degisken:<{self.isim}:{self.deger}>" if high_debug else f"<{self.isim}:{self.deger}>"
		return f"{self.cins}:<{self.isim}:{self.deger}>" if high_debug else f"<{self.isim}:{self.deger}>"

	def __str__(self):
		return self.__repr__()
# ====================================================================
 
def listelestir(girdi:str|list): 
	girdi_liste=[]
	if isinstance(girdi,str):
		if"#"in girdi:
			girdi = girdi[:girdi.index("#")]

		if '"' in girdi:
			x2=0
			Metinler={}
			i=0
			while x2 < len(girdi):
				x2=girdi.find('"',x2)+1 if girdi.find('"',x2)+1!=len(girdi) else KapanmayanTirnak
				if x2==KapanmayanTirnak :raise KapanmayanTirnak
				if x2==0:break
				metin=[]
				while x2<len(girdi) and girdi[x2]!='"':
					metin.append(girdi[x2])
					x2+=1
				if x2==len(girdi):
					raise KapanmayanTirnak
				metin=Metin("".join(metin))
				Metinler.update({metin:x2-(metin.uzunluk+1)})
				if i==0:
					girdi_liste.append(girdi[:Metinler[metin]])
					girdi_liste.append(metin)
				else:
					girdi_liste.append(girdi[list(Metinler.values())[i-1]+list(Metinler.keys())[i-1].uzunluk+2:Metinler[metin]])
					girdi_liste.append(metin)
					if (i+1)*2 == girdi.count('"') and x2!=len(girdi)-1:
						girdi_liste.append(girdi[x2+1:])
				i+=1
				x2+=1
			for bolum in girdi_liste.copy():
				if isinstance(bolum,str):
					if " " in bolum or "\t" in bolum:
						degistir(girdi_liste,bolum,ayir(bolum))
		else:
			girdi_liste=ayir(girdi)
	elif isinstance(girdi,list):
		girdi_liste=girdi
	cikti_liste=[]

	if any(["=" in bolum for bolum in girdi_liste if not isinstance(bolum,Metin)]):
			x2=girdi_liste.index('=')
			cikti_liste.append(Degisken(girdi_liste[:x2][0],listelestir(girdi_liste[x2+1:])))
	
	else:
		for bolum in girdi_liste:
			i=0
			geciciliste=[]
			if isinstance(bolum,Metin):
				cikti_liste.append(bolum)
				continue

			while i<len(bolum):
				if bolum[i] in Rakamlar and bolum[i]!=".":
					sayi=[]
					while i<len(bolum) and bolum[i] in Rakamlar:
						sayi.append(bolum[i])
						i+=1
					sayi=Sayi("".join(sayi))
					geciciliste.append(sayi)
					if i==len(bolum):
						break

				
				
				#TODO İşlemler için İşlem class'ı yap
				if bolum[i] in "+-/*":
					pass

				i+=1
			if not geciciliste:
				cikti_liste.append(bolum)
			else:
				cikti_liste.extend(geciciliste)
	return cikti_liste


def calistir(girdi:list):
	try:
		cikti = None
		# ====================================================================
		#TODO Mantıksal operatörler vs. ekle
		""" if icinde(list(Mantiksal),girdi):
		x=0
		karsilastirma=girdi.split(" \t") """
		# ====================================================================
		#TODO Değişken tespiti ekle
		""" if  Degisken.degiskenler!=dict():
		x=0
		while x<len(girdi): """
		
		# ====================================================================
		if isinstance(girdi[0],Metin) or isinstance(girdi[0],Sayi):
			cikti=girdi[0]

		if any(map(lambda x: isinstance(x,Degisken),girdi)):
			degler=list(filter(lambda x:isinstance(x,Degisken),girdi))
			if len(degler)>1:
				raise GecersizDegiskenİsmi
			degler[0].deger=calistir(degler[0].deger)
			cikti=degler[0]
			return cikti
			
			
		# ====================================================================
		if not cikti:
			try:
				cikti = str(eval(girdi))
			except ZeroDivisionError:
				cikti=SifiraBolmeHatasi()
		
			if not isinstance(cikti,Hata) and not isinstance(cikti,Degisken):
				if int(float(cikti)) == float(cikti):
					cikti = str(int(float(cikti)))
	# ====================================================================


	except ZeroDivisionError:
		cikti = SifiraBolmeHatasi()

	except NameError as e:
		for x2, harf1 in enumerate(girdi):
			if not harf1 in Matematiksel:
				isim = []
				while x2 < len(girdi) and not girdi[x2] in set(Matematiksel)-set(Rakamlar):
					isim.append(girdi[x2])
					x2 += 1
				isim = "".join(isim)
				if isim in Degisken.degiskenler.keys():
					deg = Degisken.degiskenler[isim]
					if isinstance(deg.deger, Metin):
						cikti = deg.deger
					else:
						girdi = girdi.replace(
						isim, Degisken.degiskenler[isim].deger)
						try:
							cikti = calistir(girdi)
						except Exception as e:
							raise e
						break
				else:
					cikti = BilinmeyenDegisken()

					raise cikti

	except SyntaxError:
		cikti = "Geçersiz söz dizimi"

	except Hata as e:
		cikti = e

	except Exception as e:
		cikti = e
		raise e

	finally:
		return cikti


# =====================================
if __name__ == "__main__":
	if mod == 1:
		while True:
			girdi = input("gir>>>>")
			cikti = calistir(girdi)
			print(cikti)

	elif mod == 0:
		try:
			with open("dosya.txt", "r") as f:
				liste = list(map(lambda x: x.strip("\n \t"), f.readlines()))

			for sira, satir in enumerate(liste):
				if satir == "" or satir.strip(" \t")[0] == "#":
					continue

				if "eger" in satir or "eğer" in satir:
					x = 0
					pass

				cikti = calistir(satir)
				if isinstance(cikti,Exception):
					if isinstance(cikti,Hata):
						print(f'!!!!! HATA !!!!!\n{cikti.mesaj}')
						break
					else:
						print(f'!!!!! HATA !!!!!\n{cikti}')
						raise cikti

				if not debug:
					if not isinstance(cikti, Degisken):
						print(cikti)
				else:
					print(f"{sira+1}) {cikti}")

		except FileNotFoundError:
			print("Belirtilen dosya bulunamadı")

		except Exception as e:
			print(e)

	print("\nProgram sona erdi.")