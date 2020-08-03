from django.db import models
from django.conf import settings
from wagtail.core.models import Page
from wagtail.core import fields
from wagtail.core import blocks
from wagtail.documents import blocks as docblocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import (
    StreamFieldPanel,
    FieldPanel,
    PageChooserPanel,
    TabbedInterface,
    ObjectList,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

import uuid

from esite.bifrost.models import (
    GraphQLInt,
    GraphQLBoolean,
    GraphQLString,
    GraphQLFloat,
    GraphQLImage,
    GraphQLDocument,
    GraphQLSnippet,
    GraphQLEmbed,
    GraphQLStreamfield,
)
from esite.bifrost.helpers import register_streamfield_block
from esite.colorfield.blocks import ColorBlock

# > Overview Section
@register_streamfield_block
class _S_OverviewBlock(blocks.StructBlock):
    # feed = blocks.StreamBlock(
    #     [("feed", Overview_FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
    #     null=True,
    #     blank=False,
    # )
    # total contribs of all projects
    # statistic of past and current week
    # statistic of al lyears # current
    # source code statistic language
    # source code statistic lines of code
    pass


#  "commit": "e5ab38813bfc2bb100352adcf525a98caf396411",
#       "author": "Administrator \u003cadmin@example.com\u003e",
#       "date": "Thu Jul 30 11:15:12 2020 +0000",
#       "message": "Update-.gitlab-ci.yml",
#       "files": [
#         {
#           "insertions": "1",
#           "deletions": "1",
#           "path": ".gitlab-ci.yml",
#           "raw_changes": "\u001b[31m-    paths: [log.log]\u001b[m\n\u001b[32m+\u001b[m\u001b[32m    paths: [tmp.json]\u001b[m\n"
#         }
#       ]


@register_streamfield_block
class CodeStatisticLanguageBlock(blocks.StructBlock):
    language_name = blocks.CharBlock()
    color = ColorBlock()
    insertions = blocks.CharBlock()
    deletions = blocks.CharBlock()

    graphql_fields = [
        GraphQLString("language_name"),
        GraphQLString("color"),
        GraphQLString("insertions"),
        GraphQLString("deletions"),
    ]


@register_streamfield_block
class CodeStatisticBlock(blocks.StructBlock):
    insertions = blocks.CharBlock()
    deletions = blocks.CharBlock()
    date = blocks.DateTimeBlock()

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("date"),
    ]


@register_streamfield_block
class FeedCommitFileBlock(blocks.StructBlock):
    insertions = blocks.CharBlock()
    deletions = blocks.CharBlock()
    path = blocks.CharBlock()
    raw_changes = blocks.TextBlock()

    graphql_fields = [
        GraphQLString("insertions"),
        GraphQLString("deletions"),
        GraphQLString("path"),
        GraphQLString("raw_changes"),
    ]


@register_streamfield_block
class FeedCommitBlock(blocks.StructBlock):
    contribution_id = blocks.CharBlock()
    date = blocks.DateTimeBlock()
    message = blocks.TextBlock()
    files = blocks.StreamBlock(
        [("file", FeedCommitFileBlock(null=True, blank=True, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("contribution_id"),
        GraphQLString("date"),
        GraphQLString("message"),
        GraphQLStreamfield("files"),
    ]


@register_streamfield_block
class FeedBlock(blocks.StructBlock):
    datetime = blocks.DateTimeBlock(null=True, required=True)
    data = blocks.StreamBlock(
        [
            ("commit", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
            ("issue", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
            ("pr", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
            ("review", FeedCommitBlock(null=True, blank=True, icon="fa-newspaper-o"),),
        ],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("contribution_id"),
        GraphQLStreamfield("data"),
    ]


@register_streamfield_block
class _S_ScpPageUser(blocks.StructBlock):
    name = blocks.CharBlock()
    username = blocks.CharBlock()
    active = blocks.BooleanBlock(default=False)
    avatar = ImageChooserBlock()
    feed = blocks.StreamBlock(
        [("feed", FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )
    history = blocks.StreamBlock(
        [
            (
                "history",
                CodeStatisticBlock(null=True, blank=False, icon="fa-newspaper-o"),
            )
        ],
        null=True,
        blank=True,
    )

    languages = blocks.StreamBlock(
        [
            (
                "language",
                CodeStatisticLanguageBlock(
                    null=True, blank=True, icon="fa-newspaper-o"
                ),
            )
        ],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("username"),
        GraphQLString("active"),
        GraphQLString("avatar"),
        GraphQLStreamfield("feed"),
        GraphQLStreamfield("history"),
        GraphQLStreamfield("languages"),
    ]


@register_streamfield_block
class _S_ProjectBlock(blocks.StructBlock):
    name = blocks.CharBlock(null=True, required=True, help_text="Project name")
    url = blocks.URLBlock(
        null=True,
        required=True,
        help_text="Important! Format https://www.domain.tld/xyz",
    )
    description = blocks.TextBlock(
        null=True, required=False, help_text="Project description"
    )

    maintainer_name = blocks.CharBlock()
    maintainer_username = blocks.CharBlock()
    maintainer_email = blocks.EmailBlock()

    contributors = blocks.StreamBlock(
        [("contributor", _S_ScpPageUser(null=True, blank=False, icon="fa-user"),)]
    )

    feed = blocks.StreamBlock(
        [("feed", FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )

    history = blocks.StreamBlock(
        [
            (
                "history",
                CodeStatisticBlock(null=True, blank=False, icon="fa-newspaper-o"),
            )
        ],
        null=True,
        blank=True,
    )

    languages = blocks.StreamBlock(
        [
            (
                "language",
                CodeStatisticLanguageBlock(
                    null=True, blank=True, icon="fa-newspaper-o"
                ),
            )
        ],
        null=True,
        blank=True,
    )

    graphql_fields = [
        GraphQLString("name"),
        GraphQLString("url"),
        GraphQLString("description"),
        GraphQLString("maintainer_name"),
        GraphQLString("maintainer_username"),
        GraphQLString("maintainer_email"),
        GraphQLStreamfield("contributors"),
        GraphQLStreamfield("feed"),
        GraphQLStreamfield("history"),
        GraphQLStreamfield("languages"),
    ]


# > Pages
class OpsScpagesPage(Page):
    # Only allow creating HomePages at the root level
    parent_page_types = ["wagtailcore.Page"]
    """ Header Stuff """
    email = models.CharField(null=True, blank=False, max_length=255)

    projects_section = fields.StreamField(
        [("S_ProjectBlock", _S_ProjectBlock(null=True, icon="cogs")),],
        null=True,
        blank=True,
    )
    users_section = fields.StreamField(
        [("S_UserBlock", _S_ScpPageUser(null=True, icon="cogs")),],
        null=True,
        blank=True,
    )
    feed = fields.StreamField(
        [("feed", FeedBlock(null=True, blank=False, icon="fa-newspaper-o"),)],
        null=True,
        blank=True,
    )
    history = fields.StreamField(
        [
            (
                "history",
                CodeStatisticBlock(null=True, blank=False, icon="fa-newspaper-o"),
            )
        ],
        null=True,
        blank=True,
    )

    languages = fields.StreamField(
        [
            (
                "language",
                CodeStatisticLanguageBlock(
                    null=True, blank=True, icon="fa-newspaper-o"
                ),
            )
        ],
        null=True,
        blank=True,
    )

    cache = models.TextField(null=True)

    graphql_fields = [
        GraphQLString("email"),
        # GraphQLString("url"),
        # GraphQLString("description"),
        # GraphQLString("maintainer_name"),
        # GraphQLString("maintainer_username"),
        # GraphQLString("maintainer_email"),
        GraphQLStreamfield("projects_section"),
        GraphQLStreamfield("users_section"),
        GraphQLStreamfield("feed"),
        GraphQLStreamfield("history"),
        GraphQLStreamfield("languages"),
        GraphQLStreamfield("cache"),
    ]

    overview_panels = [
        StreamFieldPanel("feed"),
        StreamFieldPanel("history"),
        StreamFieldPanel("languages"),
    ]

    user_panels = [StreamFieldPanel("users_section")]
    project_panels = [StreamFieldPanel("projects_section")]
    imprint_panels = [
        MultiFieldPanel(
            [
                # FieldPanel("city"),
                # FieldPanel("zip_code"),
                # FieldPanel("address"),
                # FieldPanel("telephone"),
                # FieldPanel("telefax"),
                # FieldPanel("whatsapp_telephone"),
                # FieldPanel("whatsapp_contactline"),
                FieldPanel("email"),
                # FieldPanel("copyrightholder"),
            ],
            heading="contact",
        ),
        MultiFieldPanel(
            [
                # FieldPanel("vat_number"),
                # FieldPanel("tax_id"),
                # FieldPanel("trade_register_number"),
                # FieldPanel("court_of_registry"),
                # FieldPanel("place_of_registry"),
                # FieldPanel("trade_register_number"),
                # FieldPanel("ownership"),
            ],
            heading="legal",
        ),
        # StreamFieldPanel("sociallinks"),
        MultiFieldPanel(
            [
                # FieldPanel("about"),
                # FieldPanel("privacy"),
                # FieldPanel("shipping"),
                # FieldPanel("gtc"),
                # FieldPanel("cancellation_policy"),
            ],
            heading="terms",
        ),
    ]
    cache_panels = [FieldPanel("cache")]

    edit_handler = TabbedInterface(
        [
            ObjectList(Page.content_panels + overview_panels, heading="Overview"),
            ObjectList(user_panels, heading="Users"),
            ObjectList(project_panels, heading="Projects"),
            ObjectList(imprint_panels, heading="Imprint"),
            ObjectList(
                Page.promote_panels + Page.settings_panels + cache_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
