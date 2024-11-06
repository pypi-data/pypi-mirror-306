import json
import logging
import pathlib

from messages import StepDefinition, TestStep, TestStepFinished, PickleStep, TestCase, TestCaseStarted, Pickle
from mkdocs import plugins

from .gherkin_results import GherkinResults

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


class GherkinPlugin(plugins.BasePlugin):

    def __init__(self, *args, **kwargs):
        self.results: GherkinResults = None
        self.process_document("gherkin_messages.ndjson")

    def on_page_markdown(self, markdown, page, config, files):
        lines = markdown.splitlines()

        docfile_path = pathlib.Path(page.file.abs_src_path)

        for step in self.results.steps:
            if step.matches_uri(docfile_path):
                lines[step.line - 1] += f" {step.result.status}"

        for test_case in self.results.test_cases:
            if test_case.matches_uri(docfile_path):
                lines[test_case.line - 1] += f" {test_case.status()}"

        # for pickle in self._pickles:
        #     pickle_path = pathlib.Path(pickle["pickle"]['uri'])
        #     if pickle_path.resolve() == docfile_path.resolve():
        #         test_case = None
        #         for tc in self._test_cases:
        #             if tc['pickleId'] == pickle['pickle']['id']:
        #                 test_case = tc
        #
        #         for test_step in test_case['testSteps']:
        #             if 'stepDefinitions' in test_step:
        #                 step_line = test_step['stepDefinitions'][0]['sourceReference']['location']['line']
        #                 step_result = test_step['result']['status']
        #
        #
        #         lines[pickle["line"]]+= " (OK)" if pickle["status"] else " (ERR)"
        #         log.info(f"CALLED ON PAGE MARKDOWN")

        result = ""

        for line in lines:
            result += line + "\n"

        return result

    def search(self, obj, key, value, results):
        if isinstance(obj, dict):
            # Check if the key exists at the current level
            if key in obj and obj[key] == value:
                results.append(obj)
            else:
                # Recursively search each key-value pair
                for v in obj.values():
                    self.search(v, key, value, results)
        elif isinstance(obj, list):
            # Iterate through each item in a list
            for item in obj:
                self.search(item, key, value, results)

    def pickle_to_ast_node(self, pickles, pickle_id):
        # Flatten steps from each pickle and find the specific one by id
        pickle = next((step for p in pickles for step in p['steps'] if p['id'] == pickle_id), None)
        return pickle['astNodeIds'] if pickle else None

    def ast_node_id_to_lines(self, ast_node_id, gherkin_document):
        results = []
        self.search(gherkin_document, 'id', ast_node_id, results)
        return [r['location'] for r in results]

    def process_document(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            ndjson_objects = [json.loads(line) for line in file if line.strip()]

        step_definitions = {}
        test_steps, test_cases = [], []
        pickles, finished_test_cases, started_test_cases, started_steps, finished_steps = [], [], [], [], []
        gherkin_document = None

        log.info("STARTING GHERKIN PLUGIN")

        for obj in ndjson_objects:
            if 'pickle' in obj:
                pickles.append(Pickle.model_validate(obj['pickle']))
            if 'stepDefinition' in obj:
                step_definitions[obj['stepDefinition']['id']] = StepDefinition.model_validate(obj['stepDefinition'])
            if 'testCase' in obj:
                test_cases.append(TestCase.model_validate(obj['testCase']))
            if 'testCaseFinished' in obj:
                finished_test_cases.append(obj['testCaseFinished'])
            if 'testCaseStarted' in obj:
                started_test_cases.append(TestCaseStarted.model_validate(obj['testCaseStarted']))
            if 'testStepStarted' in obj:
                started_steps.append(obj['testStepStarted'])
            if 'testStepFinished' in obj:
                finished_steps.append(TestStepFinished.model_validate(obj['testStepFinished']))
            if 'gherkinDocument' in obj:
                gherkin_document = obj['gherkinDocument']

        test_steps = []

        results = GherkinResults()

        for test_case in test_cases:
            results.add_test_case(test_case)

            for test_step in test_case.test_steps:
                test_steps.append(TestStep.model_validate(test_step))

        for test_case_started in started_test_cases:
            results.add_test_case_start(test_case_started)

        for step_definition in step_definitions.values():
            results.add_step(step_definition)

        for test_step in test_steps:
            results.add_test_case_step(test_step)

        for pickle in pickles:
            pickle_ast_nodes = []
            for astNodeId in pickle.ast_node_ids:
                self.search(gherkin_document, "id", astNodeId, pickle_ast_nodes)
            results.add_test_case_pickle(pickle, pickle_ast_nodes)

            for step in pickle.steps:
                ast_nodes = []
                for astNodeId in step.ast_node_ids:
                    self.search(gherkin_document, "id", astNodeId, ast_nodes)

                results.add_pickle_step(PickleStep.model_validate(step), ast_nodes, pickle)

        for finished_step in finished_steps:
            results.add_test_step_finished(finished_step)

        self.results = results

        # for finished_test_case in finished_test_cases:
        #     started_test_case = next(
        #         (t for t in started_test_cases if t['id'] == finished_test_case['testCaseStartedId']), None
        #     )
        #     test_case = next(
        #         (t for t in test_cases if t['id'] == started_test_case['testCaseId']), None
        #     )
        #
        #
        #     pickle = next((p for p in pickles if test_case['pickleId'] == p['id']), None)
        #
        #     status = self.is_test_case_passed(finished_test_case['testCaseStartedId'], finished_steps)
        #
        #     if pickle:
        #         ast_node_ids = pickle['astNodeIds']
        #
        #         for pickle_step in pickle['steps']:
        #             test_step_id = pickle_step['id']
        #             step_ast_node_id = pickle_step['astNodeIds'][0]
        #             pass
        #
        #         node_lines = self.ast_node_id_to_lines(ast_node_ids[0], gherkin_document)
        #
        #         if node_lines:
        #             line_number = node_lines[-1]['line']
        #             status_text = " **OK** " if status else " **FAILED** "
        #             # reader.lines[len(reader.lines) + 1 - line_number] += status_text
        #             log.info(f'Found pickle "{pickle["name"]}" at line {line_number} with status {status}')
        #             self._pickles.append(
        #                 {
        #                     "pickle": pickle,
        #                     "line": line_number - 1,
        #                     "status": status
        #                 })
