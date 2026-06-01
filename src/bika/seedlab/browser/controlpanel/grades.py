# -*- coding: utf-8 -*-

import collections

from bika.lims import api
from bika.lims.utils import get_link_for
from bika.seedlab import _
from senaite.core.i18n import translate
from senaite.core.permissions import AddAnalysisCategory
from senaite.app.listing import ListingView


class GradesView(ListingView):

    def __init__(self, context, request):
        super(GradesView, self).__init__(context, request)

        self.catalog = 'senaite_catalog_setup'

        self.contentFilter = {
            "portal_type": "Grade",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
            "path": {
                "query": api.get_path(self.context),
                "depth": 1,
            },
        }

        self.context_actions = {
            _("listing_grades_action_add", default="Add"): {
                "url": "++add++Grade",
                "permission": AddAnalysisCategory,
                "icon": "senaite_theme/icon/plus"
            }
        }

        self.title = translate(_(
            "listing_grades_title",
            default="Grades")
        )
        self.icon = api.get_icon("Grades", html_tag=False)
        self.show_select_column = True

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _(
                    u"listing_grades_column_title",
                    default=u"Grade",
                ),
                "index": "sortable_title"}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _(
                    u"listing_grades_state_active",
                    default=u"Active",
                ),
                "contentFilter": {"is_active": True},
                "columns": self.columns.keys(),
            }, {
                "id": "inactive",
                "title": _(
                    u"listing_grades_state_inactive",
                    default=u"Inactive",
                ),
                "contentFilter": {'is_active': False},
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _(
                    u"listing_grades_state_all",
                    default=u"All",
                ),
                "contentFilter": {},
                "columns": self.columns.keys(),
            },
        ]

    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        item["replace"]["Title"] = get_link_for(obj)

        return item
