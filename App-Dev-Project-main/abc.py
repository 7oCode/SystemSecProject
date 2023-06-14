import re

a = re.search("""[!@#$%^&*()_+-={}|<>?,./;':`~\][0-9]""", "1abc")
if a:
    print("yes")
else:
    print("no")
