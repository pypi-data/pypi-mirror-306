import json
import logging
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field

from moatless.agent.agent import ActionAgent
from moatless.completion.model import Usage
from moatless.discriminator import MeanAwardDiscriminator, Discriminator
from moatless.feedback import FeedbackGenerator
from moatless.file_context import FileContext
from moatless.index.code_index import CodeIndex
from moatless.node import Node, generate_ascii_tree
from moatless.repository.repository import Repository
from moatless.selector import BestFirstSelector, Selector, SoftmaxSelector
from moatless.value_function import ValueFunction
from moatless.runtime.runtime import RuntimeEnvironment

logger = logging.getLogger(__name__)


class SearchTree(BaseModel):
    root: Node = Field(..., description="The root node of the search tree.")
    selector: Selector = Field(..., description="Selector for node selection.")
    agent: ActionAgent = Field(..., description="Agent for generating actions.")
    value_function: Optional[ValueFunction] = Field(
        None, description="Value function for reward calculation."
    )
    feedback_generator: Optional[FeedbackGenerator] = Field(
        None, description="Feedback generator."
    )
    discriminator: Optional[Discriminator] = Field(
        None, description="Discriminator for selecting the best trajectory."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for the search tree."
    )
    persist_path: Optional[str] = Field(
        None, description="Path to persist the search tree."
    )
    unique_id: int = Field(default=0, description="Unique ID counter for nodes.")

    max_expansions: int = Field(
        1, description="The maximum number of expansions of one state."
    )
    max_iterations: int = Field(
        10, description="The maximum number of iterations to run the tree search."
    )
    max_cost: Optional[float] = Field(
        None, description="The maximum cost spent on token before finishing."
    )
    min_finished_nodes: Optional[int] = Field(
        None,
        description="The minimum number of finished nodes to consider before finishing",
    )
    max_finished_nodes: Optional[int] = Field(
        None,
        description="The maximum number of finished nodes to consider before finishing",
    )
    reward_threshold: Optional[float] = Field(
        None, description="The min reward threshold to consider before finishing."
    )
    max_depth: int = Field(
        10, description="The maximum depth for one trajectory in simulations."
    )

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def create(
        cls,
        message: Optional[str] = None,
        root: Optional[Node] = None,
        file_context: Optional[FileContext] = None,
        selector: Optional[Selector] = None,
        agent: Optional[ActionAgent] = None,
        value_function: Optional[ValueFunction] = None,
        feedback_generator: Optional[FeedbackGenerator] = None,
        discriminator: Optional[Discriminator] = None,
        metadata: Optional[Dict[str, Any]] = None,
        persist_path: Optional[str] = None,
        max_expansions: int = 1,
        max_iterations: int = 10,
        max_cost: Optional[float] = None,
        min_finished_nodes: Optional[int] = None,
        max_finished_nodes: Optional[int] = None,
        reward_threshold: Optional[float] = None,
        max_depth: int = 10,
    ) -> "SearchTree":
        if not root and not message:
            raise ValueError("Either a root node or a message must be provided.")

        if not root:
            root = Node(
                node_id=0,
                max_expansions=max_expansions,
                message=message,
                file_context=file_context,
            )

        selector = selector or BestFirstSelector()

        return cls(
            root=root,
            selector=selector,
            agent=agent,
            value_function=value_function,
            feedback_generator=feedback_generator,
            discriminator=discriminator or MeanAwardDiscriminator(),
            metadata=metadata or {},
            persist_path=persist_path,
            max_expansions=max_expansions,
            max_iterations=max_iterations,
            max_cost=max_cost,
            min_finished_nodes=min_finished_nodes,
            max_finished_nodes=max_finished_nodes,
            reward_threshold=reward_threshold,
            max_depth=max_depth,
        )

    @classmethod
    def model_validate(cls, obj: Any, repository: Repository | None = None):
        if isinstance(obj, dict):
            obj = obj.copy()

            if "selector" in obj and isinstance(obj["selector"], dict):
                selector_type = obj["selector"].get("type")
                if selector_type == "BestFirstSelector":
                    obj["selector"] = BestFirstSelector.model_validate(obj["selector"])
                elif selector_type == "SoftmaxSelector":
                    obj["selector"] = SoftmaxSelector.model_validate(obj["selector"])
                else:
                    raise ValueError(f"Unknown selector type: {selector_type}")

            if "agent" in obj and isinstance(obj["agent"], dict):
                obj["agent"] = ActionAgent.model_validate(obj["agent"])

            if "value_function" in obj and isinstance(obj["value_function"], dict):
                obj["value_function"] = ValueFunction.model_validate(
                    obj["value_function"]
                )

            if "feedback_generator" in obj and isinstance(
                obj["feedback_generator"], dict
            ):
                obj["feedback_generator"] = FeedbackGenerator.model_validate(
                    obj["feedback_generator"]
                )

            if "discriminator" in obj and isinstance(obj["discriminator"], dict):
                obj["discriminator"] = MeanAwardDiscriminator.model_validate(
                    obj["discriminator"]
                )

            if "root" in obj and isinstance(obj["root"], dict):
                obj["root"] = Node.reconstruct(obj["root"], repo=repository)

        return super().model_validate(obj)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
        persist_path: str | None = None,
        repository: Repository | None = None,
        code_index: CodeIndex | None = None,
        runtime: RuntimeEnvironment | None = None,
    ) -> "SearchTree":
        data = data.copy()
        if persist_path:
            data["persist_path"] = persist_path

        if "agent" in data and isinstance(data["agent"], dict):
            agent_data = data["agent"]
            data["agent"] = ActionAgent.model_validate(
                agent_data,
                repository=repository,
                code_index=code_index,
                runtime=runtime,
            )
        return cls.model_validate(data, repository)

    @classmethod
    def from_file(
        cls, file_path: str, persist_path: str | None = None, **kwargs
    ) -> "SearchTree":
        with open(file_path, "r") as f:
            tree_data = json.load(f)

        return cls.from_dict(
            tree_data, persist_path=persist_path or file_path, **kwargs
        )

    def run_search(self) -> Node | None:
        """Run the MCTS algorithm for a specified number of iterations."""

        self.assert_runnable()

        logger.info(generate_ascii_tree(self.root))

        if len(self.root.get_all_nodes()) > 1:
            logger.info(
                f"Restarting search tree with {len(self.root.get_all_nodes())} nodes"
            )

        while not self.is_finished():
            total_cost = self.total_usage().completion_cost

            logger.info(f"Run iteration {len(self.root.get_all_nodes())} (cost: ${total_cost}")

            if self.max_cost and self.total_usage().completion_cost and total_cost >= self.max_cost:
                logger.warning(
                    f"Search cost ${total_cost} exceeded max cost of ${self.max_cost}. Finishing search."
                )
                break

            node = self._select(self.root)
            if node:
                new_node = self._expand(node)
                self._simulate(new_node)
                self._backpropagate(new_node)
                self.maybe_persist()
                logger.info(generate_ascii_tree(self.root, new_node))
            else:
                logger.info("Search complete: no more nodes to expand.")
                break

        if not len(self.get_finished_nodes()):
            logger.warning(
                f"Search completed with no finished nodes. {len(self.root.get_all_nodes())} nodes created."
            )
        else:
            logger.info(
                f"Search completed with {len(self.get_finished_nodes())} finished nodes. {len(self.root.get_all_nodes())} nodes created."
            )

        return self.get_best_trajectory()

    def _select(self, node: Node) -> Optional[Node]:
        """Select a node for expansion using the UCT algorithm."""
        expandable_nodes = node.get_expandable_descendants()

        filtered_nodes = [n for n in expandable_nodes if n.get_depth() < self.max_depth]

        if not filtered_nodes:
            logger.info("No expandable nodes found.")
            return None

        return self.selector.select(filtered_nodes)

    def _expand(self, node: Node) -> Node:
        """Expand the node by returning an unexecuted child or adding a new child node."""
        # Check for unexecuted children
        for child in node.children:
            if not child.is_duplicate and child.observation is None:
                logger.info(
                    f"Returning unexecuted child Node{child.node_id} of Node{node.node_id}"
                )
                return child

        if self.feedback_generator:
            feedback = self.feedback_generator.generate_feedback(node)
        else:
            feedback = None

        child_node = Node(
            node_id=self._generate_unique_id(),
            parent=node,
            file_context=node.file_context.clone() if node.file_context else None,
            max_expansions=self.max_expansions,
            feedback=feedback,
        )
        node.add_child(child_node)
        logger.info(f"Expanded Node{node.node_id} to new Node{child_node.node_id}")
        return child_node

    def _simulate(self, node: Node):
        """Simulate a playout by executing the action and evaluating the result."""

        if not node.observation:
            self.agent.run(node)

        if self.value_function:
            node.reward, completion_response = self.value_function.get_reward(node=node)
            node.completions["value_function"] = completion_response
            logger.info(
                f"Node{node.node_id}: The value function returned a reward of {node.reward.value}."
            )

    def _backpropagate(self, node: Node):
        """Backpropagate the reward up the tree."""

        if not node.reward:
            logger.info(
                f"Node{node.node_id} has no evaluation. Skipping backpropagation."
            )
            return

        reward = node.reward.value
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    def get_best_trajectory(self) -> Node | None:
        """
        Get the best finished trajectory to return
        """

        nodes = self.get_finished_nodes()
        if not nodes:
            nodes = self.get_leaf_nodes()
            logger.info(
                f"get_best_trajectory() No finished nodes found. Will select from {len(nodes)} leaf nodes."
            )

        if len(nodes) == 1:
            return nodes[0]

        return self.discriminator.select(nodes)

    def is_finished(self):
        if len(self.root.get_all_nodes()) >= self.max_iterations:
            return True

        finished_nodes = self.get_finished_nodes()

        if self.max_finished_nodes and len(finished_nodes) >= self.max_finished_nodes:
            return True

        if self.reward_threshold and any(
            node.reward and node.reward.value >= self.reward_threshold
            for node in finished_nodes
        ):
            return not self.min_finished_nodes or len(finished_nodes) >= self.min_finished_nodes

        if not self.root.get_expandable_descendants():
            return True

        return False

    def get_finished_nodes(self) -> List[Node]:
        """Get all finished nodes in the search tree by uniqe parent node."""
        parent_ids = set()
        finished_nodes = []
        for node in self.root.get_all_nodes():
            # TODO: Pick finished node with highest/avg/lowest reward?
            if node.is_finished() and node.parent.node_id not in parent_ids:
                parent_ids.add(node.parent.node_id)
                finished_nodes.append(node)

        return finished_nodes

    def get_leaf_nodes(self) -> List[Node]:
        """Get all leaf nodes in the search tree."""
        return [node for node in self.root.get_all_nodes() if node.is_leaf()]

    def total_usage(self) -> Usage:
        total_usage = Usage()
        for node in self.root.get_all_nodes():
            total_usage += node.total_usage()
        return total_usage

    def maybe_persist(self):
        if self.persist_path:
            self.persist(self.persist_path)

    def persist(self, file_path: str, **kwargs):
        """
        Persist the entire SearchTree to a file.

        Args:
            file_path (str): The path to the file where the tree will be saved.
        """
        tree_data = self.model_dump(**kwargs)

        with open(file_path, "w") as f:
            try:
                json.dump(tree_data, f, indent=2)
            except Exception as e:
                logger.exception(
                    f"Error saving search tree to {file_path}: {tree_data}"
                )
                raise e

    def _generate_unique_id(self) -> int:
        self.unique_id += 1
        return self.unique_id

    def assert_runnable(self):
        if self.root is None:
            raise ValueError("SearchTree must have a root node.")

        if self.root.file_context is None:
            raise ValueError("SearchTree root node must have a file context.")

        #if self.root.file_context._repo is None:
        #    raise ValueError("SearchTree root node file context must have a repository.")

        return True

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """
        Generate a dictionary representation of the SearchTree.

        Returns:
            Dict[str, Any]: A dictionary representation of the search tree.
        """
        # Get all fields except the ones we'll handle separately
        data = {
            field: getattr(self, field)
            for field in self.model_fields
            if field
            not in [
                "root",
                "selector",
                "agent",
                "value_function",
                "feedback_generator",
                "discriminator",
                "persist_path",
            ]
        }

        # Remove persist_path if it exists
        data.pop("persist_path", None)

        # Add selector, agent, value_function, feedback_generator, and discriminator
        data["selector"] = self.selector.model_dump(**kwargs)
        data["agent"] = self.agent.model_dump(**kwargs)

        if self.value_function:
            data["value_function"] = self.value_function.model_dump(**kwargs)
        if self.feedback_generator:
            data["feedback_generator"] = self.feedback_generator.model_dump(**kwargs)
        if self.discriminator:
            data["discriminator"] = self.discriminator.model_dump(**kwargs)

        # Add root last
        data["root"] = self.root.model_dump(**kwargs)

        return data


def find_best_by_mean_award(finished_nodes: List[Node]) -> Node | None:
    best_finish_node: Node | None = None
    best_mean_reward = float("-inf")
    trajectories_mean_rewards = []

    for finished_node in finished_nodes:
        mean_reward = finished_node.calculate_mean_reward()

        trajectories_mean_rewards.append(mean_reward)
        if mean_reward > best_mean_reward:
            best_mean_reward = mean_reward
            best_finish_node = finished_node

    logger.info(f"Mean Rewards for finished trajectories: {trajectories_mean_rewards}")

    if best_finish_node:
        logger.info(
            f"Best finished path finished on Node{best_finish_node.node_id} with mean reward: {best_mean_reward}"
        )
        return best_finish_node
    else:
        logger.info(
            "No valid finished path found. This should not happen if there are finished nodes."
        )
        return None
