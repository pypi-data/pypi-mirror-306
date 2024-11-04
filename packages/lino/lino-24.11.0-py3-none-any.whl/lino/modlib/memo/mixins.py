# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from bs4 import BeautifulSoup, NavigableString
from bs4.element import Tag
from lxml.html import fragments_fromstring
from lino.utils.html import E, tostring, mark_safe
import lxml

try:
    import markdown
except ImportError:
    markdown = None

from django.conf import settings
from django.utils import translation
from django.utils.text import Truncator
from django.utils.html import format_html

from lino.core.gfks import gfk2lookup
from lino.core.model import Model
from lino.core.fields import fields_list, RichTextField, PreviewTextField
from lino.utils.restify import restify
from lino.utils.mldbc.fields import BabelTextField
from lino.core.exceptions import ChangedAPI
from lino.modlib.checkdata.choicelists import Checker
from lino.api import rt, dd, _


def old_truncate_comment(html_str, max_p_len=None):
    # returns a single paragraph with a maximum number of visible chars.
    # No longer used. Replaced by new truncate_comment() below
    if max_p_len is None:
        max_p_len = settings.SITE.plugins.memo.short_preview_length
    html_str = html_str.strip()  # remove leading or trailing newlines

    if not html_str.startswith("<"):
        if len(html_str) > max_p_len:
            txt = html_str[:max_p_len] + "..."
        else:
            txt = html_str
        return txt
    soup = BeautifulSoup(html_str, "html.parser")
    ps = soup.find_all(
        ["p", "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "pre"]
    )
    if len(ps) > 0:
        anchor_end = "</a>"
        txt = ""
        for p in ps:
            text = ""
            for c in p.contents:
                if isinstance(c, Tag):
                    if c.name == "a":
                        text += str(c)
                        max_p_len = max_p_len + len(text) - len(c.text)
                    else:
                        # text += str(c)
                        text += c.text
                else:
                    text += str(c)

            if len(txt) + len(text) > max_p_len:
                txt += text
                if anchor_end in txt:
                    ae_index = txt.index(anchor_end) + len(anchor_end)
                    if ae_index >= max_p_len:
                        txt = txt[:ae_index]
                        txt += "..."
                        break
                txt = txt[:max_p_len]
                txt += "..."
                break
            else:
                txt += text + "\n\n"
        return txt
    return html_str


def django_truncate_comment(html_str):
    # works, but we don't use it because (...)
    return Truncator(html_str).chars(
        settings.SITE.plugins.memo.short_preview_length, html=True
    )


PARAGRAPH_TAGS = {
    "p",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "h7",
    "h8",
    "h9",
    "pre",
    "li",
    "div",
}
WHITESPACE_TAGS = PARAGRAPH_TAGS | {
    "[document]",
    "span",
    "ul",
    "html",
    "head",
    "body",
    "base",
}


MARKDOWNCFG = dict(
    extensions=["toc"], extension_configs=dict(toc=dict(toc_depth=3, permalink=True))
)


class Style:
    # TODO: Extend rstgen.sphinxconf.sigal_image.Format to incoroporate this.
    def __init__(self, s):
        self._map = {}
        if s:
            for i in s.split(";"):
                k, v = i.split(":", maxsplit=1)
                self._map[k.strip()] = v.strip()
        self.is_dirty = False

    def __contains__(self, *args):
        return self._map.__contains__(*args)

    def __setitem__(self, k, v):
        if k in self._map and self._map[k] == v:
            return
        self._map[k] = v
        self.is_dirty = True

    def __delitem__(self, k):
        if k in self._map:
            self.is_dirty = True
        return self._map.__delitem__(k)

    def adjust_size(self):
        # if self['float'] == "none":
        #     return
        if "width" in self._map:
            del self["width"]
        self["height"] = dd.plugins.memo.short_preview_image_height

    def as_string(self):
        return ";".join(["{}:{}".format(*kv) for kv in self._map.items()])


class TextCollector:
    def __init__(self, max_length=None):
        self.text = ""
        self.sep = ""  # becomes "\n\n" after a PARAGRAPH_TAGS
        self.remaining = max_length or settings.SITE.plugins.memo.short_preview_length
        self.image = None

    def add_chunk(self, ch):
        # print("20230712 add_chunk", ch.name, ch)

        if ch.name in WHITESPACE_TAGS:
            for c in ch.children:
                if not self.add_chunk(c):
                    return False
            if ch.name in PARAGRAPH_TAGS:
                self.sep = "\n\n"
            else:
                self.sep = " "
            return True

        assert ch.name != "IMG"

        if ch.name == "img":
            if self.image is not None:
                # Ignore all images except the first one.
                self.text += self.sep
                return True
            style = Style(ch.get("style", None))
            if not "float" in style:
                style["float"] = "right"
            style.adjust_size()
            if style.is_dirty:
                ch["style"] = style.as_string()
            self.image = ch
            # print("20231023 a", ch)

        we_want_more = True
        if ch.string is not None:
            if len(ch.string) > self.remaining:
                # print("20231023", len(ch.string), '>', self.remaining)
                ch.string = ch.string[: self.remaining] + "..."
                we_want_more = False
                # print("20230927", ch.string, ch)
                # self.text += str(ch.string) + "..."
                # return False
            self.remaining -= len(ch.string)

        if isinstance(ch, NavigableString):
            self.text += self.sep + ch.string
        else:
            self.text += self.sep + str(ch)

        self.remaining -= len(self.sep)
        self.sep = ""
        return we_want_more


def truncate_comment(html_str, max_length=300):
    # new implementation since 20230713
    html_str = html_str.strip()  # remove leading or trailing newlines

    if not html_str.startswith("<"):
        # print("20231023 c", html_str)
        if len(html_str) > max_length:
            return html_str[:max_length] + "..."
        return html_str

    # if "choose one or the other" in html_str:
    #     print(html_str)
    #     raise Exception("20230928 {} {}".format(len(html_str), max_length))

    soup = BeautifulSoup(html_str, "html.parser")
    tc = TextCollector(max_length)
    tc.add_chunk(soup)
    return tc.text


def rich_text_to_elems(ar, description):
    if description.startswith("<"):
        # desc = E.raw('<div>%s</div>' % self.description)
        desc = fragments_fromstring(ar.parse_memo(description))
        return desc
    # desc = E.raw('<div>%s</div>' % self.description)
    html = restify(ar.parse_memo(description))
    # logger.info(u"20180320 restify %s --> %s", description, html)
    # html = html.strip()
    try:
        desc = fragments_fromstring(html)
    except Exception as e:
        raise Exception("Could not parse {!r} : {}".format(html, e))
    # logger.info(
    #     "20160704c parsed --> %s", tostring(desc))
    return desc
    # if desc.tag == 'body':
    #     # happens if it contains more than one paragraph
    #     return list(desc)  # .children
    # return [desc]


def body_subject_to_elems(ar, title, description):
    if description:
        elems = [E.p(E.b(title), E.br())]
        elems += rich_text_to_elems(ar, description)

    else:
        elems = [E.b(title)]
        # return E.span(self.title)
    return elems


class MemoReferrable(dd.Model):
    class Meta:
        abstract = True

    memo_command = None

    @classmethod
    def on_analyze(cls, site):
        super().on_analyze(site)

        if cls.memo_command is None or not site.is_installed("memo"):
            return

        mp = site.plugins.memo.parser
        mp.register_django_model(cls.memo_command, cls)
        # mp.add_suggester("[" + cls.memo_command + " ", cls.objects.all(), 'pk')

    # def get_memo_title(self):
    #    """A text to be used as title of the ``<a href>``."""
    #    return None
    # return str(self)

    def memo2html(self, ar, txt, **kwargs):
        if txt:
            kwargs.update(title=txt)
        e = self.as_summary_item(ar)
        return tostring(e)
        # return ar.obj2str(self, **kwargs)

        # return "<p>Oops, undefined memo2html()</p>"

    # def obj2memo(self, title=str):
    def obj2memo(self, text=None):
        """Render the given database object as memo markup."""
        if self.memo_command is None:
            return "**{}**".format(self)
        # title = self.get_memo_title()
        if text is None:
            # text = str(self)
            return "[{} {}]".format(self.memo_command, self.id)
        # return "[{} {}] ({})".format(self.memo_command, self.id, title)
        return "[{} {} {}]".format(self.memo_command, self.id, text)


# class MentionGenerator(dd.Model):
#
#     class Meta:
#         abstract = True
#
#     def get_memo_text(self):
#         return None
#
#     if dd.is_installed("memo"):
#         def after_ui_save(self, ar, cw):
#             super().after_ui_save(ar, cw)
#             memo_parser = settings.SITE.plugins.memo.parser
#             ref_objects = memo_parser.get_referred_objects(self.get_memo_text())
#             Mention = rt.models.memo.Mention
#             for ref_object in ref_objects:
#                 created_mention = Mention(owner=self,
#                         owner_id=ref_object.pk,
#                         owner_type=ContentType.objects.get_for_model(ref_object.__class__))
#                 created_mention.touch()
#                 created_mention.save()


# class BasePreviewable(MentionGenerator):
class BasePreviewable(dd.Model):
    class Meta:
        abstract = True

    previewable_field = None

    def get_preview_length(self):
        return settings.SITE.plugins.memo.short_preview_length

    def save(self, *args, **kwargs):
        """Updates the preview fields and the list of mentioned objects."""
        pf = self.previewable_field
        mentions = set()
        txt = self.get_previewable_text(settings.SITE.DEFAULT_LANGUAGE)
        short, full = self.parse_previews(txt, None, mentions)
        # if "choose one or the other" in short:
        #     raise Exception("20230928 {} {}".format(len(short), short))
        # print("20231023 b", short)
        setattr(self, pf + "_short_preview", short)
        setattr(self, pf + "_full_preview", full)
        if isinstance(self, BabelPreviewable):
            for lng in settings.SITE.BABEL_LANGS:
                src = self.get_previewable_text(lng)
                # src = getattr(self, pf + lng.suffix)
                with translation.override(lng.django_code):
                    short, full = self.parse_previews(src, None, mentions)
                setattr(self, pf + "_short_preview" + lng.suffix, short)
                setattr(self, pf + "_full_preview" + lng.suffix, full)
        super().save(*args, **kwargs)
        self.synchronize_mentions(mentions)

    def get_previewable_text(self, lng):
        return getattr(self, self.previewable_field + lng.suffix)

    def parse_previews(self, source, ar=None, mentions=None, **context):
        context.update(self=self)
        full = settings.SITE.plugins.memo.parser.parse(
            source, ar=ar, context=context, mentions=mentions
        )
        short = truncate_comment(full, self.get_preview_length())
        if not full.startswith("<"):
            if markdown is not None:
                full = markdown.markdown(full, **MARKDOWNCFG)
        return (short, full)

    def get_saved_mentions(self):
        Mention = rt.models.memo.Mention
        flt = gfk2lookup(Mention.owner, self)
        return Mention.objects.filter(**flt).order_by("source_type", "source_id")

    def synchronize_mentions(self, mentions):
        Mention = rt.models.memo.Mention
        for obj in self.get_saved_mentions():
            if obj.source in mentions:
                mentions.remove(obj.source)
            else:
                obj.delete()
        for source in mentions:
            obj = Mention(owner=self, source=source)
            # source_id=source.pk,
            # source_type=ContentType.objects.get_for_model(source.__class__))
            obj.full_clean()
            obj.save()

    def get_overview_elems(self, ar):
        yield E.h1(str(self))

        if self.body_short_preview:
            try:
                for e in lxml.html.fragments_fromstring(self.body_short_preview):
                    yield e
            except Exception as e:
                yield "{} [{}]".format(self.body_short_preview, e)


class Previewable(BasePreviewable):
    class Meta:
        abstract = True

    previewable_field = "body"

    body = PreviewTextField(_("Body"), blank=True, format="html", bleached=True)
    body_short_preview = RichTextField(_("Preview"), blank=True, editable=False)
    body_full_preview = RichTextField(_("Preview (full)"), blank=True, editable=False)

    def get_body_parsed(self, ar, short=False):
        if ar.renderer is settings.SITE.kernel.editing_front_end.renderer:
            return self.body_short_preview if short else self.body_full_preview
        # raise Exception("{} is not {}".format(
        #     ar.renderer, settings.SITE.kernel.editing_front_end.renderer))
        src = self.body
        s, f = self.parse_previews(src, ar, set())
        return s if short else f

    def as_paragraph(self, ar):
        s = super().as_paragraph(ar)
        # s = format_html("<b>{}</b> : {}", .format(ar.add_detail_link(self, str(self)))
        # s = ar.obj2htmls(self)
        s = format_html(
            "<b>{}</b> : {}", s, mark_safe(self.body_short_preview) or _("(no preview)")
        )
        return s


class BabelPreviewable(BasePreviewable):
    class Meta:
        abstract = True

    previewable_field = "body"

    body = BabelTextField(_("Body"), blank=True, format="html", bleached=True)
    body_short_preview = BabelTextField(_("Preview"), blank=True, editable=False)
    body_full_preview = BabelTextField(_("Preview (full)"), blank=True, editable=False)

    # def save(self, *args, **kwargs):
    #     pf = self.previewable_field
    #     mentions = set()
    #     for lng in settings.SITE.BABEL_LANGS:
    #         src = getattr(self, self.previewable_field+lng.suffix)
    #         with translation.override(lng.django_code):
    #             short, full = self.parse_previews(src, mentions)
    #         setattr(self, pf+'_short_preview'+lng.suffix, short)
    #         setattr(self, pf+'_full_preview'+lng.suffix, full)
    #     super().save(*args, **kwargs)
    #     self.synchronize_mentions(mentions)


class PreviewableChecker(Checker):
    verbose_name = _("Check for previewables needing update")
    model = BasePreviewable

    def _get_checkdata_problems(self, lng, obj, fix=False):
        src = obj.get_previewable_text(lng)
        pf = obj.previewable_field
        # src = getattr(obj, pf+suffix)
        expected_mentions = set()
        short, full = obj.parse_previews(src, None, expected_mentions)
        is_broken = False
        if (
            getattr(obj, pf + "_short_preview" + lng.suffix) != short
            or getattr(obj, pf + "_full_preview" + lng.suffix) != full
        ):
            yield (True, _("Preview differs from source."))
            is_broken = True
        found_mentions = set([obj.source for obj in obj.get_saved_mentions()])
        if expected_mentions != found_mentions:
            yield (True, _("Mentions differ from expected mentions."))
            is_broken = True
        if is_broken and fix:
            # setattr(obj, pf+'_short_preview'+suffix, short)
            # setattr(obj, pf+'_full_preview'+suffix, full)
            obj.full_clean()
            obj.save()
        # self.synchronize_mentions(mentions)

    def get_checkdata_problems(self, obj, fix=False):
        for x in self._get_checkdata_problems(settings.SITE.DEFAULT_LANGUAGE, obj, fix):
            yield x
        if isinstance(obj, BabelPreviewable):
            for lng in settings.SITE.BABEL_LANGS:
                with translation.override(lng.django_code):
                    for x in self._get_checkdata_problems(lng, obj, fix):
                        yield x


PreviewableChecker.activate()
