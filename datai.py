
import sys, json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import traceback

debug = False
definicoes = 'texto.br.json'


class Data:
	frase = None
	with open(definicoes) as f:
		frase = json.load(f)

	ignorar = ['feira']

	def __init__(self):
		data = []
		naodata = []
		depende_de_parametros = []
		datas_falsas = 0

		for dados in sys.argv:
			dados = dados.lower()
			if dados == 'datai.py':
				continue
			try:
				if "/" in dados:
					tmp = dados.split('/')
					if self.data_valida(tmp) == False:
						datas_falsas += 1
						if debug == True:
							print(f"A data {tmp} não é válida")
					else:
						data.append(tmp)

				else:

					dados = dados.replace('-', ' ')
					dados = dados.replace('=', ' ')

					if dados in self.ignorar:
						continue
					try:
						#Obtem dados especificos a partir da data atual
						#Ex: mes = Junho; ele retorna (list) {diaatual}/{numerojunho}/{ano} e a de hoje
						#{Ano} vai ser o atual caso não seja maior que a data atual

						for mes in self.frase['mes']:
							if dados in mes:
								dados = self.obterDataEmTexto('mes',mes[0],dados)
								print("\tdata no mes="+str(data))


						for semana in self.frase['semana']:
							if dados in semana:
								dados = self.obterDataEmTexto('semana',semana[0],dados)
								print("data no semana="+str(data))


						for dia in self.frase['dia']:
							if dados in dia:
								depende_de_parametros.append(dados)
								dados = None
								continue

						if dados == None:
							continue

						for x in dados:
							if(self.data_valida(x) == False):
								print("A data {data} não é válida!".format(data=x))
								raise Exception("Data gerada pelo programa inválida!")
							else:
									data.append(x)
					except Exception as e:
						if debug == True:
							print("[class=Data][__init__] Erro: ",e)
							print("[class=Data][__init__] Erro: ",e)
							print("[class=Data][__init__] sys: ",traceback.format_exc())

						naodata.append(dados)

			except Exception as e:
				if debug == True:
					print("[class=Data][__init__] Erro: ",e)
					print("[class=Data][__init__] sys: ",sys.exc_info())
					print("[class=Data][__init__] traceback: ",traceback.format_exc())



		for x in depende_de_parametros:
			dados = self.obterDataEmTexto('dia',dia[0],dados,naodata)
			for x in dados:
				if(self.data_valida(x) == False):
					if debug == True:
						print("A data {data} não é válida!".format(data=x))
						raise Exception("Data gerada pelo programa inválida!")	
				else:
						data.append(x)


		tam = len(data)
		if datas_falsas > 0:
			if tam > 0:
				if debug == True:
					print(f"{datas_falsas} datas inválidas, mas eu ainda tenho mais de 1 data...")
			else:
				print(f"{datas_falsas} datas inválida(s). Não posso trabalhar com isso.")

				mostrar_ajuda()

		if datas_falsas + tam == 0:
			mostrar_ajuda()

		if tam == 1:
			self.mostra_data_especifica(data)
		elif tam == 2:
			self.calcula_intervalo(data)
		else:
			self.calcula_tempo_medio(data)



	def data_valida(self,data):
		try:
			#determinar ordem de dia/mes/ano

			if 0 < int(data[0]) < 32 and 0 < int(data[1]) < 13 and 0 < len(str(data[2])) < 5:
				return True

			return False
		except Exception as e:
			if debug == True:
				print("[class=Data][obterDataEmTexto]: {erro}".format(erro=e))
				print("[class=Data][obterDataEmTexto] traceback: ",traceback.format_exc())
				print(sys.exc_info())
			return False


	def calcula_tempo_medio(self,valor):
		intervalos = []

		v = self.calcula_intervalo(valor)
		intervalos.append(v)

		print(v)

	def mostra_data_especifica(self,data):
		print("Mostra informaçoes da data {}".format(data[0]))
		#Informações como
		#seculo
		#estação naquele ano no pais referencia(default brasil)
		#Pegar mais de alguma de API



	def calcula_intervalo(self,datas,retorno=False):
		if len(datas) == 2:
			data1 = "-".join(map(str,datas[0]))
			data2 = '-'.join(map(str,datas[1]))
			d1 = datetime.strptime(data1,"%d-%m-%Y")
			d2 = datetime.strptime(data2,"%d-%m-%Y")

			d3 = abs((d1-d2).days)

			d1 = d1.strftime("%d/%m/%Y")
			d2 = d2.strftime("%d/%m/%Y")

			if retorno == False:
				self.explicar_intervalo(d1,d2,d3)
			else:
				return d3
		elif len(datas) > 2:
			intervalos = Data
			for x in datas:	
				d =  "-".join(map(str,x))
				d1 = datetime.strptime(d,"%d-%m-%Y")

				intervalos = intervalos + d1


			print(intervalos)

	def explicar_intervalo(self,data1,data2,intervalo):
		print(f"Intervalo entre {data1} e {data2}:")

		dias = intervalo
		horas = intervalo * 24
		minutos = horas * 60

		if intervalo > 364 * 100:
			seculos = int(int(intervalo) / (365 * 100))
			intervalo = intervalo - seculos * (365 * 100)

			print(f"\tSeculos: {seculos} seculos")

		if intervalo > 364:
			anos = int(int(intervalo) / 365)
			intervalo = intervalo - anos * 365

			print(f"\tAnos: {anos} anos")

		if intervalo > 29:
			meses = int(int(intervalo) / 30)
			intervalo = intervalo - meses * 30

			print(f"\tMeses: {meses} meses")
		if intervalo > 0:
			print(f"\tDias: {intervalo} dias")


		print('-'*50)
		print("\tTotais: ")
		print("\t\tDias: {:,}".format(dias))
		print("\t\tHoras: {:,}".format(horas))
		print("\t\tMinutos: {:,}".format(minutos))


	def obterDataEmTexto(self,chave,valor_da_chave,valor,opcao):
		now = datetime.now()
		data_atual = now.strftime('%d-%m-%Y')
		t = [now.day,now.month,now.year]

		data_nova = None
		r = None
		try:
			if chave == 'mes':
				verificar = now.strftime('%d-{}-%Y'.format(valor_da_chave))

				data_nova = datetime.strptime(verificar,"%d-%m-%Y")
				data_atual = datetime.strptime(data_atual,"%d-%m-%Y")

				if data_atual > data_nova:
					data_nova = datetime.strftime(data_nova,"%d-%m-{}".format(data_nova.year+1))
					data_nova = datetime.strptime(data_nova,"%d-%m-%Y").date()
					print("Mostrando o mes em {0} do ano que vem.".format(self.frase['mes'][valor_da_chave-1][2]))


				elif data_atual == data_nova:
					print(f"{data_atual} igual {data_nova}")

				else:
					print(f"Mostrando:  {data_atual.date()} menor que {data_nova.date()}")

				h = [data_nova.day,data_nova.month,data_nova.year]
				r = [t,h]

			elif chave == 'semana':
				pass
			elif 'dia' in chave:
				r = [t]

		except Exception as e:
			if debug == True:
				print("[class=Data][obterDataEmTexto]: {erro}".format(erro=e))
				print("[class=Data][obterDataEmTexto] traceback: ",traceback.format_exc())
				print(sys.exc_info())
		return r





def mostrar_ajuda():
	print("Ajuda: \n\n\n\n\t\t\tNada\n\n\n\n\n\n")

if __name__ == '__main__':
	Data()




