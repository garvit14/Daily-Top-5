# By Garvit Gupta
# List of today's top 5 songs is fetched from gaana.com
import bs4 as bs
import urllib
import os.path
import sys
from google import search
import progressbar

print('Downloading your songs!!')

#takes path as command line argument
#If no argument is given, saves to directory in which script is run
if(len(sys.argv)>1):
	loc = sys.argv[1]
else:
	loc=''
print('Saving to : '+loc)
#function to download the song
def download(source_url):
	sauce = urllib.urlopen(source_url)
	soup=bs.BeautifulSoup(sauce,'lxml')
	for url in soup.find_all('a',class_='btndown'):
		song_url = url.get('href')
		name = song_url.split('/')[-1]
		print(name)
		if os.path.isfile(loc+name):
			print('Song already downloaded')
			return
		f=open(loc+name,'wb')
		u=urllib.urlopen(song_url)
		size = int(u.info().getheader("Content-Length"))
		print('size : '+str((float(size)/1024)/1024)+' MB')
		block_size=81920
		file_size=0
		pbar.start()
		while True:
			buffer = u.read(block_size)
			if not buffer:
				break
			file_size+=len(buffer)
			f.write(buffer)
			p=float(file_size)/size;
			pbar.update(int(p*100))
		pbar.finish()
		break;

sauce = urllib.urlopen('https://gaana.com/playlist/gaana-dj-todays-top-5-hindi')
soup = bs.BeautifulSoup(sauce,'lxml')
dict={}

# getting the top 5 songs
for div in soup.find_all('div',class_='playlist_thumb_det'):
	for url in div.find_all('a'):
		key = url.get('data-value')
		if dict.get(key):
			dict[key] = dict[key] + ' ' + url.text
		else:
			dict[key] = url.text

#dictionary contains song names with artists :-)
pbar = progressbar.ProgressBar(maxval=100) #to show progress
for val in dict.values():
	query=val + ' mp3 song free download raagjatt' #using raagjatt.com to download the mp3 song
	found=0;
	for j in search(query, tld='co.in',num=5,stop=1,pause=2):
		if 'raagjatt' in j:
			# download this song
			download(j)
			found=1;
	if found==0:
		print('Not found : '+val)
	print('\n')
