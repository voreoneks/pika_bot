import re
import time
import requests
import sys
import random
from fake_useragent import UserAgent
from accessify import private

class Channel():
	def __init__(self, channel_url:str) -> None:
		self.channel_url = channel_url.rstrip()
		self.video_links = self.find_videos_url()
		if not isinstance(self.channel_url, str):
			print('Error. "channel_url" must be stroke type.')
			sys.exit(1)

	@private
	def __get_list_url__(self, channel_url:str, headers_:dict) -> str:
		url = channel_url
		url += '/videos'
		page = requests.get(url, headers=headers_)
		html = page.text
		pattern = re.compile(r'list=........................')
		time.sleep(3)
		list_part = pattern.findall(html)
		try:
			list_url = 'https://www.youtube.com/playlist?' + list_part[0] + '&playnext=1&index='
			return list_url
		except IndexError as er:
			print(er, '\nNo videos on channel.')
			sys.exit(1)
			

	@private
	def __get_videos_url__(self, list_url_:str, headers_:dict) -> set:
		url = list_url_
		page = requests.get(url, headers=headers_)
		html = page.text
		pattern_total = re.compile(r'totalVideos":\d*')
		found_total = pattern_total.findall(html)
		total_videos = int(found_total[0].split(':')[1])
		pattern_list = re.compile(r'/watch\?v=.................list')
		videos_url = set()

		for i in range(0, total_videos, 78):
			url = list_url_ + str(i + 1)
			page = requests.get(url, headers=headers_)
			html = page.text
			found_list = pattern_list.findall(html)
			for item in found_list:
				link = 'https://www.youtube.com' + item.split('\\')[0]
				videos_url.add(link)
				
		return videos_url

	def find_videos_url(self) -> set:
		ua = UserAgent()
		user_agent = ua.random
		headers = {
				"User-Agent": user_agent,
				'x-youtube-client-name': '1',
				'x-youtube-client-version': '2.20200429.03.00',
				}
		list_url = self.__get_list_url__(self.channel_url, headers)
		self.videos_url = self.__get_videos_url__(list_url, headers)
		return tuple(self.videos_url)

	def get_click_list(self, num_watch_per:int, num_click_per:int):
		self.num_watch = int(len(self.video_links) / 100 * num_watch_per)
		self.num_click = int(self.num_watch / 100 * num_click_per)
		self.click_list = random.sample(range(0, self.num_watch + 1), self.num_click)
		return self.click_list

	def __str__(self):
		return self.channel_url

