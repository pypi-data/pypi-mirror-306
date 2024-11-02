import re
import sys
from abc import abstractmethod
from typing import Any, Container, Dict, List, Literal, Tuple, Type

from pydantic import BaseModel
import json
import pandas as pd
import numpy as np

from apropos.src.bench.bigcodebench.backends.docker import (
    execute_code_remotely_docker_sync,
)
from apropos.src.bench.bigcodebench.backends.modal import (
    execute_code_remotely_modal_async,
    execute_code_remotely_modal_sync,
)  # change to execute_code_remotely_modal asap
from apropos.src.bench.bigcodebench.main import (
    BigCodeBench_Question,
)
from smallbench.benchmarks.bcb_a.abstractions import (
    ACIAction,
    CurrentSolution,
    Transform,
)
from smallbench.benchmarks.bcb_a.contexts import unit_test_context
from smallbench.core.aci import AgentComputerInterface
from smallbench.utilities.code.use_docker import execute_code_docker
from smallbench.utilities.code.use_modal import (
    execute_code_modal_async,
    execute_code_modal_sync,
)
from smallbench.utilities.code.linter import lint_code
from typing import Dict, Tuple
from datetime import datetime

class BCBUnitTest(BaseModel):
    test_description: str
    input_names: List[str]
    input_types: List[str]
    input_values: List[Any]
    assertion_condition: str
    assertion_type: Literal["assertTrue", "assertRaises"] = "assertTrue"

    def to_dict(self) -> Dict:
        return {
            "test_description": self.test_description,
            "input_names": self.input_names,
            "input_types": self.input_types,
            "input_values": self.input_values,
            "assertion_condition": self.assertion_condition,
            "assertion_type": self.assertion_type,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict) -> "BCBUnitTest":
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "BCBUnitTest":
        data = json.loads(json_str)
        return cls.from_dict(data)

    def to_python(self, index: int, function_name: str = "task_func"):
        definitions = [
            "import pandas as pd",
            "import numpy as np",
            "from datetime import datetime",
            "import os",
        ]
        arguments = {}
        for i, (input_name, input_type, input_value) in enumerate(
            zip(self.input_names, self.input_types, self.input_values)
        ):
            # print("Input type: ", input_type, "Input value: ", input_value)
            if input_type == "pd.DataFrame" and isinstance(input_value, pd.DataFrame):
                json_value = input_value.to_json(orient="split")
                definitions.append("import pandas as pd")
                definitions.append(
                    f"var_{i} = pd.read_json('{json_value}', orient='split')"
                )
            elif input_type == "pd.DataFrame":
                raise ValueError(f"Invalid input value for DataFrame: {input_value}")
            elif input_type == "np.ndarray":
                print("Got numpy array")
                definitions.append(f"var_{i} = np.array({input_value})")
            elif input_type == "datetime" or isinstance(input_value, datetime):
                definitions.append(f"var_{i} = datetime.fromisoformat('{input_value}')")
            elif not input_type == "str":
                definitions.append(f"var_{i} = {input_value}")
            # String stuff
            elif input_type == "str" and isinstance(input_value, str):
                if input_value in ["'", '"']:
                    definitions.append(f"var_{i} = '\"'")
                elif len(input_value) == 0:
                    definitions.append(f"var_{i} = ''")
                elif not (
                    input_value[0] in ["'", '"'] and input_value[-1] in ["'", '"']
                ):
                    definitions.append(f"var_{i} = '{input_value}'")
                else:
                    definitions.append(f"var_{i} = {input_value}")
            elif isinstance(input_value, Dict) and input_type == "str":
                definitions.append(f'var_{i} = """{input_value}"""')
            else:
                raise ValueError(
                    f"Invalid input value for string: {input_value} - {input_type}"
                )
            arguments[input_name] = f"var_{i}"
        args = ", ".join([f""""{k}":{v}""" for k, v in arguments.items()])
        defs = "\n        ".join(definitions)
        if self.assertion_type == "assertTrue":
            final_representation = f"""
    def test_case_{index}(self):
        # {self.test_description}

        {defs}
        result = {function_name}(**{{{args}}})
        self.{self.assertion_type}({self.assertion_condition})
"""
        elif self.assertion_type == "assertRaises":
            final_representation = f"""
    def test_case_{index}(self):
        # {self.test_description}
        {defs}
        with self.{self.assertion_type}({self.assertion_condition}):
            {function_name}(**{{{args}}})
"""
        else:
            raise ValueError(f"Invalid assertion type: {self.assertion_type}")
        return final_representation


class BCBPersistentContainer:
    bcb_question: BigCodeBench_Question
    container: Any

    def __init__(self, bcb_question: BigCodeBench_Question):
        self.bcb_question = bcb_question

        # warm up the container with necessary imports
        self.container = None
        self.execute_code_sync("eval.py", {"eval.py": self.get_answer_imports()})

    def get_answer_imports(self) -> str:
        answer_lines = self.bcb_question.information["answer"].split("\n")
        import_lines = [line for line in answer_lines if line.startswith("import")]
        return "\n".join(import_lines)

    @abstractmethod
    def execute_code_sync(
        self, entrypoint_script: str, scripts_by_name: Dict[str, str]
    ) -> Tuple[str, Container]:
        pass

    async def execute_code_async(self, code: str):
        raise NotImplementedError(
            "This method must be implemented once we have support for async docker"
        )


class BCBModalPersistentContainer(BCBPersistentContainer):
    bcb_question: BigCodeBench_Question

    def __init__(self, bcb_question: BigCodeBench_Question):
        super().__init__(bcb_question)

    async def execute_code(
        self, entrypoint_script: str, scripts_by_name: Dict[str, str]
    ) -> Tuple[str, Container]:
        pass


class BCBDockerPersistentContainer:
    def __init__(self, bcb_question):
        raise NotImplementedError("This needs to be implemented")

    #     self.client = docker.from_env()
    #     self.container = None
    #     self.bcb_question = bcb_question
    #     self.temp_dir = tempfile.mkdtemp()
    #     self.logger = logging.getLogger(__name__)
    #     self.start_container()

    # def start_container(self):
    #     if not self.container or not self.is_container_running():
    #         try:
    #             self.container = self.client.containers.run(
    #                 "python:3.9-slim",
    #                 command="tail -f /dev/null",
    #                 detach=True,
    #                 remove=True,
    #                 working_dir="/app",
    #                 volumes={self.temp_dir: {"bind": "/app", "mode": "rw"}}
    #             )
    #             self.logger.info(f"Container started with ID: {self.container.id}")
    #             self.warm_up_container()
    #         except APIError as e:
    #             self.logger.error(f"Error starting container: {e}")
    #             raise

    # def get_answer_imports(self):
    #     answer_lines = self.bcb_question.information["answer"].split("\n")
    #     import_lines = [line for line in answer_lines if line.startswith("import")]
    #     return "\n".join(import_lines)

    # def warm_up_container(self):
    #     warm_up_code = self.get_answer_imports()
    #     self.execute_code_sync("warm_up.py", {"warm_up.py": warm_up_code})

    # def is_container_running(self):
    #     if not self.container:
    #         return False
    #     try:
    #         self.container.reload()
    #         return self.container.status == "running"
    #     except NotFound:
    #         return False

    # def ensure_container_running(self):
    #     if not self.is_container_running():
    #         self.start_container()

    # def execute_code_sync(self, entrypoint_script: str, scripts_by_name: Dict[str, str]) -> Tuple[str, docker.models.containers.Container]:
    #     self.ensure_container_running()

    #     for name, content in scripts_by_name.items():
    #         encoded_content = content.encode('utf-8')
    #         _, exec_output = self.container.exec_run(f"sh -c 'mkdir -p /app && echo \"{encoded_content.decode('utf-8')}\" > /app/{name}'")
    #         if exec_output:
    #             self.logger.warning(f"Output while writing {name}: {exec_output.decode()}")

    #     exit_code, output = self.container.exec_run(f"python /app/{entrypoint_script}")
    #     if exit_code != 0:
    #         self.logger.error(f"Script execution failed with exit code {exit_code}")
    #     return output.decode(), self.container

    # def stop_container(self):
    #     if self.container:
    #         try:
    #             self.container.stop(timeout=10)
    #             self.container.remove(force=True)
    #             self.logger.info(f"Container {self.container.id} stopped and removed")
    #         except APIError as e:
    #             self.logger.error(f"Error stopping container: {e}")
    #         finally:
    #             self.container = None

    # def __del__(self):
    #     self.stop_container()
    #     if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
    #         try:
    #             shutil.rmtree(self.temp_dir)
    #         except OSError as e:
    #             self.logger.error(f"Error removing temporary directory: {e}")


class BCBEngine:
    backend: Literal["docker", "modal"] = "docker"
    bcb_question: BigCodeBench_Question
    persistent_container: Type[BCBPersistentContainer]
    use_persistent_container: bool = True

    def __init__(
        self,
        bcb_question: BigCodeBench_Question,
        backend: Literal["docker", "modal"] = "docker",
        use_persistent_container: bool = False,
    ):
        self.bcb_question = bcb_question
        self.backend = backend
        self.use_persistent_container = use_persistent_container
        if backend == "docker" and use_persistent_container:
            self.persistent_container = BCBDockerPersistentContainer(
                bcb_question=bcb_question
            )
        elif backend == "modal" and use_persistent_container:
            self.persistent_container = BCBModalPersistentContainer(
                bcb_question=bcb_question
            )
        elif not backend in ["docker", "modal"]:
            raise ValueError(f"Invalid backend: {backend}")

    def temp_code_hack(self, headless_submission: str):
        # TEMP HACK
        try:
            if "def task_func" in headless_submission:
                lines = headless_submission.split("\n")
                i = [i for i, line in enumerate(lines) if "def task_func" in line][0]
                headless_submission = "\n".join(lines[(i + 1) :])
        except Exception as e:
            print("Error in temp hack: ", e)
            print("Headless submission: ", headless_submission)
            raise e
        return headless_submission

    async def execute_final_submission_against_hidden_tests_async(
        self, final_submission
    ):
        final_submission = self.temp_code_hack(final_submission)
        all_unique_imports, imports_snippet = self.get_imports()
        if self.backend == "docker":
            if not self.use_persistent_container:
                success, result, container = execute_code_remotely_docker_sync(
                    self.bcb_question.information,
                    final_submission,
                )
            else:
                success, result, container = (
                    self.persistent_container.execute_code_sync(
                        entrypoint_script="eval.py",
                        scripts_by_name={"eval.py": final_submission},
                    )
                )
        elif self.backend == "modal":
            if not self.use_persistent_container:
                success, result = await execute_code_remotely_modal_async(
                    self.bcb_question.information,
                    final_submission,
                )
        else:
            raise ValueError(f"Invalid backend: {self.backend}")
        return success, result

    def execute_final_submission_against_hidden_tests_sync(self, final_submission):
        final_submission = self.temp_code_hack(final_submission)
        all_unique_imports, imports_snippet = self.get_imports()
        if self.backend == "docker":
            if not self.use_persistent_container:
                success, result, container = execute_code_remotely_docker_sync(
                    self.bcb_question.information,
                    final_submission,
                )
            else:
                success, result, container = (
                    self.persistent_container.execute_code_sync(
                        entrypoint_script="eval.py",
                        scripts_by_name={"eval.py": final_submission},
                    )
                )
        elif self.backend == "modal":
            if not self.use_persistent_container:
                success, result = execute_code_remotely_modal_sync(
                    self.bcb_question.information,
                    final_submission,
                )
        else:
            raise ValueError(f"Invalid backend: {self.backend}")
        return success, result

    def get_imports(self) -> Tuple[List[str], str]:
        code_prompt = self.bcb_question.information["eval_info"]["code_prompt"]
        from_imports = re.findall(r"from (\w+) import (\w+)", code_prompt)
        head_imports = re.findall(r"^import (\w+)(?!\s+as)$", code_prompt, re.MULTILINE)
        head_imports_with_alias = re.findall(r"import ([\w.]+) as (\w+)", code_prompt)
        imports_snippet = "\n".join(
            ["import " + imp for imp in head_imports]
            + [f"import {imp} as {alias}" for imp, alias in head_imports_with_alias]
            + [
                f"from {package} import {class_or_function}"
                for package, class_or_function in from_imports
            ]
        )
        standard_libs = set(sys.stdlib_module_names)
        all_unique_imports = [imp for imp in head_imports if imp not in standard_libs]
        for imp, _ in head_imports_with_alias:
            package = imp.split(".")[0]
            if package not in all_unique_imports and package not in standard_libs:
                all_unique_imports.append(package)
        for package, _ in from_imports:
            if package not in all_unique_imports and package not in standard_libs:
                all_unique_imports.append(package)


        # Rules
        aliases = {"sklearn": "scikit-learn", "PIL": "Pillow", "cv2": "opencv-python"}
        all_unique_imports = [aliases.get(imp, imp) for imp in all_unique_imports]

        if "scipy" in code_prompt and "scipy" not in all_unique_imports:
            print("Danger - missing scipy")
            all_unique_imports.append("scipy")
        if "sklearn" in code_prompt and "scikit-learn" not in all_unique_imports:
            print("Danger - missing scikit-learn")
            all_unique_imports.append("scikit-learn")
        return all_unique_imports, imports_snippet

    async def execute_submission_against_tests_async(
        self, headless_submission: str, tests: List[BCBUnitTest]
    ):  # Write new docker code for this
        headless_submission = self.temp_code_hack(headless_submission)
        all_unique_imports, imports_snippet = self.get_imports()
        tests_snippet = f"""
import unittest
{imports_snippet}
class TestCases(unittest.TestCase):
"""
        if len(tests) == 0:
            return "No tests found - Either you never added any, or you deleted them all"
        for i, test in enumerate(tests):
            tests_snippet += test.to_python(index=i)
        assert len(tests_snippet) > 0, "Tests snippet is empty"

        full_script = (
            self.bcb_question.information["eval_info"]["code_prompt"]
            + "\n"
            + headless_submission
            + "\n"
            + tests_snippet
        )
        if self.backend == "modal":
            location = "/vol"
        elif self.backend == "docker":
            location = "/app"
        else:
            raise Exception("Invalid backend")
        eval_snippet = f"""
import unittest
import io
def test_code():
    path = "script.py"
    loader = unittest.TestLoader()
    suite = loader.discover('{location}', pattern=path)
    runner = unittest.TextTestRunner()
    assert suite.countTestCases() != 0, "No tests found in script.py"
    result = runner.run(suite)

    result_dict = {{
        "errors": len(result.errors),
        "failures": len(result.failures),
        "testsRun": result.testsRun,
        "wasSuccessful": result.wasSuccessful()
    }}
    return result.wasSuccessful(), result_dict

if __name__ == "__main__":
    success, result = test_code()
    print("Success:", success)
    print(result)
"""
        if self.backend == "docker":
            if not self.use_persistent_container:
                results, _ = execute_code_docker(
                    script_to_run_by_name="eval.py",
                    scripts_by_name={"eval.py": eval_snippet, "script.py": full_script},
                    python_version="python:3.9-slim",
                    packages=all_unique_imports,
                    dir_name="bcb",
                )
            else:
                results, _ = self.persistent_container.execute_code_sync(
                    entrypoint_script="eval.py",
                    scripts_by_name={"eval.py": eval_snippet, "script.py": full_script},
                )
                print("Results: ", results)
            logs_pattern = r"([\s\S]*?)(?=Success:)"
            test_results_pattern = r"Success: (True|False)\s*(\{.*\})"

            logs_match = re.search(logs_pattern, results, re.DOTALL)
            test_results_match = re.search(test_results_pattern, results, re.DOTALL)
            if logs_match and test_results_match:
                logs = logs_match.group(1).strip()
                success = test_results_match.group(1) == "True"
                test_results = eval(test_results_match.group(2))
            else:
                print("No match found")
                logs = ""
                success = False
                test_results = {}
            success = (
                success
                and test_results["wasSuccessful"]
                and test_results["testsRun"] > 0
            )
            if success:
                result = "All tests passed"
            elif logs == "":
                result = "Running tests resulted in an execution hardfail"
            else:
                result = f"Not all tests passed. Results summary: {test_results}. \nExecution logs: {logs}"
            # parse these
        elif self.backend == "modal":
            results, sterror = await execute_code_modal_async(
                script_to_run_by_name="eval.py",
                scripts_by_name={"eval.py": eval_snippet, "script.py": full_script},
                python_version="3.9",
                packages=all_unique_imports,
                dir_name="bcb",
                verbose=True,
            )
            result = f"<unit test results><topline results>{results}</topline results><sterror>{sterror}</sterror></unit test results>"
            # Cut down on unnec tokens
            # if "ERROR:" in results:
            #     result = "ERROR:" + results.split("ERROR:")[1].strip()
            # else:
            #     result = results
        else:
            raise ValueError(f"Invalid backend: {self.backend}")
        return result

    def execute_submission_against_tests_sync(
        self, headless_submission: str, tests: List[BCBUnitTest]
    ):
        headless_submission = self.temp_code_hack(headless_submission)
        all_unique_imports, imports_snippet = self.get_imports()
        tests_snippet = f"""
import unittest
{imports_snippet}
class TestCases(unittest.TestCase):
"""
        if len(tests) == 0:
            return "No tests found - Either you never added any, or you deleted them all"
        for i, test in enumerate(tests):
            tests_snippet += test.to_python(index=i)
        assert len(tests_snippet) > 0, "Tests snippet is empty"

        full_script = (
            self.bcb_question.information["eval_info"]["code_prompt"]
            + "\n"
            + headless_submission
            + "\n"
            + tests_snippet
        )
        location = "/app" if self.backend == "docker" else "/vol"
        eval_snippet = f"""
import unittest
import io
def test_code():
    path = "script.py"
    loader = unittest.TestLoader()
    suite = loader.discover('{location}', pattern=path)
    runner = unittest.TextTestRunner()
    assert suite.countTestCases() != 0, "No tests found in script.py"
    result = runner.run(suite)

    result_dict = {{
        "errors": len(result.errors),
        "failures": len(result.failures),
        "testsRun": result.testsRun,
        "wasSuccessful": result.wasSuccessful()
    }}
    return result.wasSuccessful(), result_dict

if __name__ == "__main__":
    success, result = test_code()
    print("Success:", success)
    print(result)
"""
        if self.backend == "docker":
            if not self.use_persistent_container:
                results, _ = execute_code_docker(
                    script_to_run_by_name="eval.py",
                    scripts_by_name={"eval.py": eval_snippet, "script.py": full_script},
                    python_version="python:3.9-slim",
                    packages=all_unique_imports,
                    dir_name="bcb",
                )
            else:
                results, _ = self.persistent_container.execute_code_sync(
                    entrypoint_script="eval.py",
                    scripts_by_name={"eval.py": eval_snippet, "script.py": full_script},
                )
                print("Results: ", results)
            logs_pattern = r"([\s\S]*?)(?=Success:)"
            test_results_pattern = r"Success: (True|False)\s*(\{.*\})"

            logs_match = re.search(logs_pattern, results, re.DOTALL)
            test_results_match = re.search(test_results_pattern, results, re.DOTALL)
            if logs_match and test_results_match:
                logs = logs_match.group(1).strip()
                success = test_results_match.group(1) == "True"
                test_results = eval(test_results_match.group(2))
            else:
                print("No match found")
                logs = ""
                success = False
                test_results = {}
            success = (
                success
                and test_results["wasSuccessful"]
                and test_results["testsRun"] > 0
            )
            if success:
                result = "All tests passed"
            elif logs == "":
                result = "Running tests resulted in an execution hardfail"
            else:
                result = f"Not all tests passed. Results summary: {test_results}. \nExecution logs: {logs}"
        elif self.backend == "modal":
            results, sterror = execute_code_modal_sync(
                script_to_run_by_name="eval.py",
                scripts_by_name={"eval.py": eval_snippet, "script.py": full_script},
                python_version="3.9",
                packages=all_unique_imports,
                dir_name="bcb",
                verbose=True,
            )
            result = (
                "ERROR:" + results.split("ERROR:")[1].strip()
                if "ERROR:" in results
                else results
            )
        else:
            raise ValueError(f"Invalid backend: {self.backend}")
        return result


class BCBAgentComputerInterface(AgentComputerInterface):
    unit_tests: Dict[str, BCBUnitTest]
    sketch: str  # TODO: add this!
    current_solution: CurrentSolution
    bcb_backend: BCBEngine
    actions: List[ACIAction]
    final_submission: str
    final_success: bool
    terminated: bool
    synchronous: bool

    def __init__(self, bcb_backend: BCBEngine, synchronous: bool = False):
        self.unit_tests = {}
        self.current_solution = CurrentSolution(lines=[])
        self.bcb_backend = bcb_backend
        self.synchronous = synchronous
        self.actions = [
            ACIAction(
                action_name="edit_submission",
                action_arg_spec={"first_line": int, "last_line": int, "new_code": str},
                action_description="Edit the submission code",
                action_context="Edit the submission code. Use this when you want to make changes to the current solution.",
                transform=Transform(callable=self.edit_submission, type="sync"),
            ),
            ACIAction(
                action_name="add_submission",
                action_arg_spec={"submission": str},
                action_description="Add the submission code",
                action_context="Add the submission code. Use this when you want to start from scratch with a new solution.",
                transform=Transform(callable=self.add_submission, type="sync"),
            ),
            ACIAction(
                action_name="add_unit_test",
                action_arg_spec={"unit_test_name": str, "unit_test_dict": Dict},
                action_description="Add a unit test",
                action_context=f"""Add a unit test. The unit test information you submit must be in the format of a BCBUnitTest: \n
class BCBUnitTest(BaseModel):
    test_description: str
    input_names: List[str]
    input_types: List[str]
    input_values: List[Any]
    assertion_condition: str
    assertion_type: Literal["assertTrue", "assertRaises"] = "assertTrue"

\n\n It will be parsed via BCBUnitTest(**unit_test_dict)
    


{unit_test_context}""",
                transform=Transform(callable=self.add_unit_test, type="sync"),
            ),
            ACIAction(
                action_name="remove_unit_test",
                action_arg_spec={"unit_test_name": str},
                action_description="Remove a unit test",
                action_context="Remove a unit test",
                transform=Transform(callable=self.remove_unit_test, type="sync"),
            ),
        ] + self.get_submission_actions()
        self.final_success = False
        self.final_submission = None
        self.terminated = False
    
    def lint_submission(self):
        full_code = self.bcb_backend.bcb_question.information["eval_info"]["code_prompt"] + "\n" + self.current_solution.for_execution()
        return lint_code(full_code)

    def get_submission_actions(self):
        if self.synchronous:
            test = ACIAction(
                action_name="test_submission",
                action_arg_spec={},
                action_description="Test the submission",
                action_context="Test the submission",
                transform=Transform(
                    callable=self._execute_submission_against_tests_sync, type="sync"
                ),
            )
            submit = ACIAction(
                action_name="submit_solution",
                action_arg_spec={},
                action_description="Submit the solution",
                action_context="Submit the solution",
                transform=Transform(callable=self._submit_solution_sync, type="sync"),
            )
            return [test, submit]

        else:
            test = ACIAction(
                action_name="test_submission",
                action_arg_spec={},
                action_description="Test the submission",
                action_context="Test the submission",
                transform=Transform(
                    callable=self._execute_submission_against_tests_async, type="async"
                ),
            )
            submit = ACIAction(
                action_name="submit_solution",
                action_arg_spec={},
                action_description="Submit the solution",
                action_context="Submit the solution",
                transform=Transform(callable=self._submit_solution_async, type="async"),
            )
            return [test, submit]

    async def accept_delta_async(self, action_name: str, action_args: Dict):
        action = next(
            (action for action in self.actions if action.action_name == action_name),
            None,
        )
        if action is None:
            raise ValueError(f"Action {action_name} not found")
        result = await action._act_async(action_args)
        return result

    def accept_delta_sync(self, action_name: str, action_args: Dict):
        action = next(
            (action for action in self.actions if action.action_name == action_name),
            None,
        )
        if action is None:
            raise ValueError(f"Action {action_name} not found")
        result = action._act_sync(action_args)
        return result

    async def _execute_submission_against_tests_async(self):
        results = await self.bcb_backend.execute_submission_against_tests_async(
            self.current_solution.for_execution(), list(self.unit_tests.values())
        )
        return results

    def _execute_submission_against_tests_sync(self):
        results = self.bcb_backend.execute_submission_against_tests_sync(
            self.current_solution.for_execution(), list(self.unit_tests.values())
        )
        return results

    def edit_submission(self, first_line: int, last_line: int, new_code: str):
        if not isinstance(new_code, str):
            return "New code must be a string"
        self.current_solution.lines[first_line:last_line] = new_code.split("\n")
        lint_result = self.lint_submission()
        if lint_result:
            full_code = self.bcb_backend.bcb_question.information["eval_info"]["code_prompt"] + "\n" + self.current_solution.for_execution()
            return f"Your edit was added - the full script is now <full_script>{full_code}</full_script> - result of automatic linting applied to the code: \n{lint_result}"
        else:
            return "Your edit was added successfully. No linting issues were found."

    def add_submission(self, submission: str):
        if not isinstance(submission, str):
            return "Submission must be a string"
        self.current_solution = CurrentSolution(lines=submission.split("\n"))
        lint_result = self.lint_submission()
        if lint_result:
            full_code = self.bcb_backend.bcb_question.information["eval_info"]["code_prompt"] + "\n" + self.current_solution.for_execution()
            return f"Your submission was added - the full script is now <full_script>{full_code}</full_script> - result of automatic linting applied to the code: \n{lint_result}"
        else:
            return "Your submission was added successfully. No linting issues were found."

    def add_unit_test(self, unit_test_name: str, unit_test_dict: Dict):
        try:
            self.unit_tests[unit_test_name] = BCBUnitTest(**unit_test_dict)
            return "Added unit test successfully"
        except Exception as e:
            return f"Failed to add unit test: {e}"

    def remove_unit_test(self, unit_test_name: str):
        try:
            self.unit_tests.pop(unit_test_name)
            return "Removed unit test successfully"
        except Exception as e:
            return f"Failed to remove unit test: {e}"

    async def _submit_solution_async(self):
        (
            tests_ran,
            result,
        ) = await self.bcb_backend.execute_final_submission_against_hidden_tests_async(
            self.current_solution.for_execution()
        )
        if result["testsRun"] == 0:
            print("Warning: No final tests ran")
        success = tests_ran and result["wasSuccessful"] and result["testsRun"] > 0

        self.final_submission = self.current_solution.for_execution()
        self.final_success = success
        return f"Solution submitted successfully, Success: {success}"

    def _submit_solution_sync(self):
        (
            tests_ran,
            result,
        ) = self.bcb_backend.execute_final_submission_against_hidden_tests_sync(
            self.current_solution.for_execution()
        )
        if result["testsRun"] == 0:
            print("Warning: No final tests ran")

        success = tests_ran and result["wasSuccessful"] and result["testsRun"] > 0

        self.final_submission = self.current_solution.for_execution()
        self.final_success = success
        return f"Solution submitted successfully, Success: {success}"

    def check_termination(self):
        return self.final_success is not False or self.final_submission is not None

    def dump_state(self) -> str:
        """
        Dumps the stateful elements of the ACI to a JSON string.
        """
        state = {
            "unit_tests": {name: test.dict() for name, test in self.unit_tests.items()},
            "sketch": self.sketch,
            "current_solution": self.current_solution.for_execution(),
            "final_submission": self.final_submission,
            "final_success": self.final_success,
            "terminated": self.terminated,
            "synchronous": self.synchronous,
        }
        return json.dumps(state)

    def load_state(self, snapshot: str):
        """
        Loads the stateful elements from a JSON string snapshot.
        """
        state = json.loads(snapshot)
        self.unit_tests = {
            name: BCBUnitTest(**test)
            for name, test in state.get("unit_tests", {}).items()
        }
        self.sketch = state.get("sketch", "")
        self.current_solution = CurrentSolution(
            lines=state.get("current_solution", "").split("\n")
        )
        self.final_submission = state.get("final_submission", "")
        self.final_success = state.get("final_success", False)
        self.terminated = state.get("terminated", False)
        self.synchronous = state.get("synchronous", False)


