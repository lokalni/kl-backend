class Region:
    DOLNOSLASKIE = 'dolnoslaskie'
    SLASKIE = 'slaskie'

    @classmethod
    def choices(cls):
        return [
            (cls.DOLNOSLASKIE, cls.DOLNOSLASKIE),
            (cls.SLASKIE, cls.SLASKIE),
        ]