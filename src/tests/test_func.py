# -*- coding: utf-8 -*-
import unittest
from converter import Converter


class TestStringMethods(unittest.TestCase):

    def test_converter_model_com_todos_tipos_de_fields_possiveis(self):
        convert = Converter("""
class Feed(models.Model):
    title = models.CharField(max_length=500)
    feed_url = models.URLField(unique=True, max_length=500)
    public_url = models.URLField(max_length=500)
    approval_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING_FEED)
    feed_type = models.ForeignKey(FeedType, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, blank=True, null=True, related_name='owned_feeds', on_delete=models.SET_NULL)""")
        result = convert.get_fields()
        self.assertEqual(len(result.split(',')), 6)

    def test_converter_model_com_field_de_altura_de_varias_linha(self):
        convert = Converter("""
    date = models.DateTimeField(
            pgettext_lazy('Order history entry field', 'last history change'),
            default=now, editable=False)
        order = models.ForeignKey(
            Order, related_name='history',
            verbose_name=pgettext_lazy('Order history entry field', 'order'),
            on_delete=models.CASCADE)
        status = models.CharField(
            pgettext_lazy('Order history entry field', 'order status'),
            max_length=32, choices=OrderStatus.CHOICES)
        comment = models.CharField(
            pgettext_lazy('Order history entry field', 'comment'),
            max_length=100, default='', blank=True)
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL, blank=True, null=True,
            verbose_name=pgettext_lazy('Order history entry field', 'user'),
            on_delete=models.SET_NULL)""")
        result = convert.get_fields()
        self.assertEqual(len(result.split(',')), 5)

    def test_converter_model_com_field_e_funcoes(self):
        convert = Converter("""
            class Cart(models.Model):
    status = models.CharField(
        pgettext_lazy('Cart field', 'order status'),
        max_length=32, choices=CartStatus.CHOICES, default=CartStatus.OPEN)
    created = models.DateTimeField(
        pgettext_lazy('Cart field', 'created'), auto_now_add=True)
    last_status_change = models.DateTimeField(
        pgettext_lazy('Cart field', 'last status change'), auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='carts',
        verbose_name=pgettext_lazy('Cart field', 'user'),
        on_delete=models.CASCADE)
    email = models.EmailField(
        pgettext_lazy('Cart field', 'email'), blank=True, null=True)
    token = models.UUIDField(
        pgettext_lazy('Cart field', 'token'),
        primary_key=True, default=uuid4, editable=False)
    voucher = models.ForeignKey(
        'discount.Voucher', null=True, related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=pgettext_lazy('Cart field', 'token'))
    checkout_data = JSONField(
        verbose_name=pgettext_lazy('Cart field', 'checkout data'), null=True,
        editable=False,)
    total = PriceField(
        pgettext_lazy('Cart field', 'total'),
        currency=settings.DEFAULT_CURRENCY, max_digits=12, decimal_places=2,
        default=0)
    quantity = models.PositiveIntegerField(
        pgettext_lazy('Cart field', 'quantity'), default=0)

    objects = CartQueryset.as_manager()

    class Meta:
        ordering = ('-last_status_change',)
        verbose_name = pgettext_lazy('Cart model', 'Cart')
        verbose_name_plural = pgettext_lazy('Cart model', 'Carts')

    def __init__(self, *args, **kwargs):
        self.discounts = kwargs.pop('discounts', None)
        super(Cart, self).__init__(*args, **kwargs)

    def update_quantity(self):
        total_lines = self.count()['total_quantity']
        if not total_lines:
            total_lines = 0
        self.quantity = total_lines
        self.save(update_fields=['quantity'])

    def change_status(self, status):
        if status not in dict(CartStatus.CHOICES):
            raise ValueError('Not expected status')
        if status != self.status:
            self.status = status
            self.last_status_change = now()
            self.save()

    def change_user(self, user):
        open_cart = find_open_cart_for_user(user)
        if open_cart is not None:
            open_cart.change_status(status=CartStatus.CANCELED)
        self.user = user
        self.save(update_fields=['user'])

    def is_shipping_required(self):
        return any(line.is_shipping_required() for line in self.lines.all())

    def __repr__(self):
        return 'Cart(quantity=%s)' % (self.quantity,)

    def __len__(self):
        return self.lines.count()

    def get_subtotal(self, item, **kwargs):
        return item.get_total(**kwargs)

    def get_total(self, **kwargs):
        subtotals = [
            self.get_subtotal(item, **kwargs) for item in self.lines.all()]
        if not subtotals:
            raise AttributeError('Calling get_total() on an empty item set')
        zero = Price(0, currency=settings.DEFAULT_CURRENCY)
        return sum(subtotals, zero)

    def count(self):
        lines = self.lines.all()
        return lines.aggregate(total_quantity=models.Sum('quantity'))

    def clear(self):
        self.delete()

    def create_line(self, variant, quantity, data):
        return self.lines.create(
            variant=variant, quantity=quantity, data=data or {})

    def get_line(self, variant, data=None):
        all_lines = self.lines.all()
        if data is None:
            data = {}
        line = [line for line in all_lines
                if line.variant_id == variant.id and line.data == data]
        if line:
            return line[0]

    def add(self, variant, quantity=1, data=None, replace=False,
            check_quantity=True):
        cart_line, dummy_created = self.lines.get_or_create(
            variant=variant, defaults={'quantity': 0, 'data': data or {}})
        if replace:
            new_quantity = quantity
        else:
            new_quantity = cart_line.quantity + quantity

        if new_quantity < 0:
            raise ValueError('%r is not a valid quantity (results in %r)' % (
                quantity, new_quantity))

        if check_quantity:
            variant.check_quantity(new_quantity)

        cart_line.quantity = new_quantity

        if not cart_line.quantity:
            cart_line.delete()
        else:
            cart_line.save(update_fields=['quantity'])
        self.update_quantity()

    def partition(self):
        grouper = (
            lambda p: 'physical' if p.is_shipping_required() else 'digital')
        return partition(self.lines.all(), grouper, ProductGroup)q
        """)
        result = convert.get_fields()
        self.assertEqual(len(result.split(',')), 10)

    def test_todos_of_fields_padroes(self):
        convert = Converter("""class TodosFieldsPadroes(models.Model):
            auto_field = models.AutoField()
            #big_auto_field = models.BigAutoField()
            big_integer_field = models.BigIntegerField()
            #binary_field = models.BinaryField()
            boolean_field = models.BooleanField()
            char_field = models.CharField(max_length=50)
            #comma_separated_integer_field = models.CommaSeparatedIntegerField()
            date_field = models.DateField()
            datetime_field = models.DateTimeField()
            decimal_field = models.DecimalField()
            duration_field = models.DurationField()
            email_field = models.EmailField()
            field_field = models.FileField()
            float_field = models.FloatField()
            image_field = models.ImageField()
            int_field = models.IntegerField()
            #generic_ip_field = models.GenericIPAddressField()
            ip_address_field = models.IPAddressField()
            nullboolean_field = models.NullBooleanField()
            posint_field = models.PositiveIntegerField()
            spositint_field = models.PositiveSmallIntegerField()
            slug_field = models.SlugField()
            sint_field = models.SmallIntegerField()
            text_field = models.TextField()
            time_field = models.TimeField()
            url_field = models.URLField()
            uuid_field = models.UUIDField()


            class Meta:
                verbose_name = "testeTodos"
                verbose_name_plural = "testeTodoss"

            def __str__(self):
                return "teste"
        """
        )

        result = convert.get_fields()
        self.assertEqual(len(result.split(',')), 27)

    def test_converter_texto_com_class_nome(self):
        convert = Converter("""
class Feed(models.Model):
    title = models.CharField(max_length=500)
    feed_url = models.URLField(unique=True, max_length=500)
    public_url = models.URLField(max_length=500)
    approval_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING_FEED)
    feed_type = models.ForeignKey(FeedType, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, blank=True, null=True, related_name='owned_feeds', on_delete=models.SET_NULL)""")
        result = convert.get_class_name()
        self.assertEqual(result, 'Feed')

    def test_converter_texto_sem_class_nome(self):
        convert = Converter("""
    date = models.DateTimeField(
            pgettext_lazy('Order history entry field', 'last history change'),
            default=now, editable=False)
        order = models.ForeignKey(
            Order, related_name='history',
            verbose_name=pgettext_lazy('Order history entry field', 'order'),
            on_delete=models.CASCADE)
        status = models.CharField(
            pgettext_lazy('Order history entry field', 'order status'),
            max_length=32, choices=OrderStatus.CHOICES)
        comment = models.CharField(
            pgettext_lazy('Order history entry field', 'comment'),
            max_length=100, default='', blank=True)
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL, blank=True, null=True,
            verbose_name=pgettext_lazy('Order history entry field', 'user'),
            on_delete=models.SET_NULL)""")
        result = convert.get_class_name()
        self.assertEqual(result, '')
