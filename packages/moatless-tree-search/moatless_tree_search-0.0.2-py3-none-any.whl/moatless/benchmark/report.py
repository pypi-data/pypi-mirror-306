import hashlib
import json
import logging
import os
from typing import Dict, List, Optional

import pandas as pd
from pydantic import BaseModel, Field

from moatless.benchmark.utils import (
    has_identified_spans,
    has_identified_files,
    count_identified_files,
    count_identified_spans,
    get_missing_files,
    get_moatless_instance,
    read_search_trees,
    get_moatless_instances,
)
from moatless.file_context import FileContext
from moatless.index.code_index import is_test
from moatless.node import Node
from moatless.search_tree import SearchTree

logger = logging.getLogger(__name__)


class Flag(BaseModel):
    state_name: Optional[str] = Field(None)
    state_id: Optional[int] = Field(None)
    message: str


class StateStats(BaseModel):
    status: str = ""
    iterations: int = 0
    rejected: int = 0
    cost: float = 0
    found_spans: int = 0
    found_files: int = 0
    result_spans: int = 0
    result_files: int = 0
    found_spans_details: Dict[str, List[str]] = {}


class SearchStats(StateStats):
    p_query: int = 0
    p_file: int = 0
    p_code: int = 0
    p_class: int = 0
    p_function: int = 0


class CodingStats(StateStats):
    review: bool = False
    edit_retries: int = 0
    plan_retries: int = 0
    edited: bool = False

    rejected: int = 0
    largest_span: Optional[int] = None
    smallest_span: Optional[int] = None
    has_diff: bool = False
    lint: bool = False
    lints: str = ""


class FileContextStats(BaseModel):
    status: str
    patch_status: str
    found_spans: int = 0
    found_files: int = 0
    result_spans: int = 0
    result_files: int = 0
    tokens: int = 0


class TrajectoryStats(BaseModel):
    """
    Stats for one finished trajectory.
    """

    state_id: int
    resolved: Optional[bool] = None
    status: Optional[str] = None
    message: Optional[str] = None
    reward: Optional[float] = None
    avg_reward: float = 0

    cost: float = 0
    iterations: int = 0
    transitions: int = 0
    rejections: int = 0
    retries: int = 0

    action_count: int = 0
    actions: dict[str, int] = {}
    context_stats: Optional[FileContextStats] = None

    identify_status: str = ""
    search_status: str = ""

    has_diff: bool = False
    llm_monkey_status: Optional[str] = None

    edits: int = 0
    test_edits: int = 0
    failed_edits: int = 0

    missing_test_files: int = 0

    max_tests_run: int = 0
    max_failed_tests: int = 0
    initial_failed_tests: Optional[int] = None
    final_failed_tests: Optional[int] = None

    largest_span: Optional[int] = None
    smallest_span: Optional[int] = None

    test_count: int = 0
    fail_to_pass_count: int = 0
    pass_to_pass_count: int = 0


class BenchmarkResult(BaseModel):
    instance_id: str

    status: str = ""
    resolved: Optional[bool] = None
    previous_resolved: Optional[bool] = None

    duration: float = 0
    total_cost: float = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    resolved_by: int = 0
    llmonkeys_rate: Optional[float] = None

    transitions: int = 0

    trajectories: List[TrajectoryStats] = []

    # MCTS
    all_transitions: int = 0
    solutions: int = 0
    resolved_solutions: int = 0
    failed_solutions: int = 0
    rejected_solutions: int = 0

    duplicated_search_actions: int = 0

    max_reward: float | None = None
    resolved_max_reward: float | None = None
    failed_max_reward: float | None = None

    edits: int = 0
    test_edits: int = 0
    failed_edits: int = 0

    context_stats: FileContextStats | None = None
    actions: dict[str, int] = {}

    test_count: int = 0
    fail_to_pass_count: int = 0
    pass_to_pass_count: int = 0

    alternative_solutions: int = 0
    reward: Optional[float] = None
    error: str = ""


def create_sha256_hash(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()


def filter_test_code_from_diff(diff: str) -> str:
    filtered_diff = []
    in_test_file = False

    for line in diff.splitlines():
        if line.startswith("diff --git"):
            in_test_file = "tests/" in line or "test_" in line
        if not in_test_file:
            filtered_diff.append(line)

    return "\n".join(filtered_diff)


def create_trajectory_stats(
    trajectory_state: Node, instance: dict, evaluation_result: dict | None = None
) -> TrajectoryStats:
    if instance:
        context_stats = analyse_file_context(instance, trajectory_state.file_context)
    else:
        context_stats = None

    result = TrajectoryStats(
        state_id=trajectory_state.node_id, context_stats=context_stats
    )
    nodes = trajectory_state.get_trajectory()

    test_files = []
    for node in nodes:
        if node.action:
            if node.action.name not in result.actions:
                result.actions[node.action.name] = 0

            result.actions[node.action.name] += 1

            if (
                node.observation
                and node.observation.properties
                and "test_results" in node.observation.properties
            ):
                test_results = node.observation.properties["test_results"]
                failed_test_count = sum(
                    1 for test in test_results if test["status"] in ["FAILED", "ERROR"]
                )

                result.initial_failed_tests = failed_test_count

                if len(test_results) > result.max_tests_run:
                    result.max_tests_run = len(test_results)

                if failed_test_count > result.max_failed_tests:
                    result.max_failed_tests = failed_test_count

                if result.final_failed_tests is None:
                    result.final_failed_tests = failed_test_count

                for test_result in test_results:
                    if test_result["file_path"] not in test_files:
                        test_files.append(test_result["file_path"])

            if node.action.name == "RequestCodeChange":
                if node.observation:
                    if (
                        node.observation.properties
                        and "fail_reason" in node.observation.properties
                    ):
                        result.failed_edits += 1
                    elif is_test(node.action.file_path):
                        result.test_edits += 1
                    else:
                        result.edits += 1

        missing_test_files = get_missing_files(instance["test_file_spans"], test_files)

        result.missing_test_files = len(missing_test_files)

    if evaluation_result:
        result.resolved = (
            evaluation_result.get("resolved")
            if evaluation_result.get("resolved") is not None
            else None
        )

    result.reward = trajectory_state.reward.value if trajectory_state.reward else None

    if trajectory_state.file_context:
        patch = trajectory_state.file_context.generate_git_patch()
        result.has_diff = bool(patch.strip())

        if patch:
            diff_hash = create_sha256_hash(patch)

            # Filter out test code from the diff
            filtered_diff = filter_test_code_from_diff(patch)
            filtered_diff_hash = create_sha256_hash(filtered_diff)

            for patch_hash in instance.get("llm_monkeys", {}).get(
                "resolved_patches", []
            ):
                if patch_hash == diff_hash or patch_hash == filtered_diff_hash:
                    result.llm_monkey_status = "resolved"

            if not result.llm_monkey_status:
                for patch_hash in instance.get("llm_monkeys", {}).get(
                    "unresolved_patches", []
                ):
                    if patch_hash == diff_hash or patch_hash == filtered_diff_hash:
                        result.llm_monkey_status = "unresolved"

    if trajectory_state.reward:
        result.reward = trajectory_state.reward.value

    if trajectory_state.is_terminal():
        if trajectory_state.action and trajectory_state.action.name == "Finish":
            result.status = "finished"
        elif trajectory_state.action and trajectory_state.action.name == "Reject":
            result.status = "rejected"
            result.message = trajectory_state.observation.message
        else:
            result.status = "terminal"
    else:
        result.status = "abandoned"

    result.transitions = len(trajectory_state.get_trajectory())

    return result


def to_result(
    search_tree: SearchTree,
    eval_report: dict | None = None,
    external_result: dict | None = None,
    previous_result: dict | None = None,
) -> BenchmarkResult:
    info = search_tree.metadata
    instance = get_moatless_instance(info["instance_id"])

    if not eval_report:
        eval_report = {}

    if external_result:
        resolved = info.get("instance_id", "") in external_result["resolved_ids"]
    elif eval_report and eval_report.get("resolved") is not None:
        resolved = eval_report.get("resolved")
    else:
        resolved = None

    if previous_result:
        previous_resolved = (
            info.get("instance_id", "") in previous_result["resolved_ids"]
        )
    else:
        previous_resolved = None

    try:
        best_node = search_tree.get_best_trajectory()
        best_stats = None

        if best_node:
            best_stats = create_trajectory_stats(
                best_node,
                instance,
                eval_report.get("node_results", {}).get(str(best_node.node_id)),
            )

        if resolved is not None and resolved:
            status = "resolved"
        elif resolved is not None and not resolved:
            status = "failed"
        elif search_tree.is_finished():
            status = "finished"
        else:
            status = "running"  # TODO: Abandoned?

        total_usage = search_tree.total_usage()

        result = BenchmarkResult(
            instance_id=instance["instance_id"],
            status=status,
            previous_resolved=previous_resolved,
            duration=info.get("duration", 0),
            total_cost=total_usage.completion_cost,
            prompt_tokens=total_usage.prompt_tokens,
            completion_tokens=total_usage.completion_tokens,
            resolved_by=len(instance.get("resolved_by", [])),
            llmonkeys_rate=instance.get("llm_monkeys", {}).get("resolved_rate", 0),
            transitions=len(best_node.get_trajectory()) if best_node else 0,
            all_transitions=len(search_tree.root.get_all_nodes()),
            solutions=0,
            rejected_solutions=0,
            resolved_solutions=0,
            failed_solutions=0,
            context_stats=best_stats.context_stats if best_stats else None,
            actions=best_stats.actions if best_stats else {},
            error=best_stats.message if best_stats and best_stats.message else "",
        )

        trajectories = []
        for transition in search_tree.get_leaf_nodes():
            traj = create_trajectory_stats(
                transition,
                instance,
                eval_report.get("node_results", {}).get(str(transition.node_id)),
            )
            trajectories.append(traj)

            if traj.status == "finished":
                result.solutions += 1
                if traj.reward and (
                    result.max_reward is None or traj.reward > result.max_reward
                ):
                    result.max_reward = traj.reward
            elif traj.status == "rejected":
                result.rejected_solutions += 1

            if eval_report and "node_results" in eval_report:
                if (
                    eval_report["node_results"]
                    .get(str(traj.state_id), {})
                    .get("resolved")
                    is not None
                ):
                    if (
                        eval_report["node_results"]
                        .get(str(traj.state_id), {})
                        .get("resolved", False)
                    ):
                        result.resolved_solutions += 1
                        if traj.reward and (
                            result.resolved_max_reward is None
                            or traj.reward > result.resolved_max_reward
                        ):
                            result.resolved_max_reward = traj.reward
                    else:
                        result.failed_solutions += 1
                        if traj.reward and (
                            result.failed_max_reward is None
                            or traj.reward > result.failed_max_reward
                        ):
                            result.failed_max_reward = traj.reward

            if traj.edits > 0:
                result.edits += 1

            if traj.test_edits > 0:
                result.test_edits += 1

            if traj.failed_edits > 0:
                result.failed_edits += 1

        if "error" in eval_report:
            result.error = eval_report["error"].split("\n")[0]
        else:
            result.error = ""

    except Exception as e:
        raise e

    return result


def analyse_file_context(instance: dict, file_context: FileContext) -> FileContextStats:
    if not file_context:
        return FileContextStats(status="no_context", patch_status="no_context")
    expected_spans = instance.get("expected_spans", {})
    solutions = [expected_spans]
    for resolved_by in instance.get("resolved_by", []):
        if (
            "alternative_spans" in resolved_by
            and resolved_by["alternative_spans"] not in solutions
        ):
            solutions.append(resolved_by["alternative_spans"])

    identified_spans = {}
    patched_files = []
    for file in file_context.files:
        identified_spans[file.file_path] = file.span_ids

        if file.patch:
            patched_files.append(file.file_path)

    if not identified_spans:
        status = "no_spans"
    elif has_identified_spans(solutions, identified_spans):
        status = "found_spans"
    elif has_identified_files(solutions, identified_spans):
        status = "found_files"
    else:
        status = "missing_files"

    if not patched_files:
        patch_status = "no_files"
    elif has_identified_files(solutions, patched_files):
        patch_status = "right_files"
    else:
        patch_status = "wrong_files"

    return FileContextStats(
        status=status,
        patch_status=patch_status,
        result_spans=sum(len(spans) for spans in identified_spans.values()),
        result_files=len(identified_spans),
        found_spans=count_identified_spans(expected_spans, identified_spans),
        found_files=count_identified_files(expected_spans, identified_spans),
        #  TODO      tokens=file_context.context_size(),
    )


def set_found_status(
    expected_spans, alternative_solutions, identified_spans, result_stats
):
    result_stats.result_spans = sum(len(spans) for spans in identified_spans.values())
    result_stats.result_spans = len(identified_spans)
    result_stats.found_files = count_identified_files(expected_spans, identified_spans)
    result_stats.found_spans = count_identified_spans(expected_spans, identified_spans)
    result_stats.found_spans_details = identified_spans

    expected_files = list(expected_spans.keys())
    if result_stats.found_spans == sum(len(spans) for spans in expected_spans.values()):
        result_stats.status = "expected_spans"
    elif has_identified_spans(alternative_solutions, identified_spans):
        result_stats.status = "alternative_spans"
    elif result_stats.found_files == len(expected_files):
        result_stats.status = "expected_files"
    elif has_identified_files(alternative_solutions, identified_spans):
        result_stats.status = "alternative_files"
    else:
        result_stats.status = "missing_spans"


def read_reports(report_path: str) -> List[BenchmarkResult]:
    with open(report_path, "r") as f:
        data = json.load(f)

    results = [BenchmarkResult.model_validate(item) for item in data]
    return results


def trajs_to_df(
    trajectories: List[Node], report_mode: str | None = None
) -> pd.DataFrame:
    results = [to_result(None, trajectory) for trajectory in trajectories]
    return to_dataframe(results, report_mode)


def to_trajectory_dataframe(results: List[BenchmarkResult]):
    result_dicts = []
    for result in results:
        for traj_result in result.trajectories:
            result_dict = {
                "instance_id": result.instance_id,
                "resolved_instance": result.resolved,
                "resolved_by": result.resolved_by,
                "llmonkeys_rate": result.llmonkeys_rate,
            }
            result_dict.update(traj_result.model_dump())
            result_dicts.append(result_dict)

    return pd.DataFrame(result_dicts)


def to_dataframe(
    results: list[BenchmarkResult],
    report_mode: str | None = None,
    previous_report: dict = None,
) -> pd.DataFrame:
    state_keys = ["search", "identify", "decide", "coding", "context_stats"]
    rename_columns = False
    if report_mode == "code":
        state_keys = ["coding"]
    elif report_mode == "search_and_identify":
        state_keys = ["search", "identify"]
    elif report_mode in state_keys:
        state_keys = [report_mode]
        rename_columns = True

    def flatten_dict(d, parent_key="", sep="_"):
        items = []
        general_keys = [
            "instance_id",
            "duration",
            "total_cost",
            "prompt_tokens",
            "completion_tokens",
            "resolved_by",
            "llmonkeys_rate",
            "status",
            "transitions",
            "all_transitions",
            "solutions",
            "resolved_solutions",
            "failed_solutions",
            "rejected_solutions",
            "resolved_max_reward",
            "failed_max_reward",
            "alternative_solutions",
            "resolved",
            "duplicated_search_actions",
            "expected_spans",
            "expected_files",
            "error",
            "trajectory_path",
            "context_stats",
        ]

        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))

            if k.endswith("_spans_details"):
                items.append((new_key, json.dumps(v)))

        if previous_report:
            items.append(
                (
                    "previously_resolved",
                    d.get("instance_id", None) in previous_report["resolved"],
                )
            )
        return dict(items)

    flattened_results = [flatten_dict(result.model_dump()) for result in results]

    df = pd.DataFrame(flattened_results)

    if rename_columns:
        df.columns = [
            col.replace(f"{report_mode}_", "")
            if col.startswith(f"{report_mode}_")
            else col
            for col in df.columns
        ]

    if report_mode == "mcts":
        mcts_cols = [
            "instance_id",
            "resolved_by",
            "llmonkeys_rate",
            "duration",
            "total_cost",
            "prompt_tokens",
            "completion_tokens",
            "status",
            "transitions",
            "all_transitions",
            "solutions",
            "resolved_solutions",
            "failed_solutions",
            "rejected_solutions",
            "resolved_max_reward",
            "failed_max_reward",
            "duplicated_search_actions",
            "trajectory_path",
        ]

        if previous_report:
            mcts_cols.append("previously_resolved")

        # Only select columns that exist in the DataFrame
        existing_cols = [col for col in mcts_cols if col in df.columns]
        df = df[existing_cols]

        # Add missing columns with NaN values
        missing_cols = set(mcts_cols) - set(existing_cols)
        for col in missing_cols:
            df[col] = pd.NA

    elif report_mode == "summary":
        summary_cols = [
            "instance_id",
            "duration",
            "total_cost",
            "status",
            "transitions",
            "expected_spans",
            "expected_files",
            "search_status",
            "search_iterations",
            "identify_status",
            "identify_iterations",
            "decide_status",
            "decide_iterations",
            "coding_status",
            "coding_iterations",
            "coding_edit_retries",
            "coding_plan_retries",
        ]
        df = df[summary_cols]

    # Reorder columns
    column_order = [
        "instance_id",
        "duration",
        "total_cost",
        "prompt_tokens",
        "completion_tokens",
        "resolved_by",
        "status",
        "resolved",
        "transitions",
        "all_transitions",
        "expected_spans",
        "expected_files",
        "alternative_solutions",
        "expected_spans_details",
        "error",
    ]

    state_columns = [
        "status",
        "iterations",
        "rejected",
        "cost",
        "found_spans",
        "found_files",
        "result_spans",
        "result_files",
        "found_spans_details",
    ]

    for state in state_keys:
        column_order.extend([f"{state}_{col}" for col in state_columns])

    # Add any remaining columns
    remaining_columns = [col for col in df.columns if col not in column_order]
    column_order.extend(remaining_columns)

    # Reorder the dataframe columns
    df = df.reindex(columns=[col for col in column_order if col in df.columns])
    return df


def read_results_from_json(file_path: str) -> List[BenchmarkResult]:
    with open(file_path, "r") as f:
        data = json.load(f)

    results = [BenchmarkResult.validate(item) for item in data]
    return results


def generate_report(dir: str):
    result_path = os.path.join(dir, "result.json")

    external_result = None
    if os.path.exists(result_path):
        with open(result_path, "r") as f:
            external_result = json.load(f)

    search_trees = read_search_trees(dir)
    logger.info(f"Search trees: {len(search_trees)}")
    if not search_trees:
        raise ValueError("No trajectories found")
    instances = get_moatless_instances()

    results = []
    for search_tree in search_trees:
        instance_id = search_tree.metadata["instance_id"]

        instance = instances.get(instance_id)
        if not instance:
            logger.error(f"Instance {instance_id} not found")
            continue

        eval_report = None
        eval_result_file = os.path.join(dir, instance_id, "eval_result.json")
        try:
            if os.path.exists(eval_result_file):
                with open(eval_result_file, "r") as f:
                    eval_report = json.load(f)
        except Exception as e:
            logger.exception(f"Failed to load eval report from {eval_result_file}: {e}")

        result = to_result(search_tree, eval_report, external_result)
        results.append(result)

    report_path = os.path.join(dir, "report.json")
    with open(report_path, "w") as f:
        json.dump([result.model_dump() for result in results], f, indent=2)
