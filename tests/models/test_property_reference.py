import datetime
import uuid

from pykechain.enums import PropertyType, Multiplicity, FilterType
from pykechain.exceptions import IllegalArgumentError
from pykechain.models import MultiReferenceProperty, MultiReferenceProperty2
from tests.classes import TestBetamax


class TestMultiReferenceProperty(TestBetamax):
    def setUp(self):
        super(TestMultiReferenceProperty, self).setUp()

        # reference Part target (model and 1 instance)
        self.wheel_model = self.project.model(name='Wheel')

        # reference property model (with a value pointing to a target part model
        self.ref_prop_name = 'Test reference property ({})'.format(str(uuid.uuid4())[-8:])
        self.ref_part = self.project.model('Bike')
        self.ref_part.add_property(
            name=self.ref_prop_name,
            property_type=PropertyType.REFERENCES_VALUE,
            default_value=self.wheel_model
        )  # type: MultiReferenceProperty2

        self.fabrication_date_property = self.wheel_model.add_property(
            name='Fabrication date',
            property_type=PropertyType.DATETIME_VALUE,
            default_value=datetime.datetime.now().isoformat()
        )  # datetime
        self.tyre_manufacturer_property = self.wheel_model.add_property(
            name='Tyre manufacturer',
            property_type=PropertyType.SINGLE_SELECT_VALUE,
            options={'value_choices': ['Michelin', 'Pirelli', 'Bridgestone']},
            default_value='Michelin'
        )

        self.reference_to_wheel = self.ref_part.add_property(
            name=self.ref_prop_name,
            property_type=PropertyType.REFERENCES_VALUE,
            default_value=self.wheel_model.id
        )  # type: MultiReferenceProperty2

        self.ref_model = self.ref_part.property(self.ref_prop_name)
        # reference property instance (holding the value
        self.ref = self.project.part('Bike').property(self.ref_prop_name)

    def tearDown(self):
        self.tyre_manufacturer_property.delete()
        self.fabrication_date_property.delete()
        self.reference_to_wheel.delete()
        self.ref_model.delete()
        super(TestMultiReferenceProperty, self).tearDown()

    def test_referencing_a_model(self):
        # setUp
        wheel_model = self.project.model('Wheel')
        self.ref_model.value = [wheel_model]

        # testing
        self.assertEqual(len(self.ref_model.value), 1)

    def test_referencing_multiple_instances_using_parts(self):
        # setUp
        wheel_model = self.project.model('Wheel')
        self.ref_model.value = [wheel_model]
        wheel_instances = wheel_model.instances()
        wheel_instances_list = [instance for instance in wheel_instances]

        # set ref value
        self.ref.value = wheel_instances_list

        # testing
        self.assertTrue(len(self.ref.value) >= 2)

        # tearDown
        self.ref.value = None

    def test_referencing_multiple_instances_using_ids(self):
        # setUp
        wheel_model = self.project.model('Wheel')
        self.ref_model.value = [wheel_model]
        wheel_instances = wheel_model.instances()
        wheel_instances_list = [instance.id for instance in wheel_instances]

        # set ref value
        self.ref.value = wheel_instances_list
        self.ref._cached_values = None

        # testing
        self.assertTrue(len(self.ref.value) >= 2)

        # tearDown
        self.ref.value = None

    def test_referencing_a_part_not_in_a_list(self):
        # setUp
        front_wheel = self.project.part('Front Wheel')

        # testing
        with self.assertRaises(ValueError):
            self.ref.value = front_wheel

    def test_referencing_a_list_with_no_parts(self):
        # setUp
        fake_part = [15, 21, 26]

        # testing
        with self.assertRaises(ValueError):
            self.ref.value = fake_part

    def test_value_if_multi_ref_gives_back_all_parts(self):
        """because of #276 problem"""
        # setUp
        wheel_model = self.project.model('Wheel')
        self.ref_model.value = [wheel_model]

        wheel_instances = wheel_model.instances()
        wheel_instances_list = [instance.id for instance in wheel_instances]

        # set ref value
        self.ref.value = wheel_instances_list

        # testing
        all_referred_parts = self.ref.value
        self.assertEqual(len(all_referred_parts), len(self.ref._value))

        # tearDown
        self.ref.value = None

    def test_value_if_nothing_is_referenced(self):
        # setUp
        value_of_multi_ref = self.ref.value

        # testing
        self.assertEqual(None, value_of_multi_ref)

    def test_multi_ref_choices(self):
        # testing
        possible_options = self.ref.choices()
        self.assertEqual(1, len(possible_options))

    def test_create_ref_property_referencing_part_in_list(self):
        # setUp
        new_reference_to_wheel = self.ref_part.add_property(
            name=self.ref_prop_name,
            property_type=PropertyType.REFERENCES_VALUE,
            default_value=[self.wheel_model]
        )
        # testing
        self.assertTrue(self.reference_to_wheel.value[0].id, self.wheel_model.id)

        # tearDown
        new_reference_to_wheel.delete()

    def test_create_ref_property_referencing_id_in_list(self):
        # setUp
        new_reference_to_wheel = self.ref_part.add_property(
            name=self.ref_prop_name,
            property_type=PropertyType.REFERENCES_VALUE,
            default_value=[self.wheel_model.id]
        )
        # testing
        self.assertTrue(self.reference_to_wheel.value[0].id, self.wheel_model.id)

        # tearDown
        new_reference_to_wheel.delete()

    def test_create_ref_property_wrongly_referencing_in_list(self):
        # testing
        with self.assertRaises(IllegalArgumentError):
            self.ref_part.add_property(
                name=self.ref_prop_name,
                property_type=PropertyType.REFERENCES_VALUE,
                default_value=[12]
            )

    def test_create_ref_property_referencing_part(self):
        # setUp
        new_reference_to_wheel = self.ref_part.add_property(
            name=self.ref_prop_name,
            property_type=PropertyType.REFERENCES_VALUE,
            default_value=self.wheel_model
        )
        # testing
        self.assertTrue(self.reference_to_wheel.value[0].id, self.wheel_model.id)

        # tearDown
        new_reference_to_wheel.delete()

    def test_create_ref_property_referencing_id(self):
        # setUp
        new_reference_to_wheel = self.ref_part.add_property(
            name=self.ref_prop_name,
            property_type=PropertyType.REFERENCES_VALUE,
            default_value=self.wheel_model.id
        )
        # testing
        self.assertTrue(self.reference_to_wheel.value[0].id, self.wheel_model.id)

        # tearDown
        new_reference_to_wheel.delete()

    def test_create_ref_property_wrongly_referencing(self):
        # testing
        with self.assertRaises(IllegalArgumentError):
            self.ref_part.add_property(
                name=self.ref_prop_name,
                property_type=PropertyType.REFERENCES_VALUE,
                default_value=True
            )

    # new in 2.3
    # def test_add_filters_to_property(self):
    #     # setUp
    #     # wheel_property_reference = self.project.model('Bike').property('Reference wheel')
    #     # wheel_model = self.project.model('Wheel')
    #
    #     # self.ref_target_model # part model
    #     # self.ref_target # part instance
    #
    #     diameter_property = self.ref_target_model.add_property(
    #         name='Diameter',
    #         property_type=PropertyType.FLOAT_VALUE,
    #         default_value=15.0
    #     )
    #     spokes_property = self.ref_target_model.add_property(
    #         name='Spokes',
    #         property_type=PropertyType.INT_VALUE,
    #         default_value=10
    #     )
    #
    #     prefilters = {'property_value': diameter_property.id + ":{}:lte".format(15)}
    #     propmodels_excl = [spokes_property.id]
    #     options = dict()
    #     options['prefilters'] = prefilters
    #     options['propmodels_excl'] = propmodels_excl
    #
    #     # testing
    #     self.ref_model.edit(options=options)
    #
    #     self.assertTrue('property_value' in self.ref_model._options['prefilters'] and
    #                     self.ref_model._options['prefilters']['property_value'] ==
    #                     diameter_property.id + ":{}:lte".format(15))
    #     self.assertTrue(spokes_property.id in self.ref_model._options['propmodels_excl'])

    # new in 3.0
    def test_set_prefilters_on_property(self):

        # already exist, not to be deleted
        diameter_property = self.wheel_model.property(name='Diameter')  # decimal property
        spokes_property = self.wheel_model.property(name='Spokes')  # integer property
        rim_material_property = self.wheel_model.property(name='Rim Material')  # single line text

        self.reference_to_wheel.set_prefilters(
            property_models=[diameter_property,
                             spokes_property,
                             rim_material_property,
                             self.fabrication_date_property,
                             self.tyre_manufacturer_property],
            values=[30.5,
                    7,
                    'Al',
                    datetime.datetime.now(),
                    'Michelin'],
            filters_type=[FilterType.GREATER_THAN_EQUAL,
                          FilterType.LOWER_THAN_EQUAL,
                          FilterType.CONTAINS,
                          FilterType.GREATER_THAN_EQUAL,
                          FilterType.CONTAINS]
        )
