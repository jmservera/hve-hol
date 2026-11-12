"""Regression checks for the workshop content and generated website.

Run from the repository root with:
    python -m unittest discover -s tools -p "test_*.py"
"""

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

import build_site as site
from localization import UI_ES, interface


class PageStructure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.storage = []
        self.editable = 0
        self.language_switch = None
        self.scripts = []
        self.labels = []
        self.words = []
        self.code_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("data-page", "data-tpl", "data-store", "data-key"):
            if key in attrs:
                self.storage.append((key, attrs[key]))
        if attrs.get("contenteditable") == "true":
            self.editable += 1
        if "data-language-switch" in attrs:
            self.language_switch = attrs
        if tag == "script":
            self.scripts.append(attrs.get("src"))
        if tag in ("code", "pre"):
            self.code_depth += 1
        self.labels.extend(attrs[key] for key in ("aria-label", "placeholder")
                           if key in attrs)

    def handle_endtag(self, tag):
        if tag in ("code", "pre"):
            self.code_depth -= 1

    def handle_data(self, data):
        if not self.code_depth and data.strip():
            self.words.append(data.strip())


class WorkshopContentTests(unittest.TestCase):
    def test_given_interface_translation_when_rendering_code_then_only_labels_change(self):
        markup = '<p>Copy</p><pre><code>Copy</code></pre><a href="#Steps" aria-label="Steps">Steps</a>'

        with site.language("es"):
            rendered = interface(markup)

        self.assertEqual(rendered,
                         '<p>Copiar</p><pre><code>Copy</code></pre>'
                         '<a href="#Steps" aria-label="Pasos">Pasos</a>')

    def test_given_complete_translation_when_comparing_content_then_structure_and_links_remain(self):
        import content_es

        stable = {"slug", "storage_slug", "type", "id", "kind", "cls", "style", "num", "repo_url"}

        def compare(english, spanish, location, field=None):
            with self.subTest(content=location):
                self.assertIs(type(english), type(spanish))
                if isinstance(english, dict):
                    self.assertEqual(english.keys(), spanish.keys())
                    for key in english:
                        compare(english[key], spanish[key], location + "." + key, key)
                elif isinstance(english, (list, tuple)):
                    self.assertEqual(len(english), len(spanish))
                    for index, (en, es) in enumerate(zip(english, spanish)):
                        compare(en, es, "%s[%s]" % (location, index), field)
                elif isinstance(english, str):
                    if field in stable or english.startswith(("https://", "http://")):
                        self.assertEqual(english, spanish)
                    self.assertEqual(re.findall(r"https?://[^\s)]+", english),
                                     re.findall(r"https?://[^\s)]+", spanish))
                    self.assertEqual(re.findall(r"`[^`]+`", english),
                                     re.findall(r"`[^`]+`", spanish))
                else:
                    self.assertEqual(english, spanish)

        for name in ("SITE", "HOME", "GROUPS", "PAGES", "RESOURCES", "ACCELERATORS", "SHARED_AB"):
            compare(getattr(site.C, name), getattr(content_es, name), name)

    def test_given_spanish_edition_when_switching_language_then_page_and_saved_work_match(self):
        english = site.rendered_pages("en")
        spanish = site.rendered_pages("es")

        self.assertEqual(english.keys(), spanish.keys())
        for filename in english:
            with self.subTest(page=filename):
                en, es = PageStructure(), PageStructure()
                en.feed(english[filename])
                es.feed(spanish[filename])

                self.assertIn('<html lang="en">', english[filename])
                self.assertIn('<html lang="es">', spanish[filename])
                self.assertEqual(en.ids, es.ids)
                self.assertEqual(en.storage, es.storage)
                self.assertEqual(en.editable, es.editable)
                self.assertEqual(en.language_switch["href"], "es/" + filename)
                self.assertEqual(es.language_switch["href"], "../" + filename)
                self.assertEqual(en.language_switch["hreflang"], "es")
                self.assertEqual(es.language_switch["hreflang"], "en")
                self.assertEqual(en.scripts, [
                    "translations.js", "assets/translations-loader.js", "assets/theme.js", "assets/site.js",
                ])
                self.assertEqual(es.scripts, [
                    "translations.js", "../assets/translations-loader.js", "../assets/theme.js", "../assets/site.js",
                ])
        self.assertEqual(site.current_language(), "en")

    def test_given_spanish_pages_when_reading_interface_then_english_labels_are_absent(self):
        english_labels = {source for source, translated in UI_ES.items()
                          if source != translated and "%" not in source}
        for filename, rendered in site.rendered_pages("es").items():
            with self.subTest(page=filename):
                page = PageStructure()
                page.feed(rendered)

                self.assertEqual(english_labels.intersection(page.words + page.labels), set())
        home = site.rendered_pages("es")["index.html"]
        self.assertIn("Cambiar al modo oscuro", home)
        self.assertIn("Comentarios", home)
        self.assertIn("Repositorio de GitHub", home)

    def test_given_theme_preference_when_loading_pages_then_bootstrap_precedes_styles(self):
        for locale in ("en", "es"):
            for filename, rendered in site.rendered_pages(locale).items():
                with self.subTest(language=locale, page=filename):
                    self.assertLess(rendered.index("theme.js"), rendered.index('rel="stylesheet"'))
                    self.assertLess(rendered.index("translations.js"), rendered.index("theme.js"))
                    self.assertLess(rendered.index("translations-loader.js"), rendered.index("theme.js"))
                    self.assertIn('data-theme-toggle hidden', rendered)

    def test_given_language_catalogs_when_loading_then_each_covers_shared_script_messages(self):
        used = set()
        for script in ("site.js", "theme.js"):
            source = Path(site.DOCS, "assets", script).read_text(encoding="utf-8")
            used.update(re.findall(r"\bmessages\.([A-Za-z]+)", source))
            used.update(re.findall(r"'(switchTo[A-Za-z]+)'", source))

        for folder in (Path(site.DOCS), Path(site.DOCS, "es")):
            with self.subTest(language=folder.name):
                source = (folder / "translations.js").read_text(encoding="utf-8")
                messages = json.loads(source[source.index("{"):source.rindex("}") + 1])

                self.assertEqual(set(messages), used)
                self.assertTrue(all(isinstance(value, str) and value for value in messages.values()))

    def test_given_any_page_when_rendered_then_header_links_to_repository_and_new_issue(self):
        rendered_pages = [site.render_home(), site.render_404()]
        rendered_pages.extend(site.render_page(i, page) for i, page in enumerate(site.PAGES))

        for rendered in rendered_pages:
            with self.subTest(page=re.search(r"<title>(.*?)</title>", rendered).group(1)):
                header = rendered.split('<header class="topbar">', 1)[1].split("</header>", 1)[0]
                for url, label in (
                        ("https://github.com/jmservera/hve-hol", "GitHub repository"),
                        ("https://github.com/jmservera/hve-hol/issues/new", "Feedback")):
                    with self.subTest(link=label):
                        link = re.search(r'<a href="%s"([^>]*)>(.*?)</a>' % re.escape(url), header)

                        self.assertIsNotNone(link)
                        attrs, body = link.groups()
                        self.assertIn('target="_blank"', attrs)
                        self.assertIn('rel="noopener noreferrer"', attrs)
                        self.assertRegex(attrs, r'class="[^"]*\bkeep\b')
                        self.assertIn(label, body)
                        self.assertIn('(opens in a new tab)', body)
                        self.assertIn('<svg ', body)
                        self.assertIn('aria-hidden="true"', body)

    def test_given_updated_workshop_when_listing_exercises_then_order_matches_labs(self):
        exercises = [(page["num"], page["group"]) for page in site.PAGES
                     if page["kind"] in ("core", "parallel", "backup")]

        self.assertEqual(exercises, [
            ("1", "Open lab 1"), ("2", "Open lab 1"), ("3", "Open lab 1"),
            ("4", "Open lab 2"),
            ("5", "Open lab 3"), ("6", "Open lab 3"), ("7", "Open lab 3"),
            ("8", "Open lab 4"), ("9", "Open lab 4"), ("10", "Backup"),
        ])
        self.assertIn("RPI", site.BY_SLUG["exercise-5"]["title"])
        self.assertIn("Reuse", site.BY_SLUG["exercise-6"]["title"])
        self.assertIn("adoption", site.BY_SLUG["exercise-9"]["title"])
        self.assertEqual(site.BY_SLUG["exercise-10"]["kind"], "backup")
        slugs = [page["slug"] for page in site.PAGES]
        self.assertLess(slugs.index("scorecard"), slugs.index("exercise-10"))
        agenda = json.dumps(site.BY_SLUG["agenda"], ensure_ascii=False)
        self.assertIn("17:10–17:30", agenda)
        self.assertIn("before close only if time remains", agenda)

    def test_given_exercises_two_to_ten_when_rendered_then_each_has_four_start_steps(self):
        for number in range(2, 11):
            with self.subTest(exercise=number):
                page = site.BY_SLUG["exercise-%d" % number]
                blocks = page["blocks"]
                start = next(i for i, block in enumerate(blocks)
                             if block.get("id") == "how-to-start")
                toolkit = next(i for i, block in enumerate(blocks)
                               if block.get("id") == "toolkit")
                work = next(i for i, block in enumerate(blocks)
                            if block["type"] == "work")

                self.assertLess(work, start)
                self.assertLess(start, toolkit)
                self.assertEqual(blocks[start + 1]["text"], "Start here")
                self.assertEqual(blocks[start + 2]["type"], "numbered")
                self.assertEqual(len(blocks[start + 2]["items"]), 4)
                advice = blocks[start + 3:start + 5]
                if number == 5:
                    self.assertEqual(advice[0]["type"], "banner")
                    self.assertIn("Split the team", advice[0]["text"])
                else:
                    self.assertEqual(advice[0]["label"], "Tips and tricks")
                    self.assertTrue(advice[0]["items"])
                self.assertEqual(advice[1]["label"], "Watch out")
                self.assertTrue(advice[1]["items"])
                rendered = site.render_page(site.PAGES.index(page), page)
                self.assertIn('href="#how-to-start"', rendered)
                self.assertIn('id="how-to-start"', rendered)

    def test_given_renumbered_exercises_when_rendered_then_original_storage_keys_remain(self):
        for current, original in (("5", "6"), ("6", "5"), ("9", "10"), ("10", "9")):
            with self.subTest(exercise=current):
                page = site.BY_SLUG["exercise-" + current]
                rendered = site.render_page(site.PAGES.index(page), page)

                self.assertEqual(page["storage_slug"], "exercise-" + original)
                self.assertIn("page-exercise-%s" % current, rendered)
                self.assertIn('data-page="exercise-%s"' % original, rendered)
        page = site.BY_SLUG["exercise-1"]
        self.assertEqual(page["storage_slug"], "exercise-1-appointments")
        rendered = site.render_page(site.PAGES.index(page), page)
        self.assertIn('data-page="exercise-1-appointments"', rendered)

    def test_given_saved_templates_when_exercises_move_then_cell_shapes_are_preserved(self):
        for slug, template_id, expected in (
                ("exercise-6", "component-spec", 8),
                ("exercise-10", "comparison-sheet", 22),
                ("exercise-10", "recommendation", 1)):
            with self.subTest(template=template_id):
                template = next(block for block in site.BY_SLUG[slug]["blocks"]
                                if block.get("id") == template_id)
                editable = sum(cell is None or isinstance(cell, dict)
                               for row in template["rows"] for cell in row)

                self.assertEqual(editable, expected)
        canvas = next(block for block in site.BY_SLUG["exercise-9"]["blocks"]
                      if block.get("id") == "adoption-canvas")
        self.assertEqual(len(canvas["items"]), 9)

    def test_given_parallel_activities_when_referencing_the_run_then_they_use_exercise_five(self):
        for slug in ("exercise-7", "intermission-b", "intermission-c"):
            with self.subTest(page=slug):
                text = json.dumps(site.BY_SLUG[slug]).lower()

                self.assertIn("exercise-5.html", text)
                self.assertNotRegex(text, r"(?:exercise|ex) 6\b|exercise-6\.html")
        rpi = site.BY_SLUG["exercise-5"]
        self.assertIn("Exercise 7", rpi["eyebrow"])
        banners = [block["text"] for block in rpi["blocks"]
                   if block["type"] == "banner"]
        self.assertTrue(any("quality" in text.lower() and "architect" in text.lower()
                            and "auditor" in text.lower() for text in banners))

    def test_given_reuse_exercise_when_finishing_then_a_correction_is_verified_by_rerun(self):
        blocks = site.BY_SLUG["exercise-6"]["blocks"]
        proof = next(block for block in blocks if block.get("id") == "correction-proof")
        done = next(block["text"].lower() for block in blocks if block["type"] == "done")

        self.assertEqual(proof["type"], "template")
        self.assertIn("correction", done)
        self.assertIn("re-run", done)

    def test_given_backup_comparison_when_scoping_runs_then_only_one_variable_changes(self):
        blocks = site.BY_SLUG["exercise-10"]["blocks"]
        text = json.dumps(blocks).lower()

        self.assertIn("exercise-5.html", text)
        self.assertIn("same commit", text)
        self.assertIn("one variable", text)
        self.assertIn("research and plan", text)
        self.assertIn("model", text)
        self.assertIn("hve core", text)
        self.assertIn("hve-squad", text)
        self.assertIn("plain copilot agent mode", text)

    def test_given_numbered_exercise_links_when_reading_labels_then_targets_match(self):
        pattern = re.compile(r"\[(?:Exercise|Ex) (\d+)[^\]]*\]\(exercise-(\d+)\.html")
        text = json.dumps([site.C.HOME, site.C.GROUPS, site.PAGES])

        for label, target in pattern.findall(text):
            with self.subTest(label=label, target=target):
                self.assertEqual(label, target)

    def test_given_canonical_content_when_building_then_committed_html_is_current(self):
        expected = site.rendered_pages("en")
        expected.update({str(Path("es", name)): rendered
                         for name, rendered in site.rendered_pages("es").items()})

        for filename, rendered in expected.items():
            with self.subTest(page=filename):
                self.assertEqual(Path(site.DOCS, filename).read_text(encoding="utf-8"), rendered)
        self.assertEqual(site.check_links(list(expected)), [])

    def test_given_appointment_warmup_when_opened_then_six_questions_precede_closed_reveals(self):
        page = site.BY_SLUG["exercise-1"]
        rounds = [block for block in page["blocks"] if block["type"] == "round"]
        rendered = site.render_page(site.PAGES.index(page), page)
        questions = [
            "Before anyone writes code, what should the agent read, and what should it hand back to you?",
            "The agent drafts the requirements. Name 3 things it must ASK the business owner instead of "
            "deciding itself.",
            "Before planning, what 3 facts must the agent find out in the code?",
            "The agent proposes a plan. What would make you REJECT it?",
            "How much freedom would you give the agent here, and what proves the work is done?",
            "What can the agent review on its own, and what must a person still check before release?",
        ]

        self.assertEqual([block["question"] for block in rounds], questions)
        details = re.findall(r"<details\b([^>]*)>", rendered)
        self.assertEqual(len(details), 6)
        self.assertFalse(any(re.search(r"\bopen(?:=|\s|$)", attrs) for attrs in details))
        self.assertEqual(rendered.count("Illustrative example · fictional client and system · not a recorded run"), 7)
        for block in rounds:
            self.assertLess(rendered.index(site.fmt(block["question"])),
                            rendered.index('id="reveal-%s"' % block["num"]))

    def test_given_appointment_answer_sheet_when_starting_then_answers_and_scores_are_blank(self):
        page = site.BY_SLUG["exercise-1"]
        sheet = next(block for block in page["blocks"] if block.get("id") == "round-answers")

        self.assertEqual(sheet["head"], ["Round", "Step", "Our answer", "Score"])
        self.assertEqual(len(sheet["rows"]), 6)
        self.assertTrue(all(row[2:] == [None, None] for row in sheet["rows"]))
        self.assertEqual([row[0] for row in sheet["rows"]], ["1", "2", "3", "4", "5", "6"])
        self.assertIn("No agents", page["eyebrow"])

    def test_given_microsoft_reveals_when_reading_then_business_facts_and_limits_remain(self):
        text = json.dumps(site.BY_SLUG["exercise-1"], ensure_ascii=False)

        for fact in ("Azure Boards work item 482", "15-minute", "30 days", "60", "2 changes", "24 hours",
                     "R3", "R4", "R5", "AC-7", "WCAG 2.1 AA", "AppointmentService",
                     "2b", "160 characters", "manual screen-reader", "proposed, not created"):
            with self.subTest(fact=fact):
                self.assertIn(fact, text)
        self.assertNotIn("56 tests", text)

    def test_given_microsoft_defaults_when_rendering_then_legacy_examples_are_absent(self):
        canonical = json.dumps([site.C.HOME, site.PAGES, site.C.U, site.C.RESOURCES,
                                site.C.SHARED_AB], ensure_ascii=False)
        legacy = re.compile(r"jira|gitlab|confluence|atlassian|rovo|bitbucket|jenkins|bamboo|CITA-482", re.I)

        self.assertNotRegex(canonical, legacy)
        case = json.dumps(site.BY_SLUG["exercise-1"], ensure_ascii=False)
        for product in ("Azure Boards work item 482", "SharePoint", "Teams", "GitHub repository",
                        "GitHub pull request"):
            self.assertIn(product, case)
        resources = site.render_resources_body()
        self.assertNotRegex(resources, legacy)
        self.assertIn("Azure DevOps MCP", resources)
        self.assertIn("Work IQ", resources)

    def test_given_work_iq_context_when_gathering_then_access_and_fallback_are_explicit(self):
        for slug in ("exercise-2", "exercise-4", "intermission-a", "intermission-b"):
            with self.subTest(page=slug):
                text = json.dumps(site.BY_SLUG[slug], ensure_ascii=False).lower()
                for term in ("work iq", "sharepoint", "teams", "approved"):
                    self.assertIn(term, text)
        setup = json.dumps(site.BY_SLUG["how-you-run-it"], ensure_ascii=False).lower()
        for term in ("optional", "preview", "billing", "spending policy", "tenant policy",
                     "denied", "stop", "fictional"):
            self.assertIn(term, setup)
        evidence = json.dumps(site.BY_SLUG["exercise-2"], ensure_ascii=False).lower()
        self.assertIn("source urls", evidence)
        self.assertIn("read operations only", evidence)
        self.assertIn("not a permission workaround", evidence)
        self.assertNotIn("work iq is read-only", setup)

    def test_given_intermission_a_when_opened_then_workspace_uses_the_copilot_app(self):
        for locale in ("en", "es"):
            with self.subTest(language=locale):
                pages = site.rendered_pages(locale)
                rendered = pages["intermission-a.html"]

                self.assertIn("Copilot Workspace", rendered)
                self.assertIn('href="https://github.com/github/app"', rendered)
                self.assertNotIn("Copilot CLI", rendered)
                self.assertIn("Copilot CLI", pages["intermission-b.html"])
        self.assertNotIn("espacio de trabajo de Copilot", "".join(site.rendered_pages("es").values()))

    def test_given_spanish_canvas_content_when_rendered_then_canvas_remains_untranslated(self):
        pages = site.rendered_pages("es")

        self.assertIn("canvas", pages["intermission-a.html"])
        self.assertIn("Canvas de adopción", pages["exercise-9.html"])
        self.assertNotRegex("".join(pages.values()).lower(), r"\blienzos?\b")

    def test_given_intermission_a_when_creating_canvas_then_guidance_is_interactive_and_scoped(self):
        for locale in ("en", "es"):
            with self.subTest(language=locale):
                rendered = site.rendered_pages(locale)["intermission-a.html"]

                self.assertIn("/create-canvas", rendered)
                self.assertIn(".github/extensions", rendered)
                self.assertIn('href="%s"' % site.C.U["copilot_canvases"], rendered)
                self.assertIn('href="%s"' % site.C.U["copilot_canvas_docs"], rendered)
                self.assertNotIn("one issue reached a draft PR", rendered)
                self.assertNotIn("una incidencia ha llegado a una PR en borrador", rendered)

    def test_given_microsoft_controls_when_enforcing_then_product_boundaries_are_correct(self):
        controls = json.dumps(site.BY_SLUG["exercise-7"], ensure_ascii=False)
        for term in ("GitHub", "CODEOWNERS", "Azure Repos", "branch policies",
                     "required build validation", "authorised", "bypass"):
            self.assertIn(term, controls)
        self.assertIn("CODEOWNERS is not an Azure Repos feature", controls)
        loop = json.dumps(site.BY_SLUG["intermission-b"], ensure_ascii=False)
        self.assertIn("service hook", loop)
        self.assertIn("dispatcher", loop)
        self.assertIn("Do not assume", loop)
        self.assertIn("native YAML pipeline trigger", loop)
        self.assertIn("separate approval", loop)

    def test_given_comparison_context_when_repeating_then_sources_and_access_are_frozen(self):
        page = site.BY_SLUG["exercise-10"]
        text = json.dumps(page, ensure_ascii=False).lower()

        self.assertIn("same approved source snapshot", text)
        self.assertIn("access scopes", text)
        self.assertIn("different credit units separate", text)
        setup = next(block for block in page["blocks"] if block.get("id") == "comparison-setup")
        self.assertEqual(len(setup["rows"]), 5)
        self.assertTrue(all(row[1] is None for row in setup["rows"]))


if __name__ == "__main__":
    unittest.main()
