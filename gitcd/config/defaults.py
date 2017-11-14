class GitcdDefaults(object):

    def load(self):
        return {
            'test': None,
            'feature': None,
            'master': 'master',
            'tag': None,
            'versionType': 'manual',
            'versionScheme': None,
            'extraReleaseCommand': None
        }

class GitcdPersonalDefaults(object):

    def load(self):
        return {
            'token': None
        }

