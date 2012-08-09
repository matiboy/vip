
from django.utils import unittest
import daemon.models

class RequiresChannels(unittest.TestCase):
    def setUp(self):
        super(RequiresChannels, self).setUp()
        daemon.models.Channel.objects.create(channel_id = "aaa555", 
                                             search_inside_enabled = True, 
                                             update_date = 1500, 
                                             create_date = 1500, 
                                             title = "Cat channel",
                                             autoplay_enabled = True,
                                             state = "Published",
                                             rss_enabled = True,
                                             email_enabled = True,
                                             itunes_rss_enabled = True,
                                             embed_enabled = True)
        
        daemon.models.Channel.objects.create(channel_id = "zzz000", 
                                             search_inside_enabled = True, 
                                             update_date = 1500, 
                                             create_date = 1500, 
                                             title = "TV Tiga",
                                             autoplay_enabled = True,
                                             state = "Published",
                                             rss_enabled = True,
                                             email_enabled = True,
                                             itunes_rss_enabled = True,
                                             embed_enabled = True)
        
        print "RequiresChannel init done"
