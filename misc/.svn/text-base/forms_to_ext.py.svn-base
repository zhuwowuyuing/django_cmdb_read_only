from copy import copy, deepcopy
from django import newforms as forms
from django.core.serializers.json import DjangoJSONEncoder
from django.newforms import fields
from django.newforms.models import QuerySetIterator, ModelChoiceField, ModelMultipleChoiceField
from signet.canvas.fields import BooleanField, NullField

class ExtJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode django forms into ExtJS config objects.
    """

    CHECKBOX_EDITOR = {
        'editor': {
            'xtype': 'checkbox'
        }
    }
    COMBO_EDITOR = {
        'editor': {
            #'listWidth': 'auto',
            'width': 150,
            'xtype': 'jsoncombo'
        }
    }
    DATE_EDITOR = {
        'editor': {
            'xtype': 'datefield'
        }
    }
    EMAIL_EDITOR = {
        'vtype':'email',
        'editor': {
            'xtype': 'textfield'
        }
    }
    NUMBER_EDITOR = {
        'editor': {
            'xtype': 'numberfield'
        }
    }
    NULL_EDITOR = {
        'fieldHidden': True,
        'editor': {
            'xtype': 'textfield'
        },
    }
    TEXT_EDITOR = {
        'editor': {
            'xtype': 'textfield'
        }
    }
    TIME_EDITOR = {
        'editor': {
            'xtype': 'timefield'
        }
    }
    URL_EDITOR = {
        'vtype':'url',
        'editor': {
            'xtype': 'textfield'
        }
    }
    CHAR_PIXEL_WIDTH = 8

    EXT_DEFAULT_CONFIG = {
        'editor': TEXT_EDITOR
        #'labelWidth': 300,
        #'autoWidth': True,
    }

    DJANGO_EXT_FIELD_TYPES = {
        fields.BooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        fields.CharField: ["Ext.form.TextField", TEXT_EDITOR],
        fields.ChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.DateField: ["Ext.form.DateField", DATE_EDITOR],
        fields.DateTimeField: ["Ext.form.DateField", DATE_EDITOR],
        fields.DecimalField: ["Ext.form.NumberField", NUMBER_EDITOR],
        fields.EmailField: ["Ext.form.TextField", EMAIL_EDITOR],
        fields.IntegerField: ["Ext.form.NumberField", NUMBER_EDITOR],
        ModelChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        ModelMultipleChoiceField: ["Ext.form.ComboBox", COMBO_EDITOR],
        fields.MultipleChoiceField: ["Ext.form.ComboBox",COMBO_EDITOR],
        NullField: ["Ext.form.TextField", NULL_EDITOR],
        fields.NullBooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        BooleanField: ["Ext.form.Checkbox", CHECKBOX_EDITOR],
        fields.SplitDateTimeField: ["Ext.form.DateField", DATE_EDITOR],
        fields.TimeField: ["Ext.form.DateField", TIME_EDITOR],
        fields.URLField: ["Ext.form.TextField", URL_EDITOR],
    }

    EXT_DATE_ALT_FORMATS = 'm/d/Y|n/j/Y|n/j/y|m/j/y|n/d/y|m/j/Y|n/d/Y|m-d-y|m-d-Y|m/d|m-d|md|mdy|mdY|d|Y-m-d'

    EXT_TIME_ALT_FORMATS = 'm/d/Y|m-d-y|m-d-Y|m/d|m-d|d'

    DJANGO_EXT_FIELD_ATTRS = {
        #Key: django field attribute name
        #Value: tuple[0] = ext field attribute name,
        #       tuple[1] = default value
        'choices': ['store', None],
        #'default': ['value', None],
        'fieldset': ['fieldSet', None],
        'help_text': ['helpText', None],
        'initial': ['value', None],
        #'input_formats': ['altFormats', None],
        'label': ['fieldLabel', None],
        'max_length': ['maxLength', None],
        'max_value': ['maxValue', None],
        'min_value': ['minValue', None],
        'name': ['name', None],
        'required': ['allowBlank', False],
        'size': ['width', None],
        'hidden': ['fieldHidden', False],
    }

    def default(self, o):
        if issubclass(o.__class__, forms.Form):
            flds = []

            for name, field in o.fields.items():
                if isinstance(field, dict):
                    field['title'] = name
                else:
                    field.name = name
                cfg = self.default(field)
                flds.append(cfg)

            flds.append({
                "header": "text",
                "editor": {"width": 144,
                            "allowBlank": True,
                            "fieldHidden": True,
                            "xtype": "textfield",
                            "maxLength": 255},
                'name': 'text'
            })
            return flds
        elif isinstance(o, dict):
            #Fieldset
            default_config = {
                'autoHeight': True,
                'collapsible': True,
                'items': [],
                'labelWidth': 200,
                'title': o['title'],
                'xtype':'fieldset',
            }
            del o['title']

            #Ensure fields are added sorted by position
            for name, field in sorted(o.items()):
                field.name = name
                default_config['items'].append(self.default(field))
            return default_config
        elif issubclass(o.__class__, fields.Field):
            default_config = {}
            if o.__class__ in self.DJANGO_EXT_FIELD_TYPES:
                default_config.update(self.DJANGO_EXT_FIELD_TYPES[o.__class__][1])
            else:
                default_config.update(self.EXT_DEFAULT_CONFIG['editor'])
            config = deepcopy(default_config)
            for dj, ext in self.DJANGO_EXT_FIELD_ATTRS.items():
                v = None
                if dj == 'size':
                    v = o.widget.attrs.get(dj, None)
                    if v is not None:
                        if o.__class__ in (fields.DateField, fields.DateTimeField,
                           fields.SplitDateTimeField, fields.TimeField):
                            v += 8
                        #Django's size attribute is the number of characters,
                        #so multiply by the pixel width of a character
                        v = v * self.CHAR_PIXEL_WIDTH
                elif dj == 'hidden':
                    v = o.widget.attrs.get(dj, default_config.get('fieldHidden', ext[1]))
                elif dj == 'name':
                    v = o.name
                elif getattr(o, dj, ext[1]) is None:
                    pass
                #elif dj == 'input_formats':
                    #alt_fmts = []
                    ##Strip out the '%'  placeholders
                    #for fmt in getattr(field, dj, ext[1]):
                        #alt_fmts.append(fmt.replace('%', ''))
                    #v = u'|'.join(alt_fmts)
                elif isinstance(ext[1], basestring):
                    v = getattr(o, dj, getattr(field, ext[1]))
                elif ext[0] == 'store':
                    v = {
                        'autoLoad': True,
                        'storeId': o.name,
                        'url': '/csds/ext/rdo/queryset/%s/' % (o.name.lower(),),
                        #'xtype': 'jsonstore',
                    }
                else:
                    v = getattr(o, dj, ext[1])
                if v is not None:
                    if ext[0] == 'value':
                        config[ext[0]] = v
                    if ext[0] == 'name':
                        config[ext[0]] = v
                        config['header'] = v
                    elif ext[0] not in ('name', 'dataIndex', 'fieldLabel', 'header', 'defaultValue'):
                    #elif ext[0] in ('allowBlank', 'listWidth', 'store', 'width'):
                            #if isinstance(v, QuerySetIterator):
                            #    config['editor'][ext[0]] = list(v)
                        config[ext[0]] = v
                        config['editor'][ext[0]] = v
                        if ext[0] == 'store':
                            config['url'] = v['url']
                            config['editor']['displayField'] = 'display'
                            #config['editor']['forceSelection'] = True
                            config['editor']['hiddenName'] = o.name
                            config['editor']['lastQuery'] = ''
                            config['editor']['mode'] = 'remote'
                            config['editor']['triggerAction'] = 'all'
                            config['editor']['valueField'] = 'id'

                    elif isinstance(v, unicode):
                        config[ext[0]] = v.encode('utf8')
                    else:
                        config[ext[0]] = v
            return config
        else:
            return super(ExtJSONEncoder, self).default(o)