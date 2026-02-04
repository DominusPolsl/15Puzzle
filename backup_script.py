import os
from datetime import datetime

timeNow = datetime.now()
timeStamp = timeNow.strftime("%Y%m%d_%H%M")
projektDir = os.path.dirname(os.path.abspath(__file__))
fileName = f"raport_{timeStamp}.html"
fullPath = os.path.join(projektDir, f"Backup/{fileName}")

folderIn = os.path.join(projektDir, "In")
folderOut = os.path.join(projektDir, "Out")
 

html = f"<h1 style='text-align: center'>Report<br>{timeNow.strftime('Date %d.%m.%Y | Time %H:%M')}</h1><table align='center' border='1'><tr><th>In</th><th>Out</th></tr>"

if os.path.exists(folderIn):
    filesList = sorted(os.listdir(folderIn))
    
    for plik in filesList:
        pathIn = os.path.join(folderIn, plik)
        with open(pathIn, "r") as f:
            raw = f.read().strip()
            numbers = raw.split(',')
            

            miniTable = "<table style='border-collapse: collapse; border: 1px solid #333;'>"
            for i in range(0, 16, 4):
                miniTable += "<tr>"
                wiersz = numbers[i:i+4]
                for num in wiersz:
                    miniTable += f"<td style='border: 1px solid #999; padding: 5px; text-align: center; width: 25px; height: 25px;'>{num.strip()}</td>"
                miniTable += "</tr>"
            miniTable += "</table>"

        nazwa_wyniku = f"{plik[:-4]}_out.txt"
        pathOut = os.path.join(folderOut, nazwa_wyniku)

        with open(pathOut, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for linia in lines:
                if "Blank" in linia:
                    stepsArrows = "Steps required to solve:<br>"
                    zeroPositions = [int(s) for s in linia[linia.index(':')+1:].strip().split("->")]
                    prevPos = zeroPositions[0]
                    lineCapacity = len(zeroPositions) // 7
                    rawLength = 0
                    
                    for pos in zeroPositions[1:]:
                        rawLength += 1
                        if pos > prevPos:
                            if pos // 4 > prevPos // 4:
                                stepsArrows += "⬆️"
                            elif pos // 4 < prevPos // 4:
                                stepsArrows += "⬇️"
                            else:
                                stepsArrows += "⬅️"
                        else:
                            if pos // 4 > prevPos // 4:
                                stepsArrows += "⬆️"
                            elif pos // 4 < prevPos // 4:
                                stepsArrows += "⬇️"
                            else:
                                stepsArrows += "➡️"
                        if rawLength >= lineCapacity:
                            stepsArrows += "<br>"
                            rawLength = 0
                        prevPos = pos
                if "Number" in linia:
                    stepsCount = linia.split(":")[1].strip()
                if "Solution" in linia:
                    timeEvaul = linia.split(":")[1].strip()
            stepsArrCount = stepsArrows + "<br>" + "Number of moves: " + stepsCount + "<br>" + "Execution time: " + timeEvaul + "s"
        html += f"<tr><td style='text-align: center; vertical-align: middle'>{miniTable}</td><td style='text-align: left; vertical-align: middle; padding-left: 20px'>{stepsArrCount}</td></tr>"

html += "</table>"

if not os.path.exists(fullPath):
    with open(fullPath, "w", encoding="utf-8") as f:
        f.write(html)
with open(projektDir + "/LastRaport.html", 'w', encoding="utf-8") as fw:
    fw.write(html)