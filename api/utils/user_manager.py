from hashlib import blake2b

from .transliteration import Transliterator

def to_bool(value):
    """
       Converts 'something' to boolean. Raises exception for invalid formats
           Possible True  values: 1, True, "1", "TRue", "yes", "y", "t"
           Possible False values: 0, False, None, [], {}, "", "0", "faLse", "no", "n", "f", 0.0, ...
    """
    if str(value).lower() in ("yes", "y", "true",  "t", "1"): return True
    if str(value).lower() in ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))

class UserManager(object):
    USER = ('username', 'email', 'first_name', 'last_name', 'password', 'is_manager', 'is_director',
            'is_staff',  'profile', 'other')
    PROFILE = ('gender', 'birthday', 'social_link')
    OTHER = ('department_id', 'occupation', 'responsibility',)
    SEPARATOR = "_"

    @classmethod
    def to_user_data(cls, input_dictionary):
        user_data = {key.lower().strip().replace(" ", cls.SEPARATOR): value for key, value in input_dictionary.items()}
        user_data[cls.USER[-2]] = {}
        user_data[cls.USER[-1]] = {}
        for item in cls.PROFILE:
            if item in user_data:
                user_data[cls.USER[-2]][item] = user_data.pop(item)
        for item in cls.OTHER:
            if item in user_data:
                user_data[cls.USER[-1]][item] = user_data.pop(item)

        if cls.USER[0] not in user_data:
            user_data[cls.USER[0]] = cls.create_username(user_data)
        if cls.USER[4] not in user_data:
            user_data[cls.USER[4]] = cls.create_password(user_data)
        if cls.OTHER[0] in user_data[cls.USER[-1]]:
            user_data[cls.USER[-1]][cls.OTHER[0]] = int(user_data[cls.USER[-1]][cls.OTHER[0]])
        if cls.USER[5] in user_data:
            user_data[cls.USER[5]] = to_bool(user_data[cls.USER[5]])

        return user_data

    @classmethod
    def is_schema_correct(cls, user_data):
        for user_field in cls.USER:
            if user_field not in user_data:
                return False
        for profile_field in cls.PROFILE:
            if profile_field not in user_data[cls.USER[-2]]:
                return False
        for other_field in cls.OTHER:
            if other_field not in user_data[cls.USER[-1]]:
                return False
        return True

    @classmethod
    def create_password(cls, user_data):
        return blake2b(str(user_data).encode(), digest_size=8).hexdigest()

    @classmethod
    def create_username(cls, user_data):

        key_words = (
            str(user_data.get(cls.USER[-1]).get(cls.OTHER[0], '')),
            user_data.get(cls.USER[2], ''),
            user_data.get(cls.USER[3], ''),
        )

        return cls.SEPARATOR.join([Transliterator.transliterate(word.lower().strip()) for word in key_words])
