from django.db import models
	

class Source(models.Model):
	romanized_name = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	website_link = models.URLField(blank=True)
	# Sources include HelloShop.jp, other websites, official store, etc.
	# HelloShop.jp sections will be defined as separate sources (Egao, Special, etc).
	# Campaign goods (freebies) may also be defined as a source?


class Good(models.Model):
	TYPES = Choices(
		('album', 'Album'), # other?
		('badge', 'Badge'),
		('clearfile', 'Clear File'),
		('collectionitem', 'collection item'),
		('collectionset', 'collection item set'),
		('collectionphoto', 'Collection Photo'),
		('collectionphotoset', 'Collection Photo set'), # Set?
		('costume', 'Costume Good'), # other? costume fabric piece
		('dvdmagazine', 'DVD Magazine'),
		('gachagacha', 'GachaGacha collection item'),
		('gachagacha', 'GachaGacha collection set'),
		('keyholder', 'Keyholder'),
		('microfiber', 'Microfiber Towel'),
		('muffler', 'Muffler Towel'),
		('lphoto', 'L-size Photo'),
		('parka', 'Parka'), # hoodie?
		('postcardphoto', 'Postcard-size Photo'),
		('2lphoto', '2L-size Photo'),
		('A5photo', 'A5-wide Photo'),
		('photocard', 'Photo Card'), # PR cards, 4 seasons cards, birthday cards, etc.
		('pinup', 'Pin-up Poster'),
		('pinupset', 'Pin-up Poster set'), # Set?
		('a2poster', 'A2-size Poster'),
		('b2poster', 'B2-size Poster'),
		('scrunchie', 'Scrunchie'), # other? shushu?
		('strap', 'Strap'),
		('tradingcard', 'Trading Card'), # non-collection?
		('tshirt', 'T-shirt'),
		('tshirtset', 'T-shirt Set'),
		('uchiwa', 'Uchiwa'),
		('visualbook', 'Visual Book/Pamphlet'),
		('visualscreen', 'Visual Screen'), # other? tapestry?
		('poster', 'Other Poster'),
		('towel', 'Other Towel'),
		('other', 'Other'),
	)
	type = models.CharField(choices=TYPES)
	is_graduation_good = models.BooleanField(default=False)
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