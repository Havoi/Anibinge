from os import error
import requests
#()
from flask import Flask,render_template
from werkzeug.datastructures import ResponseCacheControl
app = Flask(__name__)
import Anim_links


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
	# response = requests.get(f'https://gogoanime-api-flask.vercel.app/api/watch/{anime_id1}/{epinum}')
	# result = response.json()
	main_episode_and_animecode = f"{anime_id1}-episode-{epinum}"
	response = Anim_links.main(main_episode_and_animecode)
	print(response)
	# result = response.json()
	# print(result)
	episodesreq = requests.get('https://gogoanime-api-flask.vercel.app/api/anime/'+ anime_id1)
	episodejson = episodesreq.json()
	try:
		total_episodes = int(episodejson['total_episodes'])
	except: 
		pass
	episodeslist = []
	x = 1
	epinum = int(epinum)
	try:
		while True:
			if (x<=total_episodes):
				
				if (x==epinum):
					episodeslist.append({x:"btnn btnn4"})
					
					x = x+1
					pass
				elif (x!= epinum):
					episodeslist.append({x:"btnn btnn1"})
					x = x+1
			else:
				break
	except:
		pass
	
	print(episodeslist)
	
	print(response)
	try:
		return render_template('watch.html', url = response , episodes = episodeslist , anime_id = anime_id1)
	except error as e:
		return e

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
	app.run(port = '8000' , debug = True)