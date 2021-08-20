import re

question = " 97 Cykloheximid är ett bakterietoxin som hämmar proteinsyntes genom att det blockerar ribosomens E-site. Hur påverkas proteinsyntesen av cykloheximid?"

question = re.sub(r"^\s", "QUESTION ", question)

print(question)
