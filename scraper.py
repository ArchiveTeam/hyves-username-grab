#!/usr/bin/python
import random
import re
import sys
import time
import traceback
import urllib
import urllib2


user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36'


class NoPager(Exception):
    pass


def sleep(seconds=0.75):
    sleep_time = seconds * random.uniform(0.5, 2.0)
    time.sleep(sleep_time)


def pager(hostname, name, page_number, extra):
    '''Makes a request to Hyves pager.'''
    url = 'http://{0}/index.php?xmlHttp=1&module=pager&action=showPage&name={1}'\
        .format(hostname, name)
    post_data = {
        'pageNr': page_number,
        'config': 'hyvespager-config.php',
        'showReadMoreLinks': 'false',
        'extra': extra
    }
    headers = {
        'User-Agent': user_agent
    }

    for dummy in xrange(10):
        content = ''
        try:
            request = urllib2.Request(url, urllib.urlencode(post_data), headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except urllib2.HTTPError as error:
            status_code = error.code
        else:
            status_code = response.getcode()

        if status_code == 403 or status_code == 500 or 'Try again in a moment' in content:
            sleep_time = 10
            print 'Hyves angered (code', status_code, ') Sleep for', sleep_time, 'seconds.'
            time.sleep(sleep_time)
        elif status_code != 200:
            print 'Unexpected error. (code', status_code, '.) Retrying.'
            sleep(seconds=5)
        else:
            return content

    raise Exception('Unable to fetch page')


def scrape_pager(content):
    '''Scrapes the pager params from html'''
    match = re.search(r"name: '([^']+)'.+?nrPages: ([0-9]+).+?extra: '([^']+)'",
        content, re.DOTALL)

    if not match:
        raise NoPager("Pager parameters not found")

    name = match.group(1)
    num_pages = match.group(2)
    extra = match.group(3)

    return {
        'name': name,
        'num_pages': int(num_pages),
        'extra': extra
    }


def fetch_content_page(username, category_name):
    while True:
        print 'Fetch', username, category_name

        headers = {
            'User-Agent': user_agent
        }
        url = 'http://{0}.hyves.nl/{1}'.format(username, category_name)
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except urllib2.HTTPError as error:
            status_code = error.code
            content = ""
        else:
            status_code = response.getcode()
        
        if status_code == 403 or status_code == 500 or 'Try again in a moment' in content:
            sleep_time = 10
            print 'Hyves angered (code', status_code, ') Sleep for', sleep_time, 'seconds.'
            time.sleep(sleep_time)
            continue # retry
        elif status_code != 200 and status_code != 404:
            print 'Unexpected error. (code', status_code, '.) Retrying.'
            sleep(seconds=5)
            continue # retry
        
        pager_params = scrape_pager(content)

        yield content

        print 'Pages=', pager_params['num_pages'], 'Name=', pager_params['name']

        for page_num in xrange(1, pager_params['num_pages'] + 1):
            print 'Page', page_num
            content = pager('{0}.hyves.nl'.format(username), pager_params['name'],
                page_num, pager_params['extra'])
            yield content
            sleep()
        
        break # done


def fetch_main_content_page(username, pager_name):
    while True:
        print 'Fetch', username, pager_name

        headers = {
            'User-Agent': user_agent
        }
        url = 'http://{0}.hyves.nl/'.format(username, category_name)
        
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
        except urllib2.HTTPError as error:
            status_code = error.code
            content = ""
        else:
            status_code = response.getcode()
        
        if status_code == 403 or status_code == 500 or 'Try again in a moment' in content:
            sleep_time = 10
            print 'Hyves angered (code', status_code, ') Sleep for', sleep_time, 'seconds.'
            time.sleep(sleep_time)
            continue # retry
        elif status_code != 200 and status_code != 404:
            print 'Unexpected error. (code', status_code, '.) Retrying.'
            sleep(seconds=5)
            continue # retry

        pager_params = scrape_pager(content)

        if pager_params['name'] == pager_name:
            yield content

            print 'Pages=', pager_params['num_pages'], 'Name=', pager_name

            for page_num in xrange(1, pager_params['num_pages'] + 1):
                print 'Page', page_num
                content = pager('{0}.hyves.nl'.format(username), pager_name,
                    page_num, pager_params['extra'])
                yield content
                sleep()
        else:
            raise NoPager("Pager parameters not found")
        
        break # done


def friendly_error_msg(error):
    if isinstance(error, NoPager):
        print 'Profile page is private (NoPager). Continuing.'
    elif isinstance(error, urllib2.HTTPError) and error.code == 404:
        print 'No user/group members discovered on this page (404). Continuing.'
    else:
        traceback.print_exc(limit=1)


if __name__ == '__main__':
    username = sys.argv[1]
    filename = sys.argv[2]

    for category_name in ['vrienden', 'leden']:
        with open('{0}.{1}.txt'.format(filename, category_name), 'w') as out_file:
            try:
                for content in fetch_content_page(username, category_name):
                    out_file.write(content)
            except (urllib2.HTTPError, NoPager) as error:
               friendly_error_msg(error)

    with open('{0}.hyves.txt'.format(filename), 'w') as out_file:
        try:
            for content in fetch_main_content_page(username, 'publicgroups_default_redesign'):
                out_file.write(content)
        except (urllib2.HTTPError, NoPager) as error:
            friendly_error_msg(error)
