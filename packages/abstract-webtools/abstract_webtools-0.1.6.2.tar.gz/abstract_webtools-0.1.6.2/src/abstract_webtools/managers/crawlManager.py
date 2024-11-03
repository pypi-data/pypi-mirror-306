from .soupManager import *

def normalize_url(url, base_url):
    """
    Normalize and resolve relative URLs, ensuring proper domain and format.
    """
    # If URL starts with the base URL repeated, remove the extra part
    if url.startswith(base_url):
        url = url[len(base_url):]

    # Resolve the URL against the base URL
    normalized_url = urljoin(base_url, url.split('#')[0])

    # Ensure only URLs belonging to the base domain are kept
    if not normalized_url.startswith(base_url):
        return None

    return normalized_url
class crawlManager():
    def __init__(self,url=None,req_mgr=None,url_mgr=None,source_code=None,parse_type="html.parser"):
        self.url=url
        self.source_code=source_code
        self.parse_type=parse_type
        self.url_mgr = url_mgr or urlManager(url=self.url)
        self.req_mgr = requestManager(url_mgr=self.url_mgr)
        self.get_new_source_and_url(url)
    def get_new_source_and_url(self,url=None):
        if url == None:
            url = self.url
        self.response = self.req_mgr.response
        self.source_code=self.req_mgr.source_code
    def get_classes_and_meta_info():
        class_name_1,class_name_2, class_value = 'meta','class','property','og:image'
        attrs = 'href','src'
        unique_classes, images=discover_classes_and_images(self,tag_name,class_name_1,class_name_2,class_value,attrs)
        return unique_classes, images
    def extract_links_from_url(self):
        """
        Extracts all href and src links from a given URL's source code.

        Args:
            base_url (str): The URL from which to extract links.

        Returns:
            dict: Dictionary containing image links and external links under the parent page.
        """
        agg_js = {'images':[],'external_links':[]}
        
        if self.response != None:
            attrs = 'href','src'
            href_links,src_links='',''
            links = [href_links,src_links]
            for i,each in enumerate(attrs):
                 links[i]= [a[attr[i]] for a in get_find_all_with_attributes(self, attrs[i])]
            # Convert all links to absolute links
            absolute_links = [(url, link) for link in links[0] + links[1]]
            # Separate images and external links
            images = [link for link in absolute_links if link.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
            external_links = [link for link in absolute_links if urlparse(link).netloc != urlparse(url).netloc]
            agg_js['images']=images
            agg_js['external_links']=external_links
           
        return agg_js
    def get_all_website_links(self,tag="a",attr="href") -> list:
        """
        Returns all URLs that are found on the specified URL and belong to the same website.

        Args:
            url (str): The URL to search for links.

        Returns:
            list: A list of URLs that belong to the same website as the specified URL.
        """
        all_urls=[self.url_mgr.url]
        domain = self.url_mgr.domain
        all_attribs = get_attribs(self.url_mgr.url)
        for href in all_attribs.get('href',[]):
            if href == "" or href is None:
                # href empty tag
                continue
            href=self.url_mgr.get_relative_href(self.url_mgr.url,href)
            if not self.url_mgr.is_valid_url(href):
                # not a valid URL
                continue
            if href in all_urls:
                # already in the set
                continue
            if domain not in href:
                # external link
                continue
            all_urls.append(href)
                  
        return all_urls

    def correct_xml(xml_string):
        # Parse the XML string
        root = ET.fromstring(xml_string)

        # Loop through each <image:loc> element and correct its text if needed
        for image_loc in root.findall(".//image:loc", namespaces={'image': 'http://www.google.com/schemas/sitemap-image/1.1'}):
            # Replace '&' with '&amp;' in the element's text
            if '&' in image_loc.text:
                image_loc.text = image_loc.text.replace('&', '&amp;')

        # Convert the corrected XML back to string
        corrected_xml = ET.tostring(root, encoding='utf-8').decode('utf-8')
        return corrected_xml


    def determine_values(self,url=None):
        # This is just a mockup. In a real application, you'd analyze the URL or its content.
        url = url or self.url
        # Assuming a blog site
        if 'blog' in url:
            if '2023' in url:  # Assuming it's a current year article
                return ('weekly', '0.8')
            else:
                return ('monthly', '0.6')
        elif 'contact' in url:
            return ('yearly', '0.3')
        else:  # Homepage or main categories
            return ('weekly', '1.0')
    def crawl(self,url, max_depth=3, depth=1):
        visited=set()
        if depth > max_depth:
            return []

        if url in visited:
            return []

        visited.add(url)

        try:
            soup = get_soup(url)
            links = [a['href'] for a in soup.find_all('a', href=True)]
            valid_links = []

            for link in links:
                parsed_link = urlparse(link)
                base_url = "{}://{}".format(parsed_link.scheme, parsed_link.netloc)
            
                if base_url == url:  # Avoiding external URLs
                    final_link = urljoin(url, parsed_link.path)
                    if final_link not in valid_links:
                        valid_links.append(final_link)

            for link in valid_links:
                crawl(link, max_depth, depth+1)

            return valid_links

        except Exception as e:
            print(f"Error crawling {url}: {e}")
            return []


    # Define or import required functions here, like get_all_website_links, determine_values, 
    # discover_classes_and_meta_images, and extract_links_from_url.
    def get_meta_info(self,url=None):
        url = url or self.url
        soup_mgr = soupManager(url=url)
        meta_info = {}
        # Fetch the title if available
        meta_tags = soup_mgr.find_all("meta")
        url = eatAll(str(url),['',' ','\n','\t','\\','/'])
        attribs = get_attribs(url)
        soup = get_soup(url)
        
        for meta_tag in meta_tags:
            for attr, values in meta_tag.attrs.items():
                
                if attr not in meta_tag:
                    meta_tag[attr] = []
                if values not in meta_tag[attr]:
                    meta_tag[attr].append(values)
        title_tag = soup.find_all("title")
        if title_tag:
            meta_info["title"] = title_tag
        # Fetch meta tags
        for meta_tag in soup.find_all('meta'):
            name = meta_tag.get('name') or meta_tag.get('property')
            if name:
                content = meta_tag.get('content')
                if content:
                    meta_info[name] = content

        return meta_info
    def generate_sitemap(self,domain):
        
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            string = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            
            for url in self.get_all_website_links():
                string += f'  <url>\n    <loc>{url}</loc>\n'
                preprocess=[]
                self.get_new_source_and_url(url=url)
                links = get_attribs(url)
                images = [link for link in links if link.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]

                for img in images:
                    if str(img).lower() not in preprocess:
                        try:
                            escaped_img = img.replace('&', '&amp;')

                            str_write = f'    <image:image>\n      <image:loc>{escaped_img}</image:loc>\n    </image:image>\n'
                            string += str_write
                        except:
                            pass
                        preprocess.append(str(img).lower())
                frequency, priority = self.determine_values(url)
                string += f'    <changefreq>{frequency}</changefreq>\n'
                string += f'    <priority>{priority}</priority>\n'
                string += f'  </url>\n'
                
            string += '</urlset>\n'
            f.write(string)            
        # Output summary
        print(f'Sitemap saved to sitemap.xml with {len(urls)} URLs.')
        
        # Output class and link details
        for url in urls:
            print(f"\nDetails for {url}:")
            classes, meta_img_refs = discover_classes_and_meta_images(url)

            print("\nClasses with href or src attributes:")
            for class_name in classes:
                print(f"\t{class_name}")
            
            print("\nMeta Image References:")
            for img_ref in meta_img_refs:
                print(f"\t{img_ref}")
            
            links = extract_links_from_url(url)

            print("\nImages:")
            for img in links['images']:
                print(f"\t{img}")
            
            print("\nExternal Links:")
            for ext_link in links['external_links']:
                print(f"\t{ext_link}")

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
    url = get_url(url=url,url_mgr=url_mgr)
    url_mgr = get_url(url=url,url_mgr=url_mgr)
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
