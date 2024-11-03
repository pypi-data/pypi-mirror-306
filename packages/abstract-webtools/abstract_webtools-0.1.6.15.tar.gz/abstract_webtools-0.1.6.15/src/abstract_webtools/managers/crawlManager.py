from .soupManager import * #.soupManager import *
from urllib.parse import urlparse, urljoin
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class crawlManager:
    def __init__(self, url=None, req_mgr=None, url_mgr=None, source_code=None, parse_type="html.parser"):
        self.url = url
        self.source_code = source_code
        self.parse_type = parse_type
        self.url_mgr = url_mgr or urlManager(url=self.url)
        self.req_mgr = req_mgr or requestManager(url_mgr=self.url_mgr)
        self.get_new_source_and_url(url)

    def get_new_source_and_url(self, url=None):
        """Fetches new source code and response for a given URL."""
        if url is None:
            url = self.url
        self.req_mgr.set_url(url)
        self.source_code = self.req_mgr.source_code
        self.response = self.req_mgr.response

    def get_classes_and_meta_info(self):
        """Returns unique classes and image links from meta tags."""
        tag_name = 'meta'
        class_name_1, class_name_2 = 'class', 'property'
        class_value = 'og:image'
        attrs = ['href', 'src']
        unique_classes, images = discover_classes_and_images(self, tag_name, class_name_1, class_name_2, class_value, attrs)
        return unique_classes, images

    def extract_links_from_url(self, url=None):
        """Extracts all href and src links from a given URL's source code."""
        url = url or self.url_mgr.url
        soup = BeautifulSoup(self.source_code, self.parse_type)
        links = {'images': [], 'external_links': []}

        if self.response:
            for attr in ['href', 'src']:
                for tag in soup.find_all(attrs={attr: True}):
                    link = tag.get(attr)
                    if link:
                        absolute_link = urljoin(url, link)
                        if link.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                            links['images'].append(absolute_link)
                        elif urlparse(absolute_link).netloc != urlparse(url).netloc:
                            links['external_links'].append(absolute_link)
        
        return links

    def get_all_website_links(self):
        """Finds all internal links on the website that belong to the same domain."""
        all_urls = [self.url_mgr.url]
        domain = self.url_mgr.domain
        all_attribs = get_all_attribute_values(self.url_mgr.url)
        
        for href in all_attribs.get('href', []):
            if not href or not self.url_mgr.is_valid_url(href):
                continue
            full_url = urljoin(self.url_mgr.url, href)
            if domain in full_url and full_url not in all_urls:
                all_urls.append(full_url)
        
        return all_urls

    def correct_xml(self, xml_string):
        """Corrects XML by encoding special characters in <image:loc> tags."""
        root = ET.fromstring(xml_string)
        for image_loc in root.findall(".//image:loc", namespaces={'image': 'http://www.google.com/schemas/sitemap-image/1.1'}):
            if '&' in image_loc.text:
                image_loc.text = image_loc.text.replace('&', '&amp;')
        return ET.tostring(root, encoding='utf-8').decode('utf-8')

    def determine_values(self, url=None):
        """Determines frequency and priority based on URL type."""
        url = url or self.url
        if 'blog' in url:
            return ('weekly', '0.8') if '2023' in url else ('monthly', '0.6')
        elif 'contact' in url:
            return ('yearly', '0.3')
        return ('weekly', '1.0')

    def crawl(self, url, max_depth=3, depth=1, visited=None):
        """Recursively crawls the site up to max_depth and returns valid internal links."""
        visited = visited or set()
        if depth > max_depth or url in visited:
            return []

        visited.add(url)
        try:
            soup = get_soup(url)
            links = []
            for tag in soup.find_all('a', href=True):
                link = urljoin(url, tag['href'])
                if urlparse(link).netloc == urlparse(url).netloc and link not in visited:
                    links.append(link)
                    self.crawl(link, max_depth, depth + 1, visited)
            return links
        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return []

    def get_meta_info(self, url=None):
        """Fetches metadata, including title and meta tags, from the page."""
        url = url or self.url
        soup = BeautifulSoup(self.source_code, self.parse_type)
        meta_info = {"title": None, "meta_tags": {}}
        
        title_tag = soup.find("title")
        if title_tag:
            meta_info["title"] = title_tag.text

        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_info["meta_tags"][name] = content

        return meta_info

    def generate_sitemap(self):
        """Generates a sitemap.xml file with URLs, images, change frequency, and priority."""
        urls = self.get_all_website_links()
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" ')
            f.write('xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n')

            for url in urls:
                f.write(f'  <url>\n    <loc>{url}</loc>\n')
                frequency, priority = self.determine_values(url)
                f.write(f'    <changefreq>{frequency}</changefreq>\n')
                f.write(f'    <priority>{priority}</priority>\n')

                images = [img for img in self.extract_links_from_url(url)['images']]
                for img in images:
                    escaped_img = img.replace('&', '&amp;')
                    f.write(f'    <image:image>\n      <image:loc>{escaped_img}</image:loc>\n    </image:image>\n')

                f.write('  </url>\n')

            f.write('</urlset>\n')
        
        print(f'Sitemap saved to sitemap.xml with {len(urls)} URLs.')

class crawlManagerSingleton():
    _instance = None
    @staticmethod
    def get_instance(url=None,source_code=None,parse_type="html.parser"):
        if crawlManagerSingleton._instance is None:
            crawlManagerSingleton._instance = CrawlManager(url=url,parse_type=parse_type,source_code=source_code)
        elif parse_type != crawlManagerSingleton._instance.parse_type or url != crawlManagerSingleton._instance.url  or source_code != crawlManagerSingleton._instance.source_code:
            crawlManagerSingleton._instance = CrawlManager(url=url,parse_type=parse_type,source_code=source_code)
        return crawlManagerSingleton._instance
def get_crawl_mgr(url=None,req_mgr=None,url_mgr=None,source_code=None,parse_type="html.parser"):
    
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
    url = get_url(url=url,url_mgr=url_mgr)
    req_mgr=get_req_mgr(url=url,url_mgr=url_mgr,source_code=source_code)
    source_code = get_source(url=url,url_mgr=url_mgr,source_code=source_code,req_mgr=req_mgr)
    soup_mgr = get_soup_mgr(url=url,url_mgr=url_mgr,source_code=source_code,req_mgr=req_mgr,parse_type=parse_type)
    crawl_mgr = crawlManager(url=url,req_mgr=req_mgr,url_mgr=url_mgr,source_code=source_code,parse_type=parse_type)
    return crawl_mgr
def get_domain_crawl(url=None,req_mgr=None,url_mgr=None,source_code=None,parse_type="html.parser",max_depth=3, depth=1):
    crawl_mgr = get_crawl_mgr(url=url,req_mgr=req_mgr,url_mgr=url_mgr,source_code=source_code,parse_type=parse_type)
    url = get_url(url=url,url_mgr=url_mgr)
    all_domain_links = crawl_mgr.crawl(url=url, max_depth=max_depth, depth=depth)
    return all_domain_links
