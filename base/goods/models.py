from django.db import models
	

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


class Good(models.Model):
	TYPES = Choices(
		('album', 'Album'), # other?
		('badge', 'Badge'),
		('bandana', 'Bandana'), # other?
		('bandanaset', 'Bandana Set'), # with photos. other?
		('clearfile', 'Clear File'),
		('clearfileset', 'Clear File Set'), # with photos
		('collectionphoto', 'Collection Photo'),
		('collectionphotoset', 'Collection Photo Set'), # set?
		('costume', 'Costume Good'), # other? costume fabric piece
		('dvd', 'DVD'), # DVD Magazine/DVD Memorial.. NO store-released DVD's.
		('gachagacha', 'GachaGacha Collection Item'),
		('gachagachaset', 'GachaGacha Collection Set'),
		('keyholder', 'Keyholder'),
		('keyholderset', 'Keyholder Set'), # with photos
		('microfiber', 'Microfiber Towel'),
		('muffler', 'Muffler Towel'),
		('parka', 'Parka'), # hoodie?
		('parkaset', 'Parka Set'), # with photos. hoodie?
		('tradingcardphoto', 'Trading Card-size Photo'),
		('lphoto', 'L-size Photo'),
		('postcardphoto', 'Postcard-size Photo'),
		('2lphoto', '2L-size Photo'),
		('A5photo', 'A5-wide Photo'),
		('photocard', 'Photo Card'), # PR cards, 4 seasons cards, birthday cards, etc.
		('pinup', 'Pin-up Poster'),
		('pinupset', 'Pin-up Poster Set'), # set?
		('a2poster', 'A2-size Poster'),
		('b2poster', 'B2-size Poster'),
		('scrunchie', 'Scrunchie'), # other? shushu?
		('scrunchieset', 'Scrunchie Set'), # with photos. other? shushu set?
		('strap', 'Strap/Charm'),
		('strap', 'Strap/Charm'), # with photos
		('tourbag', 'Tour Bag'),
		('tradingcard', 'Trading Card'), # non-collection?
		('tshirt', 'T-shirt'),
		('tshirtset', 'T-shirt Set'), # with photos/wristband
		('uchiwa', 'Uchiwa'),
		('visualbook', 'Visual Book/Pamphlet'),
		('visualscreen', 'Visual Screen'), # other? tapestry?
		('wristband', 'Wristband'),
		('collectionitem', 'Other Collection Item'),
		('collectionset', 'Other Collection Set'),
		('poster', 'Other Poster'),
		('towel', 'Other Towel'),
		('other', 'Other'),
	)
	type = models.CharField(choices=TYPES)
	is_graduation_good = models.BooleanField(default=False)
	is_campaign_good = models.BooleanField(default=False)
	is_lottery_good = models.BooleanField(default=False)
	is_bonus_good = models.BooleanField(default=False)
	is_set_exclusive = models.BooleanField(default=False)
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	price = models.IntegerField(blank=True, null=True)
	event = models.ForeignKey(Event, blank=True, null=True)
	source = models.ForeignKey(Source, blank=True, null=True)
	available_from = models.DateField(blank=True, null=True)
	available_until = models.DateField(blank=True, null=True)
	link = models.URLFeild(blank=True)
	image = models.ImageField(blank=True)
	parent = models.ForeignKey(blank=True, null=True, 'self')
	# Look into goods that are part of an event having the same available from/until date.
	# A Good is either from a Source or from an Event, not both. Exception: HelloShop.jp Goods section???
	# Connect to idols/groups (custom ForeignKey?)
	# Instead of 'Set', make individual items in a set have a parent?
