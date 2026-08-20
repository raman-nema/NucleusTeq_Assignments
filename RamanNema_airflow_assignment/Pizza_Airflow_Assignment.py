import random
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "Raman",
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}


def take_order(**context):
    log = context["ti"].log
    order_id = random.randint(1000, 9999)  # a random id is generated
    topping_list = random.choice(
        [
            ["cheese", "pepperoni"],
            ["cheese", "mushroom", "olives"],
            ["cheese", "pineapple"],
        ]
    )

    log.info("New order #%s received with toppings: %s", order_id, topping_list)
    context["ti"].xcom_push(key="order_id", value=order_id)
    context["ti"].xcom_push(key="topping_list", value=topping_list)


def check_ingredient_stock(**context):
    log = context["ti"].log
    topping_list = context["ti"].xcom_pull(key="topping_list", task_ids="take_order")

    if "pineapple" in topping_list:
        log.warning("Topping shortage detected for toppings: %s", topping_list)
        return "notify_stock_shortage"

    log.info("All toppings in stock, proceeding to prep.")
    return "prep_dough"


def add_toppings(**context):
    log = context["ti"].log
    topping_list = context["ti"].xcom_pull(key="topping_list", task_ids="take_order")
    log.debug("Adding toppings to base: %s", topping_list)
    log.info("Toppings added successfully.")


def quality_check(**context):
    log = context["ti"].log
    score = random.randint(70, 100)
    context["ti"].xcom_push(key="quality_score", value=score)

    if score < 80:
        log.error("Quality check scored low (%s/100) — flag for kitchen review.", score)
    else:
        log.info("Quality check passed with score %s/100.", score)


with DAG(
    dag_id="Pizza_Airflow_Assignment",
    description="DoughFlow Pizza Co. order-to-delivery pipeline",
    default_args=default_args,
    schedule_interval="0 11,17 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["pizza", "Assignment", "Airflow"],
) as dag:

    take_order_task = PythonOperator(
        task_id="take_order",
        python_callable=take_order,
    )

    check_stock_task = BranchPythonOperator(
        task_id="check_ingredient_stock",
        python_callable=check_ingredient_stock,
    )

    notify_stock_shortage_task = BashOperator(
        task_id="notify_stock_shortage",
        bash_command='echo "CRITICAL: Order cannot be completed, topping out of stock."',
    )

    prep_dough_task = BashOperator(
        task_id="prep_dough",
        bash_command='echo "Prepping dough... resting for 2 minutes." && sleep 2',
    )

    add_toppings_task = PythonOperator(
        task_id="add_toppings",
        python_callable=add_toppings,
    )

    bake_pizza_task = BashOperator(
        task_id="bake_pizza",
        bash_command='echo "Baking pizza in oven at 450F for 90 seconds." && sleep 2',
    )

    quality_check_task = PythonOperator(
        task_id="quality_check",
        python_callable=quality_check,
    )

    pack_and_dispatch_task = BashOperator(
        task_id="pack_and_dispatch",
        bash_command='echo "Packing box and dispatching for delivery."',
    
    )

    take_order_task >> check_stock_task
    check_stock_task >> [prep_dough_task, notify_stock_shortage_task]
    prep_dough_task >> add_toppings_task >> bake_pizza_task >> quality_check_task >> pack_and_dispatch_task
    