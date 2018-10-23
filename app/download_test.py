# -*- coding: utf-8 -*-

import os
import re
import requests
from selenium import webdriver




class Wy_music():
    def __init__(self, name):
        self.url_temp = 'http://music.163.com/song/media/outer/url?id={}.mp3'
        # self.url_temp = 'http://music.163.com/song/media/outer/url?id=516847399.mp3'
        self.driver = webdriver.Chrome()
        self.i_list = []
        self.id_list = []
        self.name_list = []
        self.music_name = name


    def get_id_name(self):
        self.driver.get('https://music.163.com/#/search/m/?s=%s&type=1' % self.music_name)
        # self.driver.get('https://music.163.com/'.format(self.music_name))
        self.driver.switch_to.frame('contentFrame')
        div_list = self.driver.find_elements_by_xpath('.//div[@class="srchsongst"]/div')
        print(len(div_list))


        for div in div_list:
            name = div.find_element_by_xpath('.//div[@class="text"]//b').text
            url = div.find_element_by_xpath('.//div[@class="td w0"]//a').get_attribute('href')
            id = re.search(r'id=(\d+)', url).group(1)
            singer = div.find_element_by_xpath('.//div[@class="td w1"]//a').text
            i = div_list.index(div)
            self.i_list.append(i)
            self.id_list.append(id.encode('utf-8'))
            # self.name_list.append(name + "_".decode('utf-8') + singer)
            self.name_list.append(name.encode('utf-8') + "_" + singer.encode('utf-8'))
            print("no: %d, name:%s, singer:%s, id=%s" % (i, name, singer, id))



        # for v in self.name_list:
        #     print(v)
        # name_dict = dict(zip(self.id_list, self.name_list))
        # name_list = dict(zip(self.id_list, self.name_list))
        # print('id_name字典:',  name_dict.)
        # print("id_name 字典:")
        # for k, v in name_dict.items():
        #     print("%s, %s" % (k, v))

        song_dict = {}
        for i in self.i_list:
            id_name_list = []
            id_name_list.append(self.id_list[i])
            id_name_list.append(self.name_list[i])
            song_dict[i] = id_name_list



        # song_dict = dict(zip(self.i_list, ))
        # print('最终id_歌曲字典', song_dict)
        # self.driver.close()
        # print("最终id_歌曲字典 字典:")
        # for k, v in song_dict.items():
        #     print("%s, %s, %s" % (k, v[0], v[1]))

        # self.driver.quit()
        return song_dict


    def download_music(self, url, song_name):
        print('{}正在下载'.format(song_name))
        response = requests.get(url)
        # full_songname = song_name + '.mp3'
        full_songname = song_name + '_.mp3'
        with open(r'D:\MusicWorld\MusicK\app\%s' % (full_songname.decode('utf-8')), 'wb') as f:
            f.write(response.content)
            print('{}下载完成'.format(full_songname))


    def choose_musicid(self, song_dict):
        # num_str = '1'
        num_str = raw_input('请输入你需要下载歌曲的编号,以空格隔开： ')
        num_list = num_str.split(' ')
        for num in num_list:
            try:
                num = int(num)
            except Exception as e:
                print(e, '请输入整数')
            if num > len(song_dict):
                print('请输入有效数字')
            url = self.url_temp.format(song_dict[num][0])
            print("url:%s" % url)
            song_name = song_dict[num][1]
            # print('歌曲名——歌手名',song_name)
            yield url,song_name




if __name__ == '__main__':
    name = raw_input('请输入你要搜索的歌名或歌手:')
    # name = '邓紫棋'
    print("test: %s" % name)
    wy = Wy_music(name)
    song_dict = wy.get_id_name()
    for url, song_name in wy.choose_musicid(song_dict):
        wy.download_music(url, song_name)
    wy.driver.quit()