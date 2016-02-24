import requests

class openCheezAICaller:

    API_BASE_URL = 'https://devbox-maiko.cites.illinois.edu/openCheezAI/'
    BLANK_PERSON_DICT = {
        'uin': '', 
        'uiuc_netid': '', 
        'illinois_netid': '', 
        'uillinois_netid': '', 
        'uic_netid': '', 
        'uis_netid': '',
        'i2s_firstname': '', 
        'i2s_lastname': '', 
        'banner_firstname': '', 
        'banner_lastname': '', 
        'banner_suppressed': False,
    }

    # IMPLEMENT:
    # GET single
    # GET multiple (by netid)
    # PATCH (update) single
    # POST (create) single
    # DELETE single
    # DELETE multiple (by netid)

    # Get multiple should return a list of dictionaries
    # Get single should return a single dictionary

    def get_person_by_uin(self, uin):
        '''
        Retrieve the single Person object (JSON blobs) with UIN uin
        '''
        url = self.API_BASE_URL + 'persons/' + uin
        resp = requests.get(url)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    def get_persons_by_netid(self, netid):
        '''
        Retrieve all Person objects (JSON blobs) with a NetID (anywhere)
        of netid.
        Returns list of dictionaries.
        '''
        url = self.API_BASE_URL + 'persons/' 
        resp = requests.get(url, params = {'netid' : netid})
        resp.raise_for_status()
        return resp.json()['results']

    def create_person(self, uin, person_dict):
        '''
        Create a new Person object with UIN uin and fields as given.
        Returns dictionary of the created object (with url link field newly
        populated).
        '''
        url = self.API_BASE_URL + 'persons/' 
        person_dict['uin'] = uin
        json_body = self.BLANK_PERSON_DICT
        json_body.update(person_dict)
        resp = requests.post(url, json=json_body)
        resp.raise_for_status()
        return resp.json()

    def update_person(self, uin, person_dict):
        '''
        Update an existing Person object with UIN uin and fields as given.
        Using patch which should call partial_update() behind the scenes.
        '''
        url = self.API_BASE_URL + 'persons/' + uin
        person_dict['uin'] = uin
        resp = requests.patch(url, json=person_dict)
        resp.raise_for_status()
        return resp.json()

    def delete_person(self, uin):
        '''
        Delete a Person with the UIN of uin. No JSON is returned,
        so just return None
        '''
        url = self.API_BASE_URL + 'persons/' + uin
        resp = requests.delete(url)
        resp.raise_for_status()

    def delete_persons_by_netid(self, netid):
        '''
        Delete all Persons with the NetID of netid (for any campus).
        First call get_persons_by_netid, then troll through the returned
        list and make a delete call on each.
        Here too there is nothing to return.
        '''
        people = self.get_persons_by_netid(netid)
        for person in people:
            url = self.API_BASE_URL + 'persons/' + person['uin']
            resp = requests.delete(url)
            resp.raise_for_status()

