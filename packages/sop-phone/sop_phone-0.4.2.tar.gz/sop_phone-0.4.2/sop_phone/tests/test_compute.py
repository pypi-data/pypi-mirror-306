from django.test import TestCase

from dcim.models import Site
from circuits.models import Provider

from ..models import PhoneDID, PhoneDelivery, PhoneInfo, PhoneMaintainer
from ..utils import count_all_did


class CountDIDTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        def fast_create_did(site, start, delivery=None, end=None) -> PhoneDID:
            return PhoneDID.objects.create(
                site=site,
                delivery=delivery,
                start=start,
                end=end
            )

        cls.p1 = Provider(name="PROV", slug="prov")
        cls.p1.save()
        cls.s1 = Site(name="SITE1", slug="site1")
        cls.s2 = Site(name="SITE2", slug="site2")
        cls.s1.save()
        cls.s2.save()
        cls.did1 = fast_create_did(cls.s1, 1111, None, 1121)
        cls.did2 = fast_create_did(cls.s1, 1122, None, 1129)
        cls.did3 = fast_create_did(cls.s1, 1130, None, 1139)
        cls.did3 = fast_create_did(cls.s1, 1140, None, 1150)
        cls.did4 = fast_create_did(cls.s1, 1151, None, 1161)

    def test_count_all_did_basic(self):
        """Test count all DID compute function"""
        r = count_all_did(PhoneDID.objects.filter(site=self.s1)).__int__()
        self.assertTrue(r == 51)

        r = count_all_did(PhoneDID.objects.filter(site=self.s2)).__int__()
        self.assertTrue(r == 0)

    def test_count_all_did_with_ndi(self):
        """Test count allDID compute function with PhoneDelivery NDI"""
        d = PhoneDelivery(
            site=self.s1,
            delivery="OSF",
            provider=self.p1,
            ndi=1000
        )
        d.save()
        self.did1.delivery = d
        self.did2.delivery = d
        self.did3.delivery = d
        self.did4.delivery = d
        self.did1.save()
        self.did2.save()
        self.did3.save()
        self.did4.save()
        r = count_all_did(PhoneDID.objects.filter(site=self.s1), PhoneDelivery.objects.filter(site=self.s1)).__int__()
        self.assertTrue(r == 52)

