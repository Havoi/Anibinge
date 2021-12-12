import requests
#()
import json

import regex
from flask import Flask,render_template
app = Flask(__name__)



@app.route('/')
def recent():
	response = requests.get('https://gogoanime-api-flask.vercel.app/api/recent')
	result = response.json()
	
	latest = []
	for x in range(len(result)):
		
		anime_title = result[x]['anime_title']
		anime_code = result[x]['anime_id']
		
		output = anime_code.rpartition('-')[0]

		output3 = output.rpartition('-')[0]
		anime_poster = result[x]['anime_poster']
		latest.append({anime_title:[output3,anime_poster]})
	return render_template('recent.html', latest = latest)


@app.route('/<anime_id>')
def info(anime_id):
	response = requests.get('https://gogoanime-api-flask.vercel.app/api/anime/'+ anime_id)
	result = response.json()
	latest = []
	try:
		anime_title = result['anime_name']
		latest.append(anime_title)
		anime_poster = result['anime_poster']
		latest.append(anime_poster)
		anime_plot = result['anime_plot']
		latest.append(anime_plot)
		latest.append(anime_id)

		anime_status = result['anime_status']
		latest.append(anime_status)
		released = result['released_date']
		latest.append(released)
		total_episodes = result['total_episodes']
		latest.append(total_episodes)
		print(latest)
	except:
		pass
	return render_template('copy/index.html',latest = latest)



@app.route('/<anime_id1>/episode/<epinum>')
def watch(anime_id1,epinum):
	response = requests.get(f'https://gogoanime-api-flask.vercel.app/api/watch/{anime_id1}/{epinum}')
	result = response.json()
	episodesreq = requests.get('https://gogoanime-api-flask.vercel.app/api/anime/'+ anime_id1)
	episodejson = episodesreq.json()
	try:
		total_episodes = int(episodejson['total_episodes'])
	except: 
		pass
	episodeslist = []
	x = 1
	try:
		while True:
			if (x<=total_episodes):
				episodeslist.append(x)
				
				x = x+1
			else:
				break
	except:
		pass
	
	try:
		return render_template('watch.html', url = result[0] , episodes = episodeslist , anime_id = anime_id1)
	except:
		return "NOT FOUND"

@app.route('/search/<search_id>')
def search(search_id):
	response = requests.get('https://gogoanime-api-flask.vercel.app/api/search/'+ search_id)
	result = response.json()
	
	latest = []
	for x in range(len(result)):
		
		anime_title = result[x]['anime_title']
		anime_code = result[x]['anime_id']
		
		
		anime_poster = result[x]['anime_poster']
		latest.append({anime_title:[anime_code,anime_poster]})
	if len(latest)==0:
		return render_template('nosearch.html')
	else:
		return render_template('search.html', latest = latest)




if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = False)
