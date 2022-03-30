import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from tabulate import tabulate

def add_opponent_results_for_week(weekNum, table):
	try:
		URL = "https://www.leaguesecretary.com/bowling-centers/mockingbird-lanes-omaha-nebraska/bowling-leagues/tuesday-men-2021-2022/team/recap-sheet/code-fellows/2021/Fall/" + str(weekNum) + "/55982/15"
		page = requests.get(URL)

		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find_all("table", class_="rgMasterTable")

		opponentTable = results[1].find('tbody')
		opponentTableRows = opponentTable.find_all('tr')
		opponentStrengths = ['Week ' + str(weekNum),'-','-','-','-','-']

		if len(opponentTableRows) > 5:
			return

		for row in opponentTableRows:
			columns = row.find_all('td')
			position = int(columns[0].get_text())
			average = int(columns[3].get_text())
			series = int(columns[8].get_text())

			if series == 0:
				opponentStrengths[position] = "-10"
			else:
				todayAverage = round(series / 3)
				strength = todayAverage - average
				opponentStrengths[position] = str(strength)

		table.append(opponentStrengths)
		print('done week ' + str(weekNum))

	except:
		return

def add_results_for_week(weekNum, table):
	try:
		URL = "https://www.leaguesecretary.com/bowling-centers/mockingbird-lanes-omaha-nebraska/bowling-leagues/tuesday-men-2021-2022/team/recap-sheet/code-fellows/2021/Fall/" + str(weekNum) + "/55982/15"
		page = requests.get(URL)
		
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find_all("table", class_="rgMasterTable")

		ourTable = results[0].find('tbody')
		ourTableRows = ourTable.find_all('tr')
		ourStrengths = ['Week ' + str(weekNum),'-','-','-','-','-']
		
		for row in ourTableRows:
			columns = row.find_all('td')
			position = int(columns[0].get_text())
			average = int(columns[3].get_text())
			series = int(columns[8].get_text())

			if series == 0:
				continue
			else:
				todayAverage = round(series / 3)
				strength = todayAverage - average
				#rage quit
				if strength > -100:
					ourStrengths[position] = str(strength)

		table.append(ourStrengths)
		print('done week ' + str(weekNum))

	except:
		return

def add_plot_results_for_week(weekNum, plotArrays):
	try:
		URL = "https://www.leaguesecretary.com/bowling-centers/mockingbird-lanes-omaha-nebraska/bowling-leagues/tuesday-men-2021-2022/team/recap-sheet/code-fellows/2021/Fall/" + str(weekNum) + "/55982/15"
		page = requests.get(URL)
		
		soup = BeautifulSoup(page.content, "html.parser")
		results = soup.find_all("table", class_="rgMasterTable")

		ourTable = results[0].find('tbody')
		ourTableRows = ourTable.find_all('tr')
		ourStrengths = ['Week ' + str(weekNum),'-','-','-','-','-']
		
		playerPosition = 0
		for row in ourTableRows:
			columns = row.find_all('td')
			position = int(columns[0].get_text())
			average = int(columns[3].get_text())
			series = int(columns[8].get_text())
			
			if series == 0:
				plotArrays[playerPosition].append(average - 10)
			else:
				todayAverage = round(series / 3)

				#rage quit
				if series < 200:
					plotArrays[playerPosition].append(series)
				else:
					plotArrays[playerPosition].append(todayAverage)

			playerPosition = playerPosition + 1

		print('done week ' + str(weekNum))

	except:
		print('bad')
		return

def get_total_strength(table, index):
	total = 0
	count = 0

	for row in table:
		if row[index] != '-':
			parsedValue = int(row[index])
			total += parsedValue
			count += 1
			
	return str(round(total / count))

"""
# opponent strength
table = []

for x in range(0,32):
	add_opponent_results_for_week(x + 1, table);

print(tabulate(table, headers=['', 'Chandler', 'Mike', 'Ryan', 'Ron', 'Nick'], tablefmt="fancy_grid"))

print("Average Opponent Strength")
print("Chandler:  " + get_total_strength(table, 1))
print("Mike:      " + get_total_strength(table, 2))
print("Ryan:      " + get_total_strength(table, 3))
print("Ron:       " + get_total_strength(table, 4))
print("Nick:      " + get_total_strength(table, 5))

# team strength
table = []

for x in range(0,32):
	add_results_for_week(x + 1, table);

print(tabulate(table, headers=['', 'Chandler', 'Mike', 'Ryan', 'Ron', 'Nick'], tablefmt="fancy_grid"))

print("Average Performance")
print("Chandler:  " + get_total_strength(table, 1))
print("Mike:      " + get_total_strength(table, 2))
print("Ryan:      " + get_total_strength(table, 3))
print("Ron:       " + get_total_strength(table, 4))
print("Nick:      " + get_total_strength(table, 5))
"""

# average chart
plotArrays = [[],[],[],[],[]]

for x in range(0,32):
	add_plot_results_for_week(x+1, plotArrays);

x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
y0 = plotArrays[0]
y1 = plotArrays[1]
y2 = plotArrays[2]
y3 = plotArrays[3]
y4 = plotArrays[4]

plt.plot(x, y0, label='Chandler', marker='o', markersize=4)
plt.plot(x, y1, label='Mike', marker='o', markersize=4)
plt.plot(x, y2, label='Ryan', marker='o', markersize=4)
plt.plot(x, y3, label='Ron', marker='o', markersize=4)
plt.plot(x, y4, label='Nick', marker='o', markersize=4)
plt.axis([1, 32, 0, 300])
plt.xlabel("Week")
plt.ylabel("Average")
plt.title("Average per week")

plt.grid()
plt.legend()
plt.show()




