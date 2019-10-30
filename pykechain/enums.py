class Enum(object):
    """Custom enumeration class to support class attributes as options.

    Example
    -------
    >>> class Toppings(Enum):
    ...    CHEESE = "Cheese"
    ...    SALAMI = "Salami"
    >>> topping_choice = Toppings.CHEESE

    """

    @classmethod
    def options(cls):
        """Provide a sorted list of options."""
        return sorted((value, name) for (name, value) in cls.__dict__.items() if not name.startswith('__'))

    @classmethod
    def values(cls):
        """Provide a (sorted) list of values."""
        return [value for (value, name) in cls.options()]


class Multiplicity(Enum):
    """The various multiplicities that are accepted by KE-chain.

    For more information on the representation in KE-chain, please consult the KE-chain `Part documentation`_.

    :cvar ZERO_ONE: Multiplicity 0 to 1
    :cvar ONE: Multiplicity 1
    :cvar ZERO_MANY: Multiplicity 0 to infinity
    :cvar ONE_MANY: Multiplicity 1 to infinity
    """

    ZERO_ONE = "ZERO_ONE"
    ONE = "ONE"
    ZERO_MANY = "ZERO_MANY"
    ONE_MANY = "ONE_MANY"
    # M_N = "M_N"  # not implemented


class Category(Enum):
    """The various categories of Parts that are accepted by KE-chain.

    For more information on the representation in KE-chain, please consult the KE-chain `Part documentation`_.

    :cvar INSTANCE: Category of Instance
    :cvar MODEL: Category of Model
    """

    INSTANCE = "INSTANCE"
    MODEL = "MODEL"


class Classification(Enum):
    """The various classification of Parts that are accepted by KE-chain.

    For more information on the representation in KE-chain, please consult the KE-chain `Part documentation`_.

    :cvar PRODUCT: Classification of the part object is Product
    :cvar CATALOG: Classification of the part object is a CATALOG

    .. _Part documentation: https://support.ke-chain.com/confluence/dosearchsite.action?queryString=concept+part
    """

    PRODUCT = "PRODUCT"
    CATALOG = "CATALOG"


class PropertyType(Enum):
    """The various property types that are accepted by KE-chain.

    For more information on the representation in KE-chain, please consult the KE-chain `Property documentation`_.

    :cvar CHAR_VALUE: a charfield property (single line text)
    :cvar TEXT_VALUE: text property (long text, may span multiple lines)
    :cvar BOOLEAN_VALUE: a boolean value property (True/False)
    :cvar INT_VALUE: integer property (whole number)
    :cvar FLOAT_VALUE: floating point number property (with digits)
    :cvar DATETIME_VALUE: a datetime value property
    :cvar ATTACHMENT_VALUE: an attachment property
    :cvar LINK_VALUE: url property
    :cvar REFERENCE_VALUE: a reference property, a UUID value referring to other part model

    .. versionadded:: 1.14

    :cvar SINGLE_SELECT_VALUE: single select list property (choose from a list)
    :cvar REFERENCES_VALUE: a multi reference property, a list of UUID values referring to other part models

    .. _Property documentation: https://support.ke-chain.com/confluence/dosearchsite.action?queryString=concept+property
    """

    CHAR_VALUE = "CHAR_VALUE"
    TEXT_VALUE = "TEXT_VALUE"
    BOOLEAN_VALUE = "BOOLEAN_VALUE"
    INT_VALUE = "INT_VALUE"
    FLOAT_VALUE = "FLOAT_VALUE"
    DATETIME_VALUE = "DATETIME_VALUE"
    ATTACHMENT_VALUE = "ATTACHMENT_VALUE"
    LINK_VALUE = "LINK_VALUE"
    SINGLE_SELECT_VALUE = 'SINGLE_SELECT_VALUE'
    REFERENCE_VALUE = 'REFERENCE_VALUE'
    REFERENCES_VALUE = "REFERENCES_VALUE"


class ActivityType(Enum):
    """The various Activity types that are accepted by KE-chain.

    .. versionadded:: 2.0

    :cvar TASK: a normal task
    :cvar PROCESS: a subprocess (container) containing other tasks

    For WIM version 1:

    :cvar USERTASK: a normal usertask
    :cvar SUBPROCESS: a subprocess (container) containing other tasks
    :cvar SERVICETASK: a service taks (this concept is only availabe in RND KE-chain and will be deprecated)
    """

    # WIM2:
    PROCESS = 'PROCESS'
    TASK = 'TASK'

    # WIM1:
    USERTASK = "UserTask"
    SERVICETASK = "ServiceTask"  # RND code only
    SUBPROCESS = "Subprocess"


WIMCompatibleActivityTypes = {
    # backwards pykechain script compatible with wim2
    # from WIM1 to WIM2:
    ActivityType.USERTASK: ActivityType.TASK,
    ActivityType.SUBPROCESS: ActivityType.PROCESS,

    # forwarde pykechain scripts made for wim2, compatible with wim1
    # from WIM2 to WIM1:
    ActivityType.PROCESS: ActivityType.SUBPROCESS,
    ActivityType.TASK: ActivityType.USERTASK}


class ActivityClassification(Enum):
    """The classification of Activities that are accepted by KE-chain.

    .. versionadded:: 2.0

    :cvar WORKFLOW: Classification of the activity is WORKFLOW
    :cvar CATALOG: Classification of the activity is CATALOG
    """

    WORKFLOW = 'WORKFLOW'
    CATALOG = 'CATALOG'


class ActivityRootNames(Enum):
    """The classification of Activities that are accepted by KE-chain.

    .. versionadded:: 2.0

    :cvar WORKFLOW_ROOT: Root of the activity is WORKFLOW_ROOT
    :cvar CATALOG_ROOT: Root of the activity is CATALOG_ROOT (below are CATALOG tasks)
    """

    WORKFLOW_ROOT = 'WORKFLOW_ROOT'
    CATALOG_ROOT = 'CATALOG_ROOT'


class ComponentXType(Enum):
    """The various inspectortypes supported in the customized task in KE-chain.

    :cvar PANEL: panel
    :cvar TOOLBAR: toolbar
    :cvar PROPERTYGRID: propertyGrid
    :cvar SUPERGRID: superGrid
    :cvar PAGINATEDSUPERGRID: paginatedSuperGrid
    :cvar FILTEREDGRID: filteredGrid
    :cvar DISPLAYFIELD: displayfield
    :cvar PROPERTYATTACHMENTPREVIEWER: propertyAttachmentViewer
    :cvar HTMLPANEL: htmlPanel
    :cvar EXECUTESERVICE: executeService
    :cvar NOTEBOOKPANEL: notebookPanel
    :cvar BUTTON: button
    :cvar MODELVIEWER: modelViewer
    :cvar CSVGRID: csvGrid
    :cvar JSONTREE: jsonTree
    """

    PANEL = "panel"
    TOOLBAR = "toolbar"
    PROPERTYGRID = "propertyGrid"
    SUPERGRID = "superGrid"
    PAGINATEDSUPERGRID = "paginatedSuperGrid"
    FILTEREDGRID = "filteredGrid"
    DISPLAYFIELD = "displayfield"
    # in 1.13.1
    PROPERTYATTACHMENTPREVIEWER = "propertyAttachmentViewer"
    HTMLPANEL = "htmlPanel"
    EXECUTESERVICE = "executeService"
    NOTEBOOKPANEL = "notebookPanel"
    # Issue #279:
    ACTIVITYNAVIGATIONBAR = "activityNavigationBar"

    # for RND
    BUTTON = "button"
    MODELVIEWER = "modelViewer"
    CSVGRID = "csvGrid"
    JSONTREE = "jsonTree"


class WidgetNames(Enum):
    """The various Names of the Widget that can be configured.

    :cvar SUPERGRIDWIDGET: superGridWidget
    :cvar PROPERTYGRIDWIDGET: propertyGridWidget
    :cvar HTMLWIDGET: htmlWidget
    :cvar FILTEREDGRIDWIDGET: filteredGridWidget
    :cvar SERVICEWIDGET: serviceWidget
    :cvar NOTEBOOKWIDGET: notebookWidget
    :cvar ATTACHMENTVIEWERWIDGET: attachmentViewerWidget
    :cvar TASKNAVIGATIONBARWIDGET: taskNavigationBarWidget
    :cvar JSONWIDGET: jsonWidget

    # KE-chain 3 only
    :cvar SIGNATUREWIDGET: signatureWidget
    :cvar CARDWIDGET: cardWidget
    :cvar METAPANELWIDGET: metaPanelWidget
    :cvar MULTICOLUMNWIDGET: multiColumnWidget
    :cvar PROGRESSWIDGET: progressWidget
    """

    SUPERGRIDWIDGET = 'superGridWidget'
    PROPERTYGRIDWIDGET = 'propertyGridWidget'
    HTMLWIDGET = 'htmlWidget'
    FILTEREDGRIDWIDGET = 'filteredGridWidget'
    SERVICEWIDGET = 'serviceWidget'
    NOTEBOOKWIDGET = 'notebookWidget'
    ATTACHMENTVIEWERWIDGET = 'attachmentViewerWidget'
    TASKNAVIGATIONBARWIDGET = 'taskNavigationBarWidget'
    JSONWIDGET = 'jsonWidget'
    METAPANELWIDGET = 'metaPanelWidget'
    MULTICOLUMNWIDGET = 'multiColumnWidget'
    SIGNATUREWIDGET = 'signatureWidget'
    CARDWIDGET = 'cardWidget'
    PROGRESSWIDGET = 'progressWidget'


class WidgetTypes(Enum):
    """The various widget types for the widget definitions available to the widget api.

    :cvar UNDEFINED: Undefined Widget
    :cvar PROPERTYGRID: Propertygrid widget
    :cvar SUPERGRID: Supergrid widget
    :cvar HTML: Html widget
    :cvar FILTEREDGRID: Filteredgrid widget
    :cvar SERVICE: Service widget
    :cvar NOTEBOOK: Notebook widget
    :cvar ATTACHMENTVIEWER: Attachmentviewer widget
    :cvar TASKNAVIGATIONBAR: Tasknavigationbar widget
    :cvar JSON: Json widget
    :cvar METAPANEL: Metapanel widget
    :cvar MULTICOLUMN: Multicolumn widget
    :cvar SCOPE: Scope widget
    :cvar THIRDPARTY: Thirdparty widget
    :cvar PROGRESS: Progress widget
    :cvar SIGNATURE: Signature widget
    :cvar CARD: Card widget
    """

    UNDEFINED = 'UNDEFINED'
    PROPERTYGRID = 'PROPERTYGRID'
    SUPERGRID = 'SUPERGRID'
    HTML = 'HTML'
    FILTEREDGRID = 'FILTEREDGRID'
    SERVICE = 'SERVICE'
    NOTEBOOK = 'NOTEBOOK'
    ATTACHMENTVIEWER = 'ATTACHMENTVIEWER'
    TASKNAVIGATIONBAR = 'TASKNAVIGATIONBAR'
    JSON = 'JSON'
    METAPANEL = 'METAPANEL'
    MULTICOLUMN = 'MULTICOLUMN'
    SCOPE = 'SCOPE'
    THIRDPARTY = 'THIRDPARTY'
    PROGRESS = 'PROGRESS'
    SIGNATURE = 'SIGNATURE'
    CARD = 'CARD'


WidgetCompatibleTypes = {
    WidgetNames.SUPERGRIDWIDGET: WidgetTypes.SUPERGRID,
    WidgetNames.PROPERTYGRIDWIDGET: WidgetTypes.PROPERTYGRID,
    WidgetNames.HTMLWIDGET: WidgetTypes.HTML,
    WidgetNames.FILTEREDGRIDWIDGET: WidgetTypes.FILTEREDGRID,
    WidgetNames.SERVICEWIDGET: WidgetTypes.SERVICE,
    WidgetNames.NOTEBOOKWIDGET: WidgetTypes.NOTEBOOK,
    WidgetNames.ATTACHMENTVIEWERWIDGET: WidgetTypes.ATTACHMENTVIEWER,
    WidgetNames.TASKNAVIGATIONBARWIDGET: WidgetTypes.TASKNAVIGATIONBAR,
    WidgetNames.JSONWIDGET: WidgetTypes.JSON,
    WidgetNames.METAPANELWIDGET: WidgetTypes.METAPANEL,
    WidgetNames.MULTICOLUMNWIDGET: WidgetTypes.MULTICOLUMN,
    WidgetNames.PROGRESSWIDGET: WidgetTypes.PROGRESS,
    WidgetNames.SIGNATUREWIDGET: WidgetTypes.SIGNATURE,
    WidgetNames.CARDWIDGET: WidgetTypes.CARD
}

default_metapanel_widget = dict(
    name=WidgetNames.METAPANELWIDGET,
    config=dict(),
    meta=dict(
        showAll=True,
    ),
)

default_activity_customization = dict(
    ext=dict(
        widgets=[default_metapanel_widget]
    )
)


class ActivityStatus(Enum):
    """The various Activity statuses that are accepted by KE-chain.

    :cvar OPEN: status of activity is open
    :cvar COMPLETED: status of activity is completed
    """

    OPEN = 'OPEN'
    COMPLETED = 'COMPLETED'


class ScopeStatus(Enum):
    """The various status of a scope.

    .. versionchanged:: 3.0
      The `TEMPLATE` ScopeStatus is deprecated in KE-chain 3

    :cvar ACTIVE: Status of a scope is active (default)
    :cvar CLOSED: Status of a scope is closed
    :cvar TEMPLATE: Status of a scope is a template (not actively used)(deprecated in KE-chain 3.0)
    :cvar DELETING: Status of a scope when the scope is being deleted
    """

    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'
    TEMPLATE = 'TEMPLATE'
    DELETING = 'DELETING'


class ScopeCategory(Enum):
    """The various categories of a scope.

    .. versionadded::3.0

    :cvar LIBRARY_SCOPE: The scope is a library scope
    :cvar USER_SCOPE: The scope is a normal user scope
    :cvar TEMPLATE_SCOPE: The scope is a template scope
    """

    LIBRARY_SCOPE = 'LIBRARY_SCOPE'
    USER_SCOPE = 'USER_SCOPE'
    TEMPLATE_SCOPE = 'TEMPLATE_SCOPE'


class ServiceType(Enum):
    """The file types of sim script.

    :cvar PYTHON_SCRIPT: service is a python script
    :cvar NOTEBOOK: service is a jupyter notebook
    """

    PYTHON_SCRIPT = 'PYTHON SCRIPT'
    NOTEBOOK = 'NOTEBOOK'


class ServiceEnvironmentVersion(Enum):
    """The acceptable versions of python where services run on.

    :cvar PYTHON_2_7: Service execution environment is a python 2.7 container
    :cvar PYTHON_3_5: Service execution environment is a python 3.5 container
    :cvar PYTHON_3_5_NOTEBOOKS: execution environment is a python 3.5 container with jupyter notebook preinstalled
    """

    PYTHON_2_7 = '2.7'
    PYTHON_3_5 = '3.5'
    PYTHON_3_6 = '3.6'
    PYTHON_3_5_NOTEBOOKS = '3.5_notebook'
    PYTHON_3_6_NOTEBOOKS = '3.6_notebook'


class ServiceScriptUser(Enum):
    """The acceptable usertypes under which a (trusted) service is run.

    :cvar KENODE_USER: Run as "kenode" user. Equivalent to a manager in a scope.
    :cvar TEAMMANAGER_USER: Run as "kenode_team". Equivalent to a manager in a team. (disabled until available)
    :cvar CONFIGURATOR_USER: Run as "kenode_configurator". Equivalent to GG:Configurator.
    """

    KENODE_USER = "kenode"
    # TEAMMANAGER_USER = "kenode_team"
    CONFIGURATOR_USER = "kenode_configurator"


class ServiceExecutionStatus(Enum):
    """The acceptable states of a running service.

    :cvar LOADING: Execution is in LOADING state (next RUNNING, FAILED)
    :cvar RUNNING: Execution is in RUNNING state (next COMPLETED, FAILED, TERMINATING)
    :cvar COMPLETED: Execution is in COMPLETED state
    :cvar FAILED: Execution is in FAILED state
    :cvar TERMINATING: Execution is in TERMINATING state (next TERMINATED)
    :cvar TERMINATED: Execution is in TERMINATED state
    """

    LOADING = 'LOADING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    TERMINATING = 'TERMINATING'
    TERMINATED = 'TERMINATED'


class TeamRoles(Enum):
    """Roles that exist for a team member.

    :cvar MEMBER: A normal team member
    :cvar MANAGER: A team member that may manage the team (add or remove members, change team)
    :cvar OWNER: The owner of a team
    """

    MEMBER = "MEMBER"
    MANAGER = "MANAGER"
    OWNER = "OWNER"


class KechainEnv(Enum):
    """Environment variables that can be set for pykechain.

    :cvar KECHAIN_URL: full url of KE-chain where to connect to eg: 'https://<some>.ke-chain.com'
    :cvar KECHAIN_TOKEN: authentication token for the KE-chain user provided from KE-chain user account control
    :cvar KECHAIN_USERNAME: the username for the credentials
    :cvar KECHAIN_PASSWORD: the password for the credentials
    :cvar KECHAIN_SCOPE: the name of the project / scope. Should be unique, otherwise use scope_id
    :cvar KECHAIN_SCOPE_ID: the UUID of the project / scope.
    :cvar KECHAIN_FORCE_ENV_USE: set to 'true', '1', 'ok', or 'yes' to always use the environment variables.
    :cvar KECHAIN_SCOPE_STATUS: the status of the Scope to retrieve, defaults to None to retrieve all scopes
    :cvar KECHAIN_CHECK_CERTIFICATES: if the certificates of the URL should be checked.
    """

    KECHAIN_FORCE_ENV_USE = 'KECHAIN_FORCE_ENV_USE'
    KECHAIN_URL = 'KECHAIN_URL'
    KECHAIN_TOKEN = 'KECHAIN_TOKEN'
    KECHAIN_USERNAME = 'KECHAIN_USERNAME'
    KECHAIN_PASSWORD = 'KECHAIN_PASSWORD'
    KECHAIN_SCOPE = 'KECHAIN_SCOPE'
    KECHAIN_SCOPE_ID = 'KECHAIN_SCOPE_ID'
    KECHAIN_SCOPE_STATUS = 'KECHAIN_SCOPE_STATUS'
    KECHAIN_CHECK_CERTIFICATES = 'KECHAIN_CHECK_CERTIFICATES'


class SortTable(Enum):
    """The acceptable sorting options for a grid/table.

    :cvar ASCENDING: Table is sorted in ASCENDING ORDER
    :cvar DESCENDING: Table is sorted in DESCENDING ORDER
    """

    ASCENDING = 'ASC'
    DESCENDING = 'DESC'


class NavigationBarAlignment(Enum):
    """The acceptable alignment options for a Navigation Bar Widget.

    :cvar START: Buttons are aligned to the left (for KE-chain 2)
    :cvar LEFT: Buttons are aligned to the left (for KE-chain 3)
    :cvar CENTER: Buttons are aligned to the center
    """

    CENTER = 'center'

    # for KE-chain 2
    START = 'start'

    # for KE-chain 3
    LEFT = 'left'
    RIGHT = 'right'


class PaperSize(Enum):
    """The acceptable paper sizes options for a downloaded PDF.

    :cvar A0: Paper of size A0
    :cvar A1: Paper of size A1
    :cvar A2: Paper of size A2
    :cvar A3: Paper of size A3
    :cvar A4: Paper of size A4
    """

    A0 = 'a0paper'
    A1 = 'a1paper'
    A2 = 'a2paper'
    A3 = 'a3paper'
    A4 = 'a4paper'


class PaperOrientation(Enum):
    """The acceptable paper orientation options for a downloaded PDF.

    :cvar PORTRAIT: Paper of orientation 'portrait'
    :cvar LANDSCAPE: Paper of orientation 'landscape'
    """

    PORTRAIT = 'portrait'
    LANDSCAPE = 'landscape'


class PropertyVTypes(Enum):
    """The VTypes (or validator types) that are allowed in the json.

    This corresponds to the various validator classes which SHOULD be named:
       `vtype[0].upper() + vtype[1:]`
       eg: 'numbericRangeValidator' has an implementation class of 'NumericRangeValidator'

    .. versionadded:: 2.2

    :cvar NONEVALIDATOR: noneValidator - No validation is done
    :cvar NUMERICRANGE: numericRangeValidator
    :cvar BOOLEANFIELD: booleanFieldValidator
    :cvar REQUIREDFIELD: requiredFieldValidator
    :cvar EVENNUMBER: evenNumberValidator
    :cvar ODDNUMBER: oddNumberValidator
    :cvar REGEXSTRING: regexStringValidator
    :cvar SINGLEREFERENCE: 'singleReferenceValidator'
    """

    NONEVALIDATOR = 'noneValidator'
    NUMERICRANGE = 'numericRangeValidator'
    BOOLEANFIELD = 'booleanFieldValidator'
    REQUIREDFIELD = 'requiredFieldValidator'
    EVENNUMBER = 'evenNumberValidator'
    ODDNUMBER = 'oddNumberValidator'
    REGEXSTRING = 'regexStringValidator'
    SINGLEREFERENCE = 'singleReferenceValidator'


class ValidatorEffectTypes(Enum):
    """The effects that can be attached to a validator.

    .. versionadded:: 2.2

    :cvar NONE_EFFECT: noneEffect
    :cvar VISUALEFFECT: visualEffect
    :cvar TEXT_EFFECT: textEffect
    :cvar ERRORTEXT_EFFECT: errorTextEffect
    :cvar HELPTEXT_EFFECT: helpTextEffect
    """

    NONE_EFFECT = 'noneEffect'
    VISUALEFFECT = 'visualEffect'
    TEXT_EFFECT = 'textEffect'
    ERRORTEXT_EFFECT = 'errorTextEffect'
    HELPTEXT_EFFECT = 'helpTextEffect'


class PropertyRepresentation(Enum):
    """
    The Representation configuration to display a property value.

    .. versionadded:: 3.0

    :cvar DECIMAL_PLACES: Amount of decimal places to show the number
    :cvar SIGNIFICANT_DIGITS: Number (count) of significant digits to display the number
    :cvar LINK_TARGET: configuration of a link to open the link in a new browsertab or not.
    """

    DECIMAL_PLACES = "decimalPlaces"
    SIGNIFICANT_DIGITS = "significantDigits"
    LINK_TARGET = "linkTarget"


class ShowColumnTypes(Enum):
    """The columns that can be shown in a Property grid.

    .. versionadded:: 2.3

    :cvar UNIT: unit
    :cvar DESCRIPTION: description
    """

    UNIT = 'unit'
    DESCRIPTION = 'description'


class ScopeWidgetColumnTypes(Enum):
    """The columns that can be shown in a Scope widget grid.

    .. versionadded:: 3.0

    :cvar PROJECT_NAME: Project Name
    :cvar START_DATE: Start date
    :cvar DUE_DATE: Due date
    :cvar PROGRESS: Progress
    :cvar STATUS: Status
    """

    PROJECT_NAME = 'Project Name'
    START_DATE = 'Start date'
    DUE_DATE = 'Due date'
    PROGRESS = 'Progress'
    STATUS = 'Status'


class FilterType(Enum):
    """The type of pre-filters that can be set on a Multi Reference Property.

    .. versionadded:: 3.0

    :cvar GREATER_THAN_EQUAL: 'gte'
    :cvar LOWER_THAN_EQUAL: 'lte'
    :cvar CONTAINS: 'icontains'
    :cvar EXACT: 'exact'
    """

    GREATER_THAN_EQUAL = 'gte'
    LOWER_THAN_EQUAL = 'lte'
    CONTAINS = 'icontains'
    EXACT = 'exact'


class ProgressBarColors(Enum):
    """
    Some basic colors that can be set on a Progress Bar inside a Progress Bar Widget.

    .. versionadded:: 3.0

    :cvar BLACK: '#000000'
    :cvar WHITE: '#FFFFFF'
    :cvar RED: 'FF0000'
    :cvar LIME: '#00FF00'
    :cvar BLUE: '#0000FF'
    :cvar YELLOW: '#FFFF00'
    :cvar CYAN: '#00FFFF'
    :cvar MAGENTA: '#FF00FF'
    :cvar SILVER: '#C0C0C0'
    :cvar GRAY: '#808080'
    :cvar MAROON: '#800000'
    :cvar OLIVE: '#808000'
    :cvar GREEN: '#008000'
    :cvar PURPLE: '#800080'
    :cvar TEAL: '#008080'
    :cvar NAVY: '#000080'
    :cvar DEFAULT_COMPLETED: '#339447'
    :cvar DEFAULT_IN_PROGRESS: '#FF6600'
    :cvar DEFAULT_NO_PROGRESS: '#EEEEEE'
    :cvar DEFAULT_IN_PROGRESS_BACKGROUND: '#FC7C3D'
    """

    BLACK = '#000000'
    WHITE = '#FFFFFF'
    RED = '#FF0000'
    LIME = '#00FF00'
    BLUE = '#0000FF'
    YELLOW = '#FFFF00'
    CYAN = '#00FFFF'
    MAGENTA = '#FF00FF'
    SILVER = '#C0C0C0'
    GRAY = '#808080'
    MAROON = '#800000'
    OLIVE = '#808000'
    GREEN = '#008000'
    PURPLE = '#800080'
    TEAL = '#008080'
    NAVY = '#000080'
    DEFAULT_COMPLETED = '#339447'
    DEFAULT_IN_PROGRESS = '#FF6600'
    DEFAULT_NO_PROGRESS = '#EEEEEE'
    DEFAULT_IN_PROGRESS_BACKGROUND = '#FC7C3D'


class CardWidgetLinkTarget(Enum):
    """
    Target for the CardWidget link.

    .. versionadded:: 3.0

    :cvar SAME_TAB: "_self"
    :cvar NEW_TAB: "_blank"
    """

    SAME_TAB = "_self"
    NEW_TAB = '_blank'


class CardWidgetLinkValue(Enum):
    """
    Link Value for the CardWidget.

    .. versionadded:: 3.0

    :cvar EXTERNAL_LINK: "External link"
    :cvar TASK_LINK: "Task link"
    :cvar NO_LINK: "No link"
    """

    EXTERNAL_LINK = "External link"
    TASK_LINK = "Task link"
    NO_LINK = "No link"


class CardWidgetImageValue(Enum):
    """
    Image for the CardWidget.

    .. versionadded:: 3.0

    :cvar CUSTOM_IMAGE: "Custom image"
    :cvar NO_IMAGE: "No image"
    """

    CUSTOM_IMAGE = "Custom image"
    NO_IMAGE = "No image"
