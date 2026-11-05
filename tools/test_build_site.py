"""Regression checks for the workshop content and generated website.

Run from the repository root with:
    python -m unittest discover -s tools -p "test_*.py"
"""

import json
import re
import unittest
from pathlib import Path

import build_site as site


class WorkshopContentTests(unittest.TestCase):
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
        expected = {"index.html": site.render_home(), "404.html": site.render_404()}
        expected.update({site.href(page["slug"]): site.render_page(i, page)
                         for i, page in enumerate(site.PAGES)})

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

    def test_given_illustrative_reveals_when_reading_then_original_facts_and_limits_remain(self):
        text = json.dumps(site.BY_SLUG["exercise-1"], ensure_ascii=False)

        for fact in ("CITA-482", "15-minute", "30 days", "60", "2 changes", "24 hours",
                     "R3", "R4", "R5", "AC-7", "WCAG 2.1 AA", "AppointmentService",
                     "2b", "160 characters", "manual screen-reader", "proposed, not created"):
            with self.subTest(fact=fact):
                self.assertIn(fact, text)
        self.assertNotIn("56 tests", text)


if __name__ == "__main__":
    unittest.main()
