from django.test import TestCase
from eveuniverse.models import EveSolarSystem

from evescout.models import SignatureSystem
from evescout.tests.testdata.load_eveuniverse import load_eveuniverse


class TestSignatures(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_eveuniverse()

    def test_get_ids_set(self):
        oto = EveSolarSystem.objects.get(id=30002808)

        SignatureSystem.objects.create(
            id=1, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )
        SignatureSystem.objects.create(
            id=2, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )

        ids_set = SignatureSystem.get_signature_ids_set()

        self.assertEqual({1, 2}, ids_set)

    def test_disappeared_signatures(self):
        oto = EveSolarSystem.objects.get(id=30002808)

        sig_system_1 = SignatureSystem.objects.create(
            id=1, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )
        sig_system_2 = SignatureSystem.objects.create(
            id=2, system=oto, origin=SignatureSystem.SignatureOrigin.THERA
        )

        SignatureSystem.delete_disappeared_signatures([1])

        self.assertEqual(1, SignatureSystem.objects.count())
        self.assertIn(sig_system_1, SignatureSystem.objects.all())
        self.assertNotIn(sig_system_2, SignatureSystem.objects.all())
