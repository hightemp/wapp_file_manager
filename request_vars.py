

class RequestVars:
    dProjectFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сортировка',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
    }

    dGroupFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'project': {
            'name': 'Проект',
            'type': 'select',
            'field_name': 'project',
            'list': [],
            'value': '',
            'sel_value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сортировка',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
    }

    dTaskFields = {
        'id': {
            'name': 'id',
            'type': 'hidden',
            'field_name': 'id',
            'value': '',
        },
        'group': {
            'name': 'Проект',
            'type': 'select',
            'field_name': 'group',
            'list': [],
            'value': '',
            'sel_value': '',
        },
        'name': {
            'name': 'Название',
            'type': 'text',
            'field_name': 'name',
            'value': '',
        },
        'sort': {
            'name': 'Сортировка',
            'type': 'text',
            'field_name': 'sort',
            'value': '',
        },
        'a_html': {
            'name': 'Описание HTML',
            'type': 'textarea',
            'field_name': 'a_html',
            'value': '',
        },
        'a_markdown': {
            'name': 'Описание Markdown',
            'type': 'textarea',
            'field_name': 'a_markdown',
            'value': '',
        },
    }

    dClasses = {
        'group': 'Group',
        'category': 'Category',
        'account': 'Account',
    }

    aProjectsButtons = [
        {"name":"reload", "cls":"bi-arrow-repeat", "btn_cls": "btn-primary"},
        {"name":"create-project", "cls":"bi-file-plus", "btn_cls": "btn-success"},
        {"name":"edit-project", "cls":"bi-pencil", "btn_cls": "btn-secondary"},
        {"name":"remove-project", "cls":"bi-trash", "btn_cls": "btn-danger"},
    ]

    oArgs = {}
    oArgsLists = {}

    sBaseURL = ""

    sPreviewURL = ""

    sSelectFile = ''
    sSelectTab = ''
    sSelectDir = ''
    sSelectPath = ''
    sSelectFileExt = 'Все'

    sDownload = ""
    sFullPath = ""

    sPath = ""
    sDir = ""
    sFile = ""
    sFileExt = ""

    oGroupedFiles = {}
    aFilesInfoTemp = []
    aFilesInfo = []

    oCurTab = {}

    aTabs = []
    aExitstsTabs = []

    aFiles = []
    aDirs = []
    aFilesInfo = []
    oGroupedFiles = dict()

class SessionVars:
    sSelectFile = ""
