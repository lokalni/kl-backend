class Region:
    DOLNOSLASKIE = 'dolnoslaskie'
    KUJAWSKO_POMORSKIE = 'kujawsko_pomorskie'
    LUBELSKIE = 'lubelskie'
    LUBUSKIE = 'lubuskie'
    LODZKIE = 'lodzkie'
    MALOPOLSKIE = 'malopolskie'
    MAZOWIECKIE = 'mazowieckie'
    OPOLSKIE = 'opolskie'
    PODKARPACKIE = 'podkarpackie'
    PODLASKIE = 'podlaskie'
    POMORSKIE = 'pomorskie'
    SLASKIE = 'slaskie'
    SWIETOKRZYSKIE = 'swietokrzyskie'
    WARMINSKO_MAZURSKIE = 'warminsko_mazurskie'
    WIELKOPOLSKIE = 'wielkopolskie'
    ZACHODNIOPOMORSKIE = 'zachodniopomorskie'

    @classmethod
    def choices(cls):
        return [
                (cls.DOLNOSLASKIE, cls.DOLNOSLASKIE),
                (cls.KUJAWSKO_POMORSKIE, cls.KUJAWSKO_POMORSKIE),
                (cls.LUBELSKIE, cls.LUBELSKIE),
                (cls.LUBUSKIE, cls.LUBUSKIE),
                (cls.LODZKIE, cls.LODZKIE),
                (cls.MALOPOLSKIE, cls.MALOPOLSKIE),
                (cls.MAZOWIECKIE, cls.MAZOWIECKIE),
                (cls.OPOLSKIE, cls.OPOLSKIE),
                (cls.PODKARPACKIE, cls.PODKARPACKIE),
                (cls.PODLASKIE, cls.PODLASKIE),
                (cls.POMORSKIE, cls.POMORSKIE),
                (cls.SLASKIE, cls.SLASKIE),
                (cls.SWIETOKRZYSKIE, cls.SWIETOKRZYSKIE),
                (cls.WARMINSKO-MAZURSKIE, cls.WARMINSKO-MAZURSKIE),
                (cls.WIELKOPOLSKIE, cls.WIELKOPOLSKIE),
                (cls.ZACHODNIOPOMORSKIE, cls.ZACHODNIOPOMORSKIE),
        ]
