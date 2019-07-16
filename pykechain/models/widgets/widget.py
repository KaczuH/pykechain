from typing import Any, Optional, List, AnyStr, Dict

import requests
from jsonschema import validate

from pykechain.enums import WidgetTypes
from pykechain.exceptions import APIError
from pykechain.models import Base
from pykechain.models.widgets.widget_schemas import widget_meta_schema


class Widget(Base):
    """A virtual object representing a KE-chain Widget.

    :cvar basestring id: UUID of the widget
    :cvar basestring title: Title of the widget
    :cvar basestring ref: Reference of the widget
    :cvar basestring widget_type: Type of the widget. Should be one of :class:`WidgetTypes`
    :cvar dict meta: Meta definition of the widget
    :cvar int order: Order of the widget in the list of widgets
    :cvar bool has_subwidgets: if the widgets contains any subwidgets. In case this widget being eg. a Multicolumn
    :cvar float progress: Progress of the widget
    """

    schema = widget_meta_schema

    def __init__(self, json, **kwargs):
        # type: (dict, **Any) -> None
        """Construct a Widget from a KE-chain 2 json response.

        :param json: the json response to construct the :class:`Part` from
        :type json: dict
        """
        # we need to run the init of 'Base' instead of 'Part' as we do not need the instantiation of properties
        super(Widget, self).__init__(json, **kwargs)
        del self.name

        self.title = json.get('title')
        self.ref = json.get('ref')
        self.widget_type = json.get('widget_type')
        # set schema
        if self._client:
            self.schema = self._client.widget_schema(self.widget_type)

        self.meta = self.validate_meta(json.get('meta'))
        self.order = json.get('order')
        self._activity_id = json.get('activity_id')
        self._parent_id = json.get('parent_id')
        self.has_subwidgets = json.get('has_subwidgets')
        self._scope_id = json.get('scope_id')
        self.progress = json.get('progress')

    def __repr__(self):  # pragma: no cover
        return "<pyke {} '{}' id {}>".format(self.__class__.__name__, self.widget_type, self.id[-8:])

    def activity(self):
        # type: () -> Activity2  # noqa: F821 to prevent circular imports
        """Activity associated to the widget.

        :return: The Activity
        :rtype: :class:`Activity2`
        """
        return self._client.activity(id=self._activity_id)

    def parent(self):
        # type: () -> Widget
        """Parent widget.

        :return: The parent of this widget.
        :rtype: :class:`Widget`
        """
        return self._client.widget(id=self._parent_id)

    def validate_meta(self, meta):
        # type: (dict) -> dict
        """Validate the meta and return the meta if validation is successfull.

        :param meta: meta of the widget to be validated.
        :type meta: dict
        :return meta: if the meta is validated correctly
        :raise: `ValidationError`
        """
        return validate(meta, self.schema) is None and meta

    @classmethod
    def create(cls, json, **kwargs):
        # type: (dict, **Any) -> Widget
        """Create a widget based on the json data.

        This method will attach the right class to a widget, enabling the use of type-specific methods.

        It does not create a widget object in KE-chain. But a pseudo :class:`Widget` object.

        :param json: the json from which the :class:`Widget` object to create
        :type json: dict
        :return: a :class:`Widget` object
        :rtype: :class:`Widget`
        """

        def _type_to_classname(widget_type):
            """
            Generate corresponding inner classname based on the widget type.

            :param widget_type: type of the widget (one of :class:`WidgetTypes`)
            :type widget_type: str
            :return: classname corresponding to the widget type
            :rtype: str
            """
            if widget_type is None:
                widget_type = WidgetTypes.UNDEFINED
            return "{}Widget".format(widget_type.title())

        widget_type = json.get('widget_type')

        # dispatcher to instantiate the right widget class based on the widget type
        # load all difference widget types from the pykechain.model.widgets module.
        import importlib
        all_widgets = importlib.import_module("pykechain.models.widgets")
        if hasattr(all_widgets, _type_to_classname(widget_type)):
            return getattr(all_widgets, _type_to_classname(widget_type))(json, client=kwargs.pop('client'), **kwargs)
        else:
            return getattr(all_widgets, _type_to_classname(WidgetTypes.UNDEFINED))(json, client=kwargs.pop('client'),
                                                                                   **kwargs)

    def update_associations(self, readable_models=None, writable_models=None, **kwargs):
        # type: (Optional[List], Optional[List], **Any) -> None
        """
        Update associations on this widget.

        This is an absolute list of associations. If you provide No models, than the associations are cleared.

        Alternatively you may use `inputs` or `outputs` as a alias to `readable_models` and `writable_models`
        respectively.

        :param readable_models: list of property models (of :class:`Property` or property_ids (uuids) that has
                                read rights (alias = inputs)
        :type readable_models: List[Property] or List[UUID] or None
        :param writable_models: list of property models (of :class:`Property` or property_ids (uuids) that has
                                write rights (alias = outputs)
        :type writable_models: List[Property] or List[UUID] or None
        :param kwargs: additional keyword arguments to be passed into the API call as param.
        :return: None
        :raises APIError: when the associations could not be changed
        :raise IllegalArgumentError: when the list is not of the right type
        """
        self._client.update_widget_associations(widget=self, readable_models=readable_models,
                                                writable_models=writable_models, **kwargs)

    def edit(self, title=None, meta=None, **kwargs):
        # type: (Optional[AnyStr], Optional[Dict], **Any) -> None
        """Edit the details of a widget.

        :param title: (optional) title of the widget
        :type title: basestring or None
        :param meta: (optional) new Meta definition
        :type meta: dict or None
        :raises APIError: if the widget could not be updated.
        """
        update_dict = dict()

        if update_dict is not None:
            update_dict.update(dict(meta=meta))
        if title is not None:
            update_dict.update(dict(title=title))
        if kwargs:
            update_dict.update(**kwargs)

        from pykechain.client import API_EXTRA_PARAMS
        url = self._client._build_url('widget', widget_id=self.id)
        response = self._client._request('PUT', url, params=API_EXTRA_PARAMS['widgets'], json=update_dict)

        if response.status_code != requests.codes.ok:  # pragma: no cover
            raise APIError("Could not update Widget ({})".format(response))

        self.refresh(json=response.json().get('results')[0])

    def delete(self):
        # type: () -> bool
        """Delete the widget.

        :return: True when successful
        :rtype: bool
        :raises APIError: when unable to delete the activity
        """
        url = self._client._build_url('widget', widget_id=self.id)
        response = self._client._request('DELETE', url)

        if response.status_code != requests.codes.no_content:  # pragma: no cover
            raise APIError("Could not delete Widget ({})".format(response))

        return True
