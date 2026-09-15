# World Node Selection Contract — 2026-09-16

Status: `P0 EXECUTION CONTRACT`

Parent:
- `docs/field/ROUTABLE_WORLD_NODES_2026-09-16.md`

For any route candidate, the engine must not ask only `who can do this?`.

It must ask:

```text
WHAT STATE MUST CHANGE?
WHAT NODE TYPES COULD CHANGE IT?
WHICH NODE ALREADY HAS THE REQUIRED ACCESS / CAPACITY / AUTHORITY / INFORMATION?
WHICH NODE CAN BE OPTIONED CHEAPLY AND LEGITIMATELY?
WHAT DOES THAT NODE OWNER / CONTROLLER GET?
WHAT IS THE MINIMUM INTERFACE?
WHAT PROVES SUCCESS?
CAN THIS NODE BE REPLACED OR COMPOSED?
```

Selection should prefer nodes with:
- direct leverage on the blocker;
- low irreversible capital;
- explicit permission/control path;
- observable output;
- short validation cycle;
- replaceability or composability;
- repeat access or repeat capacity;
- aligned economics for all controllers/participants.

Reject or demote nodes where:
- control is assumed rather than granted;
- the route depends on personal favors with no repeat mechanism;
- the node's owner has no visible surplus;
- regulation/permission makes activation unrealistic;
- the founder must personally operate the node indefinitely;
- activation cost consumes the expected surplus.

The unit of orchestration is therefore not `person` or `supplier`.

It is:

```text
CALLABLE NODE
+
CONTROL / PERMISSION
+
INTERFACE
+
INCENTIVE
+
ACCEPTANCE
```
