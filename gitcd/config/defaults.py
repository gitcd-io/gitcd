class GitcdDefaults(object):

    def load(self):
        return {
            'test': None,
            'feature': None,
            'master': 'main',
            'tag': None,
            'versionType': 'manual',
            'versionScheme': None,
            'extraReleaseCommand': None
            'preReleaseCommand': None
        }


class GitcdPersonalDefaults(object):

    def load(self):
        return {
            'tokens': {
                'github': None,
                'bitbucket': None,
                'gitlab': None
            }
        }
