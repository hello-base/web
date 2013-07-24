from django.db import models

from model_utils import Choices, FieldTracker
from model_utils.managers import InheritanceManager

from .. import models as base


class Shop(models.Model):
    romanized_name = models.CharField(max_length=200)
    name = models.CharField(blank=True, max_length=200)
    website_link = models.URLField(blank=True)
    slug = models.SlugField()

    # HelloShop.jp (Egao) - egao tsuuhan (mail order)
    # HelloShop.jp (Overstock) - kuradashi (warehouse)
    # HelloShop.jp (Complete Albums) - maybe don't need..?
    # HelloShop.jp (Special) - current stuff; FFUUU stuff available at H!POS
    # HelloShop.jp/H!P Official Shop (Goods) - 'goods' usually available at both
    # Hello! Project Official Shop (Photos) - just photos, not goods
    # U/F Online - event?
    # Other - Tsutaya, Tower Records, etc. (posters, Tower t-shirt, etc).

    # Campaign goods (freebies) may also be defined as a source?

    def __unicode__(self):
        return u'%s' % self.romanized_name


class BaseGood(base.Merchandise):
    # Model Managers.
    objects = InheritanceManager()
    tracker = FieldTracker()

    is_graduation_good = models.BooleanField(default=False)
    is_birthday_good = models.BooleanField(default=False)
    is_online_exclusive = models.BooleanField(default=False)
    is_mailorder_exclusive = models.BooleanField(default=False)

    event = models.ForeignKey('events.Event', blank=True, null=True,
        help_text='Is this good from an event?')
    shop = models.ForeignKey(Shop, blank=True, null=True)
    online_id = models.CharField('online ID', blank=True, null=True, max_length=16,
        help_text='The good\'s ID or catalog number (if available).')
    other_info = models.TextField(blank=True, null=True,
        help_text='Any additional information about the good. Size, restrictions, etc.')

    available_from = models.DateField(blank=True, null=True,
        help_text='When was the good originally released?')
    available_until = models.DateField(blank=True, null=True,
        help_text='When was the good taken off the market?')
    link = models.URLField(blank=True)
    image = models.ImageField(blank=True, upload_to='/')

    def __unicode__(self):
        if self.event:
            return u'%s from %s' % (self.romanized_name, self.event.nickname)
        if self.source:
            return u'%s from %s' % (self.romanized_name, self.source)
        return u'%s' % self.romanized_name

    def save(self, *args, **kwargs):
        self.released = self.available_from
        super(BaseGood, self).save(*args, **kwargs)


class Good(BaseGood):
    CATEGORIES = Choices(
        ('badge', 'Badge'),
        ('bandana', 'Bandana'),  # other?
        ('clearfile', 'Clear File'),
        ('collectionphoto', 'Collection Photo'),
        ('costume', 'Costume Good'),  # other? costume fabric piece
        ('dvd', 'DVD'),  # DVD Magazine/DVD Memorial.. NO store-released DVD's.
        ('gachagacha', 'GachaGacha Collection Item'),
        ('hoodie', 'Hoodie'),
        ('keyholder', 'Keyholder'),
        ('microfiber', 'Microfiber Towel'),
        ('muffler', 'Muffler Towel'),
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
        ('b1poster', 'B1-size Poster'),
        ('b2poster', 'B2-size Poster'),
        ('scrunchie', 'Scrunchie'),  # hair ornament?
        ('strap', 'Strap/Charm'),
        ('tourbag', 'Tour Bag'),
        ('tradingcard', 'Trading Card'),
        ('tshirt', 'T-shirt'),
        ('uchiwa', 'Uchiwa'),
        ('visualbook', 'Visual Book/Pamphlet'),
        ('visualscreen', 'Visual Screen'),
        ('wristband', 'Wristband'),
        ('collectionitem', 'Other Collection Item'),
        ('poster', 'Other Poster'),  # no fabric posters like tapestries
        ('towel', 'Other Towel'),
        ('other', 'Other'),
    )
    category = models.CharField(choices=CATEGORIES, max_length=16)
    parent = models.ForeignKey('Set', blank=True, null=True,
        help_text='Is this good a part of another good? (e.g., a photo that is part of a set)',
        verbose_name=u'parent good')

    is_bonus_good = models.BooleanField(default=False)
    is_campaign_good = models.BooleanField(default=False)
    is_lottery_good = models.BooleanField(default=False)
    is_set_exclusive = models.BooleanField(default=False)

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
    category = models.CharField(choices=CATEGORIES, max_length=18)


class SuperSet(BaseGood):
    goods = models.ManyToManyField(Good)
    sets = models.ManyToManyField(Set)
