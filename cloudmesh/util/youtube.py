import requests
from pprint import pprint
from cloudmesh_common.util import dotdict



class youtube:
    """
    gets information from public youtube videos
            
    video = youtube('CwHFaluDgzc')
    
    print video
    print video.title
    """

    
    def __init__(self, id, filename=None):

        try:
            r = requests.get('https://gdata.youtube.com/feeds/api/videos/{0}?alt=json'.format(str(id)))
            self.entry = dotdict(r.json()["entry"])
            self.entry["found"] = "ok"
        except:
            self.entry = dotdict()
            self.entry.title= {'$t': None}
            self.entry.content = {'$t': None}
            self.entry.id = {'$t': 'https://gdata.youtube.com/feeds/api/videos/{0}?alt=json'.format(str(id))}
            self.entry.updated = {'$t': None}
            self.entry["found"] = "-"

        self.entry["watch"] = "https://www.youtube.com/watch?v={0}".format(str(id))
        self.entry["filename"] = filename
        self.entry['number'] = id

    @property
    def filename(self):
        return self.entry.filename

    @property
    def found(self):
        return self.entry.found

    @filename.setter
    def filename(self, value):
        self.entry.filename = value
    
    @property
    def title(self):
        return self.entry.title['$t']

    @property
    def url(self):
        return self.entry.watch

    @property
    def id(self):
        return self.entry.number
    
    @property
    def content(self):
        return self.entry.content['$t']

    @property
    def updated(self):
        return self.entry.updated['$t']

    @property
    def entry(self):
        return self.entry

    def __str__(self):
        content = [
            self.title,
            70 * '=',
            self.content,
            '',
            'Updated: ' +  self.updated,
            ''
            ]
        return '\n'.join(content)



