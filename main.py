"""

"""

import os
import requests
import shutil
from multiprocessing import Pool
from collect_links import CollectLinks


import imghdr


class AutoCrawler:
    def __init__(self, skip_already_exist=True, n_threads=4, download_path='download'):
        """
        """

        self.skip = skip_already_exist
        self.n_threads = n_threads
        self.download_path = download_path

        os.makedirs('./{}'.format(self.download_path), exist_ok=True)

    @staticmethod
    def all_dirs(path):
        paths = []
        for dir in os.listdir(path):
            if os.path.isdir(path + '/' + dir):
                paths.append(path + '/' + dir)

        return paths

    @staticmethod
    def all_files(path):
        paths = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.isfile(path + '/' + file):
                    paths.append(path + '/' + file)

        return paths

    @staticmethod
    def get_extension_from_link(link, default='jpg'):
        splits = str(link).split('.')
        if len(splits) == 0:
            return default
        ext = splits[-1].lower()
        if ext == 'jpg' or ext == 'jpeg':
            return 'jpg'
        elif ext == 'gif':
            return 'gif'
        elif ext == 'png':
            return 'png'
        else:
            return default

    @staticmethod
    def validate_image(path):
        ext = imghdr.what(path)
        if ext == 'jpeg':
            ext = 'jpg'
        return ext  # returns None if not valid

    @staticmethod
    def make_dir(dirname):
        current_path = os.getcwd()
        path = os.path.join(current_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def get_keywords(keywords_file='keywords.txt'):

        with open(keywords_file, 'r') as f:
            text = f.read()
            lines = text.split('\n')
            lines = filter(lambda x: x != '' and x is not None, lines)
            keywords = sorted(set(lines))

        print('{} 个关键词: {}'.format(len(keywords), keywords))
        return keywords

    @staticmethod
    def save_object_to_file(object, file_path):
        try:
            with open('{}'.format(file_path), 'wb') as file:
                shutil.copyfileobj(object.raw, file)
        except Exception as e:
            print('存到文件 失败 - {}'.format(e))

    def download_images(self, keyword, links):
        self.make_dir('{}/{}'.format(self.download_path, keyword))
        total = len(links)

        for index, link in enumerate(links):
            try:
                print('开始下载 {} 图片: {} / {}'.format(keyword, index + 1, total))
                response = requests.get(link, stream=True)
                ext = self.get_extension_from_link(link)

                no_ext_path = '{}/{}/{}_{}'.format(self.download_path, keyword, keyword, str(index).zfill(4))
                path = no_ext_path + '.' + ext
                self.save_object_to_file(response, path)

                del response

                ext2 = self.validate_image(path)
                if ext2 is None:
                    print('Unreadable file - {}'.format(link))
                    os.remove(path)
                else:
                    if ext != ext2:
                        path2 = no_ext_path + '.' + ext2
                        os.rename(path, path2)
                        print('Renamed extension {} -> {}'.format(ext, ext2))

            except Exception as e:
                print('Download failed - ', e)
                continue

    def download(self, keyword):
        site_name = 'badiu'
        collect = CollectLinks()  # initialize chrome driver

        try:
            print('==>开始从 {} 搜索图片: {}...'.format(site_name, keyword))

            links = collect.baidu(keyword)

            print('==>开始下载所有图片... {} from {}'.format(keyword, site_name))
            self.download_images(keyword, links)

            print('Done {} : {}'.format(site_name, keyword))

        except Exception as e:
            print('Exception {}:{} - {}'.format(site_name, keyword, e))

    def do_crawling(self):
        keywords = self.get_keywords()

        tasks = []

        for keyword in keywords:
            dir_name = '{}/{}'.format(self.download_path, keyword)
            if os.path.exists(os.path.join(os.getcwd(), dir_name)) and self.skip:
                print('跳过已存在的目录 {}'.format(dir_name))
                continue

            tasks.append(keyword)

        pool = Pool(self.n_threads)
        pool.map_async(self.download, tasks)
        pool.close()
        pool.join()

        print('End 任务完成!')


if __name__ == '__main__':

    crawler = AutoCrawler()
    crawler.do_crawling()

