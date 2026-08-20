# Pizza Delivery Pipeline — DoughFlow Pizza Co.

## DAG Flow (Task Path)

```
take_order
    │
    ▼
check_ingredient_stock (branch)
    │
    ├── prep_dough
    │        │
    │        ▼
    │   add_toppings
    │        │
    │        ▼
    │   bake_pizza
    │        │
    │        ▼
    │   quality_check
    │        │
    │        ▼
    │   pack_and_dispatch
    │
    └── notify_stock_shortage  (dead end — no further tasks run)
```

## Tasks

| Task ID | Operator | Description |
|---|---|---|
| `take_order` | PythonOperator | Simulates a new order arriving; pushes `order_id` and `topping_list` via XCom. |
| `check_ingredient_stock` | BranchPythonOperator | Checks the topping list for stock issues and branches to either `prep_dough` or `notify_stock_shortage`. |
| `notify_stock_shortage` | BashOperator | Logs a critical shortage notice; terminates the workflow for this order. |
| `prep_dough` | BashOperator | Simulates dough preparation and resting time. |
| `add_toppings` | PythonOperator | Pulls `topping_list` via XCom and applies toppings to the base. |
| `bake_pizza` | BashOperator | Simulates baking the pizza in the oven. |
| `quality_check` | PythonOperator | Grades the finished pizza and pushes `quality_score` via XCom. |
| `pack_and_dispatch` | BashOperator | Packs the completed order and dispatches it for delivery. |

## Task Flow
The pipeline begins with `take_order`, followed by a branching decision at `check_ingredient_stock`, which routes execution along one of two paths:


• **Standard path:** `prep_dough` → `add_toppings` → `bake_pizza` → `quality_check` → `pack_and_dispatch`.
<br>
• **Shortage path:** `notify_stock_shortage`, which terminates the workflow with no further tasks executed.

This structure was chosen to reflect realistic kitchen behavior. If a required topping is unavailable, the order cannot be completed, and continuing to prep, bake, or package the pizza would be a waste of resources. The branching decision is therefore placed immediately after the order is received, before any preparation work begins.

## XCom Usage

• `take_order` pushes `order_id` and `topping_list`, representing the core order details required by downstream tasks..
<br>
• `check_ingredient_stock` pulls `topping_list` to determine which branch to execute..
<br>
• `add_toppings` pulls `topping_list` a second time to apply the correct toppings to the base..
<br>
• `quality_check` pushes `quality_score`, providing a record of the pizza's outcome for downstream reference or reporting..

## Skip Condition
`check_ingredient_stock` is implemented as a `BranchPythonOperator`. If the order's topping list contains `"pineapple"`, simulating a chronically out-of-stock ingredient, the task returns `notify_stock_shortage`, and Airflow automatically marks `prep_dough` as skipped. Because `prep_dough` is skipped and all downstream tasks use the default `all_success` trigger rule, the skip propagates through the remainder of the standard path (`add_toppings`, `bake_pizza`, `quality_check`, `pack_and_dispatch`). None of these tasks execute, consistent with there being no pizza to complete.

## Schedule
The DAG is scheduled using the cron expression `0 11,17 * * *`, triggering runs at 11:00 AM and 5:00 PM daily. This reflects the lunch and dinner rush periods during which pizza orders realistically spike.