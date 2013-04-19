from django.db import models
from model_utils import Choices

from people.models import Group, Idol
from events.models import Event


class Source(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    website_link = models.URLField(blank=True)
    # HelloShop.jp (Egao) - egao tsuuhan (mail order)
    # HelloShop.jp (Overstock) - kuradashi (warehouse)
    # HelloShop.jp (Complete Albums)
    # HelloShop.jp (Special) - current stuff
    # HelloShop.jp/H!P Official Shop (Goods) - 'goods' usually available at both
    # Hello! Project Official Shop (Photos) - just photos, not goods
    # U/F Online - event?
    # Other - Tsutaya, Tower Records, etc. (posters, Tower t-shirt, etc).

    # Campaign goods (freebies) may also be defined as a source?


class BaseGood(models.Model):
    is_graduation_good = models.BooleanField(default=False)
    is_birthday_good = models.BooleanField(default=False)
    is_campaign_good = models.BooleanField(default=False)
    is_lottery_good = models.BooleanField(default=False)

    idols = models.ManyToManyField(Idol, blank=True, null=True)
    groups = models.ManyToManyField(Group, blank=True, null=True)
    event = models.ForeignKey(Event, blank=True, null=True)

    romanized_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.IntegerField(blank=True, null=True)
    source = models.ForeignKey(Source, blank=True, null=True)
    available_from = models.DateField(blank=True, null=True)
    available_until = models.DateField(blank=True, null=True)
    link = models.URLField(blank=True)
    image = models.ImageField(blank=True)


class Good(BaseGood):
    CATEGORIES = Choices(
        ('badge', 'Badge'),
        ('bandana', 'Bandana'),  # other?
        ('clearfile', 'Clear File'),
        ('collectionphoto', 'Collection Photo'),
        ('costume', 'Costume Good'),  # other? costume fabric piece
        ('dvd', 'DVD'),  # DVD Magazine/DVD Memorial.. NO store-released DVD's.
        ('gachagacha', 'GachaGacha Collection Item'),
        ('keyholder', 'Keyholder'),
        ('microfiber', 'Microfiber Towel'),
        ('muffler', 'Muffler Towel'),
        ('parka', 'Parka'),  # hoodie?
        ('tradingcardphoto', 'Trading Card-size Photo'),
        ('lphoto', 'L-size Photo'),
        ('lmetallic', 'L-size Metallic Photo'),
        ('postcardphoto', 'Postcard-size Photo'),
        ('2lphoto', '2L-size Photo'),
        ('A5photo', 'A5-wide Photo'),
        ('A4photo', 'A4-size Photo'),
        ('photocard', 'Photo Card'),  # PR cards, 4 seasons cards, birthday cards, etc.
        ('pinup', 'Pin-up Poster'),
        ('a2poster', 'A2-size Poster'),
        ('b2poster', 'B2-size Poster'),
        ('scrunchie', 'Scrunchie'),  # other? shushu?
        ('strap', 'Strap/Charm'),
        ('tourbag', 'Tour Bag'),
        ('tradingcard', 'Trading Card'),  # non-collection?
        ('tshirt', 'T-shirt'),
        ('uchiwa', 'Uchiwa'),
        ('visualbook', 'Visual Book/Pamphlet'),
        ('visualscreen', 'Visual Screen'),  # other? tapestry?
        ('wristband', 'Wristband'),
        ('collectionitem', 'Other Collection Item'),
        ('poster', 'Other Poster'),
        ('towel', 'Other Towel'),
        ('other', 'Other'),
    )
    category = models.CharField(choices=CATEGORIES)
    is_bonus_good = models.BooleanField(default=False)
    is_set_exclusive = models.BooleanField(default=False)
    is_online_exclusive = models.BooleanField(default=False)
    is_mailorder_exclusive = models.BooleanField(default=False)
    parent = models.ForeignKey('GoodSet', blank=True, null=True)
    # Look into goods that are part of an event having the same available from/until date.
    # A Good is either from a Source or from an Event, not both. Exception: HelloShop.jp Goods section???
    # Connect to idols/groups (custom ForeignKey?)
    # Goods that you get with releases. Example: Mano NFS photo for buying any of her PB's during graduation.


class Set(BaseGood):
    CATEGORIES = Choices(
        ('bandanaset', 'Bandana Set'),
        ('clearfileset', 'Clear File Set'),
        ('collectionphotoset', 'Collection Photo Set'),
        ('gachagachaset', 'GachaGacha Collection Set'),
        ('keyholderset', 'Keyholder Set'),
        ('parkaset', 'Parka Set'),  # hoodie set?
        ('pinupset', 'Pin-up Poster Set'),
        ('scrunchieset', 'Scrunchie Set'),  # other? shushu set?
        ('strapset', 'Strap/Charm Set'),
        ('tshirtset', 'T-shirt Set'),
        ('collectionset', 'Other Collection Set'),
        ('otherset', 'Other Set'),
    )
    category = models.CharField(choices=CATEGORIES)
    # Sets within sets. Setception.


class SuperSet(BaseGood):
    goods = models.ManyToManyField(Good)
    sets = models.ManyToManyField(Set)
