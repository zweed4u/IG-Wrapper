#!/usr/bin/python3
import uuid
import requests


class Instagram:
    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        self.device_id = 'DADA237D-CB58-4D4D-8096-2F5E172921A3'
        self.pk = None
        self.csrftoken = None
        self.base_url = 'https://i.instagram.com/api/v1/'
        self.headers = {
            'Host':                           'i.instagram.com',
            'X-IG-Connection-Speed':          '44kbps',
            'Accept':                         '*/*',
            'X-IG-Connection-Type':           'WiFi',
            'X-IG-App-ID':                    '124024574287414',
            'Accept-Language':                'en-US;q=1',
            'Accept-Encoding':                'gzip, deflate',
            'Content-Type':                   'application/x-www-form-urlencoded; charset=UTF-8',
            'X-IG-ABR-Connection-Speed-KBPS': '0',
            'User-Agent':                     'Instagram 39.0.0.12.95 (iPhone6,1; iOS 10_2; en_US; en-US; scale=2.00; gamut=normal; 640x1136) AppleWebKit/420+',
            'Connection':                     'keep-alive',
            'X-IG-Capabilities':              '36r/Bw=='
        }

    def make_request(self, method, endpoint, params=None, data=None, json=None, headers=None, json_content=True):
        if json_content is True:
            return self.session.request(method, f'{self.base_url}{endpoint}', params=params, data=data, json=json, headers=headers).json()
        else:
            return self.session.request(method, f'{self.base_url}{endpoint}', params=params, data=data, json=json, headers=headers)

    def login(self):
        data = {
            'signed_body':        '2dbe11e6c15796032490782bba169043d90aad4cec450ae138c4a892c3d77ab6.{"reg_login":"0","password":"'+self.password+'","device_id":"'+self.device_id+'","username":"'+self.username+'","adid":"409DE66D-26AC-463C-BA4C-18AD6A32A1E1","login_attempt_count":"0","phone_id":"'+self.device_id+'"}',
            'ig_sig_key_version': '5'

        }
        login_response = self.make_request('POST', 'accounts/login/', data=data, headers=self.headers, json_content=False)
        self.pk = str(login_response.json()['logged_in_user']['pk'])
        self.csrftoken = login_response.cookies['csrftoken']
        return login_response.json()

    def logout(self):
        data = {
            'device_id': self.device_id
        }
        return self.make_request('POST', 'accounts/logout/', data=data, headers=self.headers)

    def change_password(self, new_password):
        data = {
            'signed_body':        '05d91a32ac739074aaa749cd97459a5883878f49c0d0ecc996707f93814ee328.{"_csrftoken":"'+self.csrftoken+'","old_password":"'+self.password+'","new_password1":"'+new_password+'","_uuid":"'+self.device_id+'","new_password2":"'+new_password+'","_uid":"'+self.pk+'"}',
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', 'accounts/change_password/', data=data, headers=self.headers)

    def get_dms(self):
        query_string_params = {
            'use_unified_inbox': 'true',
            'push_disabled':     'true',
            'persistentBadging': 'true'
        }
        return self.make_request('GET', 'direct_v2/inbox/', params=query_string_params, headers=self.headers)

    def get_autocomplete_list(self):
        query_string_params = {
            'version': '2'
        }
        return self.make_request('GET', 'friendships/autocomplete_user_list/', params=query_string_params, headers=self.headers)

    def get_reels(self):
        return self.make_request('GET', 'feed/reels_tray/', headers=self.headers)

    def get_news_inbox(self):
        query_string_params = {
            'push_disabled': 'true'
        }
        return self.make_request('GET', 'news/inbox/', params=query_string_params, headers=self.headers)

    def get_timeline(self):
        data = {
            'phone_id':             self.device_id,
            '_csrftoken':           self.pk,
            'seen_posts':           '',
            'timezone_offset':      '-14400',
            'is_charging':          '0',
            'battery_level':        '20',
            'will_sound_on':        '0',
            '_uuid':                self.device_id,
            'recovered_from_crash': '1',
            'feed_view_info':       '',
            'reason':               'cold_start_fetch',
            'session_id':           f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'unseen_posts':         '',
            'is_async_ads':         '0',
            'is_prefetch':          '0',
        }
        feed_headers = {
            'Host':                           'i.instagram.com',
            'X-FB':                           '0',
            'family_device_id':               self.device_id,
            'X-IG-Connection-Speed':          '44kbps',
            'Accept':                         '*/*',
            'X-IG-Connection-Type':           'WiFi',
            'X-IG-App-ID':                    '124024574287414',
            'Accept-Language':                'en-US;q=1',
            'Accept-Encoding':                'gzip, deflate',
            'X-IDFA':                         str(uuid.uuid4()).upper(),
            'X-Ads-Opt-Out':                  '0',
            'X-IG-ABR-Connection-Speed-KBPS': '0',
            'User-Agent':                     'Instagram 39.0.0.12.95 (iPhone6,1; iOS 10_2; en_US; en-US; scale=2.00; gamut=normal; 640x1136) AppleWebKit/420+',
            'X-DEVICE-ID':                    self.device_id,
            'X-IG-Capabilities':              '36r/Bw==',
            'Connection':                     'keep-alive',
            'Content-Type':                   'application/x-www-form-urlencoded; charset=UTF-8'
        }
        return self.make_request('POST', 'feed/timeline/', data=data, headers=feed_headers)

    def get_users_feed(self, user_pk):
        return self.make_request('GET', f'feed/user/{str(user_pk)}/', headers=self.headers)

    def get_notifications_badge(self):
        data = {
            '_csrftoken': self.csrftoken,
            '_uuid':      self.device_id,
            'user_ids':   self.pk,
            'device_id':  self.device_id,
        }
        return self.make_request('POST', 'notifications/badge/', data=data, headers=self.headers)

    def register(self, device_token):
        data = {
            '_csrftoken':   self.csrftoken,
            'users':        self.pk,
            '_uuid':        self.device_id,
            'device_id':    self.device_id,
            'device_token': device_token,
            'device_type':  'ios'
        }
        query_string_params = {
            'platform':    '12',
            'device_type': 'ios'
        }
        return self.make_request('POST', 'push/register/', data=data, params=query_string_params, headers=self.headers)

    def get_recent_searches(self):
        return self.make_request('GET', 'fbsearch/recent_searches/', headers=self.headers)

    def get_hidden_search_entities(self):
        return self.make_request('GET', 'fbsearch/get_hidden_search_entities/', headers=self.headers)

    def get_suggested_searches_user_type(self):
        query_string_params = {
            'rank_token': f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'type':       'users'
        }
        return self.make_request('GET', 'fbsearch/suggested_searches/', params=query_string_params, headers=self.headers)

    def get_suggested_searches_blended_type(self):
        query_string_params = {
            'rank_token': f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'type':       'blended'
        }
        return self.make_request('GET', 'fbsearch/suggested_searches/', params=query_string_params, headers=self.headers)

    def get_explore_page(self):
        query_string_params = {
            'session_id':      f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'is_ptr':          'true',
            'surface':         'grid',
            'timezone_offset': '-14400'
        }
        return self.make_request('GET', 'discover/explore/', params=query_string_params, headers=self.headers)

    def get_nearby_places(self, latitude, longitude):
        query_string_params = {
            'lat':             float(latitude),
            'timezone_offset': '-14400',
            'lng':             float(longitude)
        }
        return self.make_request('GET', 'fbsearch/places/', params=query_string_params, headers=self.headers)

    def get_search_places(self, latitude, longitude, place):
        query_string_params = {
            'rank_token':      f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'lat':             float(latitude),
            'lng':             float(longitude),
            'query':           str(place),
            'timezone_offset': '-14400'
        }
        return self.make_request('GET', 'fbsearch/places/', params=query_string_params, headers=self.headers)

    def search_tags(self, tag):
        query_string_params = {
            'rank_token':      f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'q':               str(tag),
            'is_typeahead':    'true',
            'timezone_offset': '-14400'
        }
        return self.make_request('GET', 'tags/search/', params=query_string_params, headers=self.headers)

    def related_tags(self, tag):
        query_string_params = {
            'visited':       '[{"id":"'+tag+'","type":"hashtag"}]',
            'related_types': '["location","hashtag"]'
        }
        return self.make_request('GET', f'v1/tags/{tag}/related/', params=query_string_params, headers=self.headers)

    def get_tag_info(self, tag):
        return self.make_request('GET', f'tags/{tag}/info/', headers=self.headers)

    def get_tag_feed(self, tag);
        return self.make_request('GET', f'feed/tag/{tag}/', headers=self.headers)        

    def search_top(self, search_string):
        query_string_params = {
            'rank_token':      f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'query':           search_string,
            'lat':             float(latitude),
            'lng':             float(longitude),
            'context':         'blended',
            'timezone_offset': '-14400'
        }
        return self.make_request('GET', 'fbsearch/topsearch_flat/', params=query_string_params, headers=self.headers)

    def search_people(self, search_string):
        query_string_params = {
            'rank_token':      f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'query':           search_string,
            'is_typeahead':    'true',
            'timezone_offset': '-14400'
        }
        return self.make_request('GET', 'users/search/', params=query_string_params, headers=self.headers)

    def get_top_live(self):
        return self.make_request('GET', 'discover/top_live/', headers=self.headers)

    def get news(self):
        return self.make_request('GET', 'news/', headers=self.headers)

    def get_news_log(self):
        data = {
            '_csrftoken': self.csrftoken,
            'pk':         self.pk, # encoded???
            '_uuid':      self.device_id,
            'action':     'click'
        }
        return self.make_request('POST', 'news/log/', data=data, headers=self.headers)

    def get_pending(self):
        query_string_params = {
            'rank_token':      f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'rank_mutual':     '0'
        }
        return self.make_request('GET', ' friendships/pending/', params=query_string_params, headers=self.headers)

    def get_friendship_status(self, user_ids_array):
        data = {
            '_csrftoken':        self.csrftoken,
            'include_reel_info': '0',
            '_uuid':             self.device_id,
            'user_ids':          ','.join(map(str, user_ids_array))
        }
        return self.make_request('POST','friendships/show_many/', data=data, headers=self.headers)

    def get_user_info(self, user_pk):
        query_string_params = {
            'device_id':   self.device_id,
            'from_module': 'feed_timeline'
        }
        return self.make_request('GET', f'users/{user_pk}/info/', params=query_string_params, headers=self.headers)

    def show_friendship(self, user_pk):
        return self.make_request('GET', f'friendships/show/{user_pk}/', headers=self.headers)

    def get_users_story(self, user_pk):
        return self.make_request('GET', f'feed/user/{user_pk}/story/', headers=self.headers)

    def get_users_highlights_reel(self, user_pk):
        return self.make_request('GET', f'highlights/{user_pk}/highlights_tray/', headers=self.headers)

    def mute_real(self, user_pk):
        data = {
            'signed_body':        '225c8229b1875791936b248baf0bfe2e65a11eed56c701ffb2b94dc8034db4d1.{"tray_position":"13","_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","_csrftoken":"'+self.csrftoken+'","reel_type":"story"}',
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/mute_friend_reel/{user_pk}/', data=data, headers=self.headers)

    def follow(self, user_pk):
        data = {
            'signed_body':        '7c646a4d663393cc6d51094b3015ab61f536efedf001209dd14de641f97993e5.{"_csrftoken":"'+self.csrftoken+'","_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","user_id":"'+user_pk+'"}',
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/create/{user_pk}/', data=data, headers=self.headers)

    def unfollow(self, user_pk):
        data = {
            'signed_body':        '7c646a4d663393cc6d51094b3015ab61f536efedf001209dd14de641f97993e5.{"_csrftoken":"'+self.csrftoken+'","_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","user_id":"'+user_pk+'"}'
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/destroy/{user_pk}/', data=data, headers=self.headers)

    def get_users_followings(self, user_pk):
        query_string_params = {
            'rank_token':  f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'rank_mutual': '0'
        }
        return self.make_request('GET', f'friendships/{user_pk}/following/', params=query_string_params, headers=self.headers)

    def search_users_followings(self, user_pk, search_string):
        query_string_params = {
            'rank_token':  f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'query':       search_string,
            'rank_mutual': '0'
        }
        return self.make_request('GET', f'friendships/{user_pk}/following/', params=query_string_params, headers=self.headers)

    def get_users_followers(self, user_pk):
        query_string_params = {
            'rank_token':  f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'rank_mutual': '0'
        }
        return self.make_request('GET', f'friendships/{user_pk}/followers/', params=query_string_params, headers=self.headers)

    def search_users_followers(self, user_pk, search_string):
        query_string_params = {
            'rank_token':  f'{self.pk}_{str(uuid.uuid4()).upper()}',
            'query':       search_string,
            'rank_mutual': '0'
        }
        return self.make_request('GET', f'friendships/{user_pk}/followers/', params=query_string_params, headers=self.headers)

    def get_users_followed_tags(self, user_pk):
        return self.make_request('GET', f'users/{user_pk}/following_tags_info/', headers=self.headers)

    def block_user(self, user_pk):
        data = {
            'signed_body':        '7c646a4d663393cc6d51094b3015ab61f536efedf001209dd14de641f97993e5.{"_csrftoken":"'+self.csrftoken+'","_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","user_id":"'+user_pk+'"}'
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/block/{user_pk}/', data=data, headers=self.headers)

    def unblock_user(self, user_pk):
        data = {
            'signed_body':        '7c646a4d663393cc6d51094b3015ab61f536efedf001209dd14de641f97993e5.{"_csrftoken":"'+self.csrftoken+'","_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","user_id":"'+user_pk+'"}'
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/unblock/{user_pk}/', data=data, headers=self.headers)

    def get_user_tagged_media(self, user_pk):
        return self.make_request('GET', f'usertags/{user_pk}/feed/', headers=self.headers)

    def turn_on_users_post_notifications(self, user_pk):
        data = {
            'signed_body':       'd66ab4203ca00942a031ba4dfda404575144be9efd9e2ed315330b284cd46663.{"_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","_csrftoken":"'+self.csrftoken+'"}',
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/favorite/{user_pk}/', data=data, headers=self.headers)

    def turn_off_users_post_notifications(self, user_pk):
        data = {
            'signed_body':       'd66ab4203ca00942a031ba4dfda404575144be9efd9e2ed315330b284cd46663.{"_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","_csrftoken":"'+self.csrftoken+'"}',
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/unfavorite/{user_pk}/', data=data, headers=self.headers)

    def get_all_saved(self):
        return self.make_request('GET', 'feed/saved/', headers=self.headers)

    def get_saved_collections(self):
        return self.make_request('GET', 'collections/list/', headers=self.headers)

    def create_dm_thread(self, user_pk):
        data = {
            'signed_body':        'c523c2aac3f3ea68f6ee427edd7c64ccbf9268975d98870490c4f8c8e95ecc36.{"_csrftoken":"'+self.csrftoken+'","use_unified_inbox":"true","_uuid":"'+self.device_id+'","recipient_users":"[\"'+user_pk+'\"]","_uid":"'+self.pk+'"}'
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', 'direct_v2/create_group_thread/', data=data, headers=self.headers)

    def get_dm_thread_contents(self, thread_id):
        query_string_params = {
            'use_unified_inbox': 'true'
        }
        return self.make_request('GET', f'direct_v2/threads/{thread_id}/', params=query_string_params, headers=self.headers)

    def mute_dm_thread(self, thread_id):
        data = {
            '_uuid':             self.device_id,
            '_csrftoken':        self.csrftoken,
            'use_unified_inbox': 'true'
        }
        return self.make_request('POST', f'direct_v2/threads/{thread_id}/mute/', data=data, headers=self.headers)

    def unmute_dm_thread(self, thread_id):
        data = {
            '_uuid':             self.device_id,
            '_csrftoken':        self.csrftoken,
            'use_unified_inbox': 'true'
        }
        return self.make_request('POST', f'direct_v2/threads/{thread_id}/unmute/', data=data, headers=self.headers)

    def delete_dm_thread(self, thread_id):
        data = {
            '_uuid':             self.device_id,
            '_csrftoken':        self.csrftoken,
            'use_unified_inbox': 'true'
        }
        return self.make_request('POST', f'direct_v2/threads/{thread_id}/hide/', data=data, headers=self.headers)

    def hide_search_entity(self, user_pk):
        data = {
            '_csrftoken': self.csrftoken,
            '_uuid':      self.device_id,
            'section':    'suggested'
            'user':       '["'+user_pk+'"]'
        }
        return self.make_request('POST', 'fbsearch/hide_search_entities/', data=data, headers=self.headers)

    def clear_search_history(self):
        data = {
            '_uuid':      self.device_id,
            '_csrftoken': self.csrftoken
        }
        return self.make_request('POST', 'fbsearch/clear_search_history/', data=data, headers=self.headers)

    def get_all_liked_posts(self):
        return self.make_request('GET', 'feed/liked/', headers=self.headers)

    def get_blocked_list(self):
        return self.make_request('GET', 'users/blocked_list/', headers=self.headers)

    def approve_user_follow(self, user_pk):
        data = {
            'signed_body':        '57f5058e927f9b701c9da791ca7275c731cb46456445a00522c9de3adb512c0b.{"_csrftoken":"'+self.csrftoken+'","_uuid":"'+self.device_id+'","_uid":"'+self.pk+'","user_id":"'+user_pk+'"}',
            'ig_sig_key_version': '5'
        }
        return self.make_request('POST', f'friendships/approve/{user_pk}/', data=data, headers=self.headers)


IG = Instagram('USERNAME','PASSWORD')
IG.login()
