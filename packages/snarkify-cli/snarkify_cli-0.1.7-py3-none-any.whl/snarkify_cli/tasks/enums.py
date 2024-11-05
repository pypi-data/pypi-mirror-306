from enum import Enum


class TaskField(Enum):
    TASK_ID = "task_id"
    PROVER_ID = "prover_id"
    CREATED = "created"
    STARTED = "started"
    FINISHED = "finished"
    STATE = "state"
    INPUT = "input"
    PROOF = "proof"
    ERROR = "error"
    PROOF_TYPE = "proof_type"
    EXTRAS = "extras"
    NETWORK = "network"
