from django.test import TestCase
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError

from dcim.models import Site
from circuits.models import Provider

from ..models import PhoneDelivery, PhoneDID, PhoneMaintainer, PhoneInfo


class PhoneInfoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.site = Site.objects.create(
            name="Hogwarts",
            slug="hogwarts",
            status="active"
        )

        cls.maintainer = PhoneMaintainer.objects.create(
            name="DAUPHIN TELECOM",
            slug="dauphin_telecom",
            status="active",
            physical_address="Hello, i live \nFar from here... \n"
        )
        cls.maintainer.full_clean()

    def test_valid_phone_info(self):
        """Test that a valid PhoneInfo can be cleaned"""
        info = PhoneInfo.objects.create(
            site=self.site,
            maintainer=self.maintainer
        )
        info.full_clean()

    def test_unique_site(self):
        """Test that non-unique site raises IntegrityError"""
        info = PhoneInfo.objects.create(
            site=self.site,
            maintainer=self.maintainer
        )

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                info = PhoneInfo.objects.create(
                    site=self.site,
                    maintainer=self.maintainer
                )


class PhoneMaintainerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.maintainer = PhoneMaintainer.objects.create(
            name="DAUPHIN TELECOM",
            slug="dauphin_telecom",
            status="active",
            physical_address="Hello, i live \nFar from here... \n"
        )
        cls.maintainer.full_clean()

    def test_unique_maintainer_name(self):
        """Test that non-unique name raises IntegrityError"""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                mt = PhoneMaintainer.objects.create(
                    name="DAUPHIN TELECOM",
                    slug="dauphin_telelom",
                    status="retired"
                )

    def test_unique_maintainer_slug(self):
        """Test that non-unique slug raises IntegrityError"""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                mt = PhoneMaintainer.objects.create(
                    name="DAUPHIN TELELOM",
                    slug="dauphin_telecom",
                    status="active",
                )

    def test_address_validator(self):
        """Test that bad-format address raises ValidationError"""
        with self.assertRaises(ValidationError):
            mt = PhoneMaintainer.objects.create(
                name="Haboobs",
                slug="haboobs",
                status="retired",
                physical_address="hello, i live very far from here !\nyesyesyes"
            )
            mt.full_clean()


class PhoneDeliveryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.site1 = Site.objects.create(
            name="TESTING_SITE1",
            slug="testing-site-1"
        )
        cls.site2 = Site.objects.create(
            name="TESTING_SITE2",
            slug="testing-site-2"
        )
        cls.provider = Provider.objects.create(
            name="TESTING_PROV",
            slug="testing-prov"
        )
        cls.did = PhoneDID.objects.create(
            start=100001,
            end=100005,
            site=cls.site1
        )

    def test_valid_delivery(self):
        """Test a valid and IntegrityError PhoneDelivery"""
        deli = PhoneDelivery.objects.create(
            delivery="T0",
            provider=self.provider,
            site=self.site1,
            status="active",
            ndi=123000,
            dto=123400,
        )
        deli.full_clean
        deli.save()
        self.assertTrue(PhoneDelivery.objects.filter(delivery="T0", site=self.site1).exists())

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                PhoneDelivery.objects.create(
                    delivery="T0",
                    provider=self.provider,
                    site=self.site1,
                    status="active"
                ).full_clean()

    def test_unique_ndi(self):
        """Test that non-unique NDI raises IntegrityError"""
        deli = PhoneDelivery.objects.create(
                delivery="DAUPHIN",
                provider=self.provider,
                site=self.site2,
                status="retired",
                ndi=123000
            )
        deli.full_clean()
        deli.save()

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                deli = PhoneDelivery.objects.create(
                    delivery="T2",
                    provider=self.provider,
                    site=self.site2,
                    status="retired",
                    ndi=123000
                )
                deli.full_clean()

    def test_dto_not_ndi(self):
        """Test that DTO cannot be the NDI of its own delivery"""
        with self.assertRaises(ValidationError):
            deli = PhoneDelivery.objects.create(
                delivery="BTIP",
                provider=self.provider,
                site=self.site1,
                status="staging",
                ndi=124000,
                dto=124000
            )
            deli.full_clean()

    def test_dto_overlaps_did_range(self):
        """Test the ValidationError when DTO overlaps same site DID"""
        with self.assertRaises(ValidationError):
            did = self.did
            did.save()

            deli = PhoneDelivery.objects.create(
                delivery="T2",
                provider=self.provider,
                site=self.site1,
                status="active"
            )
            deli.save()

            did.delivery = deli
            did.save()

            deli.dto = 100004
            deli.full_clean()

    def test_ndi_overlaps_did_range(self):
        """Test NDI overlaps another site DID"""
        did = self.did
        did.save()

        deli = PhoneDelivery.objects.create(
            delivery="T2",
            provider=self.provider,
            site=self.site1,
            status="active",
            ndi=100004
        )
        deli.full_clean()
        deli.save()

        with self.assertRaises(ValidationError):
            deli.site = self.site2
            deli.full_clean()


class PhoneDIDTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.site1 = Site.objects.create(
            name="TESTING_SITE1",
            slug="testing-site-1"
        )
        cls.site2 = Site.objects.create(
            name="TESTING_SITE2",
            slug="testing-site-2"
        )
        cls.provider = Provider.objects.create(
            name="TESTING_PROV",
            slug="testing-prov"
        )

        cls.delivery = PhoneDelivery.objects.create(
            delivery="TESTING",
            site=cls.site1,
            provider=cls.provider,
            ndi=1000000000,
            dto=1000000001,
            status="active"
        )

    def test_did_end_bigger_than_start(self):
        """Test that the constraint 'end' > 'start' raises an IntegrityError."""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                PhoneDID.objects.create(
                    start=1100000000,
                    end=110000000,
                    delivery=self.delivery,
                    site=self.site1
                )

    def test_did_overlaps_ndi(self):
        """Test that the DID range does not overlap with the NDI."""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                PhoneDID.objects.create(
                    start=9999999999,
                    end=1000000000,
                    site=self.site2
                )

    def test_did_overlaps_dto(self):
        """Test that the DID range does not overlap with the DTO."""
        with self.assertRaises(ValidationError):
            PhoneDID.objects.create(
                start=1000000001,
                end=1000000002,
                site=self.site1,
                delivery=self.delivery
            ).full_clean()

    def test_did_range_overlaps(self):
        """Test that DID ranges do not overlap."""
        did_valid = PhoneDID.objects.create(
            start=200000000,
            end=200000008,
            delivery=self.delivery,
            site=self.site1
        )
        did_valid.full_clean()
        did_valid.save()

        with self.assertRaises(ValidationError):
            PhoneDID.objects.create(
                start=200000005,
                end=200000010,
                delivery=self.delivery,
                site=self.site1
            ).full_clean()

