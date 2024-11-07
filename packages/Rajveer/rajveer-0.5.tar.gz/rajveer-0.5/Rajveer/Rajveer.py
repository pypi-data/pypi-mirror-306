import os
import uuid
import requests
from secrets import token_hex
from user_agent import generate_user_agent
import re
import random
import time
class API:
	@staticmethod
	def GetAolToken():
		try:	  
			qq = requests.get('https://login.aol.com/account/create', headers={
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
			'accept-language': 'en-US,en;q=0.9',
		})
			cookies = qq.cookies.get_dict()
			tm1 = str(time.time()).split('.')[0]
			cookies.update({
			'gpp': 'DBAA',
			'gpp_sid': '-1',
			'__gads': f'ID=c0M0fd00676f0ea1:T={tm1}:RT={tm1}:S=ALNI_MaEGaVTSG6nQFkSJ-RnxSZrF5q5XA',
			'__gpi': f'UID=00000cf0e8904e94:T={tm1}:RT={tm1}:S=ALNI_MYCzPrYn9967HtpDSITUe5Z4ZwGOQ',
			'cmp': f't={tm1}&j=0&u=1---',
		})
			specData = qq.text.split('name="attrSetIndex">\n		<input type="hidden" value="')[1].split('" name="specData">')[0]
			specId = qq.text.split('name="browser-fp-data" id="browser-fp-data" value="" />\n		<input type="hidden" value="')[1].split('" name="specId">')[0]
			crumb = qq.text.split('name="cacheStored">\n		<input type="hidden" value="')[1].split('" name="crumb">')[0]
			sessionIndex = qq.text.split('"acrumb">\n		<input type="hidden" value="')[1].split('" name="sessionIndex">')[0]
			acrumb = qq.text.split('name="crumb">\n		<input type="hidden" value="')[1].split('" name="acrumb">')[0]
			try:
				os.remove('aol_req.txt')
				os.remove('aol_cok.txt')
			except:
				pass
			with open('aol_req.txt', 'a') as t:
				t.write(f"{specData}Π{specId}Π{crumb}Π{sessionIndex}Π{acrumb}\n")

			with open('aol_cok.txt', 'a') as g:
				g.write(str(cookies) + '\n')
		except Exception as e:
			print(e)
			API.GetAolToken()
	@staticmethod
	def GetGmailToken():
		try:
			ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
			pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
			port = random.choice(pl)
			proxy = ip + ":" + str(port)
			n1 = ''.join(random.choice('azertyuiopmlkjhgfdsqwxcvbn') for _ in range(random.randrange(6, 9)))
			n2 = ''.join(random.choice('azertyuiopmlkjhgfdsqwxcvbn') for _ in range(random.randrange(3, 9)))
			host = ''.join(random.choice('azertyuiopmlkjhgfdsqwxcvbn') for _ in range(random.randrange(15, 30)))
			he3 = {
			"accept": "*/*",
			"accept-language": "ar-YE,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
			"content-type": "application/x-www-form-urlencoded;charset=UTF-8",
			"google-accounts-xsrf": "1",
			"sec-ch-ua": "\"Not)A;Brand\";v=\"24\", \"Chromium\";v=\"116\"",
			"sec-ch-ua-arch": "\"\"",
			"sec-ch-ua-bitness": "\"\"",
			"sec-ch-ua-full-version": "\"116.0.5845.72\"",
			"sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"24.0.0.0\", \"Chromium\";v=\"116.0.5845.72\"",
			"sec-ch-ua-mobile": "?1",
			"sec-ch-ua-model": "\"ANY-LX2\"",
			"sec-ch-ua-platform": "\"Android\"",
			"sec-ch-ua-platform-version": "\"13.0.0\"",
			"sec-ch-ua-wow64": "?0",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-origin",
			"x-chrome-connected": "source=Chrome,eligible_for_consistency=true",
			"x-client-data": "CJjbygE=",
			"x-same-domain": "1",
			"Referrer-Policy": "strict-origin-when-cross-origin",
			'user-agent': str(generate_user_agent()),
		}

			res1 = requests.get('https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB', headers=he3)
			tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text).group(2)
			cookies = {'__Host-GAPS': host}
			headers = {
			'authority': 'accounts.google.com',
			'accept': '*/*',
			'accept-language': 'en-US,en;q=0.9',
			'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
			'google-accounts-xsrf': '1',
			'origin': 'https://accounts.google.com',
			'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
			'user-agent': generate_user_agent(),
		}
			data = {
			'f.req': '["' + tok + '","' + n1 + '","' + n2 + '","' + n1 + '","' + n2 + '",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
			'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
		}
			response = requests.post(
			'https://accounts.google.com/_/signup/validatepersonaldetails',
			cookies=cookies,
			headers=headers,
			data=data,
			proxies={'http://': proxy}
		)
			tl = str(response.text).split('",null,"')[1].split('"')[0]
			host = response.cookies.get_dict()['__Host-GAPS']
			try:
				os.remove('tlcok.txt')
			except:
				pass
			with open('tlcok.txt', 'a') as f:
				f.write(tl + 'Π' + host + '\n')
		except Exception as e:
			print(e)
			API.GetGmailToken()
	@staticmethod
	def GetHotmailToken():
		try:
			headers = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	'accept-language': 'en-US,en;q=0.9',
	'upgrade-insecure-requests': '1',
	'user-agent': generate_user_agent(),
		}
			response = requests.get('https://signup.live.com/signup', headers=headers)
			canary=str.encode(response.text.split('"apiCanary":"')[1].split('"')[0]).decode("unicode_escape").encode("ascii").decode("unicode_escape").encode("ascii").decode("ascii")
			mc=response.cookies.get_dict()['amsc']
			cookies = {
	'amsc': mc,
}
			headers = {
	'accept': 'application/json',
	'accept-language': 'en-US,en;q=0.9',
	'canary': canary,
	'content-type': 'application/json; charset=utf-8',
	'origin': 'https://signup.live.com',
	'referer': 'https://signup.live.com/',
	'user-agent': generate_user_agent(),
}
			json_data = {
	'clientExperiments': [
		{
			'parallax': 'enableplaintextforsignupexperiment',
			'control': 'enableplaintextforsignupexperiment_control',
			'treatments': [
				'enableplaintextforsignupexperiment_treatment',
			],
		},
	],
}
			response = requests.post(
	'https://signup.live.com/API/EvaluateExperimentAssignments',
	cookies=cookies,
	headers=headers,
	json=json_data,
).json()
			try:
				ca=response['apiCanary']
			except Exception as e:
				 print(e)	   
				 GetHotmailToken()


			try:
				os.remove('hotmail_req.txt')
			except:
				pass

			with open('hotmail_req.txt', 'a') as t:
				t.write(f"{mc}Π{ca}\n")

		except Exception as e:
			print(e)
			API.GetHotmailToken()

	@staticmethod
	def GetYahooToken():
		try:
			qq = requests.get('https://login.yahoo.com/account/create', headers={
			'user-agent': 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/122.0.0.0'
		})
			cookies = qq.cookies.get_dict()
			cookies.update({'gpp': 'DBAA', 'gpp_sid': '-1',})
			z = qq.text
			crumb = z.split('''name="cacheStored">
		<input type="hidden" value="''')[1].split('" name="crumb">')[0]
			specData = z.split('''name="attrSetIndex">
		<input type="hidden" value="''')[1].split('" name="specData">')[0]
			acrumb = z.split('''name="crumb">
		<input type="hidden" value="''')[1].split('" name="acrumb">')[0]
			specId = z.split('''id="browser-fp-data" value="" />
		<input type="hidden" value="''')[1].split('" name="specId">')[0]
			sessionIndex = z.split('''name="acrumb">
		<input type="hidden" value="''')[1].split('" name="sessionIndex">')[0]

			try:
				os.remove('yahoo_req.txt')
				os.remove('yahoo_cok.txt')
			except:
				pass

			with open('yahoo_req.txt', 'a') as t:
				t.write(f"{crumb}Π{specData}Π{acrumb}Π{specId}Π{sessionIndex}\n")
		
			with open('yahoo_cok.txt', 'a') as g:
				g.write(str(cookies) + '\n')
		except Exception as e:
			print(e)
			API.GetYahooToken()
	@staticmethod
	def GetGmxToken():
		try:
			cookies = { 
			'AB_COOKIE': 'A',
		}
			headers = {
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
			'Accept-Language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
			'Cache-Control': 'max-age=0',
			'Connection': 'keep-alive',
			'Referer': 'https://www.gmx.com/',
			'Sec-Fetch-Dest': 'document',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-User': '?1',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
			'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
			'sec-ch-ua-mobile': '?1',
			'sec-ch-ua-platform': '"Android"',
		}

			req = requests.get('https://signup.gmx.com/', cookies=cookies, headers=headers).text
			if "Your IP address suggests you are trying to sign up in a country where GMX" in req:
				access_token = None
				guid = None
			else:
				access_token = re.search(r'"accessToken": "(.*?)"', req).group(1)
				guid = re.search(r'"clientCredentialGuid": "(.*?)"', req).group(1)
				print("accessToken:", access_token)
				print("clientCredentialGuid:", guid)
				try:
					os.remove('AccGuid.txt')
				except:
					pass
				with open('AccGuid.txt', 'a') as f:
					f.write(access_token+ '|' + guid + '\n')
		except Exception as e:
			print(e)
			API.GetGmxToken()

#Aol
	@staticmethod
	def CheckAol(email):
		try:
			if '@' in email:
				name = email.split('@')[0]
			else:
				name = email

			try:
				with open("aol_req.txt", "r") as f:
					for line in f:
						specData, specId, crumb, sessionIndex, acrumb = line.strip().split('Π')

				with open("aol_cok.txt", "r") as f:
					for line in f:
						cookies = eval(line.strip())
			except:
				API.GetAolToken()
				with open("aol_req.txt", "r") as f:
					for line in f:
						specData, specId, crumb, sessionIndex, acrumb = line.strip().split('Π')

				with open("aol_cok.txt", "r") as f:
					for line in f:
						cookies = eval(line.strip())

			headers = {
			'authority': 'login.aol.com',
			'accept': '*/*',
			'accept-language': 'en-US,en;q=0.9',
			'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'origin': 'https://login.aol.com',
			'referer': f'https://login.aol.com/account/create?specId={specId}&done=https%3A%2F%2Fwww.aol.com',
			'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
			'sec-ch-ua-mobile': '?0',
			'sec-ch-ua-platform': '"Windows"',
			'sec-fetch-dest': 'empty',
			'sec-fetch-mode': 'cors',
			'sec-fetch-site': 'same-origin',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
			'x-requested-with': 'XMLHttpRequest',
		}

			params = {
			'validateField': 'userId',
		}

			data = f'browser-fp-data=%7B%22language%22%3A%22en-US%22%2C%22colorDepth%22%3A24%2C%22deviceMemory%22%3A8%2C%22pixelRatio%22%3A1%2C%22hardwareConcurrency%22%3A4%2C%22timezoneOffset%22%3A-60%2C%22timezone%22%3A%22Africa%2FCasablanca%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22Win32%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A5%2C%22hash%22%3A%222c14024bf8584c3f7f63f24ea490e812%22%7D%2C%22canvas%22%3A%22canvas%20winding%3Ayes~canvas%22%2C%22webgl%22%3A1%2C%22webglVendorAndRenderer%22%3A%22Google%20Inc.%20(Intel)~ANGLE%20(Intel%2C%20Intel(R)%20HD%20Graphics%204000%20(0x00000166)%20Direct3D11%20vs_5_0%20ps_5_0%2C%20D3D11)%22%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A33%2C%22hash%22%3A%22edeefd360161b4bf944ac045e41d0b21%22%7D%2C%22audio%22%3A%22124.04347527516074%22%2C%22resolution%22%3A%7B%22w%22%3A%221600%22%2C%22h%22%3A%22900%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%22860%22%2C%22h%22%3A%221600%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1704793094844%2C%22render%22%3A1704793096534%7D%7D&specId={specId}&cacheStored=&crumb={crumb}&acrumb={acrumb}&sessionIndex={sessionIndex}&done=https%3A%2F%2Fwww.aol.com&googleIdToken=&authCode=&attrSetIndex=0&specData={specData}&multiDomain=&tos0=oath_freereg%7Cus%7Cen-US&firstName=ahmed&lastName=Mahos&userid-domain=yahoo&userId={name}&password=Drahmed2006##$$&mm=10&dd=24&yyyy=2000&signup='

			res = requests.post('https://login.aol.com/account/module/create', params=params, headers=headers, data=data, cookies=cookies).text
			if '{"errors":[]}' in res:
				return {'status': 'ok', 'Available': True}
			elif 'IDENTIFIER_EXISTS' in res or 'IDENTIFIER_NOT_AVAILABLE' in res:
				return {'status': 'ok', 'Available': False}
			elif 'LENGTH_TOO_SHORT' in res:
				return {'status': 'bad', 'Available': False}
			else:
				return {'status': 'ok', 'Available': 'Error'}
				API.GetAolToken()  
		except Exception as e:
			print(e)
			API.GetAolToken()  
#Gmail
	@staticmethod
	def CheckGmail(email):
		try:
			try:
				with open("tlcok.txt", "r") as f:
					for line in f:
						tl, host = line.strip().split('Π')
			except:
				API.GetGmailToken()
				with open("tlcok.txt", "r") as f:
					for line in f:
						tl, host = line.strip().split('Π')

			if '@' in email:
				email = str(email).split('@')[0]
			else:
				email = email
				ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
				pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
				port = random.choice(pl)
				proxy = ip + ":" + str(port)
				cookies = {'__Host-GAPS': host}
				headers = {
				'authority': 'accounts.google.com',
				'accept': '*/*',
				'accept-language': 'en-US,en;q=0.9',
				'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
				'google-accounts-xsrf': '1',
				'origin': 'https://accounts.google.com',
				'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL={tl}',
				'user-agent': generate_user_agent(),
			}
				params = {'TL': tl}
				data = f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D&gmscoreversion=undefined&flowName=GlifWebSignIn&'
				response = requests.post(
				'https://accounts.google.com/_/signup/usernameavailability',
				params=params,
				cookies=cookies,
				headers=headers,
				data=data,
				proxies={'http://': proxy}
			)
				if '"gf.uar",1' in str(response.text):
					return {'status': 'ok', 'Available': True}
				elif '"gf.uar",2' in response.text or '"gf.uar",3' in response.text:
					return {'status': 'ok', 'Available': False}
				else:
					return {'status': 'ok', 'Available': 'Error'}
					API.GetGmailToken()
		except Exception as e:
			return {'status': 'ok', 'Available': 'Error'}
			API.GetGmailToken()
#Hotmail
	@staticmethod
	def CheckHotmail(email):
		try:
			if '@hotmail.com' in email or '@outlook.com' in email or '@outlook.sa' in email:
				try:
					with open("hotmail_req.txt", "r") as f:
						for line in f:
							mc, ca = line.strip().split('Π')
				except FileNotFoundError:
					API.GetHotmailToken()
					with open("hotmail_req.txt", "r") as f:
						for line in f:
							mc, ca = line.strip().split('Π')

				cookies = {
				'mkt': 'ar-YE',
				'MicrosoftApplicationsTelemetryDeviceId': f'{uuid.uuid4()}',
				'MUID': f'{token_hex(8) * 2}',
				'mkt1': 'ar-AR',
				'ai_session': 'CyuLoU6vSi7HJzZeYNyVoH|1709731817506|1709731817506',
				'amsc': f'{mc}',
				'clrc': '{%2219789%22%3a[%22+VC+x0R6%22%2c%22FutSZdvn%22%2c%22d7PFy/1V%22]}',
			}
				headers = {
				'authority': 'signup.live.com',
				'accept': 'application/json',
				'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
				'canary': f'{ca}',
				'content-type': 'application/json',
				'hpgid': '200639',
				'origin': 'https://signup.live.com',
				'referer': f'https://signup.live.com/signup?mkt=AR-AR&lic=1&uaid={uuid.uuid4()}',
				'scid': '100118',
				'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
				'sec-ch-ua-mobile': '?1',
				'sec-ch-ua-platform': '"Android"',
				'sec-fetch-dest': 'empty',
				'sec-fetch-mode': 'cors',
				'sec-fetch-site': 'same-origin',
				'tcxt': 'VWlP20OW8k/xH6tFupQw1HwrEFETf+tDxcIS0OeqhsBSbBIMy4srnqBeqY1i2lMA5VbPfXSuTUEhdSw9AWoPPSNJeuzfyYceefIZ/1EGoBqppRyXgczQuaM5teemKuAKiUXDaBYMj8Ng8fhejlVVuQmHCBl+PgEGlG7A/8uqXNwqIlrg9tbOqIzHkn5X1jUytMlmFxmEjdLCQnainFfCoxqgPZjkQwcE6hQFElIuxniqWRWk6lmEleIPwhGFID2kbSE5kxjiT5eoUt/S5zxP2a1Yp+shu8ITJrys5pkwMbsWO+L18h8bH4+BG3LFLJk00zd28yeJz7uTq3NRNR1uK+OiCVwGdB5JhxmvsItOIwHc83/xeN0XuTlXGgueChmPKulABKjR4v0VDkutbyPQwRVqRPRALfutQaEjOXdx9FXOCUTySJLtPpeMPIj172+PUSlBhgueKn3Iiz2mzKbR8Kv4JgBlQF5m3dVYyNpSN998fVQE3x94ruAsioYwEOBdfEViB34QpbzAuNfoNmNisCvzI9PKzc+cDKeWkcVd7OtYQSR0AR2Ibr6LE0iulNI5/zqg/BYp3Vf2zaExAmpf8Q==:2:3',		   
				'uaid': f'{uuid.uuid4()}',
				'uiflvr': '1001',
				'user-agent': generate_user_agent(),
				'x-ms-apitransport': 'xhr',
				'x-ms-apiversion': '2',
			}
				params = {
				'mkt': 'AR-AR',
				'lic': '1',
				'uaid': f'{uuid.uuid4()}',
			}
				data = {
				'signInName': f'{email}',
				'uaid': f'{uuid.uuid4()}',
				'includeSuggestions': True,
				'uiflvr': 1001,
				'scid': 100118,
				'hpgid': 200639,
			}

				req = requests.post('https://signup.live.com/API/CheckAvailableSigninNames', params=params, cookies=cookies, headers=headers, json=data).text
				if '"isAvailable":true,' in req:
					return {'status': 'ok', 'Available': True}
				elif '"isAvailable":false,' in req:
					return {'status': 'ok', 'Available': False}
				else:
					return {'status': 'ok', 'Available': 'Error'}
					API.GetHotmailToken()
			else:
				return {'status': 'ok', 'Available': 'Error'}

		except Exception as e:
			print(e)
#Yahoo
	@staticmethod
	def CheckYahoo(email):
		try:
			if '@' in email:
				name = email.split('@')[0]
			else:
				name = email	   
			try:
				with open("yahoo_req.txt", "r") as f:
					for line in f:
						crumb, specData, acrumb, specId, sessionIndex = line.strip().split('Π')
			
				with open("yahoo_cok.txt", "r") as f:
					for line in f:
						cookies = eval(line.strip())
			except:
				API.GetYahooToken()
				with open("yahoo_req.txt", "r") as f:
					for line in f:
						crumb, specData, acrumb, specId, sessionIndex = line.strip().split('Π')
			
				with open("yahoo_cok.txt", "r") as f:
					for line in f:
						cookies = eval(line.strip())

			headers = {
			'authority': 'login.yahoo.com',
			'accept': '*/*',
			'accept-language': 'en-US,en;q=0.9',
			'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'dnt': '1',
			'origin': 'https://login.yahoo.com',
			'user-agent': 'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/122.0.0.0',
			'x-requested-with': 'XMLHttpRequest',
		}
		
			params = {
			'validateField': 'userId',
		}
		
			data = (
			'browser-fp-data=%7B%22language%22%3A%22en-US%22%2C%22colorDepth%22%3A24%2C%22deviceMemory%22%3A8%2C%22pixelRatio%22%3A2%2C'
			'%22hardwareConcurrency%22%3A4%2C%22timezoneOffset%22%3A-60%2C%22timezone%22%3A%22Africa%2FCasablanca%22%2C%22sessionStorage'
			'%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22Win32%22%2C'
			'%22doNotTrack%22%3A%221%22%2C%22plugins%22%3A%7B%22count%22%3A0%2C%22hash%22%3A%2224700f9f1986800ab4fcc880530dd0ed%22%7D%2C'
			'%22canvas%22%3A%22canvas%20winding%3Ayes~canvas%22%2C%22webgl%22%3A1%2C%22webglVendorAndRenderer%22%3A%22Google%20Inc.%20'
			'(Intel)~ANGLE%20(Intel%2C%20Intel(R)%20HD%20Graphics%204000%20(0x00000166)%20Direct3D11%20vs_5_0%20ps_5_0%2C%20D3D11)%22%2C'
			'%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A1%2C%22hasLiedBrowser%22'
			'%3A1%2C%22touchSupport%22%3A%7B%22points%22%3A1%2C%22event%22%3A1%2C%22start%22%3A1%7D%2C%22fonts%22%3A%7B%22count%22%3A33%2C'
			'%22hash%22%3A%22edeefd360161b4bf944ac045e41d0b21%22%7D%2C%22audio%22%3A%22124.04347527516074%22%2C%22resolution%22%3A%7B%22w'
			'%22%3A%22768%22%2C%22h%22%3A%221024%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%221024%22%2C%22h%22%3A%22768%22%7D%2C'
			'%22ts%22%3A%7B%22serve%22%3A1709817628760%2C%22render%22%3A1709817628268%7D%7D&specId=' + specId + '&cacheStored=&crumb=' + crumb +
			'&acrumb=' + acrumb + '&sessionIndex=' + sessionIndex + '&done=https%3A%2F%2Fwww.yahoo.com%2F&googleIdToken=&authCode=&attrSetIndex=0&specData=' +
			specData + '&tos0=oath_freereg%7Cxa%7Cen-JO&multiDomain=&firstName=ahmed&lastName=mahos&userid-domain=yahoo&userId=' + name +
			'&password=Drahmed2006##$$##$$&mm=10&dd=24&yyyy=2000&signup='
		)

			res = requests.post('https://login.yahoo.com/account/module/create', params=params, cookies=cookies, headers=headers, data=data).text
			if '{"errors":[]}' in res:
				return {'status': 'ok', 'Available': True}
			elif 'IDENTIFIER_EXISTS' in res or 'IDENTIFIER_NOT_AVAILABLE' in res:
				return {'status': 'ok', 'Available': False}
			elif 'LENGTH_TOO_SHORT' in res:
				return {'status': 'ok', 'Available': False}
			else:
				return {'status': 'ok', 'Available': 'Error'}
				API.GetYahooToken()  
		except Exception as e:
			#print(e)
			API.GetYahooToken()
#GMX
	@staticmethod
	def CheckGmx(email):
		if not '@' in email:
			email = email + '@gmx.com'
		else:
			email = email
		try:
			with open("AccGuid.txt", "r") as f:
				for line in f:
					access_token = line.strip().split('|')[0]
					guid = line.strip().split('|')[1]
		except:
			API.GetGmxToken()
			with open("AccGuid.txt", "r") as f:
				for line in f:
					access_token = line.strip().split('|')[0]
					guid = line.strip().split('|')[1]

		headers = {
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
		'Authorization': f'Bearer {access_token}',
		'Connection': 'keep-alive',
		'Content-Type': 'application/json',
		'Origin': 'https://signup.gmx.com',
		'Referer': 'https://signup.gmx.com/',
		'Sec-Fetch-Dest': 'empty',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'same-origin',
		'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
		'X-CCGUID': guid,
		'X-UI-APP': '@umreg/registration-app2/7.4.31',
		'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
	}

		json_data = {
		'emailAddress': email,
		'firstName': '',
		'lastName': '',
		'birthDate': '',
		'city': '',
		'countryCode': 'US',
		'suggestionProducts': [
			'gmxcomFree',
		],
		'maxResultCountPerProduct': '10',
		'mdhMaxResultCount': '5',
		'initialRequestedEmailAddress': '',
		'requestedEmailAddressProduct': 'gmxcomFree',
	}
		try:
			res = requests.post(
		'https://signup.gmx.com/suggest/rest/email-alias/availability',
		headers=headers,
		json=json_data,
	).text
			if '"emailAddressAvailable":true,' in res or '"emailAddressAvailable":True,' in res:
				return {'status': 'ok', 'Available': True}
			elif '"emailAddressAvailable":false,' in res or '"emailAddressAvailable":False,' in res:
				return {'status': 'ok', 'Available': False}
			else:
				return {'status': 'ok', 'Available': 'TryAgainLater'}
				API.GetGmxToken()
		except Exception as e:
		 	print(e)
		 	return {'status': 'ok', 'Available': e}
		 	API.GetGmxToken()
#Mail_ru
	@staticmethod
	def CheckMailRu(email):
		try:
			url = "https://account.mail.ru/api/v1/user/exists"
			headers = {"User-Agent": str(generate_user_agent())}
			data = {'email': str(email)}
			res = requests.post(url, data=data, headers=headers)
			if res.json()['body']['exists'] == False:
				return {'status': 'ok', 'Available': True}
			else:
				return {'status': 'ok', 'Available': False}
		except Exception as e:
			return {'status': 'ok', 'Available': 'Error'}
class Insta:
	@staticmethod
	def AvailableIG(email):
		ua = generate_user_agent()
		dev = 'android-'
		device_id = dev + hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[:16]
		uui = str(uuid.uuid4())
		headers = {
        'User-Agent': ua,
        'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
		data = {
        'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.' + json.dumps({
            '_csrftoken': '9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
            'adid': uui,
            'guid': uui,
            'device_id': device_id,
            'query': email
        }),
        'ig_sig_key_version': '4',
    }
		response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/', headers=headers, data=data).text
		return response
	@staticmethod
	def Date(id):
		try:
			ranges = [
            (1278889, 2010),
            (17750000, 2011),
            (279760000, 2012),
            (900990000, 2013),
            (1629010000, 2014),
            (2369359761, 2015),
            (4239516754, 2016),
            (6345108209, 2017),
            (10016232395, 2018),
            (27238602159, 2019),
            (43464475395, 2020),
            (50289297647, 2021),
            (57464707082, 2022),
            (63313426938, 2023)
            
        ]
        
			for upper, year in ranges:
				if id <= upper:
					return year
			return 2024
    
		except Exception:
			pass
	@staticmethod
	def Rest(user):
		try:
			headers = {
    'X-Pigeon-Session-Id': '50cc6861-7036-43b4-802e-fb4282799c60',
    'X-Pigeon-Rawclienttime': '1700251574.982',
    'X-IG-Connection-Speed': '-1kbps',
    'X-IG-Bandwidth-Speed-KBPS': '-1.000',
    'X-IG-Bandwidth-TotalBytes-B': '0',
    'X-IG-Bandwidth-TotalTime-MS': '0',
    'X-Bloks-Version-Id': 'c80c5fb30dfae9e273e4009f03b18280bb343b0862d663f31a3c63f13a9f31c0',
    'X-IG-Connection-Type': 'WIFI',
    'X-IG-Capabilities': '3brTvw==',
    'X-IG-App-ID': '567067343352427',
    'User-Agent': 'Instagram 100.0.0.17.129 Android (29/10; 420dpi; 1080x2129; samsung; SM-M205F; m20lte; exynos7904; en_GB; 161478664)',
    'Accept-Language': 'en-GB, en-US',
     'Cookie': 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'i.instagram.com',
    'X-FB-HTTP-Engine': 'Liger',
    'Connection': 'keep-alive',
    'Content-Length': '356',
}
			data = {
    'signed_body': '0d067c2f86cac2c17d655631c9cec2402012fb0a329bcafb3b1f4c0bb56b1f1f.{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","adid":"0dfaf820-2748-4634-9365-c3d8c8011256","guid":"1f784431-2663-4db9-b624-86bd9ce1d084","device_id":"android-b93ddb37e983481c","query":"'+user+'"}',
    'ig_sig_key_version': '4',
  }
			response = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',headers=headers,data=data,).json()
			r=response['email']
		except:
			r='Craked'
		return r
	@staticmethod
	def Info(username):
		headers = {
				  'accept': '*/*',
				  'accept-language': 'en',
				  'referer': 'https://www.instagram.com/{}/'.format(username),
				  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
				  'x-ig-app-id': '936619743392459',
				  'x-ig-www-claim': '0',
				  'x-requested-with': 'XMLHttpRequest',
			  }
		params = {
				  'username': username,
			  }
		try:response = requests.get(
					  'https://www.instagram.com/api/v1/users/web_profile_info/',
					  params=params,
					  headers=headers,
				  ).json()
		except:response=None
		try:
			  id=response['data']['user']['id']
		except:
			  id=None
		try:
			followerNum=response['data']['user']['edge_followed_by']['count']
		except:
			followerNum=None
		try:
			followingNum=response['data']['user']['edge_follow']['count']
		except:
			followingNum=None
		try:
			postNum=response['data']['user']['edge_owner_to_timeline_media']['count']
		except:
			  postNum=None
		try:
			isPraise=response['data']['user']['is_private']
		except:
			isPraise=None
		try:
			full_name=response['data']['user']['full_name']
		except:
			full_name=None
		try:
			biography=response['data']['user']['biography']
		except:
			biography=None
		try:
			is_verified=response['data']['user']['is_verified']
		except:
			is_verified=None
		try:
			if id == None:date=None
			else:
				try:
					date=Insta.Date(id)
				except:date=None
		except:date=None
		return {
            "Name": full_name,
            "Username": username,
            "Followers": followerNum,
            "Following": followingNum,
            "Date": date,
            "Id": id,
            "Post": postNum,
            "Bio": biography,
            "Verified": is_verified,
            "Private": isPraise,
            		}
	@staticmethod
	def Usergen(age):
		if age == 2010 or age == '2010':
			start=1
			end=1278889
		elif age == 2011 or age == '2011':
			start=1279000
			end=17750000
		elif age == 2012 or age == '2012':
			start=17750000
			end=279760000
		elif age == 2013 or age == '2013':
			start=279760000
			end=900990000
		elif age == 2014 or age == '2014':
			start=900990000
			end=1629010000
		elif age == 2015 or age == '2015':
			start=1629010000
			end=2369359761
		elif age == 2016 or age == '2016':
			start=2369359762
			end=4239516754
		elif age == 2017 or age == '2017':
			start=4239516755
			end=6345108209
		elif age == 2018 or age == '2018':
			start=6345108210
			end=10016232395
		elif age == 2019 or age == '2019':
			start=10016232396
			end=27238602159
		elif age == 2020 or age == '2020':
			start=27238602160
			end=50289297647
		elif age == 2021 or age == '2021':
			start=50289297648
			end=57464707082
		elif age == 2022 or age == '2022':
			start=57464707083
			end=63313426938
		elif age == 2023 or age == '2023':
			start=63313426939
			end=63399426998
		else:
			return 'NoAccount'
		def gg():
			headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0',
                'x-ig-app-id': '936619743392459',
                'x-csrftoken': 'QOeFYsOi8enKuW80uC0WezhvEgiydc2Y',
                'x-ig-www-claim': 'hmac.AR3iNxyHufbREf9pIUL6m2ciMIIxA3vQTyCHW_yWjgu5dmsq',
            }

			data = {
                'av': '17841408545457742',
                '__user': '0',
                '__a': '1',
                '__req': '53',
                'dpr': '1',
                '__csr': 'iMkMF5NsIh2I4Aggpik9SLfZgxAZOsJh6DcNcUFXH-GHqnlaoSiypHBiVaFkhtdFmO',
                '__spin_r': '1014910249',
                'variables': '{"id":"' + str(randrange(start, end)) + '","render_surface":"PROFILE"}',
                'server_timestamps': 'true',
                'doc_id': '7663723823674585',
            }

			try:
				response = requests.post(
                    'https://www.instagram.com/graphql/query',
                    headers=headers,
                    data=data
                )
				username = response.json()['data']['user']['username']
				return username
			except Exception as e:
				return 'NoAccount'

		return gg()
class Tiktok:
	@staticmethod
	def CheckTiktok(email):
		try:
			ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
			pl = [19, 20, 21, 22, 23, 24, 25, 80, 53, 111, 110, 443, 8080, 139, 445, 512, 513, 514, 4444, 2049, 1524, 3306, 5900]
			port = random.choice(pl)
			proxy = ip + ":" + str(port)
			url = "https://www.tiktok.com/passport/web/user/check_email_registered?shark_extra=%7B%22aid%22%3A1459%2C%22app_name%22%3A%22Tik_Tok_Login%22%2C%22app_language%22%3A%22en%22%2C%22device_platform%22%3A%22web_mobile%22%2C%22region%22%3A%22SA%22%2C%22os%22%3A%22ios%22%2C%22referer%22%3A%22https%3A%2F%2Fwww.tiktok.com%2Fprofile%22%2C%22root_referer%22%3A%22https%3A%2F%2Fwww.google.com%22%2C%22cookie_enabled%22%3Atrue%2C%22screen_width%22%3A390%2C%22screen_height%22%3A844%2C%22browser_language%22%3A%22en-us%22%2C%22browser_platform%22%3A%22iPhone%22%2C%22browser_name%22%3A%22Mozilla%22%2C%22browser_version%22%3A%225.0%20%28iPhone%3B%20CPU%20iPhone%20OS%2014_4%20like%20Mac%20OS%20X%29%20AppleWebKit%2F605.1.15%20%28KHTML%2C%20like%20Gecko%29%20Version%2F14.0.3%20Mobile%2F15E148%20Safari%2F604.1%22%2C%22browser_online%22%3Atrue%2C%22timezone_name%22%3A%22Asia%2FRiyadh%22%2C%22is_page_visible%22%3Atrue%2C%22focus_state%22%3Atrue%2C%22is_fullscreen%22%3Afalse%2C%22history_len%22%3A17%2C%22battery_info%22%3A%7B%7D%7D&msToken=vPgBDLGXZNEf56bl_V4J6muu5nAYCQi5dA6zj49IuWrw2DwDUZELsX2wz2_2ZYtzkbUF9UyblyjQTsIDI5cclvJQ6sZA-lHqzKS1gLIJD9M6LDBgII0nxKqCfwwVstZxhpppXA==&X-Bogus=DFSzsIVLC8A-dJf6SXgssmuyRsO1&_signature=_02B4Z6wo00001dTdX3QAAIDBDn9.7WbolA3U3FvAABfU8c"
			data = f"email={email}&aid=1459&language=en&account_sdk_source=web&region=SA"
			headers = {
				"User-Agent": generate_user_agent(),
			}
			response = requests.post(url, headers=headers, data=data, proxies={'http': proxy})
			if '"data":{"is_registered":1},"message":"success"' in response.text:
				return 'Good'
			elif '{"data":{"is_registered":0},"message":"success"}' in response.text:
				return 'Bad'
			else:
				return 'On VPN'
		except:
			return 'Proxy ERROR'
	@staticmethod
	def Info(username):
		try:
			patre = {
				"Host": "www.tiktok.com",
				"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
				"sec-ch-ua-mobile": "?1",
				"sec-ch-ua-platform": "\"Android\"",
				"upgrade-insecure-requests": "1",
				"user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Plume L2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 Mobile Safari/537.36",
				"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"sec-fetch-site": "none",
				"sec-fetch-mode": "navigate",
				"sec-fetch-user": "?1",
				"sec-fetch-dest": "document",
				"accept-language": "en-US,en;q=0.9,ar-DZ;q=0.8,ar;q=0.7,fr;q=0.6,hu;q=0.5,zh-CN;q=0.4,zh;q=0.3"
			}

			tikinfo = requests.get(f'https://www.tiktok.com/@{username}', headers=patre).text

			try:
				getting = str(tikinfo.split('webapp.user-detail"')[1]).split('"RecommendUserList"')[0]
				try:
					id = str(getting.split('id":"')[1]).split('",')[0]
				except:
					id = ""
				try:
					name = str(getting.split('nickname":"')[1]).split('",')[0]
				except:
					name = ""
				try:
					bio = str(getting.split('signature":"')[1]).split('",')[0]
				except:
					bio = ""
				try:
					country = str(getting.split('region":"')[1]).split('",')[0]
				except:
					country = ""
				try:
					private = str(getting.split('privateAccount":')[1]).split(',"')[0]
				except:
					private = ""
				try:
					followers = str(getting.split('followerCount":')[1]).split(',"')[0]
				except:
					followers = ""
				try:
					following = str(getting.split('followingCount":')[1]).split(',"')[0]
				except:
					following = ""
				try:
					like = str(getting.split('heart":')[1]).split(',"')[0]
				except:
					like = ""
				try:
					video = str(getting.split('videoCount":')[1]).split(',"')[0]
				except:
					video = ""
				try:
					secid = str(getting.split('secUid":"')[1]).split('"')[0]
				except:
					secid = ""
				try:
					countryn = pycountry.countries.get(alpha_2=country).name
				except:
					countryn = ""
				try:
					countryf = pycountry.countries.get(alpha_2=country).flag
				except:
					countryf = ""

				binary = "{0:b}".format(int(id))
				i = 0
				bits = ""
				while i < 31:
					bits += binary[i]
					i += 1
				timestamp = int(bits, 2)
				try:
					cdt = datetime.fromtimestamp(timestamp)
				except:
					cdt = ""

				return {				
					"username": username,
					"secuid": secid,
					"name": name,
					"followers": followers,
					"following": following,
					"like": like,
					"video": video,
					"private": private,
					"country": countryn,
					"flag": countryf,
					"Date": cdt,
					"id": id,
					"bio": bio,
					"status": "ok"
					}
			except:
				return {
					"error": "Invalid username",
					"status": "bad"
				}
		except Exception as e:
			return {			
				"status": "bad"
			}
			
def SendHit(Id, Message, Token):
		try:
			url=f'https://api.telegram.org/bot{Token}/sendMessage'
			params={'chat_id' : Id, 'text' : Message}
			return get(url,params=params).text
		except Exception as e:
			print('No Internet')
	
print(dir())
