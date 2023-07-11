from Login import *
from SQL_Functions import  *
toCheck = ({'id': 2, 'fullname': 'Jeff Card', 'card_num': 'gAAAAABkrK7GtIBz-YjaWNnuXz_VqdD3xAKhv2ToNWpuDoO36aiuvcIJsxYOesN9IwqeMiW31aOaIz71RLh3bwBE99jkH417wNbjCKBH8br_0xpfKSJ-Kfk=', 'exp_date': '2025/05', 'cvv': 'gAAAAABkrK7G-WWJ-H3ny8OgXuzpRxH0jobEg9-Qcmd5G1TJiQNy_zHmRp7kmfYiNl6DBfF3-iTkeEWICmHpj0J9NWZ9h3TObw==', 'budget': None}, {'id': 3, 'fullname': 'Jeff Card', 'card_num': 'gAAAAABkrLDFnjRYnTuuVl7xx_B1oM2pGrDXCro9TAkX9VRyF3dEvg9HfJ_reaRg17GsQkf3mhdSwBL3KNt_0_TT34WCaAtsEydMMA_mlrNqyCZXxwEuKXo=', 'exp_date': '2025/05', 'cvv': 'gAAAAABkrLDFWhX2P376dbnUuew1mTAqZXL6B0Hc8oO1pGt_-AL1oXTedrkXyC3r2NQcB7c4CqoWen-1VLx06IS_LV9fsiXDXw==', 'budget': None}, {'id': 4, 'fullname': 'Jeff Card', 'card_num': 'gAAAAABkrLEO4lWjUTmfjeeugpYekneo8juG2YW_MeRmCtnzzllyWV2wk8lFWZR8nvMGsP-KxGPgrPwkkTTng33PDIUUkp1UJ_GTUM6BuoTSdpUjgDtRZAI=', 'exp_date': '2025/05', 'cvv': 'gAAAAABkrLEOmzrLBM6CBLj9J3U1aohpU9geq9fW0T0lx6BBnJu04ktw51LxK4nYPfMQjGoWfCYGmUqQvSoGLm4YMJuFSucDqA==', 'budget': None}, {'id': 5, 'fullname': 'Jeff Card', 'card_num': 'gAAAAABkrLHOzXZmJ0-Xh3fWt54A1v6GNlB9NXguLd2hIWRgqDOOhJ6qqJyKB_BeSPPNVuNtnYqiH1Sc8aHFQVN-Ld_GcXva9tnxj01J_ziQ3Acnn0BBIyg=', 'exp_date': '2025/05', 'cvv': 'gAAAAABkrLHOfPe33R3pju2TsRUkiGRu8HsQ1tuPa92TkOGnLixi05OhEIFX6ym3wEw7App0N43Yw_BJ0ZpOlw4LRK0GWX9lOQ==', 'budget': None})
# file = open('symmetric_card.key', 'rb')
# key = file.read()
# file.close()
# f = Fernet(key)
# a = []
# # for i in toCheck:
# #     encrypted_card = i['card_num'].encode()
# #     print(encrypted_card)
# en = toCheck[0]['card_num'].encode()
# de = f.decrypt(en)
# print(de.decode())

for i in toCheck:
    print(type(i['card_num']))

toCheck = list(toCheck)
print(type(toCheck))
